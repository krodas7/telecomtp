"""
Configuración específica para la base de datos del sistema de construcción
"""

import os
from pathlib import Path

# Configuración base de directorios
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuración de base de datos SQLite (desarrollo)
DATABASE_SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
            'check_same_thread': False,
        },
        'ATOMIC_REQUIRES': True,
        'CONN_MAX_AGE': 600,
    }
}

# Configuración de base de datos PostgreSQL (producción)
DATABASE_POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'sistema_construccion'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'connect_timeout': 10,
            'application_name': 'sistema_construccion',
            'client_encoding': 'UTF8',
        },
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
        'POOL_OPTIONS': {
            'POOL_SIZE': 20,
            'MAX_OVERFLOW': 30,
            'RECYCLE': 3600,
        }
    }
}

# Configuración de base de datos MySQL (alternativa)
DATABASE_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'sistema_construccion'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 10,
            'autocommit': True,
        },
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
        'POOL_OPTIONS': {
            'POOL_SIZE': 20,
            'MAX_OVERFLOW': 30,
            'RECYCLE': 3600,
        }
    }
}

# Configuración de índices de base de datos
DATABASE_INDEXES = {
    'proyectos': [
        'estado',
        'creado_en',
        'cliente_id',
        'activo',
        'fecha_inicio',
        'fecha_fin',
    ],
    'facturas': [
        'fecha_emision',
        'estado',
        'cliente_id',
        'proyecto_id',
        'monto_total',
        'fecha_vencimiento',
        'monto_pendiente',
    ],
    'gastos': [
        'fecha_gasto',
        'categoria_id',
        'proyecto_id',
        'aprobado',
        'monto',
        'creado_en',
    ],
    'clientes': [
        'activo',
        'creado_en',
        'razon_social',
        'codigo_fiscal',
    ],
    'colaboradores': [
        'activo',
        'fecha_contratacion',
        'fecha_vencimiento_contrato',
        'salario',
    ],
    'archivos_proyecto': [
        'proyecto_id',
        'fecha_subida',
        'tipo_archivo',
        'tamaño',
    ],
    'notificaciones': [
        'usuario_id',
        'fecha_creacion',
        'tipo',
        'leida',
        'prioridad',
    ],
    'anticipos': [
        'cliente_id',
        'proyecto_id',
        'estado',
        'fecha_recepcion',
        'fecha_vencimiento',
        'monto',
    ],
    'presupuestos': [
        'proyecto_id',
        'estado',
        'fecha_creacion',
        'monto_total',
        'aprobado',
    ],
    'inventario': [
        'categoria_id',
        'activo',
        'stock_actual',
        'stock_minimo',
        'precio_unitario',
    ],
}

# Configuración de conexiones de base de datos
DATABASE_CONNECTIONS = {
    'default': {
        'max_connections': 100,
        'min_connections': 5,
        'connection_timeout': 30,
        'command_timeout': 60,
        'idle_timeout': 300,
        'max_lifetime': 3600,
    },
    'read_replica': {
        'max_connections': 50,
        'min_connections': 3,
        'connection_timeout': 30,
        'command_timeout': 60,
        'idle_timeout': 300,
        'max_lifetime': 3600,
    }
}

# Configuración de transacciones
TRANSACTION_CONFIG = {
    'default_timeout': 30,
    'max_retries': 3,
    'retry_delay': 1,
    'isolation_level': 'READ_COMMITTED',
    'auto_commit': False,
}

# Configuración de consultas
QUERY_CONFIG = {
    'max_query_time': 30,
    'max_rows_returned': 10000,
    'enable_query_logging': True,
    'slow_query_threshold': 5.0,
    'enable_query_cache': True,
    'query_cache_timeout': 300,
}

# Configuración de respaldo
BACKUP_CONFIG = {
    'auto_backup': True,
    'backup_frequency': 'daily',
    'backup_time': '02:00',
    'backup_retention_days': 30,
    'backup_compression': True,
    'backup_encryption': False,
    'backup_verification': True,
}

# Configuración de migraciones
MIGRATION_CONFIG = {
    'auto_migrate': False,
    'migration_timeout': 300,
    'rollback_on_failure': True,
    'backup_before_migration': True,
    'test_migration': True,
}

