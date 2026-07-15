from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    扩展Django默认用户模型
    """
    GENDER_CHOICES = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True, verbose_name='头像')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    age = models.IntegerField(blank=True, null=True, verbose_name='年龄')
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='身高(cm)')
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='体重(kg)')

    class Meta:
        db_table = 'auth_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class UserInfo(models.Model):
    """
    用户扩展信息表（可选，用于存储更多用户详细信息）
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info', verbose_name='用户')
    nickname = models.CharField(max_length=50, blank=True, null=True, verbose_name='昵称')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')
    occupation = models.CharField(max_length=100, blank=True, null=True, verbose_name='职业')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'users_userinfo'
        verbose_name = '用户扩展信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.user.username}的扩展信息"
