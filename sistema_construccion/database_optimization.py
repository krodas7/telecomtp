"""
Configuración de optimización de base de datos para el sistema de construcción
"""

# Configuración de conexiones de base de datos optimizadas
DATABASE_OPTIMIZATION = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,  # Timeout de conexión
            'check_same_thread': False,
        },
        'ATOMIC_REQUESTS': True,  # Transacciones automáticas
        'CONN_MAX_AGE': 600,  # Mantener conexiones vivas por 10 minutos
        'OPTIONS': {
            'timeout': 20,
            'check_same_thread': False,
        }
    }
}

# Configuración para PostgreSQL (producción)
DATABASE_POSTGRESQL = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sistema_construccion',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 10,
            'application_name': 'sistema_construccion',
        },
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
        'CONN_HEALTH_CHECKS': True,
    }
}

# Configuración para MySQL (alternativa)
DATABASE_MYSQL = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sistema_construccion',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'connect_timeout': 10,
        },
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,
    }
}

# Configuración de índices de base de datos
DATABASE_INDEXES = {
    'proyectos': [
        'estado',
        'creado_en',
        'cliente_id',
        'activo',
    ],
    'facturas': [
        'fecha_emision',
        'estado',
        'cliente_id',
        'proyecto_id',
        'monto_total',
    ],
    'gastos': [
        'fecha_gasto',
        'categoria_id',
        'proyecto_id',
        'aprobado',
        'monto',
    ],
    'clientes': [
        'activo',
        'creado_en',
        'razon_social',
    ],
    'colaboradores': [
        'activo',
        'proyecto_id',
        'rol',
    ],
    'archivos_proyecto': [
        'proyecto_id',
        'fecha_subida',
        'tipo_archivo',
    ],
    'notificaciones': [
        'usuario_id',
        'fecha_creacion',
        'leida',
        'tipo',
    ],
}

# Configuración de consultas optimizadas
QUERY_OPTIMIZATION = {
    'select_related': {
        'proyecto': ['cliente'],
        'factura': ['cliente', 'proyecto'],
        'gasto': ['categoria', 'proyecto'],
        'archivo': ['proyecto'],
        'colaborador': ['proyecto'],
    },
    'prefetch_related': {
        'proyecto': ['colaboradores', 'archivos', 'gastos'],
        'cliente': ['proyectos', 'facturas'],
        'factura': ['pagos'],
        'gasto': ['documentos'],
    },
    'only_fields': {
        'proyecto_list': ['id', 'nombre', 'estado', 'creado_en', 'cliente__razon_social'],
        'factura_list': ['id', 'numero_factura', 'monto_total', 'estado', 'fecha_emision'],
        'gasto_list': ['id', 'descripcion', 'monto', 'fecha_gasto', 'categoria__nombre'],
        'cliente_list': ['id', 'razon_social', 'email', 'telefono', 'activo'],
    },
    'defer_fields': {
        'proyecto_list': ['descripcion_detallada', 'notas_internas'],
        'factura_list': ['observaciones', 'condiciones_pago'],
        'gasto_list': ['justificacion', 'comentarios'],
        'cliente_list': ['direccion', 'informacion_adicional'],
    }
}

# Configuración de paginación optimizada
PAGINATION_OPTIMIZATION = {
    'default_page_size': 25,
    'max_page_size': 100,
    'page_size_options': [10, 25, 50, 100],
    'cache_pages': True,
    'cache_timeout': 300,
}

# Configuración de búsqueda optimizada
SEARCH_OPTIMIZATION = {
    'min_search_length': 2,
    'max_results': 50,
    'search_fields': {
        'proyecto': ['nombre', 'descripcion', 'cliente__razon_social'],
        'cliente': ['razon_social', 'email', 'telefono'],
        'factura': ['numero_factura', 'cliente__razon_social'],
        'gasto': ['descripcion', 'categoria__nombre'],
        'colaborador': ['nombre', 'email'],
    },
    'full_text_search': {
        'enabled': True,
        'language': 'spanish',
        'rank_threshold': 0.1,
    }
}

# Configuración de agregaciones optimizadas
AGGREGATION_OPTIMIZATION = {
    'batch_size': 1000,
    'use_subquery': True,
    'cache_aggregations': True,
    'cache_timeout': 1800,
    'aggregation_fields': {
        'proyectos': ['estado', 'cliente', 'responsable'],
        'facturas': ['estado', 'cliente', 'proyecto'],
        'gastos': ['categoria', 'proyecto', 'fecha_gasto'],
        'clientes': ['activo', 'fecha_registro'],
    }
}

