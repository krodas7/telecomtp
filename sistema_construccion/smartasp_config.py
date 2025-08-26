"""
Configuración específica para SmartASP
"""

# Configuración de base de datos para SmartASP
SMARTASP_DATABASE = {
    'ENGINE': 'sql_server.pyodbc',
    'DRIVER': 'ODBC Driver 17 for SQL Server',
    'PORT': '1433',
    'OPTIONS': {
        'unicode_results': True,
        'timeout': 60,
    }
}

# Configuración de archivos para SmartASP
SMARTASP_FILES = {
    'STATIC_ROOT': 'staticfiles',
    'MEDIA_ROOT': 'media',
    'BACKUP_ROOT': 'backups',
    'LOGS_ROOT': 'logs',
}

# Configuración de rendimiento para SmartASP
SMARTASP_PERFORMANCE = {
    'MAX_CONNECTIONS': 50,
    'CONNECTION_POOL_SIZE': 10,
    'QUERY_TIMEOUT': 60,
    'CACHE_TIMEOUT': 300,
}

# Configuración de seguridad para SmartASP
SMARTASP_SECURITY = {
    'SSL_REDIRECT': False,  # SmartASP maneja SSL
    'SESSION_SECURE': False,
    'CSRF_SECURE': False,
    'HSTS_SECONDS': 31536000,
}

# Configuración de monitoreo para SmartASP
SMARTASP_MONITORING = {
    'HEALTH_CHECK_INTERVAL': 600,  # 10 minutos
    'METRICS_COLLECTION': 300,     # 5 minutos
    'LOG_RETENTION': 90,           # días
    'BACKUP_FREQUENCY': 24,        # horas
}
