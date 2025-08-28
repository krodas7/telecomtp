# ============================================================================
# CONFIGURACIÓN DE GUNICORN PARA PRODUCCIÓN
# Sistema ARCA Construcción
# ============================================================================

import os
import multiprocessing
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN BÁSICA
# ============================================================================

# Aplicación WSGI
wsgi_app = 'sistema_construccion.wsgi_production:application'

# Configuración del servidor
bind = '0.0.0.0:8000'
backlog = 2048

# ============================================================================
# CONFIGURACIÓN DE WORKERS
# ============================================================================

# Número de workers (recomendado: 2-4 x número de CPUs)
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Tipo de worker
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'sync')

# Conexiones por worker
worker_connections = int(os.environ.get('GUNICORN_WORKER_CONNECTIONS', 1000))

# Máximo de requests por worker antes de reiniciar
max_requests = int(os.environ.get('GUNICORN_MAX_REQUESTS', 1000))

# Jitter para evitar que todos los workers se reinicien al mismo tiempo
max_requests_jitter = int(os.environ.get('GUNICORN_MAX_REQUESTS_JITTER', 50))

# ============================================================================
# CONFIGURACIÓN DE TIMEOUTS
# ============================================================================

# Timeout para workers
timeout = 30

# Timeout para keep-alive
keepalive = 2

# Timeout para graceful shutdown
graceful_timeout = 30

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

# Directorio de logs
log_dir = Path(__file__).resolve().parent / 'logs'
log_dir.mkdir(exist_ok=True)

# Archivo de logs de acceso
accesslog = str(log_dir / 'gunicorn_access.log')

# Archivo de logs de error
errorlog = str(log_dir / 'gunicorn_error.log')

# Nivel de logging
loglevel = 'info'

# Formato de logs
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

# Usuario y grupo para ejecutar Gunicorn
user = os.environ.get('GUNICORN_USER', 'arca')
group = os.environ.get('GUNICORN_GROUP', 'arca')

# Directorio de trabajo
chdir = str(Path(__file__).resolve().parent)

# Variables de entorno
raw_env = [
    'DJANGO_SETTINGS_MODULE=sistema_construccion.production_settings',
    'PYTHONPATH=' + str(Path(__file__).resolve().parent),
]

# ============================================================================
# CONFIGURACIÓN DE RENDIMIENTO
# ============================================================================

# Preload de la aplicación
preload_app = True

# Worker tmp directory
worker_tmp_dir = '/dev/shm'

# ============================================================================
# CONFIGURACIÓN DE MONITOREO
# ============================================================================

# Habilitar stats
statsd_host = os.environ.get('STATSD_HOST', 'localhost:8125')
statsd_prefix = 'gunicorn'

# ============================================================================
# CONFIGURACIÓN DE PROCESOS
# ============================================================================

# PID file
pidfile = str(log_dir / 'gunicorn.pid')

# Daemon mode (False para systemd)
daemon = False

# ============================================================================
# CONFIGURACIÓN DE SEÑALES
# ============================================================================

# Señales para reload
reload_extra_files = [
    str(Path(__file__).resolve().parent / 'sistema_construccion' / 'settings.py'),
    str(Path(__file__).resolve().parent / 'sistema_construccion' / 'production_settings.py'),
]

# ============================================================================
# CONFIGURACIÓN DE LIMITES
# ============================================================================

# Límite de archivos abiertos
worker_abort_on_error = True

# ============================================================================
# CONFIGURACIÓN DE CHECKUP
# ============================================================================

# Health check
def when_ready(server):
    """Callback cuando el servidor está listo"""
    server.log.info("🚀 Gunicorn está listo para recibir conexiones")
    server.log.info(f"📊 Workers: {workers}")
    server.log.info(f"🔗 Bind: {bind}")
    server.log.info(f"📁 Working Directory: {chdir}")

def on_starting(server):
    """Callback cuando el servidor está iniciando"""
    server.log.info("🔄 Iniciando Gunicorn...")

def on_reload(server):
    """Callback cuando se recarga el servidor"""
    server.log.info("🔄 Recargando Gunicorn...")

def worker_int(worker):
    """Callback cuando un worker se interrumpe"""
    worker.log.info("⚠️ Worker interrumpido")

def pre_fork(server, worker):
    """Callback antes de crear un worker"""
    server.log.info(f"🆕 Creando worker {worker.pid}")

def post_fork(server, worker):
    """Callback después de crear un worker"""
    server.log.info(f"✅ Worker {worker.pid} creado")

def post_worker_init(worker):
    """Callback después de inicializar un worker"""
    worker.log.info(f"🚀 Worker {worker.pid} inicializado")

def worker_abort(worker):
    """Callback cuando un worker falla"""
    worker.log.info(f"❌ Worker {worker.pid} falló")

# ============================================================================
# CONFIGURACIÓN DE LIMPIEZA
# ============================================================================

# Limpiar archivos temporales al salir
def cleanup():
    """Limpieza al salir"""
    import tempfile
    import shutil
    
    # Limpiar directorio temporal de workers
    temp_dir = Path('/dev/shm')
    if temp_dir.exists():
        for item in temp_dir.glob('gunicorn-*'):
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)

# ============================================================================
# CONFIGURACIÓN DE ENTORNO
# ============================================================================

# Variables de entorno adicionales
env = {
    'DJANGO_SETTINGS_MODULE': 'sistema_construccion.production_settings',
    'PYTHONPATH': str(Path(__file__).resolve().parent),
    'GUNICORN_CMD_ARGS': '--config gunicorn.conf.py',
}

# ============================================================================
# CONFIGURACIÓN DE DEBUG
# ============================================================================

# Habilitar debug en desarrollo
if os.environ.get('DEBUG', 'False').lower() == 'true':
    reload = True
    workers = 1
    loglevel = 'debug'
    print("🔧 Modo debug habilitado")
    print(f"📊 Configuración: {workers} workers, reload={reload}")
else:
    print("🚀 Modo producción habilitado")
    print(f"📊 Configuración: {workers} workers, timeout={timeout}s")
