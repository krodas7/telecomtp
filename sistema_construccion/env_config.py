"""
Configuración de entorno para el sistema de construcción
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / '.env'

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

# Configuración del entorno
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-construccion-2025-kevin-sistema')

# Configuración de base de datos
DATABASE_CONFIG = {
    'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
    'NAME': os.getenv('DB_NAME', str(BASE_DIR / 'db.sqlite3')),
    'USER': os.getenv('DB_USER', ''),
    'PASSWORD': os.getenv('DB_PASSWORD', ''),
    'HOST': os.getenv('DB_HOST', ''),
    'PORT': os.getenv('DB_PORT', ''),
}

# Configuración de email
EMAIL_CONFIG = {
    'BACKEND': os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend'),
    'HOST': os.getenv('EMAIL_HOST', 'smtp.gmail.com'),
    'PORT': int(os.getenv('EMAIL_PORT', '587')),
    'USE_TLS': os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true',
    'HOST_USER': os.getenv('EMAIL_HOST_USER', ''),
    'HOST_PASSWORD': os.getenv('EMAIL_HOST_PASSWORD', ''),
    'DEFAULT_FROM_EMAIL': os.getenv('DEFAULT_FROM_EMAIL', ''),
}

# Configuración de caché
CACHE_CONFIG = {
    'BACKEND': os.getenv('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
    'LOCATION': os.getenv('CACHE_LOCATION', 'unique-snowflake'),
    'TIMEOUT': int(os.getenv('CACHE_TIMEOUT', '300')),
}

# Configuración de Redis
REDIS_CONFIG = {
    'HOST': os.getenv('REDIS_HOST', 'localhost'),
    'PORT': int(os.getenv('REDIS_PORT', '6379')),
    'DB': int(os.getenv('REDIS_DB', '0')),
    'PASSWORD': os.getenv('REDIS_PASSWORD', ''),
    'SSL': os.getenv('REDIS_SSL', 'False').lower() == 'true',
}

# Configuración de AWS (opcional)
AWS_CONFIG = {
    'ACCESS_KEY_ID': os.getenv('AWS_ACCESS_KEY_ID', ''),
    'SECRET_ACCESS_KEY': os.getenv('AWS_SECRET_ACCESS_KEY', ''),
    'REGION_NAME': os.getenv('AWS_REGION_NAME', 'us-east-1'),
    'S3_BUCKET_NAME': os.getenv('AWS_S3_BUCKET_NAME', ''),
    'CLOUDFRONT_DOMAIN': os.getenv('AWS_CLOUDFRONT_DOMAIN', ''),
}

# Configuración de Google (opcional)
GOOGLE_CONFIG = {
    'CLIENT_ID': os.getenv('GOOGLE_CLIENT_ID', ''),
    'CLIENT_SECRET': os.getenv('GOOGLE_CLIENT_SECRET', ''),
    'OAUTH2_REDIRECT_URI': os.getenv('GOOGLE_OAUTH2_REDIRECT_URI', ''),
}

# Configuración de Facebook (opcional)
FACEBOOK_CONFIG = {
    'APP_ID': os.getenv('FACEBOOK_APP_ID', ''),
    'APP_SECRET': os.getenv('FACEBOOK_APP_SECRET', ''),
    'OAUTH2_REDIRECT_URI': os.getenv('FACEBOOK_OAUTH2_REDIRECT_URI', ''),
}

# Configuración de Stripe (opcional)
STRIPE_CONFIG = {
    'PUBLISHABLE_KEY': os.getenv('STRIPE_PUBLISHABLE_KEY', ''),
    'SECRET_KEY': os.getenv('STRIPE_SECRET_KEY', ''),
    'WEBHOOK_SECRET': os.getenv('STRIPE_WEBHOOK_SECRET', ''),
}

# Configuración de PayPal (opcional)
PAYPAL_CONFIG = {
    'CLIENT_ID': os.getenv('PAYPAL_CLIENT_ID', ''),
    'CLIENT_SECRET': os.getenv('PAYPAL_CLIENT_SECRET', ''),
    'MODE': os.getenv('PAYPAL_MODE', 'sandbox'),  # sandbox o live
}

# Configuración de Twilio (opcional)
TWILIO_CONFIG = {
    'ACCOUNT_SID': os.getenv('TWILIO_ACCOUNT_SID', ''),
    'AUTH_TOKEN': os.getenv('TWILIO_AUTH_TOKEN', ''),
    'PHONE_NUMBER': os.getenv('TWILIO_PHONE_NUMBER', ''),
}

# Configuración de SendGrid (opcional)
SENDGRID_CONFIG = {
    'API_KEY': os.getenv('SENDGRID_API_KEY', ''),
    'FROM_EMAIL': os.getenv('SENDGRID_FROM_EMAIL', ''),
    'FROM_NAME': os.getenv('SENDGRID_FROM_NAME', ''),
}

# Configuración de Cloudinary (opcional)
CLOUDINARY_CONFIG = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME', ''),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY', ''),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET', ''),
}

# Configuración de Sentry (opcional)
SENTRY_CONFIG = {
    'DSN': os.getenv('SENTRY_DSN', ''),
    'ENVIRONMENT': ENVIRONMENT,
    'TRACES_SAMPLE_RATE': float(os.getenv('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
}

# Configuración de Logging
LOGGING_CONFIG = {
    'LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
    'FILE': os.getenv('LOG_FILE', str(BASE_DIR / 'logs' / 'django.log')),
    'MAX_SIZE_MB': int(os.getenv('LOG_MAX_SIZE_MB', '10')),
    'BACKUP_COUNT': int(os.getenv('LOG_BACKUP_COUNT', '5')),
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'ALLOWED_HOSTS': os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(','),
    'CSRF_TRUSTED_ORIGINS': os.getenv('CSRF_TRUSTED_ORIGINS', '').split(','),
    'SECURE_SSL_REDIRECT': os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true',
    'SECURE_HSTS_SECONDS': int(os.getenv('SECURE_HSTS_SECONDS', '0')),
    'SECURE_HSTS_INCLUDE_SUBDOMAINS': os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'False').lower() == 'true',
    'SECURE_HSTS_PRELOAD': os.getenv('SECURE_HSTS_PRELOAD', 'False').lower() == 'true',
    'SECURE_CONTENT_TYPE_NOSNIFF': os.getenv('SECURE_CONTENT_TYPE_NOSNIFF', 'True').lower() == 'true',
    'SECURE_BROWSER_XSS_FILTER': os.getenv('SECURE_BROWSER_XSS_FILTER', 'True').lower() == 'true',
    'SECURE_FRAME_DENY': os.getenv('SECURE_FRAME_DENY', 'True').lower() == 'true',
}

# Configuración de archivos
FILE_CONFIG = {
    'MAX_UPLOAD_SIZE_MB': int(os.getenv('MAX_UPLOAD_SIZE_MB', '50')),
    'MEDIA_ROOT': os.getenv('MEDIA_ROOT', str(BASE_DIR / 'media')),
    'STATIC_ROOT': os.getenv('STATIC_ROOT', str(BASE_DIR / 'staticfiles')),
    'BACKUP_ROOT': os.getenv('BACKUP_ROOT', str(BASE_DIR / 'backups')),
    'TEMP_ROOT': os.getenv('TEMP_ROOT', str(BASE_DIR / 'temp')),
}

# Configuración de API
API_CONFIG = {
    'RATE_LIMIT_ENABLED': os.getenv('API_RATE_LIMIT_ENABLED', 'True').lower() == 'true',
    'RATE_LIMIT_PER_HOUR': int(os.getenv('API_RATE_LIMIT_PER_HOUR', '1000')),
    'CORS_ENABLED': os.getenv('API_CORS_ENABLED', 'False').lower() == 'true',
    'CORS_ALLOWED_ORIGINS': os.getenv('API_CORS_ALLOWED_ORIGINS', '').split(','),
    'AUTHENTICATION_REQUIRED': os.getenv('API_AUTHENTICATION_REQUIRED', 'True').lower() == 'true',
}

# Configuración de IA
AI_CONFIG = {
    'ENABLED': os.getenv('AI_ENABLED', 'True').lower() == 'true',
    'MODEL_PATH': os.getenv('AI_MODEL_PATH', str(BASE_DIR / 'core' / 'ml_models')),
    'TRAINING_ENABLED': os.getenv('AI_TRAINING_ENABLED', 'False').lower() == 'true',
    'PREDICTION_CACHE_TIMEOUT': int(os.getenv('AI_PREDICTION_CACHE_TIMEOUT', '3600')),
    'CONFIDENCE_THRESHOLD': float(os.getenv('AI_CONFIDENCE_THRESHOLD', '0.8')),
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    'EMAIL_ENABLED': os.getenv('NOTIFICATION_EMAIL_ENABLED', 'True').lower() == 'true',
    'SMS_ENABLED': os.getenv('NOTIFICATION_SMS_ENABLED', 'False').lower() == 'true',
    'PUSH_ENABLED': os.getenv('NOTIFICATION_PUSH_ENABLED', 'False').lower() == 'true',
    'WEBHOOK_ENABLED': os.getenv('NOTIFICATION_WEBHOOK_ENABLED', 'False').lower() == 'true',
    'BATCH_SIZE': int(os.getenv('NOTIFICATION_BATCH_SIZE', '50')),
    'RETRY_ATTEMPTS': int(os.getenv('NOTIFICATION_RETRY_ATTEMPTS', '3')),
}

# Configuración de respaldo
BACKUP_CONFIG = {
    'ENABLED': os.getenv('BACKUP_ENABLED', 'True').lower() == 'true',
    'FREQUENCY_HOURS': int(os.getenv('BACKUP_FREQUENCY_HOURS', '24')),
    'RETENTION_DAYS': int(os.getenv('BACKUP_RETENTION_DAYS', '30')),
    'COMPRESSION': os.getenv('BACKUP_COMPRESSION', 'True').lower() == 'true',
    'ENCRYPTION': os.getenv('BACKUP_ENCRYPTION', 'False').lower() == 'true',
    'VERIFICATION': os.getenv('BACKUP_VERIFICATION', 'True').lower() == 'true',
}

# Configuración de mantenimiento
MAINTENANCE_CONFIG = {
    'ENABLED': os.getenv('MAINTENANCE_ENABLED', 'False').lower() == 'true',
    'MESSAGE': os.getenv('MAINTENANCE_MESSAGE', 'El sistema está en mantenimiento. Por favor, inténtelo más tarde.'),
    'ALLOWED_IPS': os.getenv('MAINTENANCE_ALLOWED_IPS', '127.0.0.1,localhost').split(','),
    'START_TIME': os.getenv('MAINTENANCE_START_TIME', ''),
    'END_TIME': os.getenv('MAINTENANCE_END_TIME', ''),
}

# Función para obtener configuración del entorno
def get_environment():
    """
    Obtiene el entorno actual del sistema
    
    Returns:
        String con el nombre del entorno
    """
    return ENVIRONMENT

# Función para verificar si es desarrollo
def is_development():
    """
    Verifica si el sistema está en modo desarrollo
    
    Returns:
        Boolean indicando si es desarrollo
    """
    return ENVIRONMENT == 'development'

# Función para verificar si es producción
def is_production():
    """
    Verifica si el sistema está en modo producción
    
    Returns:
        Boolean indicando si es producción
    """
    return ENVIRONMENT == 'production'

# Función para verificar si es testing
def is_testing():
    """
    Verifica si el sistema está en modo testing
    
    Returns:
        Boolean indicando si es testing
    """
    return ENVIRONMENT == 'testing'

# Función para obtener configuración de base de datos
def get_database_config():
    """
    Obtiene la configuración de base de datos
    
    Returns:
        Diccionario con la configuración de base de datos
    """
    return DATABASE_CONFIG

# Función para obtener configuración de email
def get_email_config():
    """
    Obtiene la configuración de email
    
    Returns:
        Diccionario con la configuración de email
    """
    return EMAIL_CONFIG

# Función para obtener configuración de caché
def get_cache_config():
    """
    Obtiene la configuración de caché
    
    Returns:
        Diccionario con la configuración de caché
    """
    return CACHE_CONFIG

# Función para obtener configuración de Redis
def get_redis_config():
    """
    Obtiene la configuración de Redis
    
    Returns:
        Diccionario con la configuración de Redis
    """
    return REDIS_CONFIG

# Función para obtener configuración de AWS
def get_aws_config():
    """
    Obtiene la configuración de AWS
    
    Returns:
        Diccionario con la configuración de AWS
    """
    return AWS_CONFIG

# Función para obtener configuración de Google
def get_google_config():
    """
    Obtiene la configuración de Google
    
    Returns:
        Diccionario con la configuración de Google
    """
    return GOOGLE_CONFIG

# Función para obtener configuración de Facebook
def get_facebook_config():
    """
    Obtiene la configuración de Facebook
    
    Returns:
        Diccionario con la configuración de Facebook
    """
    return FACEBOOK_CONFIG

# Función para obtener configuración de Stripe
def get_stripe_config():
    """
    Obtiene la configuración de Stripe
    
    Returns:
        Diccionario con la configuración de Stripe
    """
    return STRIPE_CONFIG

# Función para obtener configuración de PayPal
def get_paypal_config():
    """
    Obtiene la configuración de PayPal
    
    Returns:
        Diccionario con la configuración de PayPal
    """
    return PAYPAL_CONFIG

# Función para obtener configuración de Twilio
def get_twilio_config():
    """
    Obtiene la configuración de Twilio
    
    Returns:
        Diccionario con la configuración de Twilio
    """
    return TWILIO_CONFIG

# Función para obtener configuración de SendGrid
def get_sendgrid_config():
    """
    Obtiene la configuración de SendGrid
    
    Returns:
        Diccionario con la configuración de SendGrid
    """
    return SENDGRID_CONFIG

# Función para obtener configuración de Cloudinary
def get_cloudinary_config():
    """
    Obtiene la configuración de Cloudinary
    
    Returns:
        Diccionario con la configuración de Cloudinary
    """
    return CLOUDINARY_CONFIG

# Función para obtener configuración de Sentry
def get_sentry_config():
    """
    Obtiene la configuración de Sentry
    
    Returns:
        Diccionario con la configuración de Sentry
    """
    return SENTRY_CONFIG

# Función para obtener configuración de logging
def get_logging_config():
    """
    Obtiene la configuración de logging
    
    Returns:
        Diccionario con la configuración de logging
    """
    return LOGGING_CONFIG

# Función para obtener configuración de seguridad
def get_security_config():
    """
    Obtiene la configuración de seguridad
    
    Returns:
        Diccionario con la configuración de seguridad
    """
    return SECURITY_CONFIG

# Función para obtener configuración de archivos
def get_file_config():
    """
    Obtiene la configuración de archivos
    
    Returns:
        Diccionario con la configuración de archivos
    """
    return FILE_CONFIG

# Función para obtener configuración de API
def get_api_config():
    """
    Obtiene la configuración de API
    
    Returns:
        Diccionario con la configuración de API
    """
    return API_CONFIG

# Función para obtener configuración de IA
def get_ai_config():
    """
    Obtiene la configuración de IA
    
    Returns:
        Diccionario con la configuración de IA
    """
    return AI_CONFIG

# Función para obtener configuración de notificaciones
def get_notification_config():
    """
    Obtiene la configuración de notificaciones
    
    Returns:
        Diccionario con la configuración de notificaciones
    """
    return NOTIFICATION_CONFIG

# Función para obtener configuración de respaldo
def get_backup_config():
    """
    Obtiene la configuración de respaldo
    
    Returns:
        Diccionario con la configuración de respaldo
    """
    return BACKUP_CONFIG

# Función para obtener configuración de mantenimiento
def get_maintenance_config():
    """
    Obtiene la configuración de mantenimiento
    
    Returns:
        Diccionario con la configuración de mantenimiento
    """
    return MAINTENANCE_CONFIG

# Función para validar configuración del entorno
def validate_environment_config():
    """
    Valida la configuración del entorno
    
    Returns:
        Tuple (is_valid, errors)
    """
    errors = []
    
    # Validar configuración de base de datos
    db_config = get_database_config()
    if not db_config['ENGINE']:
        errors.append("Motor de base de datos no configurado")
    
    # Validar configuración de email en producción
    if is_production():
        email_config = get_email_config()
        if email_config['BACKEND'] == 'django.core.mail.backends.console.EmailBackend':
            errors.append("Backend de email de consola no permitido en producción")
        
        if not email_config['HOST_USER'] or not email_config['HOST_PASSWORD']:
            errors.append("Credenciales de email requeridas en producción")
    
    # Validar configuración de seguridad en producción
    if is_production():
        security_config = get_security_config()
        if not security_config['SECURE_SSL_REDIRECT']:
            errors.append("Redirección SSL requerida en producción")
        
        if security_config['SECURE_HSTS_SECONDS'] == 0:
            errors.append("HSTS requerido en producción")
    
    return len(errors) == 0, errors

# Función para crear archivo .env de ejemplo
def create_env_example():
    """
    Crea un archivo .env.example con todas las variables de entorno
    """
    env_example_content = """# Configuración del entorno
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-here

