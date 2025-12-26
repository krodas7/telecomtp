"""
Utilidades comunes para el Telecom Technology
"""

import logging
from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.core.cache import cache
from django.db import transaction
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from decimal import Decimal
import json

logger = logging.getLogger(__name__)

def handle_exceptions(view_func):
    """
    Decorador para manejar excepciones de manera consistente
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except ValidationError as e:
            messages.error(request, f"Error de validación: {e}")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        except Exception as e:
            logger.error(f"Error en {view_func.__name__}: {e}")
            messages.error(request, "Ocurrió un error inesperado. Por favor, inténtelo de nuevo.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return wrapper

def validate_decimal(value, min_value=None, max_value=None, field_name="Valor"):
    """
    Valida un valor decimal
    """
    try:
        decimal_value = Decimal(str(value))
        if min_value is not None and decimal_value < min_value:
            raise ValidationError(f"{field_name} debe ser mayor o igual a {min_value}")
        if max_value is not None and decimal_value > max_value:
            raise ValidationError(f"{field_name} debe ser menor o igual a {max_value}")
        return decimal_value
    except (ValueError, TypeError):
        raise ValidationError(f"{field_name} debe ser un número válido")

def validate_percentage(value, field_name="Porcentaje"):
    """
    Valida un valor de porcentaje (0-100)
    """
    return validate_decimal(value, 0, 100, field_name)

def validate_positive_decimal(value, field_name="Valor"):
    """
    Valida un valor decimal positivo
    """
    return validate_decimal(value, 0, None, field_name)

def format_currency(amount):
    """
    Formatea un monto como moneda
    """
    if amount is None:
        return "Q0.00"
    return f"Q{amount:,.2f}"

def format_percentage(value):
    """
    Formatea un valor como porcentaje
    """
    if value is None:
        return "0%"
    return f"{value:.1f}%"

def get_cached_data(key, callback, timeout=300):
    """
    Obtiene datos del caché o los genera si no existen
    """
    cached_data = cache.get(key)
    if cached_data is None:
        cached_data = callback()
        cache.set(key, cached_data, timeout)
    return cached_data

def invalidate_cache_pattern(pattern):
    """
    Invalida todas las claves de caché que coincidan con un patrón
    """
    # En desarrollo con cache local, no hay mucho que invalidar
    # En producción con Redis, se implementaría la invalidación real
    logger.info(f"Cache invalidation requested for pattern: {pattern}")

def safe_json_response(data, status=200):
    """
    Crea una respuesta JSON segura
    """
    try:
        return JsonResponse(data, status=status, safe=False)
    except (TypeError, ValueError) as e:
        logger.error(f"Error serializando JSON: {e}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)

def log_activity(user, action, details=None, project=None):
    """
    Registra una actividad del usuario
    """
    try:
        from .models import LogActividad
        LogActividad.objects.create(
            usuario=user,
            accion=action,
            detalles=details or "",
            proyecto=project
        )
    except Exception as e:
        logger.error(f"Error registrando actividad: {e}")

def calculate_percentage(part, total):
    """
    Calcula el porcentaje de una parte del total
    """
    if total == 0:
        return 0
    return (part / total) * 100

def calculate_progress(completed, total):
    """
    Calcula el progreso como porcentaje
    """
    return calculate_percentage(completed, total)

def validate_date_range(start_date, end_date, start_field="Fecha inicio", end_field="Fecha fin"):
    """
    Valida que un rango de fechas sea válido
    """
    if start_date and end_date and start_date > end_date:
        raise ValidationError(f"{start_field} debe ser anterior a {end_field}")

def clean_phone_number(phone):
    """
    Limpia y valida un número de teléfono
    """
    if not phone:
        return ""
    
    # Remover caracteres no numéricos
    cleaned = ''.join(filter(str.isdigit, str(phone)))
    
    # Validar longitud mínima
    if len(cleaned) < 8:
        raise ValidationError("El número de teléfono debe tener al menos 8 dígitos")
    
    return cleaned

def validate_email_domain(email):
    """
    Valida el dominio de un email
    """
    if not email:
        return True
    
    # Lista de dominios permitidos (opcional)
    allowed_domains = [
        'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com',
        'empresa.com', 'construccion.com'  # Dominios corporativos
    ]
    
    domain = email.split('@')[-1].lower()
    if domain not in allowed_domains:
        logger.warning(f"Email con dominio no reconocido: {domain}")
    
    return True

def format_file_size(size_bytes):
    """
    Formatea el tamaño de un archivo en bytes a formato legible
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

def truncate_text(text, max_length=100):
    """
    Trunca un texto a una longitud máxima
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def generate_unique_code(prefix, model_class, field_name='codigo', length=8):
    """
    Genera un código único para un modelo
    """
    import random
    import string
    
    while True:
        # Generar código aleatorio
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        full_code = f"{prefix}-{code}"
        
        # Verificar que no exista
        if not model_class.objects.filter(**{field_name: full_code}).exists():
            return full_code

def get_model_field_choices(model_class, field_name):
    """
    Obtiene las opciones de un campo de elección de un modelo
    """
    try:
        field = model_class._meta.get_field(field_name)
        if hasattr(field, 'choices'):
            return field.choices
        return []
    except Exception as e:
        logger.error(f"Error obteniendo choices de {field_name}: {e}")
        return []

def validate_file_extension(filename, allowed_extensions):
    """
    Valida la extensión de un archivo
    """
    import os
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_extensions:
        raise ValidationError(
            f"Tipo de archivo no permitido. Extensiones permitidas: {', '.join(allowed_extensions)}"
        )
    return True

def validate_file_size(file, max_size_mb):
    """
    Valida el tamaño de un archivo
    """
    max_size_bytes = max_size_mb * 1024 * 1024
    if file.size > max_size_bytes:
        raise ValidationError(
            f"El archivo es demasiado grande. Tamaño máximo: {max_size_mb} MB"
        )
    return True
