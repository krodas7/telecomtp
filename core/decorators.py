"""
Decoradores del Telecom Technology
Para funcionalidades comunes y control de acceso
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
import time


def require_permission(permission_code):
    """
    Decorador para verificar permisos específicos
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'error': 'No autenticado'}, status=401)
                return redirect('login')
            
            # Verificar si el usuario tiene el permiso
            try:
                perfil = request.user.perfilusuario
                if perfil and perfil.tiene_permiso(permission_code):
                    return view_func(request, *args, **kwargs)
                else:
                    if request.headers.get('Content-Type') == 'application/json':
                        return JsonResponse({'error': 'Sin permisos'}, status=403)
                    messages.error(request, 'No tienes permisos para realizar esta acción.')
                    return redirect('dashboard')
            except:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'error': 'Error de permisos'}, status=500)
                messages.error(request, 'Error al verificar permisos.')
                return redirect('dashboard')
        
        return wrapper
    return decorator


def require_ajax(view_func):
    """
    Decorador para requerir peticiones AJAX
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Petición no válida'}, status=400)
        return view_func(request, *args, **kwargs)
    return wrapper


def cache_view(timeout=300, key_prefix=''):
    """
    Decorador para cachear vistas
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Generar clave de caché única
            cache_key = f"{key_prefix}_{request.user.id}_{request.get_full_path()}"
            
            # Intentar obtener del caché
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Ejecutar vista y cachear resultado
            result = view_func(request, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result
        
        return wrapper
    return decorator


def log_activity(activity_name):
    """
    Decorador para registrar actividad del usuario
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Ejecutar la vista
            result = view_func(request, *args, **kwargs)
            
            # Registrar actividad si el usuario está autenticado
            if request.user.is_authenticated:
                try:
                    from .models import LogActividad
                    LogActividad.objects.create(
                        usuario=request.user,
                        accion=activity_name,
                        modulo=view_func.__module__.split('.')[-1],
                        descripcion=f"{activity_name} - {request.path}",
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
                    )
                except:
                    pass  # No fallar si no se puede registrar la actividad
            
            return result
        
        return wrapper
    return decorator


def handle_exceptions(view_func):
    """
    Decorador para manejo de excepciones
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            # Log del error
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error en {view_func.__name__}: {str(e)}")
            
            # Respuesta según el tipo de petición
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False,
                    'error': 'Error interno del servidor'
                }, status=500)
            
            messages.error(request, 'Ocurrió un error inesperado. Por favor intenta de nuevo.')
            return redirect('dashboard')
    
    return wrapper


def rate_limit(max_requests=10, window=60):
    """
    Decorador para limitar la frecuencia de peticiones
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            
            # Crear clave de rate limiting
            rate_key = f"rate_limit_{request.user.id}_{view_func.__name__}"
            
            # Obtener contador actual
            current_requests = cache.get(rate_key, 0)
            
            if current_requests >= max_requests:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({
                        'error': 'Demasiadas peticiones. Intenta más tarde.'
                    }, status=429)
                
                messages.error(request, 'Demasiadas peticiones. Intenta más tarde.')
                return redirect('dashboard')
            
            # Incrementar contador
            cache.set(rate_key, current_requests + 1, window)
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def validate_form(form_class):
    """
    Decorador para validar formularios
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.method == 'POST':
                form = form_class(request.POST, request.FILES)
                if not form.is_valid():
                    if request.headers.get('Content-Type') == 'application/json':
                        return JsonResponse({
                            'success': False,
                            'errors': form.errors
                        }, status=400)
                    
                    messages.error(request, 'Por favor corrige los errores en el formulario.')
                    return render(request, view_func.__name__.replace('_', '/') + '.html', {
                        'form': form
                    })
                
                # Agregar formulario validado al contexto
                request.validated_form = form
            
            return view_func(request, *args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(view_func):
    """
    Decorador para requerir permisos de administrador
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_superuser:
            messages.error(request, 'Solo los administradores pueden acceder a esta sección.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def staff_required(view_func):
    """
    Decorador para requerir permisos de staff
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if not request.user.is_staff:
            messages.error(request, 'Solo el personal autorizado puede acceder a esta sección.')
            return redirect('dashboard')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper


def json_response(view_func):
    """
    Decorador para respuestas JSON automáticas
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            result = view_func(request, *args, **kwargs)
            
            # Si la vista retorna un diccionario, convertirlo a JSON
            if isinstance(result, dict):
                return JsonResponse(result)
            
            return result
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return wrapper


# Decoradores combinados comunes
def api_view(permission_code=None):
    """
    Decorador combinado para APIs
    """
    def decorator(view_func):
        decorators = [require_ajax, handle_exceptions, json_response]
        
        if permission_code:
            decorators.insert(0, require_permission(permission_code))
        
        for decorator_func in decorators:
            view_func = decorator_func(view_func)
        
        return view_func
    return decorator


def secure_view(permission_code=None, log_activity_name=None):
    """
    Decorador combinado para vistas seguras
    """
    def decorator(view_func):
        decorators = [handle_exceptions]
        
        if permission_code:
            decorators.insert(0, require_permission(permission_code))
        
        if log_activity_name:
            decorators.append(log_activity(log_activity_name))
        
        for decorator_func in decorators:
            view_func = decorator_func(view_func)
        
        return view_func
    return decorator
