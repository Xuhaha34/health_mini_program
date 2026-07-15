"""
WSGI config for health_manage project.
用于 Gunicorn 等 WSGI 服务器部署
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'health_manage.settings')
application = get_wsgi_application()
