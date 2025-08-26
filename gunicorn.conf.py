# Configuración de Gunicorn para el Sistema de Construcción
import multiprocessing

# Configuración del servidor
bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Configuración de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configuración de procesos
preload_app = True
daemon = False
pidfile = "gunicorn.pid"
user = None
group = None
tmp_upload_dir = None

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de performance
worker_tmp_dir = "/dev/shm"
forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}

# Configuración específica para Django
def when_ready(server):
    server.log.info("Servidor Gunicorn listo para recibir conexiones")

def on_starting(server):
    server.log.info("Iniciando servidor Gunicorn...")

def on_reload(server):
    server.log.info("Recargando servidor Gunicorn...")

def worker_int(worker):
    worker.log.info("Worker recibió señal INT o QUIT")

def pre_fork(server, worker):
    server.log.info("Worker %d iniciando...", worker.pid)

def post_fork(server, worker):
    server.log.info("Worker %d iniciado", worker.pid)

def post_worker_init(worker):
    worker.log.info("Worker %d inicializado", worker.pid)

def worker_abort(worker):
    worker.log.info("Worker %d abortado", worker.pid)
