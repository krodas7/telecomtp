"""
Configuración específica para middleware del sistema de construcción
"""

import os
from pathlib import Path

# Configuración base de directorios
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de middleware de seguridad
SECURITY_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Configuración de middleware de autenticación
AUTHENTICATION_MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

# Configuración de middleware de caché
CACHE_MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# Configuración de middleware de compresión
COMPRESSION_MIDDLEWARE = [
    'django.middleware.gzip.GZipMiddleware',
]

# Configuración de middleware de CORS
CORS_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

# Configuración de middleware de rate limiting
RATE_LIMITING_MIDDLEWARE = [
    'django_ratelimit.middleware.RatelimitMiddleware',
]

# Configuración de middleware de logging
LOGGING_MIDDLEWARE = [
    'django.middleware.logging.LoggingMiddleware',
]

# Configuración de middleware de mantenimiento
MAINTENANCE_MIDDLEWARE = [
    'core.middleware.MaintenanceModeMiddleware',
]

# Configuración de middleware de auditoría
AUDIT_MIDDLEWARE = [
    'core.middleware.AuditMiddleware',
]

# Configuración de middleware de notificaciones
NOTIFICATION_MIDDLEWARE = [
    'core.middleware.NotificationMiddleware',
]

# Configuración de middleware de IA
AI_MIDDLEWARE = [
    'core.middleware.AIMiddleware',
]

# Configuración de middleware de optimización
OPTIMIZATION_MIDDLEWARE = [
    'core.middleware.PerformanceMiddleware',
    'core.middleware.CacheMiddleware',
]

# Configuración de middleware de seguridad avanzada
ADVANCED_SECURITY_MIDDLEWARE = [
    'django_axes.middleware.AxesMiddleware',
    'core.middleware.SecurityMiddleware',
    'core.middleware.IPFilterMiddleware',
]

# Configuración de middleware de monitoreo
MONITORING_MIDDLEWARE = [
    'core.middleware.MonitoringMiddleware',
    'core.middleware.HealthCheckMiddleware',
]

# Configuración de middleware de respaldo
BACKUP_MIDDLEWARE = [
    'core.middleware.BackupMiddleware',
]

# Configuración de middleware de archivos
FILE_MIDDLEWARE = [
    'core.middleware.FileUploadMiddleware',
    'core.middleware.FileDownloadMiddleware',
]

# Configuración de middleware de API
API_MIDDLEWARE = [
    'core.middleware.APIAuthenticationMiddleware',
    'core.middleware.APIRateLimitMiddleware',
    'core.middleware.APIVersionMiddleware',
]

# Configuración de middleware de usuario
USER_MIDDLEWARE = [
    'core.middleware.UserActivityMiddleware',
    'core.middleware.UserPreferencesMiddleware',
    'core.middleware.UserNotificationMiddleware',
]

# Configuración de middleware de proyecto
PROJECT_MIDDLEWARE = [
    'core.middleware.ProjectAccessMiddleware',
    'core.middleware.ProjectNotificationMiddleware',
]

# Configuración de middleware de facturación
BILLING_MIDDLEWARE = [
    'core.middleware.BillingMiddleware',
    'core.middleware.PaymentMiddleware',
]

# Configuración de middleware de inventario
INVENTORY_MIDDLEWARE = [
    'core.middleware.InventoryMiddleware',
    'core.middleware.StockMiddleware',
]

# Configuración de middleware de presupuestos
BUDGET_MIDDLEWARE = [
    'core.middleware.BudgetMiddleware',
    'core.middleware.ApprovalMiddleware',
]

# Configuración de middleware de anticipos
ADVANCE_MIDDLEWARE = [
    'core.middleware.AdvanceMiddleware',
    'core.middleware.ApplicationMiddleware',
]

# Configuración de middleware de archivos de proyecto
PROJECT_FILE_MIDDLEWARE = [
    'core.middleware.FileAccessMiddleware',
    'core.middleware.FileSecurityMiddleware',
]

# Configuración de middleware de notificaciones del sistema
SYSTEM_NOTIFICATION_MIDDLEWARE = [
    'core.middleware.SystemNotificationMiddleware',
    'core.middleware.EmailNotificationMiddleware',
    'core.middleware.SMSNotificationMiddleware',
    'core.middleware.PushNotificationMiddleware',
]

