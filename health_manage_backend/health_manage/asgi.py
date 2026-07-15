"""
ASGI config for health_manage project.
用于异步服务器部署（Daphne、Uvicorn）
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_manage.settings')
application = get_asgi_application()
