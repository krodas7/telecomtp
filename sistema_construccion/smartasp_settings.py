"""
Configuración específica para SmartASP con dominio de Hostinger
"""

from .settings import *
from .env_config import get_environment

# Configuración para SmartASP
DEBUG = False
ENVIRONMENT = 'smartasp'

# Configuración de base de datos para SmartASP (SQL Server)
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': os.getenv('DB_NAME', 'sistema_construccion'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', '1433'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'unicode_results': True,
        },
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
    }
}

# Configuración de archivos estáticos para SmartASP
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Configuración de archivos de media para SmartASP
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Configuración de caché para SmartASP (memoria local)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}

# Configuración de logging para SmartASP
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
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django_smartasp.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# Configuración de email para SmartASP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.hostinger.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', '')

# Configuración de middleware para SmartASP
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.SmartASPMiddleware',
    'core.middleware.SecurityMiddleware',
    'core.middleware.PerformanceMiddleware',
]

# Configuración de seguridad para SmartASP
SECURE_SSL_REDIRECT = False  # SmartASP maneja SSL
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_FRAME_DENY = True

# Configuración de sesiones para SmartASP
SESSION_COOKIE_SECURE = False  # SmartASP maneja SSL
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Configuración de CORS para SmartASP
CORS_ALLOWED_ORIGINS = [
    'https://tu-dominio.com',
    'https://www.tu-dominio.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

CORS_ALLOW_CREDENTIALS = True

# Configuración de archivos de respaldo para SmartASP
BACKUP_ROOT = BASE_DIR / 'backups'
BACKUP_ENABLED = True
BACKUP_FREQUENCY_HOURS = 24
BACKUP_RETENTION_DAYS = 30

# Configuración de monitoreo para SmartASP
MONITORING_ENABLED = True
PERFORMANCE_MONITORING = True
SECURITY_MONITORING = True

# Configuración de notificaciones para SmartASP
NOTIFICATION_EMAIL_ENABLED = True
NOTIFICATION_SMS_ENABLED = False
NOTIFICATION_PUSH_ENABLED = False
NOTIFICATION_WEBHOOK_ENABLED = True

# Configuración de IA para SmartASP
AI_ENABLED = True
AI_TRAINING_ENABLED = False
AI_PREDICTION_CACHE_TIMEOUT = 7200  # 2 horas

# Configuración de mantenimiento para SmartASP
MAINTENANCE_MODE = False
MAINTENANCE_MESSAGE = 'El sistema está en mantenimiento. Por favor, inténtelo más tarde.'

# Configuración de respaldo automático para SmartASP
AUTO_BACKUP_ENABLED = True
BACKUP_COMPRESSION = True
BACKUP_ENCRYPTION = False  # SmartASP puede tener limitaciones
BACKUP_VERIFICATION = True

# Configuración de limpieza automática para SmartASP
AUTO_CLEANUP_ENABLED = True
LOG_RETENTION_DAYS = 90
TEMP_FILE_RETENTION_DAYS = 7

# Configuración de optimización para SmartASP
DATABASE_OPTIMIZATION_ENABLED = True
CACHE_OPTIMIZATION_ENABLED = True
QUERY_OPTIMIZATION_ENABLED = True

# Configuración de auditoría para SmartASP
AUDIT_ENABLED = True
AUDIT_LOG_RETENTION_DAYS = 365
AUDIT_ENCRYPTION_ENABLED = False

# Configuración de respaldo de seguridad para SmartASP
SECURITY_BACKUP_ENABLED = True
SECURITY_LOG_RETENTION_DAYS = 180
SECURITY_ALERT_ENABLED = True

# Configuración de escalabilidad para SmartASP
LOAD_BALANCING_ENABLED = False  # SmartASP puede no soportar
AUTO_SCALING_ENABLED = False
PERFORMANCE_THRESHOLDS = {
    'response_time_ms': 1000,  # Más permisivo para SmartASP
    'database_queries': 100,
    'memory_usage_mb': 256,
}

# Configuración de métricas para SmartASP
METRICS_ENABLED = True
METRICS_COLLECTION_INTERVAL = 300  # 5 minutos para SmartASP
METRICS_RETENTION_DAYS = 30

# Configuración de alertas para SmartASP
ALERTS_ENABLED = True
ALERT_CHANNELS = ['email']
ALERT_THRESHOLDS = {
    'error_rate': 0.10,  # 10% para SmartASP
    'response_time': 2000,  # 2 segundos para SmartASP
    'disk_usage': 0.90,  # 90% para SmartASP
    'memory_usage': 0.85,  # 85% para SmartASP
}

# Configuración de respaldo de emergencia para SmartASP
EMERGENCY_BACKUP_ENABLED = True
EMERGENCY_BACKUP_INTERVAL = 7200  # 2 horas para SmartASP
EMERGENCY_BACKUP_RETENTION = 7

# Configuración de recuperación de desastres para SmartASP
DISASTER_RECOVERY_ENABLED = True
RECOVERY_POINT_OBJECTIVE = 7200  # 2 horas para SmartASP
RECOVERY_TIME_OBJECTIVE = 14400   # 4 horas para SmartASP

# Configuración de cumplimiento para SmartASP
COMPLIANCE_ENABLED = True
GDPR_COMPLIANCE = True
DATA_RETENTION_POLICY = True
PRIVACY_POLICY_ENFORCEMENT = True

# Configuración de rendimiento para SmartASP
PERFORMANCE_OPTIMIZATION = True
QUERY_TIMEOUT = 60  # segundos para SmartASP
MAX_CONNECTIONS = 50  # Limitado para SmartASP
CONNECTION_POOL_SIZE = 10

# Configuración de caché inteligente para SmartASP
INTELLIGENT_CACHING = True
PREDICTIVE_CACHING = True
CACHE_INVALIDATION_STRATEGY = 'lazy'

# Configuración de monitoreo de salud para SmartASP
HEALTH_CHECK_ENABLED = True
HEALTH_CHECK_INTERVAL = 600  # 10 minutos para SmartASP
HEALTH_CHECK_ENDPOINTS = [
    '/health/',
    '/health/database/',
    '/health/cache/',
]

# Configuración de métricas de negocio para SmartASP
BUSINESS_METRICS_ENABLED = True
REVENUE_TRACKING = True
COST_ANALYSIS = True
PROFITABILITY_MONITORING = True

# Configuración de reportes automáticos para SmartASP
AUTO_REPORTING_ENABLED = True
DAILY_REPORTS = True
WEEKLY_REPORTS = True
MONTHLY_REPORTS = True

# Configuración de integración para SmartASP
API_INTEGRATION_ENABLED = True
WEBHOOK_INTEGRATION = True
THIRD_PARTY_SERVICES = True

# Configuración de sincronización para SmartASP
DATA_SYNC_ENABLED = True
REAL_TIME_SYNC = False  # SmartASP puede tener limitaciones
BATCH_SYNC_INTERVAL = 7200  # 2 horas para SmartASP

# Configuración de validación de datos para SmartASP
DATA_VALIDATION_ENABLED = True
INTEGRITY_CHECKS = True
CONSTRAINT_VALIDATION = True

# Configuración de transformación de datos para SmartASP
DATA_TRANSFORMATION_ENABLED = True
ETL_PROCESSES = True
DATA_ENRICHMENT = True

# Configuración de análisis de datos para SmartASP
DATA_ANALYTICS_ENABLED = True
PREDICTIVE_ANALYTICS = True
MACHINE_LEARNING = True

# Configuración de visualización para SmartASP
DATA_VISUALIZATION_ENABLED = True
INTERACTIVE_CHARTS = True
REAL_TIME_DASHBOARDS = False  # SmartASP puede tener limitaciones

# Configuración de exportación para SmartASP
DATA_EXPORT_ENABLED = True
EXPORT_FORMATS = ['pdf', 'excel', 'csv', 'json']
EXPORT_SCHEDULING = True

# Configuración de búsqueda para SmartASP
SEARCH_FUNCTIONALITY_ENABLED = True
FULL_TEXT_SEARCH = True
ADVANCED_FILTERING = True

# Configuración de paginación para SmartASP
PAGINATION_ENABLED = True
PAGE_SIZE_OPTIONS = [10, 25, 50, 100]
INFINITE_SCROLL = False

# Configuración de ordenamiento para SmartASP
SORTING_ENABLED = True
MULTI_COLUMN_SORT = True
CUSTOM_SORT_ORDERS = True

# Configuración de agrupación para SmartASP
GROUPING_ENABLED = True
HIERARCHICAL_GROUPING = True
CUSTOM_GROUPING = True

# Configuración de agregación para SmartASP
AGGREGATION_ENABLED = True
CUSTOM_AGGREGATIONS = True
REAL_TIME_AGGREGATIONS = False  # SmartASP puede tener limitaciones

# Configuración de estadísticas para SmartASP
STATISTICS_ENABLED = True
ADVANCED_STATISTICS = True
STATISTICAL_MODELS = True

# Configuración de alertas inteligentes para SmartASP
INTELLIGENT_ALERTS = True
PREDICTIVE_ALERTS = True
CONTEXTUAL_ALERTS = True

# Configuración de escalado automático para SmartASP
AUTO_SCALING = False  # SmartASP puede no soportar
RESOURCE_MONITORING = True
PERFORMANCE_OPTIMIZATION = True

# Configuración de workflow para SmartASP
WORKFLOW_ENABLED = True
APPROVAL_WORKFLOWS = True
AUTOMATED_WORKFLOWS = True

# Configuración de auditoría de cambios para SmartASP
CHANGE_AUDIT_ENABLED = True
VERSION_CONTROL = True
CHANGE_TRACKING = True

# Configuración de sincronización de datos para SmartASP
DATA_SYNC_ENABLED = True
CONFLICT_RESOLUTION = True
DATA_INTEGRITY = True

# Configuración de validación de integridad para SmartASP
INTEGRITY_VALIDATION = True
CONSTRAINT_CHECKING = True
REFERENTIAL_INTEGRITY = True

# Configuración de optimización de consultas para SmartASP
QUERY_OPTIMIZATION_ENABLED = True
INDEX_OPTIMIZATION = True
QUERY_CACHING = True

# Configuración de compresión de respuestas para SmartASP
RESPONSE_COMPRESSION = True
CONTENT_OPTIMIZATION = True
BANDWIDTH_OPTIMIZATION = True

# Configuración de caché inteligente para SmartASP
INTELLIGENT_CACHING = True
PREDICTIVE_CACHING = True
ADAPTIVE_CACHING = True

# Configuración de balanceo de carga para SmartASP
LOAD_BALANCING = False  # SmartASP puede no soportar
HEALTH_CHECKING = True
FAILOVER_SUPPORT = False

# Configuración de recuperación para SmartASP
FAILOVER_ENABLED = False  # SmartASP puede no soportar
RECOVERY_PROCEDURES = True
BACKUP_VERIFICATION = True

# Configuración de monitoreo de rendimiento para SmartASP
PERFORMANCE_MONITORING = True
BOTTLENECK_DETECTION = True
RESOURCE_UTILIZATION = True

# Configuración de optimización automática para SmartASP
AUTO_OPTIMIZATION = True
ADAPTIVE_OPTIMIZATION = True
PERFORMANCE_TUNING = True