# Configuración de base de datos
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=

# Configuración de email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Configuración de caché
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
CACHE_LOCATION=unique-snowflake
CACHE_TIMEOUT=300

# Configuración de Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
REDIS_SSL=False

# Configuración de seguridad
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
SECURE_HSTS_INCLUDE_SUBDOMAINS=False
SECURE_HSTS_PRELOAD=False

# Configuración de archivos
MAX_UPLOAD_SIZE_MB=50
MEDIA_ROOT=
STATIC_ROOT=
BACKUP_ROOT=
TEMP_ROOT=

# Configuración de API
API_RATE_LIMIT_ENABLED=True
API_RATE_LIMIT_PER_HOUR=1000
API_CORS_ENABLED=False
API_CORS_ALLOWED_ORIGINS=
API_AUTHENTICATION_REQUIRED=True

# Configuración de IA
AI_ENABLED=True
AI_MODEL_PATH=
AI_TRAINING_ENABLED=False
AI_PREDICTION_CACHE_TIMEOUT=3600
AI_CONFIDENCE_THRESHOLD=0.8

# Configuración de notificaciones
NOTIFICATION_EMAIL_ENABLED=True
NOTIFICATION_SMS_ENABLED=False
NOTIFICATION_PUSH_ENABLED=False
NOTIFICATION_WEBHOOK_ENABLED=False
NOTIFICATION_BATCH_SIZE=50
NOTIFICATION_RETRY_ATTEMPTS=3

# Configuración de respaldo
BACKUP_ENABLED=True
BACKUP_FREQUENCY_HOURS=24
BACKUP_RETENTION_DAYS=30
BACKUP_COMPRESSION=True
BACKUP_ENCRYPTION=False
BACKUP_VERIFICATION=True

# Configuración de mantenimiento
MAINTENANCE_ENABLED=False
MAINTENANCE_MESSAGE=El sistema está en mantenimiento. Por favor, inténtelo más tarde.
MAINTENANCE_ALLOWED_IPS=127.0.0.1,localhost
MAINTENANCE_START_TIME=
MAINTENANCE_END_TIME=

# Configuración de logging
LOG_LEVEL=INFO
LOG_FILE=
LOG_MAX_SIZE_MB=10
LOG_BACKUP_COUNT=5
"""
    
    env_example_file = BASE_DIR / '.env.example'
    with open(env_example_file, 'w', encoding='utf-8') as f:
        f.write(env_example_content)
    
    return env_example_file
