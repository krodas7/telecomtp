"""
Configuración específica para seguridad del sistema de construcción
"""

import os
from pathlib import Path

# Configuración base de directorios
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de contraseñas
PASSWORD_CONFIG = {
    'min_length': 8,
    'max_length': 128,
    'require_uppercase': True,
    'require_lowercase': True,
    'require_numbers': True,
    'require_special_chars': True,
    'common_password_check': True,
    'password_history_count': 5,
    'expiration_days': 90,
    'warn_before_expiry_days': 14,
}

# Configuración de autenticación
AUTHENTICATION_CONFIG = {
    'max_login_attempts': 5,
    'lockout_duration_minutes': 30,
    'lockout_reset_hours': 24,
    'remember_me_days': 30,
    'session_timeout_hours': 24,
    'inactive_timeout_hours': 8,
    'force_logout_on_password_change': True,
    'require_2fa': False,
    '2fa_methods': ['email', 'sms', 'app'],
}

# Configuración de sesiones
SESSION_CONFIG = {
    'engine': 'django.contrib.sessions.backends.db',
    'cookie_name': 'sessionid',
    'cookie_age': 86400,  # 24 horas
    'cookie_domain': None,
    'cookie_httponly': True,
    'cookie_secure': False,  # Cambiar a True en producción con HTTPS
    'cookie_samesite': 'Lax',
    'expire_at_browser_close': False,
    'save_every_request': False,
    'serializer': 'django.contrib.sessions.serializers.JSONSerializer',
}

# Configuración de CSRF
CSRF_CONFIG = {
    'cookie_name': 'csrftoken',
    'cookie_age': 31449600,  # 1 año
    'cookie_domain': None,
    'cookie_httponly': False,
    'cookie_secure': False,  # Cambiar a True en producción con HTTPS
    'cookie_samesite': 'Lax',
    'trusted_origins': [],
    'failure_view': None,
    'csrf_header_name': 'HTTP_X_CSRFTOKEN',
    'csrf_cookie_name': 'csrftoken',
    'csrf_use_sessions': False,
    'csrf_cookie_httponly': False,
}

# Configuración de XSS
XSS_CONFIG = {
    'enable_xss_protection': True,
    'xss_protection_header': '1; mode=block',
    'content_type_options': 'nosniff',
    'referrer_policy': 'strict-origin-when-cross-origin',
    'permissions_policy': 'geolocation=(), microphone=(), camera=()',
}

# Configuración de HTTPS
HTTPS_CONFIG = {
    'secure_ssl_redirect': False,  # Cambiar a True en producción
    'secure_proxy_ssl_header': ('HTTP_X_FORWARDED_PROTO', 'https'),
    'secure_content_type_nosniff': True,
    'secure_browser_xss_filter': True,
    'secure_frame_deny': True,
    'secure_hsts_seconds': 31536000,  # 1 año
    'secure_hsts_include_subdomains': True,
    'secure_hsts_preload': False,
}

# Configuración de rate limiting
RATE_LIMITING_CONFIG = {
    'enabled': True,
    'default_rate': '100/h',  # 100 requests por hora
    'login_rate': '5/m',      # 5 intentos de login por minuto
    'api_rate': '1000/h',     # 1000 requests API por hora
    'upload_rate': '10/m',    # 10 uploads por minuto
    'download_rate': '100/m', # 100 downloads por minuto
    'block_duration_minutes': 30,
    'cache_timeout': 300,
}

# Configuración de IP whitelist/blacklist
IP_SECURITY_CONFIG = {
    'whitelist_enabled': False,
    'whitelist_ips': [
        '127.0.0.1',
        'localhost',
        '::1',
    ],
    'blacklist_enabled': True,
    'blacklist_ips': [],
    'block_suspicious_ips': True,
    'suspicious_patterns': [
        r'\.(tor|vpn|proxy)\.',
        r'^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)',
    ],
}

