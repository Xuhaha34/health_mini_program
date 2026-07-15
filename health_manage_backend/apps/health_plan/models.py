from django.db import models
from django.conf import settings
from django.utils import timezone


class HealthPlan(models.Model):
    """健康计划"""
    PLAN_TYPE_CHOICES = (
        ('diet', '饮食计划'),
        ('sport', '运动计划'),
        ('body', '体征管理'),
        ('comprehensive', '综合计划'),
    )

    STATUS_CHOICES = (
        (0, '进行中'),
        (1, '已完成'),
        (2, '已放弃'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_plans', verbose_name='用户')
    title = models.CharField(max_length=200, verbose_name='计划标题')
    plan_type = models.CharField(max_length=50, choices=PLAN_TYPE_CHOICES, verbose_name='计划类型')
    target_value = models.CharField(max_length=100, blank=True, null=True, verbose_name='目标值')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=0, verbose_name='状态')
    description = models.TextField(blank=True, null=True, verbose_name='计划描述')
    reminder = models.BooleanField(default=False, verbose_name='是否提醒')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'health_plan_healthplan'
        verbose_name = '健康计划'
        verbose_name_plural = verbose_name
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['user', 'status']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class PlanCheckIn(models.Model):
    """健康计划打卡记录"""
    plan = models.ForeignKey(HealthPlan, on_delete=models.CASCADE, related_name='checkins', verbose_name='计划')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plan_checkins', verbose_name='用户')
    checkin_date = models.DateField(default=timezone.now, verbose_name='打卡日期')
    checkin_time = models.DateTimeField(auto_now_add=True, verbose_name='打卡时间')
    note = models.CharField(max_length=200, blank=True, null=True, verbose_name='备注')

    class Meta:
        db_table = 'health_plan_checkin'
        verbose_name = '计划打卡'
        verbose_name_plural = verbose_name
        unique_together = ['plan', 'user', 'checkin_date']
        ordering = ['-checkin_time']
        indexes = [
            models.Index(fields=['plan', 'user', 'checkin_date']),
            models.Index(fields=['user', 'checkin_date']),
        ]

    def __str__(self):
        return f"{self.plan.title} - {self.checkin_date}"