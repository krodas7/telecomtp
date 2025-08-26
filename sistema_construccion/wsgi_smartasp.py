"""
WSGI config for sistema_construccion project in SmartASP.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Configurar variables de entorno para SmartASP
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.smartasp_settings')
os.environ.setdefault('ENVIRONMENT', 'smartasp')

# Configuración de logging para WSGI en SmartASP
import logging
from pathlib import Path

# Crear directorio de logs si no existe
logs_dir = BASE_DIR / 'logs'
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / 'wsgi_smartasp.log'),
        logging.StreamHandler()
    ]
)

# Importar Django después de configurar el path
from django.core.wsgi import get_wsgi_application

# Middleware personalizado para SmartASP
class SmartASPMiddleware:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        # Agregar headers específicos para SmartASP
        environ['HTTP_X_FORWARDED_PROTO'] = 'https'
        environ['HTTP_X_FORWARDED_FOR'] = environ.get('REMOTE_ADDR', '')
        
        # Configurar variables de entorno para SmartASP
        environ['SMARTASP_ENVIRONMENT'] = 'true'
        environ['SMARTASP_HOSTING'] = 'true'
        
        return self.application(environ, start_response)

class PerformanceMiddleware:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        import time
        start_time = time.time()
        
        def custom_start_response(status, headers, exc_info=None):
            # Agregar header de tiempo de respuesta
            headers.append(('X-Response-Time', str(time.time() - start_time)))
            return start_response(status, headers, exc_info)
        
        return self.application(environ, custom_start_response)

class SecurityMiddleware:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        def custom_start_response(status, headers, exc_info=None):
            # Headers de seguridad para SmartASP
            security_headers = [
                ('X-Content-Type-Options', 'nosniff'),
                ('X-Frame-Options', 'DENY'),
                ('X-XSS-Protection', '1; mode=block'),
                ('Referrer-Policy', 'strict-origin-when-cross-origin'),
                ('Permissions-Policy', 'geolocation=(), microphone=(), camera=()'),
            ]
            
            # Agregar headers de seguridad
            for header_name, header_value in security_headers:
                headers.append((header_name, header_value))
            
            return start_response(status, headers, exc_info)
        
        return self.application(environ, custom_start_response)

class ErrorHandlingMiddleware:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        try:
            return self.application(environ, start_response)
        except Exception as e:
            # Log del error
            logging.error(f"Error en WSGI: {str(e)}")
            
            # Respuesta de error personalizada
            status = '500 Internal Server Error'
            headers = [('Content-Type', 'text/html; charset=utf-8')]
            
            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error del Sistema</title>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 50px; }}
                    .error {{ color: #721c24; background-color: #f8d7da; padding: 20px; border-radius: 5px; }}
                </style>
            </head>
            <body>
                <h1>Error del Sistema</h1>
                <div class="error">
                    <p>Ha ocurrido un error en el sistema. Por favor, inténtelo más tarde.</p>
                    <p>Si el problema persiste, contacte al administrador del sistema.</p>
                </div>
            </body>
            </html>
            """
            
            start_response(status, headers)
            return [error_html.encode('utf-8')]

class HealthCheckMiddleware:
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        # Endpoint de health check para SmartASP
        if environ.get('PATH_INFO') == '/health/':
            status = '200 OK'
            headers = [('Content-Type', 'application/json; charset=utf-8')]
            
            health_data = {
                'status': 'healthy',
                'environment': 'smartasp',
                'timestamp': time.time(),
                'version': '1.0.0'
            }
            
            import json
            start_response(status, headers)
            return [json.dumps(health_data).encode('utf-8')]
        
        return self.application(environ, start_response)

# Obtener la aplicación WSGI base
application = get_wsgi_application()

# Aplicar middlewares en orden para SmartASP
application = SmartASPMiddleware(application)
application = PerformanceMiddleware(application)
application = SecurityMiddleware(application)
application = ErrorHandlingMiddleware(application)
application = HealthCheckMiddleware(application)

# Configuración de logging final
logging.info("WSGI application started in SmartASP mode")

# Exportar la aplicación
app = application
