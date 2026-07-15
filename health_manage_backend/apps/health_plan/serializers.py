from rest_framework import serializers
from .models import HealthPlan


class HealthPlanSerializer(serializers.ModelSerializer):
    """健康计划序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    plan_name = serializers.CharField(source='title', required=False)
    plan_type_display = serializers.CharField(source='get_plan_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    goal = serializers.CharField(source='target_value', required=False, allow_blank=True, allow_null=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = HealthPlan
        fields = [
            'id', 'user_name', 'title', 'plan_name', 'plan_type', 'plan_type_display',
            'goal', 'target_value', 'start_date', 'end_date', 'status', 'status_display',
            'progress', 'description', 'reminder', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_progress(self, obj):
        if obj.status == 1:
            return 100
        elif obj.status == 2:
            return 0
        from django.utils import timezone
        if obj.start_date and obj.end_date:
            total_days = (obj.end_date - obj.start_date).days
            if total_days > 0:
                elapsed = (timezone.localdate() - obj.start_date).days
                return min(max(int(elapsed / total_days * 100), 0), 99)
        return 0

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_internal_value(self, data):
        # 兼容前端传 plan_name 或 title
        if 'plan_name' in data and 'title' not in data:
            data = data.copy()
            data['title'] = data.pop('plan_name')
        # 兼容前端传 goal 或 target_value
        if 'goal' in data and 'target_value' not in data:
            data = data.copy()
            data['target_value'] = data.pop('goal')
        # 兼容 status 为字符串
        if 'status' in data and isinstance(data['status'], str):
            data = data.copy()
            status_map = {
                'active': 0, 'in_progress': 0, '0': 0,
                'completed': 1, 'finished': 1, '1': 1,
                'paused': 2, 'abandoned': 2, '2': 2
            }
            data['status'] = status_map.get(data['status'], 0)
        # 兼容 admin-web 自定义 plan_type 值
        if 'plan_type' in data:
            data = data.copy()
            pt_map = {
                'weight_loss': 'diet', 'muscle_gain': 'sport',
                'health_maintenance': 'body', 'training': 'sport',
                'sleep': 'body', 'weight': 'body', 'other': 'comprehensive'
            }
            data['plan_type'] = pt_map.get(data['plan_type'], data['plan_type'])
        return super().to_internal_value(data)