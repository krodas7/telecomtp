"""
Constantes del sistema de construcción
"""

# Estados de proyectos
PROJECT_STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('en_progreso', 'En Progreso'),
    ('completado', 'Completado'),
    ('cancelado', 'Cancelado'),
    ('pausado', 'Pausado'),
]

# Estados de facturas
INVOICE_STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('pagada', 'Pagada'),
    ('parcial', 'Parcialmente Pagada'),
    ('vencida', 'Vencida'),
    ('cancelada', 'Cancelada'),
]

# Estados de gastos
EXPENSE_STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aprobado', 'Aprobado'),
    ('rechazado', 'Rechazado'),
    ('reembolsado', 'Reembolsado'),
]

# Estados de anticipos
ADVANCE_STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aplicado', 'Aplicado'),
    ('parcial', 'Parcialmente Aplicado'),
    ('vencido', 'Vencido'),
    ('cancelado', 'Cancelado'),
]

# Tipos de anticipos
ADVANCE_TYPE_CHOICES = [
    ('inicial', 'Anticipo Inicial'),
    ('progreso', 'Anticipo por Progreso'),
    ('materiales', 'Anticipo para Materiales'),
    ('equipos', 'Anticipo para Equipos'),
    ('otros', 'Otros'),
]

# Métodos de pago
PAYMENT_METHOD_CHOICES = [
    ('efectivo', 'Efectivo'),
    ('cheque', 'Cheque'),
    ('transferencia', 'Transferencia Bancaria'),
    ('tarjeta', 'Tarjeta de Crédito/Débito'),
    ('deposito', 'Depósito Bancario'),
    ('otros', 'Otros'),
]

# Tipos de archivos permitidos
ALLOWED_FILE_EXTENSIONS = [
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp',
    '.dwg', '.dxf', '.rvt', '.skp', '.3ds',
    '.zip', '.rar', '.7z'
]

# Tamaños máximos de archivos (en MB)
MAX_FILE_SIZES = {
    'document': 10,      # Documentos
    'image': 5,          # Imágenes
    'cad': 25,           # Archivos CAD
    'archive': 50,       # Archivos comprimidos
    'default': 10        # Por defecto
}

# Configuración de paginación
PAGINATION_CONFIG = {
    'default_page_size': 20,
    'max_page_size': 100,
    'page_size_choices': [10, 20, 50, 100],
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    'max_notifications': 100,
    'auto_delete_days': 30,
    'batch_size': 50,
}

# Configuración de caché
CACHE_TIMEOUTS = {
    'dashboard': 300,        # 5 minutos
    'projects': 600,         # 10 minutos
    'clients': 1800,         # 30 minutos
    'invoices': 300,         # 5 minutos
    'expenses': 300,         # 5 minutos
    'reports': 3600,         # 1 hora
}

# Configuración de seguridad
SECURITY_CONFIG = {
    'max_login_attempts': 5,
    'lockout_duration_minutes': 30,
    'password_min_length': 8,
    'session_timeout_hours': 24,
}

# Configuración de reportes
REPORT_CONFIG = {
    'max_export_rows': 10000,
    'export_formats': ['pdf', 'excel', 'csv'],
    'chart_types': ['bar', 'line', 'pie', 'area'],
}

# Configuración de inventario
INVENTORY_CONFIG = {
    'low_stock_threshold': 0.2,  # 20% del stock mínimo
    'critical_stock_threshold': 0.1,  # 10% del stock mínimo
    'auto_reorder_enabled': True,
    'max_assignment_days': 30,
}

# Configuración de presupuestos
BUDGET_CONFIG = {
    'max_variance_percentage': 10,  # 10% de variación permitida
    'approval_threshold': 50000,    # Monto que requiere aprobación
    'revision_required': True,
}

# Configuración de colaboradores
COLLABORATOR_CONFIG = {
    'max_projects': 5,
    'min_contract_days': 30,
    'evaluation_required': True,
}

# Configuración de clientes
CLIENT_CONFIG = {
    'max_active_projects': 10,
    'credit_limit_default': 100000,
    'payment_terms_days': 30,
}

# Configuración de archivos
FILE_CONFIG = {
    'thumbnail_size': (200, 200),
    'preview_size': (800, 600),
    'compression_quality': 85,
    'backup_enabled': True,
}

# Configuración de logs
LOG_CONFIG = {
    'max_log_files': 10,
    'max_file_size_mb': 10,
    'retention_days': 90,
    'log_level': 'INFO',
}

# Configuración de email
EMAIL_CONFIG = {
    'max_retries': 3,
    'retry_delay_seconds': 300,
    'batch_size': 50,
    'timeout_seconds': 30,
}

# Configuración de API
API_CONFIG = {
    'rate_limit_per_minute': 100,
    'max_request_size_mb': 10,
    'cors_enabled': True,
    'authentication_required': True,
}

# Mensajes del sistema
SYSTEM_MESSAGES = {
    'welcome': 'Bienvenido al Sistema de Construcción',
    'session_expired': 'Su sesión ha expirado. Por favor, inicie sesión nuevamente.',
    'access_denied': 'No tiene permisos para acceder a esta funcionalidad.',
    'operation_success': 'Operación realizada exitosamente.',
    'operation_failed': 'La operación no pudo ser completada.',
    'data_not_found': 'No se encontraron los datos solicitados.',
    'validation_error': 'Los datos ingresados no son válidos.',
    'system_error': 'Ocurrió un error del sistema. Por favor, inténtelo más tarde.',
}

# Códigos de error
ERROR_CODES = {
    'VALIDATION_ERROR': 'VAL001',
    'AUTHENTICATION_ERROR': 'AUTH001',
    'AUTHORIZATION_ERROR': 'AUTH002',
    'NOT_FOUND_ERROR': 'NF001',
    'SYSTEM_ERROR': 'SYS001',
    'DATABASE_ERROR': 'DB001',
    'FILE_ERROR': 'FILE001',
}

# Configuración de moneda
CURRENCY_CONFIG = {
    'default_currency': 'GTQ',
    'currency_symbol': 'Q',
    'decimal_places': 2,
    'thousands_separator': ',',
    'decimal_separator': '.',
}

# Configuración de fechas
DATE_CONFIG = {
    'default_format': '%d/%m/%Y',
    'database_format': '%Y-%m-%d',
    'datetime_format': '%d/%m/%Y %H:%M',
    'timezone': 'America/Guatemala',
}

# Configuración de idioma
LANGUAGE_CONFIG = {
    'default_language': 'es',
    'supported_languages': ['es', 'en'],
    'fallback_language': 'es',
}

# Configuración de tema
THEME_CONFIG = {
    'default_theme': 'neostructure',
    'available_themes': ['neostructure', 'classic', 'modern', 'dark'],
    'auto_theme': True,
}

# Configuración de respaldo
BACKUP_CONFIG = {
    'auto_backup': True,
    'backup_frequency_hours': 24,
    'max_backup_files': 30,
    'backup_retention_days': 90,
    'include_media': True,
    'include_database': True,
}

# Configuración de mantenimiento
MAINTENANCE_CONFIG = {
    'maintenance_mode': False,
    'maintenance_message': 'El sistema está en mantenimiento. Por favor, inténtelo más tarde.',
    'allowed_ips': ['127.0.0.1', 'localhost'],
    'maintenance_start': None,
    'maintenance_end': None,
}
