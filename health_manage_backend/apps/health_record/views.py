from rest_framework import generics, permissions, views
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db.models import Sum, Avg, Count, Min, Max
from datetime import timedelta
from utils.common_response import success_response, error_response
from utils.permissions import IsOwnerOrReadOnly
from utils.pagination import StandardPagination
from .models import BodyData, DietRecord, SportRecord
from .serializers import (
    BodyDataSerializer, DietRecordSerializer, SportRecordSerializer,
    BodyDataStatsSerializer, DietStatsSerializer, SportStatsSerializer
)


class BodyDataListView(generics.ListCreateAPIView):
    """体征数据列表/创建"""
    serializer_class = BodyDataSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['record_date']
    search_fields = ['remark']
    ordering_fields = ['record_date', 'created_at']
    ordering = ['-record_date']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = BodyData.objects.all()
            username = self.request.query_params.get('username', None)
            if username:
                queryset = queryset.filter(user__username__icontains=username)
            start_date = self.request.query_params.get('start_date', None)
            if start_date:
                queryset = queryset.filter(record_date__gte=start_date)
            end_date = self.request.query_params.get('end_date', None)
            if end_date:
                queryset = queryset.filter(record_date__lte=end_date)
            return queryset
        qs = BodyData.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            qs = qs.filter(record_date__gte=start_date)
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            qs = qs.filter(record_date__lte=end_date)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=BodyDataSerializer(instance, context={'request': request}).data,
                message='创建成功'
            )
        return error_response(message=serializer.errors, code=400)


class BodyDataDetailView(generics.RetrieveUpdateDestroyAPIView):
    """体征数据详情"""
    queryset = BodyData.objects.all()
    serializer_class = BodyDataSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return success_response(
            data=self.get_serializer(instance).data,
            message='获取成功'
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=self.get_serializer(instance).data,
                message='更新成功'
            )
        return error_response(message=serializer.errors, code=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message='删除成功')


class BodyDataStatsView(views.APIView):
    """体征数据统计"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 7))
        start_date = timezone.localdate() - timedelta(days=days)
        user = request.user

        if user.is_staff or user.is_superuser:
            qs = BodyData.objects.filter(record_date__gte=start_date)
        else:
            qs = BodyData.objects.filter(user=user, record_date__gte=start_date)
        stats = qs.aggregate(
            avg_weight=Avg('weight'),
            max_weight=Max('weight'),
            min_weight=Min('weight'),
            avg_heart_rate=Avg('heart_rate'),
        )
        stats['total_records'] = qs.count()

        return success_response(data=BodyDataStatsSerializer(stats).data)


class DietRecordListView(generics.ListCreateAPIView):
    """饮食记录列表/创建"""
    serializer_class = DietRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['meal_type']
    search_fields = ['food_name', 'remark']
    ordering_fields = ['record_datetime', 'created_at']
    ordering = ['-record_datetime']

    def get_queryset(self):
        from datetime import datetime

        def _date_to_dt(d):
            return timezone.make_aware(datetime.combine(d, datetime.min.time()))

        def _parse(s):
            return datetime.strptime(s, '%Y-%m-%d').date()

        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = DietRecord.objects.all()
            username = self.request.query_params.get('username', None)
            if username:
                queryset = queryset.filter(user__username__icontains=username)
            start_date = self.request.query_params.get('start_date', None)
            if start_date:
                queryset = queryset.filter(record_datetime__gte=_date_to_dt(_parse(start_date)))
            end_date = self.request.query_params.get('end_date', None)
            if end_date:
                queryset = queryset.filter(record_datetime__lt=_date_to_dt(_parse(end_date) + timedelta(days=1)))
            return queryset
        qs = DietRecord.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            qs = qs.filter(record_datetime__gte=_date_to_dt(_parse(start_date)))
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            qs = qs.filter(record_datetime__lt=_date_to_dt(_parse(end_date) + timedelta(days=1)))
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=DietRecordSerializer(instance, context={'request': request}).data,
                message='创建成功'
            )
        return error_response(message=serializer.errors, code=400)


class DietRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """饮食记录详情"""
    queryset = DietRecord.objects.all()
    serializer_class = DietRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return success_response(
            data=self.get_serializer(instance).data,
            message='获取成功'
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=self.get_serializer(instance).data,
                message='更新成功'
            )
        return error_response(message=serializer.errors, code=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message='删除成功')


class DietStatsView(views.APIView):
    """饮食统计"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from datetime import datetime
        days = int(request.query_params.get('days', 7))
        start_date = timezone.localdate() - timedelta(days=days)
        start_dt = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        user = request.user

        if user.is_staff or user.is_superuser:
            qs = DietRecord.objects.filter(record_datetime__gte=start_dt)
        else:
            qs = DietRecord.objects.filter(user=user, record_datetime__gte=start_dt)
        stats = qs.aggregate(
            total_calories=Sum('calories'),
            total_records=Count('id'),
        )

        meal_dist = {}
        for mt in ['breakfast', 'lunch', 'dinner', 'snack']:
            meal_dist[mt] = qs.filter(meal_type=mt).count()

        result = {
            'total_calories': stats['total_calories'] or 0,
            'avg_calories': (stats['total_calories'] / days) if stats['total_calories'] else 0,
            'total_records': stats['total_records'] or 0,
            'meal_type_distribution': meal_dist
        }

        return success_response(data=DietStatsSerializer(result).data)