# Configuración de archivos
FILE_SECURITY_CONFIG = {
    'allowed_extensions': [
        '.pdf', '.doc', '.docx', '.xls', '.xlsx',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp',
        '.dwg', '.dxf', '.rvt', '.skp', '.3ds',
        '.zip', '.rar', '.7z'
    ],
    'blocked_extensions': [
        '.exe', '.bat', '.cmd', '.com', '.pif',
        '.scr', '.vbs', '.js', '.jar', '.msi',
        '.dll', '.sys', '.drv', '.bin', '.dat'
    ],
    'max_file_size_mb': 50,
    'scan_uploads': True,
    'quarantine_suspicious': True,
    'virus_scan_enabled': False,
}

# Configuración de logging de seguridad
SECURITY_LOGGING_CONFIG = {
    'enabled': True,
    'log_level': 'WARNING',
    'log_file': BASE_DIR / 'logs' / 'security.log',
    'max_file_size_mb': 10,
    'backup_count': 5,
    'log_events': [
        'login_success',
        'login_failure',
        'logout',
        'password_change',
        'permission_denied',
        'suspicious_activity',
        'file_upload',
        'file_download',
        'data_export',
        'admin_action',
    ],
}

# Configuración de auditoría
AUDIT_CONFIG = {
    'enabled': True,
    'log_user_actions': True,
    'log_data_changes': True,
    'log_admin_actions': True,
    'retention_days': 365,
    'encrypt_logs': False,
    'log_sensitive_data': False,
    'audit_trail_enabled': True,
}

# Configuración de backup de seguridad
SECURITY_BACKUP_CONFIG = {
    'enabled': True,
    'frequency': 'daily',
    'encrypt_backups': True,
    'encryption_key_file': BASE_DIR / 'security' / 'backup_key.key',
    'backup_location': BASE_DIR / 'backups' / 'security',
    'retention_days': 90,
    'verify_backups': True,
    'test_restore': False,
}

# Configuración de monitoreo de seguridad
SECURITY_MONITORING_CONFIG = {
    'enabled': True,
    'check_interval_minutes': 15,
    'alert_on_suspicious_activity': True,
    'alert_on_failed_logins': True,
    'alert_on_permission_denied': True,
    'alert_on_file_uploads': False,
    'alert_thresholds': {
        'failed_logins_per_hour': 10,
        'suspicious_ips_per_day': 5,
        'permission_denied_per_hour': 20,
    },
    'notification_methods': ['email', 'sms', 'webhook'],
}

# Configuración de cifrado
ENCRYPTION_CONFIG = {
    'algorithm': 'AES-256-GCM',
    'key_derivation': 'PBKDF2',
    'iterations': 100000,
    'salt_length': 32,
    'key_length': 32,
    'encrypt_sensitive_fields': True,
    'sensitive_fields': [
        'password', 'api_key', 'secret_key',
        'credit_card', 'ssn', 'dpi'
    ],
}

# Configuración de tokens
TOKEN_CONFIG = {
    'jwt_enabled': False,
    'jwt_secret_key': os.getenv('JWT_SECRET_KEY', 'your-secret-key'),
    'jwt_algorithm': 'HS256',
    'jwt_expiration_hours': 24,
    'api_token_enabled': True,
    'api_token_expiration_days': 30,
    'refresh_token_enabled': True,
    'refresh_token_expiration_days': 7,
}

# Función para obtener configuración de contraseñas
def get_password_config():
    """
    Obtiene la configuración de contraseñas
    
    Returns:
        Diccionario con la configuración de contraseñas
    """
    return PASSWORD_CONFIG

# Función para obtener configuración de autenticación
def get_authentication_config():
    """
    Obtiene la configuración de autenticación
    
    Returns:
        Diccionario con la configuración de autenticación
    """
    return AUTHENTICATION_CONFIG

# Función para obtener configuración de sesiones
def get_session_config():
    """
    Obtiene la configuración de sesiones
    
    Returns:
        Diccionario con la configuración de sesiones
    """
    return SESSION_CONFIG