# Configuración de middleware de respaldo automático
AUTO_BACKUP_MIDDLEWARE = [
    'core.middleware.AutoBackupMiddleware',
    'core.middleware.BackupVerificationMiddleware',
]

# Configuración de middleware de limpieza automática
AUTO_CLEANUP_MIDDLEWARE = [
    'core.middleware.AutoCleanupMiddleware',
    'core.middleware.TempFileCleanupMiddleware',
    'core.middleware.LogCleanupMiddleware',
]

# Configuración de middleware de sincronización
SYNC_MIDDLEWARE = [
    'core.middleware.DataSyncMiddleware',
    'core.middleware.CacheSyncMiddleware',
]

# Configuración de middleware de validación
VALIDATION_MIDDLEWARE = [
    'core.middleware.DataValidationMiddleware',
    'core.middleware.FileValidationMiddleware',
]

# Configuración de middleware de transformación
TRANSFORMATION_MIDDLEWARE = [
    'core.middleware.DataTransformationMiddleware',
    'core.middleware.FileTransformationMiddleware',
]

# Configuración de middleware de enriquecimiento
ENRICHMENT_MIDDLEWARE = [
    'core.middleware.DataEnrichmentMiddleware',
    'core.middleware.UserEnrichmentMiddleware',
]

# Configuración de middleware de análisis
ANALYTICS_MIDDLEWARE = [
    'core.middleware.AnalyticsMiddleware',
    'core.middleware.TrackingMiddleware',
]

# Configuración de middleware de reportes
REPORTING_MIDDLEWARE = [
    'core.middleware.ReportingMiddleware',
    'core.middleware.ExportMiddleware',
]

# Configuración de middleware de búsqueda
SEARCH_MIDDLEWARE = [
    'core.middleware.SearchMiddleware',
    'core.middleware.IndexMiddleware',
]

# Configuración de middleware de filtrado
FILTERING_MIDDLEWARE = [
    'core.middleware.FilterMiddleware',
    'core.middleware.SortMiddleware',
]

# Configuración de middleware de paginación
PAGINATION_MIDDLEWARE = [
    'core.middleware.PaginationMiddleware',
]

# Configuración de middleware de ordenamiento
SORTING_MIDDLEWARE = [
    'core.middleware.SortingMiddleware',
]

# Configuración de middleware de agrupación
GROUPING_MIDDLEWARE = [
    'core.middleware.GroupingMiddleware',
]

# Configuración de middleware de agregación
AGGREGATION_MIDDLEWARE = [
    'core.middleware.AggregationMiddleware',
]

# Configuración de middleware de estadísticas
STATISTICS_MIDDLEWARE = [
    'core.middleware.StatisticsMiddleware',
    'core.middleware.MetricsMiddleware',
]

# Configuración de middleware de alertas
ALERT_MIDDLEWARE = [
    'core.middleware.AlertMiddleware',
    'core.middleware.ThresholdMiddleware',
]

# Configuración de middleware de escalado
ESCALATION_MIDDLEWARE = [
    'core.middleware.EscalationMiddleware',
    'core.middleware.PriorityMiddleware',
]

# Configuración de middleware de workflow
WORKFLOW_MIDDLEWARE = [
    'core.middleware.WorkflowMiddleware',
    'core.middleware.ApprovalWorkflowMiddleware',
]

# Configuración de middleware de auditoría de cambios
CHANGE_AUDIT_MIDDLEWARE = [
    'core.middleware.ChangeAuditMiddleware',
    'core.middleware.VersionControlMiddleware',
]

# Configuración de middleware de sincronización de datos
DATA_SYNC_MIDDLEWARE = [
    'core.middleware.DataSyncMiddleware',
    'core.middleware.ConflictResolutionMiddleware',
]

# Configuración de middleware de validación de integridad
INTEGRITY_MIDDLEWARE = [
    'core.middleware.DataIntegrityMiddleware',
    'core.middleware.ConstraintValidationMiddleware',
]

# Configuración de middleware de optimización de consultas
QUERY_OPTIMIZATION_MIDDLEWARE = [
    'core.middleware.QueryOptimizationMiddleware',
    'core.middleware.IndexOptimizationMiddleware',
]

