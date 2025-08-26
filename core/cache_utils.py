"""
Utilidades de cache para optimizar consultas pesadas
"""

from django.core.cache import cache
from django.conf import settings
import hashlib
import json
from functools import wraps
from typing import Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)

def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Genera una clave de cache única basada en el prefijo y los argumentos
    
    Args:
        prefix: Prefijo para la clave del cache
        *args: Argumentos posicionales
        **kwargs: Argumentos nombrados
    
    Returns:
        Clave de cache única
    """
    # Crear un hash de los argumentos
    key_data = f"{prefix}:{str(args)}:{str(sorted(kwargs.items()))}"
    key_hash = hashlib.md5(key_data.encode('utf-8')).hexdigest()
    return f"{prefix}_{key_hash}"

def cache_result(timeout: int = 3600, key_prefix: str = "query", cache_alias: str = "default"):
    """
    Decorador para cachear el resultado de una función
    
    Args:
        timeout: Tiempo de vida del cache en segundos
        key_prefix: Prefijo para la clave del cache
        cache_alias: Alias del cache a usar
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar clave única para el cache
            cache_key = generate_cache_key(key_prefix, *args, **kwargs)
            
            # Intentar obtener del cache
            try:
                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache HIT: {cache_key}")
                    return cached_result
            except Exception as e:
                logger.warning(f"Error al obtener del cache: {e}")
            
            # Si no está en cache, ejecutar función
            logger.debug(f"Cache MISS: {cache_key}")
            result = func(*args, **kwargs)
            
            # Guardar en cache
            try:
                cache.set(cache_key, result, timeout)
                logger.debug(f"Cache SET: {cache_key}")
            except Exception as e:
                logger.warning(f"Error al guardar en cache: {e}")
            
            return result
        return wrapper
    return decorator

def cache_model_queryset(model_class, timeout: int = 3600, key_prefix: str = "queryset"):
    """
    Decorador para cachear querysets de modelos
    
    Args:
        model_class: Clase del modelo
        timeout: Tiempo de vida del cache en segundos
        key_prefix: Prefijo para la clave del cache
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generar clave única incluyendo la clase del modelo
            cache_key = generate_cache_key(f"{key_prefix}_{model_class.__name__}", *args, **kwargs)
            
            # Intentar obtener del cache
            try:
                cached_result = cache.get(cache_key)
                if cached_result is not None:
                    logger.debug(f"Cache HIT para {model_class.__name__}: {cache_key}")
                    return cached_result
            except Exception as e:
                logger.warning(f"Error al obtener del cache: {e}")
            
            # Si no está en cache, ejecutar función
            logger.debug(f"Cache MISS para {model_class.__name__}: {cache_key}")
            result = func(*args, **kwargs)
            
            # Guardar en cache
            try:
                cache.set(cache_key, result, timeout)
                logger.debug(f"Cache SET para {model_class.__name__}: {cache_key}")
            except Exception as e:
                logger.warning(f"Error al guardar en cache: {e}")
            
            return result
        return wrapper
    return decorator

def invalidate_cache_pattern(pattern: str, cache_alias: str = "default"):
    """
    Invalida todas las claves de cache que coincidan con un patrón
    
    Args:
        pattern: Patrón para buscar claves a invalidar
        cache_alias: Alias del cache a usar
    """
    try:
        # Nota: Esta funcionalidad requiere Redis
        # En SQLite no se puede hacer esto fácilmente
        logger.info(f"Invalidando cache con patrón: {pattern}")
        # Aquí podrías implementar lógica específica para Redis
    except Exception as e:
        logger.warning(f"Error al invalidar cache: {e}")

def get_or_set_cache(key: str, default_func: Callable, timeout: int = 3600, cache_alias: str = "default") -> Any:
    """
    Obtiene un valor del cache o lo establece si no existe
    
    Args:
        key: Clave del cache
        default_func: Función que se ejecuta si no hay cache
        timeout: Tiempo de vida del cache en segundos
        cache_alias: Alias del cache a usar
    
    Returns:
        Valor del cache o resultado de default_func
    """
    try:
        # Intentar obtener del cache
        cached_value = cache.get(key)
        if cached_value is not None:
            logger.debug(f"Cache HIT: {key}")
            return cached_value
        
        # Si no está en cache, ejecutar función por defecto
        logger.debug(f"Cache MISS: {key}")
        value = default_func()
        
        # Guardar en cache
        cache.set(key, value, timeout)
        logger.debug(f"Cache SET: {key}")
        
        return value
        
    except Exception as e:
        logger.warning(f"Error en get_or_set_cache: {e}")
        # En caso de error, ejecutar función por defecto
        return default_func()

def cache_dashboard_data(user_id: int, timeout: int = 1800):
    """
    Función específica para cachear datos del dashboard
    
    Args:
        user_id: ID del usuario
        timeout: Tiempo de vida del cache en segundos (30 min por defecto)
    
    Returns:
        Clave del cache para el dashboard
    """
    return f"dashboard_data_{user_id}"

def cache_proyecto_data(proyecto_id: int, timeout: int = 3600):
    """
    Función específica para cachear datos de proyectos
    
    Args:
        proyecto_id: ID del proyecto
        timeout: Tiempo de vida del cache en segundos
    
    Returns:
        Clave del cache para el proyecto
    """
    return f"proyecto_data_{proyecto_id}"

def cache_facturas_data(filters: dict, timeout: int = 1800):
    """
    Función específica para cachear datos de facturas
    
    Args:
        filters: Filtros aplicados a las facturas
        timeout: Tiempo de vida del cache en segundos
    
    Returns:
        Clave del cache para las facturas
    """
    # Crear clave basada en los filtros
    filters_str = json.dumps(filters, sort_keys=True)
    return f"facturas_data_{hashlib.md5(filters_str.encode()).hexdigest()}"

def clear_user_cache(user_id: int):
    """
    Limpia todo el cache relacionado con un usuario específico
    
    Args:
        user_id: ID del usuario
    """
    try:
        # Invalidar cache del dashboard
        dashboard_key = cache_dashboard_data(user_id)
        cache.delete(dashboard_key)
        
        # Invalidar cache de proyectos del usuario
        proyecto_pattern = f"proyecto_data_{user_id}_*"
        invalidate_cache_pattern(proyecto_pattern)
        
        logger.info(f"Cache del usuario {user_id} limpiado")
    except Exception as e:
        logger.warning(f"Error al limpiar cache del usuario {user_id}: {e}")

def cache_performance_monitor(func_name: str, execution_time: float, cache_hits: int = 0, cache_misses: int = 0):
    """
    Registra métricas de performance del cache
    
    Args:
        func_name: Nombre de la función
        execution_time: Tiempo de ejecución
        cache_hits: Número de hits del cache
        cache_misses: Número de misses del cache
    """
    try:
        # Guardar métricas en cache para análisis
        metrics_key = f"cache_metrics_{func_name}"
        metrics = {
            'execution_time': execution_time,
            'cache_hits': cache_hits,
            'cache_misses': cache_misses,
            'hit_rate': cache_hits / (cache_hits + cache_misses) if (cache_hits + cache_misses) > 0 else 0,
            'timestamp': cache.get('current_timestamp', 0)
        }
        
        cache.set(metrics_key, metrics, 86400)  # 24 horas
        logger.info(f"Métricas de cache para {func_name}: {metrics}")
        
    except Exception as e:
        logger.warning(f"Error al registrar métricas de cache: {e}")
