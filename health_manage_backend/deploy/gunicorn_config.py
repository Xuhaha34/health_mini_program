"""
Gunicorn 部署配置
启动命令: gunicorn -c deploy/gunicorn_config.py health_manage.wsgi:application
"""
import multiprocessing

# 绑定地址和端口
bind = "0.0.0.0:8000"

# 工作进程数（推荐：CPU核心数 * 2 + 1）
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 每个worker的线程数
threads = 2

# 最大请求数（防止内存泄漏）
max_requests = 1000
max_requests_jitter = 50

# 超时时间
timeout = 30
graceful_timeout = 30

# 日志
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# 进程名
proc_name = "health_manage"

# 守护进程（生产环境设为True）
daemon = False

# PID文件
pidfile = "gunicorn.pid"