# Configuración de middleware de compresión de respuestas
RESPONSE_COMPRESSION_MIDDLEWARE = [
    'core.middleware.ResponseCompressionMiddleware',
    'core.middleware.ContentOptimizationMiddleware',
]

# Configuración de middleware de caché inteligente
INTELLIGENT_CACHE_MIDDLEWARE = [
    'core.middleware.IntelligentCacheMiddleware',
    'core.middleware.PredictiveCacheMiddleware',
]

# Configuración de middleware de balanceo de carga
LOAD_BALANCING_MIDDLEWARE = [
    'core.middleware.LoadBalancingMiddleware',
    'core.middleware.HealthCheckMiddleware',
]

# Configuración de middleware de failover
FAILOVER_MIDDLEWARE = [
    'core.middleware.FailoverMiddleware',
    'core.middleware.RecoveryMiddleware',
]

# Configuración de middleware de monitoreo de rendimiento
PERFORMANCE_MONITORING_MIDDLEWARE = [
    'core.middleware.PerformanceMonitoringMiddleware',
    'core.middleware.BottleneckDetectionMiddleware',
]

# Configuración de middleware de optimización automática
AUTO_OPTIMIZATION_MIDDLEWARE = [
    'core.middleware.AutoOptimizationMiddleware',
    'core.middleware.AdaptiveOptimizationMiddleware',
]

# Función para obtener middleware según el entorno
def get_middleware_config(environment='development'):
    """
    Obtiene la configuración de middleware según el entorno
    
    Args:
        environment: Entorno del sistema ('development', 'production', 'testing')
        
    Returns:
        Lista con la configuración de middleware
    """
    # Middleware base para todos los entornos
    base_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    
    # Middleware específico por entorno
    if environment == 'development':
        development_middleware = [
            'django.middleware.gzip.GZipMiddleware',
            'core.middleware.DevelopmentMiddleware',
            'core.middleware.DebugMiddleware',
        ]
        return base_middleware + development_middleware
    
    elif environment == 'production':
        production_middleware = [
            'django.middleware.cache.UpdateCacheMiddleware',
            'django.middleware.gzip.GZipMiddleware',
            'corsheaders.middleware.CorsMiddleware',
            'django_ratelimit.middleware.RatelimitMiddleware',
            'core.middleware.ProductionMiddleware',
            'core.middleware.SecurityMiddleware',
            'core.middleware.PerformanceMiddleware',
            'core.middleware.MonitoringMiddleware',
            'django.middleware.cache.FetchFromCacheMiddleware',
        ]
        return base_middleware + production_middleware
    
    elif environment == 'testing':
        testing_middleware = [
            'core.middleware.TestingMiddleware',
            'core.middleware.MockMiddleware',
        ]
        return base_middleware + testing_middleware
    
    else:
        return base_middleware

# Función para obtener middleware de seguridad
def get_security_middleware():
    """
    Obtiene el middleware de seguridad
    
    Returns:
        Lista con el middleware de seguridad
    """
    return SECURITY_MIDDLEWARE

# Función para obtener middleware de autenticación
def get_authentication_middleware():
    """
    Obtiene el middleware de autenticación
    
    Returns:
        Lista con el middleware de autenticación
    """
    return AUTHENTICATION_MIDDLEWARE

# Función para obtener middleware de caché
def get_cache_middleware():
    """
    Obtiene el middleware de caché
    
    Returns:
        Lista con el middleware de caché
    """
    return CACHE_MIDDLEWARE

# Función para obtener middleware de compresión
def get_compression_middleware():
    """
    Obtiene el middleware de compresión
    
    Returns:
        Lista con el middleware de compresión
    """
    return COMPRESSION_MIDDLEWARE

# Función para obtener middleware de CORS
def get_cors_middleware():
    """
    Obtiene el middleware de CORS
    
    Returns:
        Lista con el middleware de CORS
    """
    return CORS_MIDDLEWARE

# Función para obtener middleware de rate limiting
def get_rate_limiting_middleware():
    """
    Obtiene el middleware de rate limiting
    
    Returns:
        Lista con el middleware de rate limiting
    """
    return RATE_LIMITING_MIDDLEWARE

