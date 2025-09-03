"""
Configuración de producción para Sistema ARCA Construcción
Este archivo importa la configuración base y la sobrescribe para producción
"""

from .settings import *

# ============================================================================
# CONFIGURACIÓN DE PRODUCCIÓN
# ============================================================================

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-in-production')

# Configurar hosts permitidos desde variables de entorno
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# ============================================================================
# BASE DE DATOS POSTGRESQL PARA PRODUCCIÓN
# ============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'arca_construccion'),
        'USER': os.environ.get('DB_USER', 'arca_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'charset': 'utf8',
        },
    }
}

# ============================================================================
# ARCHIVOS ESTÁTICOS Y MEDIA PARA PRODUCCIÓN
# ============================================================================

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuración de archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

# Headers de seguridad
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configuración HTTPS (descomentar cuando tengas SSL)
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# Configuración de sesiones
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 3600  # 1 hora
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ============================================================================
# CONFIGURACIÓN DE LOGGING PARA PRODUCCIÓN
# ============================================================================

# Crear directorio de logs si no existe
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'django.log',
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'error.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# ============================================================================
# CONFIGURACIÓN DE CACHE PARA PRODUCCIÓN
# ============================================================================

# Cache con fallback a memoria local (en producción usar Redis)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'sistema_construccion_production_cache',
        'TIMEOUT': 3600,  # 1 hora
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
            'CULL_FREQUENCY': 3,
        }
    },
    'session': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'session_production_cache',
        'TIMEOUT': 86400,  # 24 horas
        'OPTIONS': {
            'MAX_ENTRIES': 2000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# ============================================================================
# CONFIGURACIÓN DE EMAIL PARA PRODUCCIÓN
# ============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# ============================================================================
# CONFIGURACIÓN PWA PARA PRODUCCIÓN
# ============================================================================

PWA_APP_NAME = 'Sistema ARCA Construcción'
PWA_APP_DESCRIPTION = 'Sistema integral de gestión para construcción'
PWA_APP_THEME_COLOR = '#0d6efd'
PWA_APP_BACKGROUND_COLOR = '#ffffff'

# ============================================================================
# CONFIGURACIONES ADICIONALES DE PRODUCCIÓN
# ============================================================================

# Deshabilitar debug toolbar en producción
if 'django_debug_toolbar' in INSTALLED_APPS:
    INSTALLED_APPS.remove('django_debug_toolbar')

# Configuración de archivos temporales
TEMP_DIR = BASE_DIR / 'temp'
TEMP_DIR.mkdir(exist_ok=True)

# Configuración de respaldos
BACKUP_DIR = BASE_DIR / 'backups'
BACKUP_DIR.mkdir(exist_ok=True)

# Configuración de archivos estáticos compilados
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Configuración de compresión
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

print("✅ Configuración de producción cargada correctamente")
print(f"🔒 DEBUG: {DEBUG}")
print(f"🌐 ALLOWED_HOSTS: {ALLOWED_HOSTS}")
print(f"🗄️ Database: {DATABASES['default']['ENGINE']}")
print(f"📁 Static Root: {STATIC_ROOT}")
print(f"📁 Media Root: {MEDIA_ROOT}")
print(f"📝 Logs Dir: {LOGS_DIR}")