# Configuración de transacciones optimizadas
TRANSACTION_OPTIMIZATION = {
    'atomic_requests': True,
    'isolation_level': 'READ_COMMITTED',
    'deadlock_retry': True,
    'max_retries': 3,
    'retry_delay': 0.1,
}

# Configuración de conexiones de base de datos
CONNECTION_OPTIMIZATION = {
    'max_connections': 20,
    'min_connections': 5,
    'connection_timeout': 10,
    'idle_timeout': 300,
    'health_check_interval': 60,
    'retry_on_failure': True,
    'connection_pooling': True,
}

# Configuración de logging de base de datos
DATABASE_LOGGING = {
    'enabled': True,
    'log_slow_queries': True,
    'slow_query_threshold': 1.0,  # segundos
    'log_queries': False,  # Solo en desarrollo
    'log_errors': True,
    'log_connections': False,
}

# Configuración de mantenimiento de base de datos
DATABASE_MAINTENANCE = {
    'vacuum_enabled': True,
    'vacuum_interval': 86400,  # 24 horas
    'analyze_enabled': True,
    'analyze_interval': 3600,  # 1 hora
    'reindex_enabled': False,
    'reindex_interval': 604800,  # 7 días
}

# Configuración de respaldo de base de datos
DATABASE_BACKUP = {
    'enabled': True,
    'backup_interval': 86400,  # 24 horas
    'backup_retention': 7,  # días
    'backup_compression': True,
    'backup_encryption': False,
    'backup_location': '/backups/',
}

# Función para obtener configuración de base de datos según el entorno
def get_database_config(environment='development'):
    """
    Obtiene la configuración de base de datos según el entorno
    
    Args:
        environment: Entorno del sistema
        
    Returns:
        Diccionario con la configuración de base de datos
    """
    configs = {
        'development': DATABASE_OPTIMIZATION,
        'production': DATABASE_POSTGRESQL,
        'mysql': DATABASE_MYSQL,
    }
    
    return configs.get(environment, DATABASE_OPTIMIZATION)

# Función para aplicar índices de base de datos
def apply_database_indexes():
    """
    Aplica índices de base de datos para optimización
    """
    from django.db import connection
    
    with connection.cursor() as cursor:
        # Crear índices para proyectos
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_proyectos_estado 
            ON core_proyecto(estado);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_proyectos_creado_en 
            ON core_proyecto(creado_en);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_proyectos_cliente 
            ON core_proyecto(cliente_id);
        """)
        
        # Crear índices para facturas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_facturas_fecha_emision 
            ON core_factura(fecha_emision);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_facturas_estado 
            ON core_factura(estado);
        """)
        
        # Crear índices para gastos
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gastos_fecha_gasto 
            ON core_gasto(fecha_gasto);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_gastos_categoria 
            ON core_gasto(categoria_id);
        """)
        
        # Crear índices para clientes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_clientes_activo 
            ON core_cliente(activo);
        """)
        
        # Crear índices para notificaciones
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notificaciones_usuario_fecha 
            ON core_notificacionsistema(usuario_id, fecha_creacion);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_notificaciones_leida 
            ON core_notificacionsistema(leida);
        """)

# Función para optimizar consultas
def optimize_queryset(queryset, model_name):
    """
    Optimiza un queryset según la configuración
    
    Args:
        queryset: QuerySet a optimizar
        model_name: Nombre del modelo
        
    Returns:
        QuerySet optimizado
    """
    if model_name in QUERY_OPTIMIZATION['select_related']:
        queryset = queryset.select_related(
            *QUERY_OPTIMIZATION['select_related'][model_name]
        )
    
    if model_name in QUERY_OPTIMIZATION['prefetch_related']:
        queryset = queryset.prefetch_related(
            *QUERY_OPTIMIZATION['prefetch_related'][model_name]
        )
    
    if model_name in QUERY_OPTIMIZATION['only_fields']:
        queryset = queryset.only(
            *QUERY_OPTIMIZATION['only_fields'][model_name]
        )
    
    if model_name in QUERY_OPTIMIZATION['defer_fields']:
        queryset = queryset.defer(
            *QUERY_OPTIMIZATION['defer_fields'][model_name]
        )
    
    return queryset

# Función para configurar base de datos
def setup_database_optimization():
    """
    Configura la optimización de base de datos
    """
    try:
        apply_database_indexes()
        print("✅ Índices de base de datos aplicados correctamente")
    except Exception as e:
        print(f"⚠️ Error al aplicar índices: {e}")
    
    print("✅ Configuración de base de datos optimizada")

# Ejecutar configuración al importar
if __name__ == "__main__":
    setup_database_optimization()
