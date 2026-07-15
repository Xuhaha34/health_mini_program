from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from utils.common_response import success_response, error_response
from utils.permissions import IsOwnerOrReadOnly
from utils.pagination import StandardPagination
from .serializers import (
    UserRegisterSerializer, 
    UserLoginSerializer, 
    UserInfoSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    UserListSerializer,
    UserCreateSerializer,
    UserUpdateSerializer
)

User = get_user_model()


class RegisterView(APIView):
    """用户注册接口"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return success_response(
                data={'user_id': user.id, 'username': user.username},
                message='注册成功'
            )
        return error_response(message=serializer.errors, code=400)


class LoginView(APIView):
    """用户登录接口"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            user = validated_data['user']
            
            # 获取用户信息
            user_info = UserInfoSerializer(user, context={'request': request}).data
            
            return success_response(
                data={
                    'access_token': validated_data['access_token'],
                    'refresh_token': validated_data['refresh_token'],
                    'user': user_info
                },
                message='登录成功'
            )
        return error_response(message=serializer.errors, code=400)


class UserInfoView(APIView):
    """获取/更新用户信息"""
    
    def get(self, request):
        """获取当前用户信息"""
        serializer = UserInfoSerializer(request.user, context={'request': request})
        return success_response(data=serializer.data)

    def put(self, request):
        """更新用户信息"""
        serializer = UserProfileUpdateSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=serializer.data,
                message='更新成功'
            )
        return error_response(message=serializer.errors, code=400)


class ChangePasswordView(APIView):
    """修改密码接口"""

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            # 验证旧密码
            if not user.check_password(old_password):
                return error_response(message='旧密码错误', code=400)

            # 设置新密码
            user.set_password(new_password)
            user.save()

            return success_response(message='密码修改成功')
        return error_response(message=serializer.errors, code=400)


class UserStatsView(APIView):
    """用户统计数据（管理后台用）"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from datetime import datetime, timedelta
        from django.utils import timezone

        total_users = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        today = timezone.localdate()
        today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        today_end = today_start + timedelta(days=1)
        today_registrations = User.objects.filter(
            date_joined__gte=today_start, date_joined__lt=today_end
        ).count()

        # 近7天每日注册数（用range方式避免MySQL CONVERT_TZ问题）
        daily_registrations = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_start = timezone.make_aware(datetime.combine(day, datetime.min.time()))
            day_end = day_start + timedelta(days=1)
            count = User.objects.filter(date_joined__gte=day_start, date_joined__lt=day_end).count()
            daily_registrations.append({
                'date': day.strftime('%m-%d'),
                'count': count
            })

        return success_response(data={
            'total_users': total_users,
            'active_users': active_users,
            'today_registrations': today_registrations,
            'daily_registrations': daily_registrations,
        })


class UserListView(generics.ListCreateAPIView):
    """用户列表/创建（管理后台用）"""
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = User.objects.all()
        
        # 搜索功能
        username = self.request.query_params.get('username', None)
        phone = self.request.query_params.get('phone', None)
        
        if username:
            queryset = queryset.filter(username__icontains=username)
        if phone:
            queryset = queryset.filter(phone__icontains=phone)
        
        return queryset.order_by('-date_joined')
    
    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=UserListSerializer(instance).data,
                message='创建成功'
            )
        return error_response(message=serializer.errors, code=400)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情/更新/删除（管理后台用）"""
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = UserUpdateSerializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return success_response(
                data=UserListSerializer(instance).data,
                message='更新成功'
            )
        return error_response(message=serializer.errors, code=400)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            return error_response(message='不能删除当前登录的账号', code=400)
        
        instance.delete()
        return success_response(message='删除成功')


class StatisticsOverviewView(APIView):
    """平台总览数据"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from datetime import datetime, timedelta
        from django.utils import timezone
        from apps.health_record.models import BodyData, DietRecord, SportRecord
        from apps.health_news.models import News
        from apps.health_plan.models import HealthPlan

        total_users = User.objects.count()
        today = timezone.localdate()
        today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        today_end = today_start + timedelta(days=1)
        today_users = User.objects.filter(
            date_joined__gte=today_start, date_joined__lt=today_end
        ).count()
        total_records = BodyData.objects.count() + DietRecord.objects.count() + SportRecord.objects.count()
        total_news = News.objects.filter(is_published=True).count()
        total_plans = HealthPlan.objects.count()

        return success_response(data={
            'total_users': total_users,
            'today_users': today_users,
            'total_records': total_records,
            'total_news': total_news,
            'total_plans': total_plans,
        })


class StatisticsUserTrendView(APIView):
    """用户增长趋势"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from datetime import datetime, timedelta
        from django.utils import timezone

        days = int(request.query_params.get('days', 7))
        today = timezone.localdate()
        start_date = today - timedelta(days=days - 1)

        trend = []
        for i in range(days):
            day = start_date + timedelta(days=i)
            day_start = timezone.make_aware(datetime.combine(day, datetime.min.time()))
            day_end = day_start + timedelta(days=1)
            count = User.objects.filter(date_joined__gte=day_start, date_joined__lt=day_end).count()
            trend.append({'day': day.strftime('%Y-%m-%d'), 'count': count})

        return success_response(data=trend)



class StatisticsHealthDistributionView(APIView):
    """健康数据分布"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from apps.health_record.models import BodyData, DietRecord, SportRecord

        body_count = BodyData.objects.count()
        diet_count = DietRecord.objects.count()
        sport_count = SportRecord.objects.count()

        return success_response(data={
            'body_data': body_count,
            'diet_record': diet_count,
            'sport_record': sport_count,
        })


class StatisticsActivityView(APIView):
    """活跃度统计"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from datetime import datetime, timedelta
        from django.utils import timezone
        from apps.health_record.models import BodyData, DietRecord, SportRecord

        today = timezone.localdate()
        week_ago = today - timedelta(days=7)
        today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
        today_end = today_start + timedelta(days=1)
        week_start = timezone.make_aware(datetime.combine(week_ago, datetime.min.time()))

        today_body = BodyData.objects.filter(record_date=today).count()
        today_diet = DietRecord.objects.filter(record_datetime__gte=today_start, record_datetime__lt=today_end).count()
        today_sport = SportRecord.objects.filter(sport_date=today).count()

        week_body = BodyData.objects.filter(record_date__gte=week_ago).count()
        week_diet = DietRecord.objects.filter(record_datetime__gte=week_start).count()
        week_sport = SportRecord.objects.filter(sport_date__gte=week_ago).count()

        return success_response(data={
            'today': {
                'body': today_body,
                'diet': today_diet,
                'sport': today_sport,
            },
            'week': {
                'body': week_body,
                'diet': week_diet,
                'sport': week_sport,
            },
        })