class SportRecordListView(generics.ListCreateAPIView):
    """运动记录列表/创建"""
    serializer_class = SportRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['sport_type', 'sport_date']
    search_fields = ['remark']
    ordering_fields = ['sport_date', 'created_at']
    ordering = ['-sport_date']

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            queryset = SportRecord.objects.all()
            username = self.request.query_params.get('username', None)
            if username:
                queryset = queryset.filter(user__username__icontains=username)
            start_date = self.request.query_params.get('start_date', None)
            if start_date:
                queryset = queryset.filter(sport_date__gte=start_date)
            end_date = self.request.query_params.get('end_date', None)
            if end_date:
                queryset = queryset.filter(sport_date__lte=end_date)
            return queryset
        qs = SportRecord.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            qs = qs.filter(sport_date__gte=start_date)
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            qs = qs.filter(sport_date__lte=end_date)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=SportRecordSerializer(instance, context={'request': request}).data,
                message='创建成功'
            )
        return error_response(message=serializer.errors, code=400)


class SportRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    """运动记录详情"""
    queryset = SportRecord.objects.all()
    serializer_class = SportRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return success_response(
            data=self.get_serializer(instance).data,
            message='获取成功'
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            instance = serializer.save()
            return success_response(
                data=self.get_serializer(instance).data,
                message='更新成功'
            )
        return error_response(message=serializer.errors, code=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message='删除成功')


class SportStatsView(views.APIView):
    """运动统计"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        days = int(request.query_params.get('days', 7))
        start_date = timezone.localdate() - timedelta(days=days)
        user = request.user

        if user.is_staff or user.is_superuser:
            qs = SportRecord.objects.filter(sport_date__gte=start_date)
        else:
            qs = SportRecord.objects.filter(user=user, sport_date__gte=start_date)
        stats = qs.aggregate(
            total_duration=Sum('duration'),
            total_calories=Sum('calories'),
            total_distance=Sum('distance'),
            total_records=Count('id'),
        )

        result = {
            'total_duration': stats['total_duration'] or 0,
            'total_calories': stats['total_calories'] or 0,
            'total_distance': stats['total_distance'] or 0,
            'total_records': stats['total_records'] or 0,
        }

        return success_response(data=SportStatsSerializer(result).data)


class OverallStatisticsView(views.APIView):
    """综合统计（小程序首页用）"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        from datetime import datetime
        days = int(request.query_params.get('days', 7))
        start_date = timezone.localdate() - timedelta(days=days)
        start_dt = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
        user = request.user

        if user.is_staff or user.is_superuser:
            diet_qs = DietRecord.objects.filter(record_datetime__gte=start_dt)
            sport_qs = SportRecord.objects.filter(sport_date__gte=start_date)
            body_qs = BodyData.objects.filter(record_date__gte=start_date)
        else:
            diet_qs = DietRecord.objects.filter(user=user, record_datetime__gte=start_dt)
            sport_qs = SportRecord.objects.filter(user=user, sport_date__gte=start_date)
            body_qs = BodyData.objects.filter(user=user, record_date__gte=start_date)

        diet_stats = diet_qs.aggregate(
            total_calories=Sum('calories'),
            total_records=Count('id')
        )

        sport_stats = sport_qs.aggregate(
            total_calories=Sum('calories'),
            total_duration=Sum('duration'),
            total_distance=Sum('distance'),
            total_records=Count('id')
        )

        body_qs = body_qs.order_by('-record_date')
        latest_body = body_qs.first()
        body_stats = body_qs.aggregate(
            avg_weight=Avg('weight'),
            avg_systolic=Avg('blood_pressure_systolic'),
            avg_diastolic=Avg('blood_pressure_diastolic'),
            avg_heart_rate=Avg('heart_rate')
        )

        result = {
            'diet': {
                'total_calories': diet_stats['total_calories'] or 0,
                'total_records': diet_stats['total_records'] or 0,
            },
            'sport': {
                'total_calories': sport_stats['total_calories'] or 0,
                'total_minutes': sport_stats['total_duration'] or 0,
                'total_distance': sport_stats['total_distance'] or 0,
                'total_records': sport_stats['total_records'] or 0,
            },
            'body': {
                'latest_weight': latest_body.weight if latest_body else None,
                'avg_weight': body_stats['avg_weight'],
                'avg_systolic': body_stats['avg_systolic'],
                'avg_diastolic': body_stats['avg_diastolic'],
                'avg_heart_rate': body_stats['avg_heart_rate'],
                'total_records': body_qs.count(),
            }
        }
        return success_response(data=result)


class RecentActivitiesView(views.APIView):
    """最近活动（Dashboard用）"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        user = request.user
        activities = []

        # 体征数据
        body_qs = BodyData.objects.select_related('user')
        if not user.is_staff:
            body_qs = body_qs.filter(user=user)
        for r in body_qs.order_by('-record_date', '-created_at')[:limit]:
            activities.append({
                'time': r.record_date.strftime('%Y-%m-%d') if r.record_date else '',
                'user': r.user.username,
                'type': '体征数据',
                'content': f'体重{r.weight}kg' if r.weight else '记录体征',
                'route': '/body-records'
            })

        # 饮食记录
        diet_qs = DietRecord.objects.select_related('user')
        if not user.is_staff:
            diet_qs = diet_qs.filter(user=user)
        for r in diet_qs.order_by('-record_datetime', '-created_at')[:limit]:
            meal_map = {'breakfast': '早餐', 'lunch': '午餐', 'dinner': '晚餐', 'snack': '加餐'}
            activities.append({
                'time': r.record_datetime.strftime('%Y-%m-%d %H:%M') if r.record_datetime else '',
                'user': r.user.username,
                'type': '饮食记录',
                'content': f'{meal_map.get(r.meal_type, r.meal_type)}: {r.food_name}',
                'route': '/diet-records'
            })

        # 运动记录
        sport_qs = SportRecord.objects.select_related('user')
        if not user.is_staff:
            sport_qs = sport_qs.filter(user=user)
        for r in sport_qs.order_by('-sport_date', '-created_at')[:limit]:
            sport_map = {
                'running': '跑步', 'walking': '散步', 'cycling': '骑行',
                'swimming': '游泳', 'gym': '健身', 'yoga': '瑜伽',
                'basketball': '篮球', 'badminton': '羽毛球'
            }
            activities.append({
                'time': r.sport_date.strftime('%Y-%m-%d') if r.sport_date else '',
                'user': r.user.username,
                'type': '运动记录',
                'content': f'{sport_map.get(r.sport_type, r.sport_type)} {r.duration}分钟',
                'route': '/sport-records'
            })

        activities.sort(key=lambda x: x['time'], reverse=True)
        activities = activities[:limit]

        return success_response(data=activities)