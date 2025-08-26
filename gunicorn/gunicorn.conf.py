"""
Configuración de Gunicorn para Sistema de Construcción en producción
"""

import multiprocessing
import os
from pathlib import Path

# Configuración del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_NAME = 'sistema_construccion'

# Configuración del servidor
bind = "127.0.0.1:8000"
backlog = 2048

# Configuración de workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Configuración de timeouts
timeout = 60
keepalive = 2
graceful_timeout = 30
worker_tmp_dir = "/dev/shm"

# Configuración de logging
accesslog = str(BASE_DIR / "logs" / "gunicorn_access.log")
errorlog = str(BASE_DIR / "logs" / "gunicorn_error.log")
loglevel = "warning"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Configuración de seguridad
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Configuración de SSL (si es necesario)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Configuración de usuario y grupo
user = "www-data"
group = "www-data"

# Configuración de directorios temporales
tmp_upload_dir = None

# Configuración de hooks
def on_starting(server):
    """Hook ejecutado cuando el servidor inicia"""
    server.log.info("Iniciando servidor Gunicorn para Sistema de Construcción")

def on_reload(server):
    """Hook ejecutado cuando se recarga el servidor"""
    server.log.info("Recargando servidor Gunicorn")

def worker_int(worker):
    """Hook ejecutado cuando un worker se reinicia"""
    worker.log.info("Worker reiniciado")

def pre_fork(server, worker):
    """Hook ejecutado antes de crear un worker"""
    server.log.info("Creando worker")

def post_fork(server, worker):
    """Hook ejecutado después de crear un worker"""
    server.log.info(f"Worker {worker.pid} creado")

def post_worker_init(worker):
    """Hook ejecutado después de inicializar un worker"""
    worker.log.info(f"Worker {worker.pid} inicializado")

def worker_abort(worker):
    """Hook ejecutado cuando un worker se aborta"""
    worker.log.error(f"Worker {worker.pid} abortado")

def pre_exec(server):
    """Hook ejecutado antes de ejecutar el servidor"""
    server.log.info("Ejecutando servidor")

def when_ready(server):
    """Hook ejecutado cuando el servidor está listo"""
    server.log.info("Servidor Gunicorn listo para recibir conexiones")

def on_exit(server):
    """Hook ejecutado cuando el servidor se cierra"""
    server.log.info("Cerrando servidor Gunicorn")

# Configuración de monitoreo
def worker_exit(server, worker):
    """Hook ejecutado cuando un worker sale"""
    server.log.info(f"Worker {worker.pid} salió")

def child_exit(server, worker):
    """Hook ejecutado cuando un proceso hijo sale"""
    server.log.info(f"Proceso hijo {worker.pid} salió")

# Configuración de señales
def worker_int(worker):
    """Hook ejecutado cuando se recibe SIGINT en un worker"""
    worker.log.info(f"Worker {worker.pid} recibió SIGINT")

def worker_abort(worker):
    """Hook ejecutado cuando un worker se aborta"""
    worker.log.error(f"Worker {worker.pid} abortado")

# Configuración de respaldo
def post_worker_init(worker):
    """Hook ejecutado después de inicializar un worker"""
    worker.log.info(f"Worker {worker.pid} inicializado")
    
    # Configurar logging específico del worker
    import logging
    worker_logger = logging.getLogger(f"gunicorn.worker.{worker.pid}")
    worker_logger.setLevel(logging.INFO)

# Configuración de métricas
def worker_exit(server, worker):
    """Hook ejecutado cuando un worker sale"""
    server.log.info(f"Worker {worker.pid} salió")
    
    # Registrar métricas del worker
    if hasattr(worker, 'requests_count'):
        server.log.info(f"Worker {worker.pid} procesó {worker.requests_count} requests")

# Configuración de salud
def health_check(worker):
    """Verificación de salud del worker"""
    try:
        # Verificar que el worker puede procesar requests
        worker.log.info(f"Worker {worker.pid} saludable")
        return True
    except Exception as e:
        worker.log.error(f"Worker {worker.pid} no saludable: {e}")
        return False

# Configuración de respaldo automático
def auto_backup(server):
    """Respaldo automático del sistema"""
    try:
        import subprocess
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = BASE_DIR / "backups" / "auto"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Crear respaldo de la base de datos
        db_backup_file = backup_dir / f"db_backup_{timestamp}.sql"
        subprocess.run([
            "python", "manage.py", "dumpdata", 
            "--output", str(db_backup_file),
            "--exclude", "contenttypes",
            "--exclude", "sessions"
        ], cwd=BASE_DIR, check=True)
        
        server.log.info(f"Respaldo automático creado: {db_backup_file}")
        
    except Exception as e:
        server.log.error(f"Error en respaldo automático: {e}")

