""" 
gunicorn配置文件
参考文档:https://docs.gunicorn.org/en/latest/index.html
参考文档:https://www.uvicorn.org/deployment/
参考文档:https://github.com/blaze33/newco-legacy/blob/master/gunicorn.conf.py.sample
"""


# Server socket
# 绑定HOST和PORT
bind = '0.0.0.0:8082'
# Server最大连接数（64-2048）
backlog = 2048


# Worker processes
# Server的工作进程数,正常范围:2-4 x $(NUM_CORES)
workers = 2
# worker类
worker_class = 'uvicorn.workers.UvicornH11Worker'
# 限制单个进程同时处理的客户端最大数量,normal:1000
worker_connections = 1000
# 处理单个请求所需时间,worker在此时间内没有通知master进程,它将被kill并添加一个新的worker
timeout = 30
# normal:1-5
keepalive = 2


# Debugging
# 调试功能
debug = False
# 输出运行时的执行结果
spew = False


# Server mechanics
# 开启守护进程,将主进程(gunicorn)与控制终端分离并进入后台
daemon = True
# 要写入的pid文件路径
pidfile = None
# gunicorn编写的文件权限掩码
umask = 0
# 以该用户身份运行工作进程,用户id，or用户名，or用None表示当前用户
user = None
# 工作进程所在的用户组,组id，or用户名，or用None表示当前所在用户组
group = None
# 存储临时请求数据的目录,请求被读取后可能很快就会消失
tmp_upload_dir = None


# Logging
# logfile - The path to a log file to write to.
# A path string. "-" means log to stdout.
# loglevel - The granularity of log output
# A string of "debug", "info", "warning", "error", "critical"
errorlog = '-'
loglevel = 'info'
accesslog = '-'


# Process naming
# 与setproctitle一起使用，进程命名，多个gunicorn时用以区分
proc_name = None


# Server hooks
# server钩子
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker):
    pass


def pre_exec(server):
    server.log.info("Forked child, re-executing.")


def when_ready(server):
    server.log.info("Server is ready. Spwawning workers")