"""
Configuración de cache para optimizar el rendimiento del sistema
"""

# Configuración de cache para desarrollo
CACHE_DEVELOPMENT = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutos
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# Configuración de cache para producción (usando Redis)
CACHE_PRODUCTION = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 50,
                'retry_on_timeout': True,
            },
            'SERIALIZER': 'django_redis.serializers.json.JSONSerializer',
            'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
        },
        'TIMEOUT': 3600,  # 1 hora
        'KEY_PREFIX': 'sistema_construccion',
        'VERSION': 1,
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 86400,  # 24 horas
        'KEY_PREFIX': 'session',
    },
    'long_term': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/3',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 86400 * 7,  # 7 días
        'KEY_PREFIX': 'long_term',
    }
}

# Configuración de cache para testing
CACHE_TESTING = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Configuración de cache híbrida (memoria local + archivos)
CACHE_HYBRID = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 2000,
            'CULL_FREQUENCY': 3,
        }
    },
    'file': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
        'TIMEOUT': 3600,
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
        }
    }
}

# Configuración de cache para diferentes entornos
def get_cache_config(environment='development'):
    """
    Obtiene la configuración de cache según el entorno
    
    Args:
        environment: Entorno del sistema ('development', 'production', 'testing', 'hybrid')
        
    Returns:
        Diccionario con la configuración de cache
    """
    cache_configs = {
        'development': CACHE_DEVELOPMENT,
        'production': CACHE_PRODUCTION,
        'testing': CACHE_TESTING,
        'hybrid': CACHE_HYBRID
    }
    
    return cache_configs.get(environment, CACHE_DEVELOPMENT)

# Configuración de cache por módulo
CACHE_MODULES = {
    'dashboard': {
        'timeout': 300,  # 5 minutos
        'key_prefix': 'dashboard',
        'version': 1,
    },
    'proyectos': {
        'timeout': 600,  # 10 minutos
        'key_prefix': 'proyectos',
        'version': 1,
    },
    'clientes': {
        'timeout': 1800,  # 30 minutos
        'key_prefix': 'clientes',
        'version': 1,
    },
    'facturas': {
        'timeout': 300,  # 5 minutos
        'key_prefix': 'facturas',
        'version': 1,
    },
    'gastos': {
        'timeout': 300,  # 5 minutos
        'key_prefix': 'gastos',
        'version': 1,
    },
    'reportes': {
        'timeout': 3600,  # 1 hora
        'key_prefix': 'reportes',
        'version': 1,
    }
}

# Configuración de invalidación de cache
CACHE_INVALIDATION_PATTERNS = {
    'proyecto_updated': ['proyectos:*', 'dashboard:*'],
    'cliente_updated': ['clientes:*', 'proyectos:*'],
    'factura_updated': ['facturas:*', 'dashboard:*'],
    'gasto_updated': ['gastos:*', 'dashboard:*'],
    'user_updated': ['dashboard:*'],
}

# Configuración de compresión de cache
CACHE_COMPRESSION = {
    'enabled': True,
    'algorithm': 'gzip',
    'min_size': 1024,  # Comprimir solo archivos mayores a 1KB
    'compression_level': 6,  # Nivel de compresión (1-9)
}

# Configuración de cache de sesiones
SESSION_CACHE_CONFIG = {
    'timeout': 86400,  # 24 horas
    'key_prefix': 'session',
    'serializer': 'json',
    'compress': True,
}

# Configuración de cache de consultas
QUERY_CACHE_CONFIG = {
    'enabled': True,
    'timeout': 300,  # 5 minutos
    'max_queries': 1000,
    'key_prefix': 'query',
}

# Configuración de cache de archivos estáticos
STATIC_CACHE_CONFIG = {
    'enabled': True,
    'timeout': 86400 * 30,  # 30 días
    'key_prefix': 'static',
    'compress': True,
}

# Función para generar claves de cache
def generate_cache_key(module, identifier, user_id=None):
    """
    Genera una clave de cache consistente
    
    Args:
        module: Módulo del sistema
        identifier: Identificador único
        user_id: ID del usuario (opcional)
        
    Returns:
        Clave de cache generada
    """
    if user_id:
        return f"{module}:{identifier}:{user_id}"
    return f"{module}:{identifier}"

# Función para invalidar cache por patrón
def invalidate_cache_by_pattern(pattern):
    """
    Invalida todas las claves de cache que coincidan con un patrón
    
    Args:
        pattern: Patrón para buscar claves a invalidar
    """
    # En desarrollo, usar el cache local
    from django.core.cache import cache
    
    # Obtener todas las claves del cache (solo funciona con Redis)
    if hasattr(cache, 'keys'):
        keys = cache.keys(pattern)
        for key in keys:
            cache.delete(key)
    
    # Log de la invalidación
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Cache invalidation requested for pattern: {pattern}")

# Función para limpiar cache expirado
def cleanup_expired_cache():
    """
    Limpia el cache expirado
    """
    from django.core.cache import cache
    
    # En desarrollo, no hay mucho que limpiar
    # En producción con Redis, se puede implementar limpieza automática
    import logging
    logger = logging.getLogger(__name__)
    logger.info("Cache cleanup requested")

# Configuración de cache para diferentes tipos de datos
CACHE_DATA_TYPES = {
    'list': {
        'timeout': 300,
        'compress': True,
        'serializer': 'json',
    },
    'detail': {
        'timeout': 600,
        'compress': False,
        'serializer': 'json',
    },
    'aggregate': {
        'timeout': 1800,
        'compress': True,
        'serializer': 'pickle',
    },
    'search': {
        'timeout': 300,
        'compress': True,
        'serializer': 'json',
    }
}

# Función para obtener configuración de cache por tipo de dato
def get_cache_config_for_data_type(data_type):
    """
    Obtiene la configuración de cache para un tipo de dato específico
    
    Args:
        data_type: Tipo de dato ('list', 'detail', 'aggregate', 'search')
        
    Returns:
        Diccionario con la configuración de cache
    """
    return CACHE_DATA_TYPES.get(data_type, CACHE_DATA_TYPES['list'])

# Configuración de cache para diferentes usuarios
def get_user_cache_config(user):
    """
    Obtiene configuración de cache específica para un usuario
    
    Args:
        user: Usuario del sistema
        
    Returns:
        Diccionario con la configuración de cache del usuario
    """
    if user.is_superuser:
        return {
            'timeout': 1800,  # 30 minutos para superusuarios
            'key_prefix': f'admin_{user.id}',
        }
    elif user.is_staff:
        return {
            'timeout': 900,  # 15 minutos para staff
            'key_prefix': f'staff_{user.id}',
        }
    else:
        return {
            'timeout': 300,  # 5 minutos para usuarios normales
            'key_prefix': f'user_{user.id}',
        }
