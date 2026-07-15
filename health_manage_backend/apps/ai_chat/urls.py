from django.urls import path
from .views import AIChatView, AIChatConfigView, ChatHistoryListView, ClearChatHistoryView, ChatSessionListView

urlpatterns = [
    # AI问答
    path('chat/', AIChatView.as_view(), name='ai-chat'),

    # AI 当前配置（前端调试显示）
    path('config/', AIChatConfigView.as_view(), name='ai-config'),

    # 会话列表
    path('sessions/', ChatSessionListView.as_view(), name='chat-sessions'),

    # 对话历史
    path('history/', ChatHistoryListView.as_view(), name='chat-history'),

    # 清空历史
    path('history/clear/', ClearChatHistoryView.as_view(), name='clear-history'),
]