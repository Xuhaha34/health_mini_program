from django.urls import path
from .views import (
    RegisterView, LoginView, UserInfoView, ChangePasswordView, UserStatsView,
    UserListView, UserDetailView,
    StatisticsOverviewView, StatisticsUserTrendView,
    StatisticsHealthDistributionView, StatisticsActivityView
)

urlpatterns = [
    # 用户认证
    path('register/', RegisterView.as_view(), name='user-register'),      # 用户注册
    path('login/', LoginView.as_view(), name='user-login'),               # 用户登录
    
    # 用户信息
    path('info/', UserInfoView.as_view(), name='user-info'),              # 获取/更新用户信息
    path('password/change/', ChangePasswordView.as_view(), name='change-password'),  # 修改密码
    
    # 统计数据（管理后台）
    path('stats/', UserStatsView.as_view(), name='user-stats'),           # 用户统计
    
    # 管理后台用户管理（CRUD）
    path('', UserListView.as_view(), name='user-list'),                   # 用户列表/创建
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),      # 用户详情/更新/删除
]

# 平台统计路由
statistics_urlpatterns = [
    path('overview/', StatisticsOverviewView.as_view(), name='statistics-overview'),
    path('user-trend/', StatisticsUserTrendView.as_view(), name='statistics-user-trend'),
    path('health-distribution/', StatisticsHealthDistributionView.as_view(), name='statistics-health-distribution'),
    path('activity/', StatisticsActivityView.as_view(), name='statistics-activity'),
]