# Función para obtener configuración de CSRF
def get_csrf_config():
    """
    Obtiene la configuración de CSRF
    
    Returns:
        Diccionario con la configuración de CSRF
    """
    return CSRF_CONFIG

# Función para obtener configuración de XSS
def get_xss_config():
    """
    Obtiene la configuración de XSS
    
    Returns:
        Diccionario con la configuración de XSS
    """
    return XSS_CONFIG

# Función para obtener configuración de HTTPS
def get_https_config():
    """
    Obtiene la configuración de HTTPS
    
    Returns:
        Diccionario con la configuración de HTTPS
    """
    return HTTPS_CONFIG

# Función para obtener configuración de rate limiting
def get_rate_limiting_config():
    """
    Obtiene la configuración de rate limiting
    
    Returns:
        Diccionario con la configuración de rate limiting
    """
    return RATE_LIMITING_CONFIG

# Función para obtener configuración de IP
def get_ip_security_config():
    """
    Obtiene la configuración de seguridad de IP
    
    Returns:
        Diccionario con la configuración de IP
    """
    return IP_SECURITY_CONFIG

# Función para obtener configuración de archivos
def get_file_security_config():
    """
    Obtiene la configuración de seguridad de archivos
    
    Returns:
        Diccionario con la configuración de archivos
    """
    return FILE_SECURITY_CONFIG

# Función para obtener configuración de logging
def get_security_logging_config():
    """
    Obtiene la configuración de logging de seguridad
    
    Returns:
        Diccionario con la configuración de logging
    """
    return SECURITY_LOGGING_CONFIG

# Función para obtener configuración de auditoría
def get_audit_config():
    """
    Obtiene la configuración de auditoría
    
    Returns:
        Diccionario con la configuración de auditoría
    """
    return AUDIT_CONFIG

# Función para obtener configuración de backup
def get_security_backup_config():
    """
    Obtiene la configuración de backup de seguridad
    
    Returns:
        Diccionario con la configuración de backup
    """
    return SECURITY_BACKUP_CONFIG

# Función para obtener configuración de monitoreo
def get_security_monitoring_config():
    """
    Obtiene la configuración de monitoreo de seguridad
    
    Returns:
        Diccionario con la configuración de monitoreo
    """
    return SECURITY_MONITORING_CONFIG

# Función para obtener configuración de cifrado
def get_encryption_config():
    """
    Obtiene la configuración de cifrado
    
    Returns:
        Diccionario con la configuración de cifrado
    """
    return ENCRYPTION_CONFIG

# Función para obtener configuración de tokens
def get_token_config():
    """
    Obtiene la configuración de tokens
    
    Returns:
        Diccionario con la configuración de tokens
    """
    return TOKEN_CONFIG

# Función para validar configuración de seguridad
def validate_security_config():
    """
    Valida la configuración de seguridad
    
    Returns:
        Tuple (is_valid, errors)
    """
    errors = []
    
    # Validar configuración de contraseñas
    password_config = get_password_config()
    if password_config['min_length'] < 8:
        errors.append("La longitud mínima de contraseña debe ser al menos 8")
    
    if password_config['min_length'] > password_config['max_length']:
        errors.append("La longitud mínima no puede ser mayor que la máxima")
    
    # Validar configuración de autenticación
    auth_config = get_authentication_config()
    if auth_config['max_login_attempts'] < 1:
        errors.append("El número máximo de intentos de login debe ser al menos 1")
    
    # Validar configuración de sesiones
    session_config = get_session_config()
    if session_config['cookie_age'] < 300:  # 5 minutos
        errors.append("El tiempo de vida de la cookie de sesión debe ser al menos 5 minutos")
    
    return len(errors) == 0, errors

# Función para crear directorios de seguridad
def create_security_directories():
    """
    Crea los directorios necesarios para seguridad
    """
    directories = [
        BASE_DIR / 'logs',
        BASE_DIR / 'backups' / 'security',
        BASE_DIR / 'security',
        BASE_DIR / 'temp' / 'uploads',
        BASE_DIR / 'temp' / 'downloads',
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    return directories
