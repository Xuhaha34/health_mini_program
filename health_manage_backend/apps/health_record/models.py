from django.db import models
from django.conf import settings


class BodyData(models.Model):
    """体征数据记录"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='body_data', verbose_name='用户')
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='体重(kg)')
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='身高(cm)')
    blood_pressure_systolic = models.IntegerField(blank=True, null=True, verbose_name='收缩压(mmHg)')
    blood_pressure_diastolic = models.IntegerField(blank=True, null=True, verbose_name='舒张压(mmHg)')
    heart_rate = models.IntegerField(blank=True, null=True, verbose_name='心率(次/分)')
    blood_sugar = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='血糖(mmol/L)')
    temperature = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='体温(℃)')
    record_date = models.DateField(verbose_name='记录日期')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'health_record_bodydata'
        verbose_name = '体征数据'
        verbose_name_plural = verbose_name
        ordering = ['-record_date']
        indexes = [
            models.Index(fields=['user', 'record_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.record_date}"


class DietRecord(models.Model):
    """饮食记录"""
    MEAL_TYPE_CHOICES = (
        ('breakfast', '早餐'),
        ('lunch', '午餐'),
        ('dinner', '晚餐'),
        ('snack', '加餐'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='diet_records', verbose_name='用户')
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES, verbose_name='餐别')
    food_name = models.CharField(max_length=200, verbose_name='食物名称')
    calories = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='热量(kcal)')
    protein = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='蛋白质(g)')
    fat = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='脂肪(g)')
    carbohydrate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='碳水化合物(g)')
    portion_size = models.CharField(max_length=50, blank=True, null=True, verbose_name='份量')
    record_datetime = models.DateTimeField(verbose_name='记录时间')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'health_record_dietrecord'
        verbose_name = '饮食记录'
        verbose_name_plural = verbose_name
        ordering = ['-record_datetime']
        indexes = [
            models.Index(fields=['user', 'record_datetime']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.food_name} - {self.record_datetime}"


class SportRecord(models.Model):
    """运动记录"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sport_records', verbose_name='用户')
    sport_type = models.CharField(max_length=50, verbose_name='运动类型')
    duration = models.IntegerField(blank=True, null=True, verbose_name='运动时长(分钟)')
    distance = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='距离(km)')
    calories = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='消耗热量(kcal)')
    steps = models.IntegerField(blank=True, null=True, verbose_name='步数')
    sport_date = models.DateField(verbose_name='运动日期')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'health_record_sportrecord'
        verbose_name = '运动记录'
        verbose_name_plural = verbose_name
        ordering = ['-sport_date']
        indexes = [
            models.Index(fields=['user', 'sport_date']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.sport_type} - {self.sport_date}"