# Función para obtener middleware de logging
def get_logging_middleware():
    """
    Obtiene el middleware de logging
    
    Returns:
        Lista con el middleware de logging
    """
    return LOGGING_MIDDLEWARE

# Función para obtener middleware de mantenimiento
def get_maintenance_middleware():
    """
    Obtiene el middleware de mantenimiento
    
    Returns:
        Lista con el middleware de mantenimiento
    """
    return MAINTENANCE_MIDDLEWARE

# Función para obtener middleware de auditoría
def get_audit_middleware():
    """
    Obtiene el middleware de auditoría
    
    Returns:
        Lista con el middleware de auditoría
    """
    return AUDIT_MIDDLEWARE

# Función para obtener middleware de notificaciones
def get_notification_middleware():
    """
    Obtiene el middleware de notificaciones
    
    Returns:
        Lista con el middleware de notificaciones
    """
    return NOTIFICATION_MIDDLEWARE

# Función para obtener middleware de IA
def get_ai_middleware():
    """
    Obtiene el middleware de IA
    
    Returns:
        Lista con el middleware de IA
    """
    return AI_MIDDLEWARE

# Función para obtener middleware de optimización
def get_optimization_middleware():
    """
    Obtiene el middleware de optimización
    
    Returns:
        Lista con el middleware de optimización
    """
    return OPTIMIZATION_MIDDLEWARE

# Función para obtener middleware de seguridad avanzada
def get_advanced_security_middleware():
    """
    Obtiene el middleware de seguridad avanzada
    
    Returns:
        Lista con el middleware de seguridad avanzada
    """
    return ADVANCED_SECURITY_MIDDLEWARE

# Función para obtener middleware de monitoreo
def get_monitoring_middleware():
    """
    Obtiene el middleware de monitoreo
    
    Returns:
        Lista con el middleware de monitoreo
    """
    return MONITORING_MIDDLEWARE

# Función para obtener middleware de respaldo
def get_backup_middleware():
    """
    Obtiene el middleware de respaldo
    
    Returns:
        Lista con el middleware de respaldo
    """
    return BACKUP_MIDDLEWARE

# Función para obtener middleware de archivos
def get_file_middleware():
    """
    Obtiene el middleware de archivos
    
    Returns:
        Lista con el middleware de archivos
    """
    return FILE_MIDDLEWARE

# Función para obtener middleware de API
def get_api_middleware():
    """
    Obtiene el middleware de API
    
    Returns:
        Lista con el middleware de API
    """
    return API_MIDDLEWARE

# Función para obtener middleware de usuario
def get_user_middleware():
    """
    Obtiene el middleware de usuario
    
    Returns:
        Lista con el middleware de usuario
    """
    return USER_MIDDLEWARE

# Función para obtener middleware de proyecto
def get_project_middleware():
    """
    Obtiene el middleware de proyecto
    
    Returns:
        Lista con el middleware de proyecto
    """
    return PROJECT_MIDDLEWARE

# Función para obtener middleware de facturación
def get_billing_middleware():
    """
    Obtiene el middleware de facturación
    
    Returns:
        Lista con el middleware de facturación
    """
    return BILLING_MIDDLEWARE

# Función para obtener middleware de inventario
def get_inventory_middleware():
    """
    Obtiene el middleware de inventario
    
    Returns:
        Lista con el middleware de inventario
    """
    return INVENTORY_MIDDLEWARE

# Función para obtener middleware de presupuestos
def get_budget_middleware():
    """
    Obtiene el middleware de presupuestos
    
    Returns:
        Lista con el middleware de presupuestos
    """
    return BUDGET_MIDDLEWARE

# Función para obtener middleware de anticipos
def get_advance_middleware():
    """
    Obtiene el middleware de anticipos
    
    Returns:
        Lista con el middleware de anticipos
    """
    return ADVANCE_MIDDLEWARE

# Función para obtener middleware de archivos de proyecto
def get_project_file_middleware():
    """
    Obtiene el middleware de archivos de proyecto
    
    Returns:
        Lista con el middleware de archivos de proyecto
    """
    return PROJECT_FILE_MIDDLEWARE

# Función para obtener middleware de notificaciones del sistema
def get_system_notification_middleware():
    """
    Obtiene el middleware de notificaciones del sistema
    
    Returns:
        Lista con el middleware de notificaciones del sistema
    """
    return SYSTEM_NOTIFICATION_MIDDLEWARE

