from rest_framework import serializers
from .models import BodyData, DietRecord, SportRecord


class BodyDataSerializer(serializers.ModelSerializer):
    """体征数据序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    bmi = serializers.SerializerMethodField()
    blood_pressure = serializers.SerializerMethodField()

    class Meta:
        model = BodyData
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_bmi(self, obj):
        if obj.weight and obj.height and obj.height > 0:
            try:
                height_m = float(obj.height) / 100
                if height_m > 0:
                    return round(float(obj.weight) / (height_m * height_m), 2)
            except (TypeError, ValueError):
                pass
        return None

    def get_blood_pressure(self, obj):
        if obj.blood_pressure_systolic and obj.blood_pressure_diastolic:
            return f"{obj.blood_pressure_systolic}/{obj.blood_pressure_diastolic}"
        return None

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_internal_value(self, data):
        data = dict(data)
        if 'systolic_pressure' in data and 'blood_pressure_systolic' not in data:
            data['blood_pressure_systolic'] = data.pop('systolic_pressure')
        if 'diastolic_pressure' in data and 'blood_pressure_diastolic' not in data:
            data['blood_pressure_diastolic'] = data.pop('diastolic_pressure')
        if 'body_temperature' in data and 'temperature' not in data:
            data['temperature'] = data.pop('body_temperature')
        if 'note' in data and 'remark' not in data:
            data['remark'] = data.pop('note')
        for key in ['weight', 'blood_pressure_systolic', 'blood_pressure_diastolic',
                    'heart_rate', 'blood_sugar', 'temperature']:
            if key in data and data[key] == '':
                data[key] = None
        return super().to_internal_value(data)


class DietRecordSerializer(serializers.ModelSerializer):
    """饮食记录序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    meal_type_display = serializers.CharField(source='get_meal_type_display', read_only=True)

    class Meta:
        model = DietRecord
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_internal_value(self, data):
        data = dict(data)
        if 'quantity' in data and 'portion_size' not in data:
            data['portion_size'] = data.pop('quantity')
        if 'carbs' in data and 'carbohydrate' not in data:
            data['carbohydrate'] = data.pop('carbs')
        if 'note' in data and 'remark' not in data:
            data['remark'] = data.pop('note')
        if 'record_datetime' not in data or data['record_datetime'] == '':
            from django.utils import timezone
            data['record_datetime'] = timezone.now().isoformat()
        for key in ['calories', 'protein', 'fat', 'carbohydrate']:
            if key in data and data[key] == '':
                data[key] = None
        return super().to_internal_value(data)


class SportRecordSerializer(serializers.ModelSerializer):
    """运动记录序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    sport_type_display = serializers.CharField(source='sport_type', read_only=True)

    class Meta:
        model = SportRecord
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_internal_value(self, data):
        data = dict(data)
        if 'record_date' in data and 'sport_date' not in data:
            data['sport_date'] = data.pop('record_date')
        if 'calories_burned' in data and 'calories' not in data:
            data['calories'] = data.pop('calories_burned')
        if 'note' in data and 'remark' not in data:
            data['remark'] = data.pop('note')
        for key in ['duration', 'calories', 'distance', 'steps']:
            if key in data and data[key] == '':
                data[key] = None
        return super().to_internal_value(data)


class BodyDataStatsSerializer(serializers.Serializer):
    """体征数据统计"""
    avg_weight = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    max_weight = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    min_weight = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    avg_heart_rate = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)
    total_records = serializers.IntegerField()


class DietStatsSerializer(serializers.Serializer):
    """饮食统计"""
    total_calories = serializers.IntegerField()
    avg_calories = serializers.FloatField()
    total_records = serializers.IntegerField()
    meal_type_distribution = serializers.DictField()


class SportStatsSerializer(serializers.Serializer):
    """运动统计"""
    total_duration = serializers.IntegerField()
    total_calories = serializers.IntegerField()
    total_distance = serializers.FloatField()
    total_records = serializers.IntegerField()