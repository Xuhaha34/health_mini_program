"""
Django settings for health_manage project.
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'change-this-on-real-server-but-local-test-ok'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# ==================== 应用注册 ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方应用
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    # 业务应用
    'apps.users',
    'apps.health_record',
    'apps.health_plan',
    'apps.health_news',
    'apps.ai_chat',
]

# ==================== 中间件 ====================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',          # 跨域中间件（放在最上层）
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'health_manage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'health_manage.wsgi.application'

# ==================== 数据库配置（MySQL） ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'health_manage_db',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# ==================== 自定义用户模型 ====================
AUTH_USER_MODEL = 'users.User'

# ==================== 密码验证 ====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]

# ==================== 国际化 ====================
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# ==================== 静态文件 & 媒体文件 ====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==================== 跨域配置 ====================
CORS_ALLOW_ALL_ORIGINS = True  # 开发环境允许所有来源
CORS_ALLOW_CREDENTIALS = True

# ==================== DRF 配置 ====================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.StandardPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    'COERCE_DECIMAL_TO_STRING': False,
}

# ==================== SimpleJWT 配置 ====================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== AI 健康问答配置 ====================
# 供应商：local / deepseek / zhipu / qwen / doubao / openai
# 建议在环境变量中设置（不把密钥写进 settings.py 提交到 git）
# PowerShell 设置示例：
#   $env:AI_PROVIDER = "zhipu"
#   $env:AI_API_KEY  = "sk-xxxxxxxxxxxxxxxxxxxx"
AI_PROVIDER = "zhipu"           # 改这里切换供应商（也可以不设，默认 local）
AI_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
AI_API_KEY = "4fca78aa25d2466fa8ffeb023b6f2902.6zuh2ua4Qz2tKUkR"
AI_MODEL = "glm-4-flash"
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 1000
AI_TIMEOUT = 30

# 本地模拟生产环境：收集静态文件到这里
STATIC_ROOT = os.path.join(BASE_DIR, 'static_prod')