# Función para obtener middleware de respaldo automático
def get_auto_backup_middleware():
    """
    Obtiene el middleware de respaldo automático
    
    Returns:
        Lista con el middleware de respaldo automático
    """
    return AUTO_BACKUP_MIDDLEWARE

# Función para obtener middleware de limpieza automática
def get_auto_cleanup_middleware():
    """
    Obtiene el middleware de limpieza automática
    
    Returns:
        Lista con el middleware de limpieza automática
    """
    return AUTO_CLEANUP_MIDDLEWARE

# Función para obtener middleware de sincronización
def get_sync_middleware():
    """
    Obtiene el middleware de sincronización
    
    Returns:
        Lista con el middleware de sincronización
    """
    return SYNC_MIDDLEWARE

# Función para obtener middleware de validación
def get_validation_middleware():
    """
    Obtiene el middleware de validación
    
    Returns:
        Lista con el middleware de validación
    """
    return VALIDATION_MIDDLEWARE

# Función para obtener middleware de transformación
def get_transformation_middleware():
    """
    Obtiene el middleware de transformación
    
    Returns:
        Lista con el middleware de transformación
    """
    return TRANSFORMATION_MIDDLEWARE

# Función para obtener middleware de enriquecimiento
def get_enrichment_middleware():
    """
    Obtiene el middleware de enriquecimiento
    
    Returns:
        Lista con el middleware de enriquecimiento
    """
    return ENRICHMENT_MIDDLEWARE

# Función para obtener middleware de análisis
def get_analytics_middleware():
    """
    Obtiene el middleware de análisis
    
    Returns:
        Lista con el middleware de análisis
    """
    return ANALYTICS_MIDDLEWARE

# Función para obtener middleware de reportes
def get_reporting_middleware():
    """
    Obtiene el middleware de reportes
    
    Returns:
        Lista con el middleware de reportes
    """
    return REPORTING_MIDDLEWARE

# Función para obtener middleware de búsqueda
def get_search_middleware():
    """
    Obtiene el middleware de búsqueda
    
    Returns:
        Lista con el middleware de búsqueda
    """
    return SEARCH_MIDDLEWARE

# Función para obtener middleware de filtrado
def get_filtering_middleware():
    """
    Obtiene el middleware de filtrado
    
    Returns:
        Lista con el middleware de filtrado
    """
    return FILTERING_MIDDLEWARE

# Función para obtener middleware de paginación
def get_pagination_middleware():
    """
    Obtiene el middleware de paginación
    
    Returns:
        Lista con el middleware de paginación
    """
    return PAGINATION_MIDDLEWARE

# Función para obtener middleware de ordenamiento
def get_sorting_middleware():
    """
    Obtiene el middleware de ordenamiento
    
    Returns:
        Lista con el middleware de ordenamiento
    """
    return SORTING_MIDDLEWARE

# Función para obtener middleware de agrupación
def get_grouping_middleware():
    """
    Obtiene el middleware de agrupación
    
    Returns:
        Lista con el middleware de agrupación
    """
    return GROUPING_MIDDLEWARE

# Función para obtener middleware de agregación
def get_aggregation_middleware():
    """
    Obtiene el middleware de agregación
    
    Returns:
        Lista con el middleware de agregación
    """
    return AGGREGATION_MIDDLEWARE

# Función para obtener middleware de estadísticas
def get_statistics_middleware():
    """
    Obtiene el middleware de estadísticas
    
    Returns:
        Lista con el middleware de estadísticas
    """
    return STATISTICS_MIDDLEWARE

# Función para obtener middleware de alertas
def get_alert_middleware():
    """
    Obtiene el middleware de alertas
    
    Returns:
        Lista con el middleware de alertas
    """
    return ALERT_MIDDLEWARE

# Función para obtener middleware de escalado
def get_escalation_middleware():
    """
    Obtiene el middleware de escalado
    
    Returns:
        Lista con el middleware de escalado
    """
    return ESCALATION_MIDDLEWARE

# Función para obtener middleware de workflow
def get_workflow_middleware():
    """
    Obtiene el middleware de workflow
    
    Returns:
        Lista con el middleware de workflow
    """
    return WORKFLOW_MIDDLEWARE

