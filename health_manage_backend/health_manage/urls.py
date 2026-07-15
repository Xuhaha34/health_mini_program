"""
项目总路由：分发至各子应用
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users.urls import statistics_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),

    # 用户模块
    path('api/users/', include('apps.users.urls')),

    # 健康记录模块
    path('api/records/', include('apps.health_record.urls')),

    # 健康计划模块
    path('api/plans/', include('apps.health_plan.urls')),

    # 健康资讯模块
    path('api/news/', include('apps.health_news.urls')),

    # AI健康问答模块
    path('api/ai/', include('apps.ai_chat.urls')),

    # 平台统计模块
    path('api/statistics/', include(statistics_urlpatterns)),
]

# 开发环境提供媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)