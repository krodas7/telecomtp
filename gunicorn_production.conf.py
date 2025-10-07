"""
Configuración optimizada de Gunicorn para producción
"""
import multiprocessing
import os

# Configuración básica
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1  # Optimizado para CPU
worker_class = "sync"
worker_connections = 1000
max_requests = 1000  # Reiniciar worker después de 1000 requests
max_requests_jitter = 50  # Variación aleatoria para evitar reinicios simultáneos

# Configuración de timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Configuración de memoria
worker_tmp_dir = "/dev/shm"  # Usar memoria RAM para archivos temporales

# Configuración de logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "warning"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configuración de procesos
preload_app = True  # Cargar aplicación antes de fork
daemon = False
pidfile = "/var/run/gunicorn/telecomtp.pid"
user = "www-data"
group = "www-data"

# Configuración de SSL (si se usa)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de archivos estáticos
static_map = {
    '/static': '/path/to/staticfiles',
    '/media': '/path/to/media'
}

# Configuración de caché
forwarded_allow_ips = '*'
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}