# Función para obtener middleware de auditoría de cambios
def get_change_audit_middleware():
    """
    Obtiene el middleware de auditoría de cambios
    
    Returns:
        Lista con el middleware de auditoría de cambios
    """
    return CHANGE_AUDIT_MIDDLEWARE

# Función para obtener middleware de sincronización de datos
def get_data_sync_middleware():
    """
    Obtiene el middleware de sincronización de datos
    
    Returns:
        Lista con el middleware de sincronización de datos
    """
    return DATA_SYNC_MIDDLEWARE

# Función para obtener middleware de validación de integridad
def get_integrity_middleware():
    """
    Obtiene el middleware de validación de integridad
    
    Returns:
        Lista con el middleware de validación de integridad
    """
    return INTEGRITY_MIDDLEWARE

# Función para obtener middleware de optimización de consultas
def get_query_optimization_middleware():
    """
    Obtiene el middleware de optimización de consultas
    
    Returns:
        Lista con el middleware de optimización de consultas
    """
    return QUERY_OPTIMIZATION_MIDDLEWARE

# Función para obtener middleware de compresión de respuestas
def get_response_compression_middleware():
    """
    Obtiene el middleware de compresión de respuestas
    
    Returns:
        Lista con el middleware de compresión de respuestas
    """
    return RESPONSE_COMPRESSION_MIDDLEWARE

# Función para obtener middleware de caché inteligente
def get_intelligent_cache_middleware():
    """
    Obtiene el middleware de caché inteligente
    
    Returns:
        Lista con el middleware de caché inteligente
    """
    return INTELLIGENT_CACHE_MIDDLEWARE

# Función para obtener middleware de balanceo de carga
def get_load_balancing_middleware():
    """
    Obtiene el middleware de balanceo de carga
    
    Returns:
        Lista con el middleware de balanceo de carga
    """
    return LOAD_BALANCING_MIDDLEWARE

# Función para obtener middleware de failover
def get_failover_middleware():
    """
    Obtiene el middleware de failover
    
    Returns:
        Lista con el middleware de failover
    """
    return FAILOVER_MIDDLEWARE

# Función para obtener middleware de monitoreo de rendimiento
def get_performance_monitoring_middleware():
    """
    Obtiene el middleware de monitoreo de rendimiento
    
    Returns:
        Lista con el middleware de monitoreo de rendimiento
    """
    return PERFORMANCE_MONITORING_MIDDLEWARE

# Función para obtener middleware de optimización automática
def get_auto_optimization_middleware():
    """
    Obtiene el middleware de optimización automática
    
    Returns:
        Lista con el middleware de optimización automática
    """
    return AUTO_OPTIMIZATION_MIDDLEWARE

# Función para validar configuración de middleware
def validate_middleware_config(middleware_list):
    """
    Valida la configuración de middleware
    
    Args:
        middleware_list: Lista de middleware a validar
        
    Returns:
        Tuple (is_valid, errors)
    """
    errors = []
    
    # Verificar que el middleware de seguridad esté presente
    required_security_middleware = [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ]
    
    for required in required_security_middleware:
        if required not in middleware_list:
            errors.append(f"Middleware de seguridad requerido faltante: {required}")
    
    # Verificar que el middleware de autenticación esté presente
    required_auth_middleware = [
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ]
    
    for required in required_auth_middleware:
        if required not in middleware_list:
            errors.append(f"Middleware de autenticación requerido faltante: {required}")
    
    # Verificar que el middleware de mensajes esté presente
    if 'django.contrib.messages.middleware.MessageMiddleware' not in middleware_list:
        errors.append("Middleware de mensajes requerido faltante")
    
    # Verificar que el middleware común esté presente
    if 'django.middleware.common.CommonMiddleware' not in middleware_list:
        errors.append("Middleware común requerido faltante")
    
    return len(errors) == 0, errors

# Función para crear directorios de middleware
def create_middleware_directories():
    """
    Crea los directorios necesarios para middleware
    """
    directories = [
        BASE_DIR / 'core' / 'middleware',
        BASE_DIR / 'logs' / 'middleware',
        BASE_DIR / 'temp' / 'middleware',
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
    
    return directories