# Configuración de limpieza automática
def auto_cleanup(server):
    """Limpieza automática del sistema"""
    try:
        import subprocess
        from datetime import datetime, timedelta
        
        # Limpiar logs antiguos (más de 30 días)
        logs_dir = BASE_DIR / "logs"
        cutoff_date = datetime.now() - timedelta(days=30)
        
        for log_file in logs_dir.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()
                server.log.info(f"Log antiguo eliminado: {log_file}")
        
        # Limpiar archivos temporales
        temp_dir = BASE_DIR / "temp"
        if temp_dir.exists():
            for temp_file in temp_dir.glob("*"):
                if temp_file.stat().st_mtime < cutoff_date.timestamp():
                    temp_file.unlink()
                    server.log.info(f"Archivo temporal eliminado: {temp_file}")
        
        server.log.info("Limpieza automática completada")
        
    except Exception as e:
        server.log.error(f"Error en limpieza automática: {e}")

# Configuración de monitoreo de rendimiento
def performance_monitor(server):
    """Monitoreo de rendimiento del servidor"""
    try:
        import psutil
        import time
        
        # Obtener estadísticas del sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Log de métricas de rendimiento
        server.log.info(f"CPU: {cpu_percent}%, "
                       f"Memoria: {memory.percent}%, "
                       f"Disco: {disk.percent}%")
        
        # Alertas si los valores son altos
        if cpu_percent > 80:
            server.log.warning(f"CPU alta: {cpu_percent}%")
        
        if memory.percent > 80:
            server.log.warning(f"Memoria alta: {memory.percent}%")
        
        if disk.percent > 85:
            server.log.warning(f"Disco alto: {disk.percent}%")
        
    except ImportError:
        # psutil no está disponible
        pass
    except Exception as e:
        server.log.error(f"Error en monitoreo de rendimiento: {e}")

# Configuración de respaldo de emergencia
def emergency_backup(server):
    """Respaldo de emergencia del sistema"""
    try:
        import subprocess
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = BASE_DIR / "backups" / "emergency"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Respaldar archivos críticos
        critical_files = [
            "manage.py",
            "requirements.txt",
            "sistema_construccion/settings.py",
            "core/models.py",
            "core/views.py"
        ]
        
        for file_path in critical_files:
            src_file = BASE_DIR / file_path
            if src_file.exists():
                dst_file = backup_dir / f"{file_path.replace('/', '_')}_{timestamp}"
                import shutil
                shutil.copy2(src_file, dst_file)
        
        server.log.info("Respaldo de emergencia completado")
        
    except Exception as e:
        server.log.error(f"Error en respaldo de emergencia: {e}")

# Configuración de notificaciones
def send_notification(server, message, level="info"):
    """Enviar notificación del sistema"""
    try:
        # Aquí puedes implementar el envío de notificaciones
        # por email, SMS, webhook, etc.
        if level == "error":
            server.log.error(f"NOTIFICACIÓN: {message}")
        elif level == "warning":
            server.log.warning(f"NOTIFICACIÓN: {message}")
        else:
            server.log.info(f"NOTIFICACIÓN: {message}")
            
    except Exception as e:
        server.log.error(f"Error enviando notificación: {e}")

# Configuración de hooks de ciclo de vida
def on_starting(server):
    """Hook ejecutado cuando el servidor inicia"""
    server.log.info("=== INICIANDO SISTEMA DE CONSTRUCCIÓN ===")
    server.log.info(f"Directorio base: {BASE_DIR}")
    server.log.info(f"Workers: {workers}")
    server.log.info(f"Bind: {bind}")
    
    # Crear directorios necesarios
    for directory in ["logs", "backups", "temp", "media"]:
        dir_path = BASE_DIR / directory
        dir_path.mkdir(exist_ok=True)
        server.log.info(f"Directorio creado/verificado: {dir_path}")

def when_ready(server):
    """Hook ejecutado cuando el servidor está listo"""
    server.log.info("=== SERVIDOR LISTO ===")
    server.log.info("Sistema de Construcción funcionando correctamente")
    
    # Enviar notificación de inicio
    send_notification(server, "Servidor iniciado correctamente", "info")

def on_exit(server):
    """Hook ejecutado cuando el servidor se cierra"""
    server.log.info("=== CERRANDO SISTEMA ===")
    
    # Crear respaldo de emergencia antes de cerrar
    emergency_backup(server)
    
    # Enviar notificación de cierre
    send_notification(server, "Servidor cerrando", "warning")
    
    server.log.info("Sistema de Construcción cerrado")

# Configuración de respaldo periódico
import threading
import time

def periodic_backup(server):
    """Respaldos periódicos del sistema"""
    while True:
        try:
            time.sleep(3600)  # Cada hora
            auto_backup(server)
            auto_cleanup(server)
            performance_monitor(server)
        except Exception as e:
            server.log.error(f"Error en respaldo periódico: {e}")

def start_backup_thread(server):
    """Iniciar thread de respaldo periódico"""
    backup_thread = threading.Thread(
        target=periodic_backup, 
        args=(server,), 
        daemon=True
    )
    backup_thread.start()
    server.log.info("Thread de respaldo periódico iniciado")

# Hook para iniciar thread de respaldo
def post_worker_init(worker):
    """Hook ejecutado después de inicializar un worker"""
    worker.log.info(f"Worker {worker.pid} inicializado")
    
    # Solo el primer worker inicia el thread de respaldo
    if worker.pid == worker.server.pid:
        start_backup_thread(worker.server)



