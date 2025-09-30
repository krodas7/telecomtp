"""
Configuración de caché para el sistema ARCA Construcción
"""

from django.core.cache import cache
from django.conf import settings
from .query_utils import CacheKeys
import json


class CacheManager:
    """Gestor de caché para el sistema"""
    
    @staticmethod
    def get_dashboard_stats(user_id=None):
        """Obtiene estadísticas del dashboard desde caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.DASHBOARD_STATS) if user_id else CacheKeys.DASHBOARD_STATS
        return cache.get(key)
    
    @staticmethod
    def set_dashboard_stats(data, user_id=None, timeout=300):
        """Guarda estadísticas del dashboard en caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.DASHBOARD_STATS) if user_id else CacheKeys.DASHBOARD_STATS
        cache.set(key, data, timeout)
    
    @staticmethod
    def get_proyectos_recientes(user_id=None):
        """Obtiene proyectos recientes desde caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.PROYECTOS_RECIENTES) if user_id else CacheKeys.PROYECTOS_RECIENTES
        return cache.get(key)
    
    @staticmethod
    def set_proyectos_recientes(data, user_id=None, timeout=600):
        """Guarda proyectos recientes en caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.PROYECTOS_RECIENTES) if user_id else CacheKeys.PROYECTOS_RECIENTES
        cache.set(key, data, timeout)
    
    @staticmethod
    def get_gastos_recientes(user_id=None):
        """Obtiene gastos recientes desde caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.GASTOS_RECIENTES) if user_id else CacheKeys.GASTOS_RECIENTES
        return cache.get(key)
    
    @staticmethod
    def set_gastos_recientes(data, user_id=None, timeout=600):
        """Guarda gastos recientes en caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.GASTOS_RECIENTES) if user_id else CacheKeys.GASTOS_RECIENTES
        cache.set(key, data, timeout)
    
    @staticmethod
    def get_facturas_vencidas(user_id=None):
        """Obtiene facturas vencidas desde caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.FACTURAS_VENCIDAS) if user_id else CacheKeys.FACTURAS_VENCIDAS
        return cache.get(key)
    
    @staticmethod
    def set_facturas_vencidas(data, user_id=None, timeout=300):
        """Guarda facturas vencidas en caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.FACTURAS_VENCIDAS) if user_id else CacheKeys.FACTURAS_VENCIDAS
        cache.set(key, data, timeout)
    
    @staticmethod
    def get_gastos_pendientes(user_id=None):
        """Obtiene gastos pendientes desde caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.GASTOS_PENDIENTES) if user_id else CacheKeys.GASTOS_PENDIENTES
        return cache.get(key)
    
    @staticmethod
    def set_gastos_pendientes(data, user_id=None, timeout=300):
        """Guarda gastos pendientes en caché"""
        key = CacheKeys.get_user_key(user_id, CacheKeys.GASTOS_PENDIENTES) if user_id else CacheKeys.GASTOS_PENDIENTES
        cache.set(key, data, timeout)
    
    @staticmethod
    def invalidate_user_cache(user_id):
        """Invalida todo el caché de un usuario"""
        keys_to_invalidate = [
            CacheKeys.get_user_key(user_id, CacheKeys.DASHBOARD_STATS),
            CacheKeys.get_user_key(user_id, CacheKeys.PROYECTOS_RECIENTES),
            CacheKeys.get_user_key(user_id, CacheKeys.GASTOS_RECIENTES),
            CacheKeys.get_user_key(user_id, CacheKeys.FACTURAS_VENCIDAS),
            CacheKeys.get_user_key(user_id, CacheKeys.GASTOS_PENDIENTES),
        ]
        
        for key in keys_to_invalidate:
            cache.delete(key)
    
    @staticmethod
    def invalidate_project_cache(project_id):
        """Invalida el caché relacionado con un proyecto"""
        keys_to_invalidate = [
            CacheKeys.get_project_key(project_id, 'stats'),
            CacheKeys.get_project_key(project_id, 'gastos'),
            CacheKeys.get_project_key(project_id, 'facturas'),
        ]
        
        for key in keys_to_invalidate:
            cache.delete(key)
    
    @staticmethod
    def clear_all_cache():
        """Limpia todo el caché del sistema"""
        cache.clear()
    
    @staticmethod
    def get_cache_info():
        """Obtiene información del caché"""
        try:
            # Esta implementación depende del backend de caché usado
            if hasattr(cache, '_cache'):
                return {
                    'backend': str(type(cache._cache).__name__),
                    'timeout': getattr(cache, 'default_timeout', 'No definido'),
                }
            else:
                return {
                    'backend': 'Desconocido',
                    'timeout': 'No definido',
                }
        except:
            return {
                'backend': 'Error al obtener información',
                'timeout': 'No definido',
            }


class CacheDecorators:
    """Decoradores para caché específicos del sistema"""
    
    @staticmethod
    def cache_dashboard_data(timeout=300):
        """Decorador para cachear datos del dashboard"""
        def decorator(func):
            def wrapper(request, *args, **kwargs):
                user_id = request.user.id if request.user.is_authenticated else None
                cached_data = CacheManager.get_dashboard_stats(user_id)
                
                if cached_data is not None:
                    return cached_data
                
                result = func(request, *args, **kwargs)
                CacheManager.set_dashboard_stats(result, user_id, timeout)
                return result
            
            return wrapper
        return decorator
    
    @staticmethod
    def cache_project_data(timeout=600):
        """Decorador para cachear datos de proyecto"""
        def decorator(func):
            def wrapper(request, project_id, *args, **kwargs):
                cached_data = cache.get(f"project_{project_id}_data")
                
                if cached_data is not None:
                    return cached_data
                
                result = func(request, project_id, *args, **kwargs)
                cache.set(f"project_{project_id}_data", result, timeout)
                return result
            
            return wrapper
        return decorator


class CacheWarmup:
    """Clase para precalentar el caché con datos frecuentemente accedidos"""
    
    @staticmethod
    def warmup_dashboard_data():
        """Precalienta datos del dashboard"""
        try:
            from .services import DashboardService
            
            # Precalentar estadísticas generales
            stats = DashboardService.obtener_estadisticas_generales()
            CacheManager.set_dashboard_stats(stats, timeout=300)
            
            # Precalentar proyectos recientes
            proyectos = DashboardService.obtener_proyectos_recientes(5)
            CacheManager.set_proyectos_recientes(list(proyectos), timeout=600)
            
            # Precalentar gastos recientes
            gastos = DashboardService.obtener_gastos_recientes(5)
            CacheManager.set_gastos_recientes(list(gastos), timeout=600)
            
            return True
        except Exception as e:
            print(f"Error precalentando caché: {e}")
            return False
    
    @staticmethod
    def warmup_user_data(user_id):
        """Precalienta datos específicos de un usuario"""
        try:
            from .services import DashboardService
            
            # Precalentar estadísticas del usuario
            stats = DashboardService.obtener_estadisticas_generales()
            CacheManager.set_dashboard_stats(stats, user_id, 300)
            
            return True
        except Exception as e:
            print(f"Error precalentando datos del usuario {user_id}: {e}")
            return False