# Configuración de optimización
OPTIMIZATION_CONFIG = {
    'enable_query_optimization': True,
    'enable_index_optimization': True,
    'enable_table_optimization': True,
    'optimization_frequency': 'weekly',
    'vacuum_database': True,
    'analyze_tables': True,
}

# Configuración de monitoreo
MONITORING_CONFIG = {
    'enable_performance_monitoring': True,
    'enable_connection_monitoring': True,
    'enable_query_monitoring': True,
    'monitoring_interval': 60,
    'alert_thresholds': {
        'connection_usage': 80,
        'query_time': 10.0,
        'disk_usage': 85,
    }
}

# Función para obtener configuración de base de datos según el entorno
def get_database_config(environment='development'):
    """
    Obtiene la configuración de base de datos según el entorno
    
    Args:
        environment: Entorno del sistema ('development', 'production', 'testing')
        
    Returns:
        Diccionario con la configuración de base de datos
    """
    database_configs = {
        'development': DATABASE_SQLITE,
        'production': DATABASE_POSTGRESQL,
        'testing': DATABASE_SQLITE,
        'staging': DATABASE_POSTGRESQL,
    }
    
    return database_configs.get(environment, DATABASE_SQLITE)

# Función para obtener configuración de índices
def get_database_indexes():
    """
    Obtiene la configuración de índices de base de datos
    
    Returns:
        Diccionario con la configuración de índices
    """
    return DATABASE_INDEXES

# Función para obtener configuración de conexiones
def get_connection_config():
    """
    Obtiene la configuración de conexiones de base de datos
    
    Returns:
        Diccionario con la configuración de conexiones
    """
    return DATABASE_CONNECTIONS

# Función para obtener configuración de transacciones
def get_transaction_config():
    """
    Obtiene la configuración de transacciones
    
    Returns:
        Diccionario con la configuración de transacciones
    """
    return TRANSACTION_CONFIG

# Función para obtener configuración de consultas
def get_query_config():
    """
    Obtiene la configuración de consultas
    
    Returns:
        Diccionario con la configuración de consultas
    """
    return QUERY_CONFIG

# Función para obtener configuración de respaldo
def get_backup_config():
    """
    Obtiene la configuración de respaldo
    
    Returns:
        Diccionario con la configuración de respaldo
    """
    return BACKUP_CONFIG

# Función para obtener configuración de migraciones
def get_migration_config():
    """
    Obtiene la configuración de migraciones
    
    Returns:
        Diccionario con la configuración de migraciones
    """
    return MIGRATION_CONFIG

# Función para obtener configuración de optimización
def get_optimization_config():
    """
    Obtiene la configuración de optimización
    
    Returns:
        Diccionario con la configuración de optimización
    """
    return OPTIMIZATION_CONFIG

# Función para obtener configuración de monitoreo
def get_monitoring_config():
    """
    Obtiene la configuración de monitoreo
    
    Returns:
        Diccionario con la configuración de monitoreo
    """
    return MONITORING_CONFIG

# Función para validar configuración de base de datos
def validate_database_config(config):
    """
    Valida la configuración de base de datos
    
    Args:
        config: Configuración de base de datos a validar
        
    Returns:
        Tuple (is_valid, errors)
    """
    errors = []
    
    required_fields = ['ENGINE', 'NAME']
    
    for field in required_fields:
        if field not in config:
            errors.append(f"Campo requerido faltante: {field}")
    
    if 'ENGINE' in config:
        valid_engines = [
            'django.db.backends.sqlite3',
            'django.db.backends.postgresql',
            'django.db.backends.mysql',
            'django.db.backends.oracle',
        ]
        if config['ENGINE'] not in valid_engines:
            errors.append(f"Motor de base de datos no válido: {config['ENGINE']}")
    
    return len(errors) == 0, errors

# Función para crear directorios de base de datos
def create_database_directories():
    """
    Crea los directorios necesarios para la base de datos
    """
    directories = [
        BASE_DIR / 'logs',
        BASE_DIR / 'backups',
        BASE_DIR / 'temp',
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
    
    return directories
