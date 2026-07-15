from django.db import models
from django.conf import settings


class ChatHistory(models.Model):
    """AI对话历史记录"""
    ROLE_CHOICES = (
        ('user', '用户'),
        ('assistant', '助手'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_histories', verbose_name='用户')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, verbose_name='角色')
    message = models.TextField(verbose_name='消息内容')
    session_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='会话ID')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'ai_chat_chathistory'
        verbose_name = 'AI对话历史'
        verbose_name_plural = verbose_name
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', 'session_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role} - {self.created_at}"
