from rest_framework import generics, permissions, views
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db import IntegrityError
from utils.common_response import success_response, error_response
from utils.permissions import IsOwnerOrReadOnly
from .models import HealthPlan, PlanCheckIn
from .serializers import HealthPlanSerializer


class HealthPlanListView(generics.ListCreateAPIView):
    """健康计划列表/创建"""
    serializer_class = HealthPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['plan_type']
    search_fields = ['title']
    ordering_fields = ['start_date', 'created_at']
    ordering = ['-start_date']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = HealthPlan.objects.all()
            username = self.request.query_params.get('username', None)
            if username:
                queryset = queryset.filter(user__username__icontains=username)
            plan_name = self.request.query_params.get('planName', None)
            if plan_name:
                queryset = queryset.filter(title__icontains=plan_name)
            # 兼容 planType 或 plan_type 参数
            plan_type_param = self.request.query_params.get('planType', None) or self.request.query_params.get('plan_type', None)
            if plan_type_param and plan_type_param != '':
                pt_map = {
                    'weight_loss': 'diet',
                    'muscle_gain': 'sport',
                    'health_maintenance': 'body',
                    'training': 'comprehensive',
                    'diet': 'diet', 'sport': 'sport', 'body': 'body', 'comprehensive': 'comprehensive'
                }
                actual_pt = pt_map.get(plan_type_param)
                if actual_pt:
                    queryset = queryset.filter(plan_type=actual_pt)
            status_str = self.request.query_params.get('status', None)
            if status_str and status_str != '':
                status_map = {'active': 0, 'completed': 1, 'paused': 2, '0': 0, '1': 1, '2': 2}
                status_val = status_map.get(status_str)
                if status_val is not None:
                    queryset = queryset.filter(status=status_val)
            return queryset
        return HealthPlan.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=HealthPlanSerializer(instance, context={'request': request}).data,
                message='创建成功'
            )
        return error_response(message=serializer.errors, code=400)


class HealthPlanDetailView(generics.RetrieveUpdateDestroyAPIView):
    """健康计划详情/更新/删除"""
    serializer_class = HealthPlanSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return HealthPlan.objects.all()
        return HealthPlan.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return success_response(data=response.data, message='更新成功')

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return success_response(message='删除成功')


class HealthPlanCheckInView(views.APIView):
    """健康计划打卡"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        # 管理员可以打卡任何计划；普通用户只能打卡自己的
        if request.user.is_staff or request.user.is_superuser:
            plan = HealthPlan.objects.filter(pk=pk).first()
        else:
            plan = HealthPlan.objects.filter(pk=pk, user=request.user).first()

        if not plan:
            return error_response(message='计划不存在', code=404)

        today = timezone.localdate()
        try:
            checkin = PlanCheckIn.objects.create(
                plan=plan, user=request.user, checkin_date=today,
                note=request.data.get('note', '') if isinstance(request.data, dict) else ''
            )
        except IntegrityError:
            return error_response(message='今日已打卡', code=409)

        plan.updated_at = timezone.now()
        plan.save()

        total = PlanCheckIn.objects.filter(plan=plan).count()
        return success_response(
            data={
                'checked': True,
                'checkin_time': checkin.checkin_time.isoformat(),
                'checkin_date': today.isoformat(),
                'total_checkins': total,
                'plan_id': plan.id,
                'plan_title': plan.title
            },
            message='打卡成功'
        )