from django import template
from decimal import Decimal
import locale

register = template.Library()

@register.filter
def permiso_color(tipo):
    """Retorna el color CSS para el tipo de permiso"""
    colores = {
        'ver': 'primary',
        'crear': 'success',
        'editar': 'warning',
        'eliminar': 'danger',
        'exportar': 'info',
        'importar': 'secondary',
        'reset': 'dark'
    }
    return colores.get(tipo, 'secondary')

@register.filter
def get_item(dictionary, key):
    """Obtiene un item de un diccionario por clave"""
    return dictionary.get(key)

@register.filter
def is_list(value):
    """Verifica si un valor es una lista"""
    return isinstance(value, list)

@register.filter
def divide(value, arg):
    """Divide value por arg"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiplica value por arg"""
    try:
        return float(value) * float(arg)
    except (ValueError):
        return 0

@register.filter
def percentage(value, total):
    """Calcula el porcentaje de value sobre total"""
    try:
        if float(total) == 0:
            return 0
        return round((float(value) / float(total)) * 100, 1)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def currency_format(value):
    """Formatea un valor como moneda con separador de miles"""
    try:
        if value is None:
            return "0.00"
        
        # Convertir a float si es Decimal
        if isinstance(value, Decimal):
            value = float(value)
        
        # Formatear con separador de miles y 2 decimales
        return f"{value:,.2f}"
    except (ValueError, TypeError):
        return "0.00"

@register.filter
def currency_gtq(value):
    """Formatea un valor como moneda (USD)"""
    try:
        if value is None:
            return "$0.00"
        
        # Convertir a float si es Decimal
        if isinstance(value, Decimal):
            value = float(value)
        
        # Formatear con separador de miles y 2 decimales
        return f"${value:,.2f}"
    except (ValueError, TypeError):
        return "$0.00"

@register.filter
def js_float(value):
    """Convierte un valor Decimal a float para JavaScript"""
    try:
        if value is None:
            return 0.0
        
        # Convertir a float si es Decimal
        if isinstance(value, Decimal):
            return float(value)
        
        return float(value)
    except (ValueError, TypeError):
        return 0.0

@register.filter
def add_class(field, css_class):
    """Agrega una clase CSS a un campo de formulario"""
    if hasattr(field, 'field') and hasattr(field.field, 'widget'):
        field.field.widget.attrs['class'] = field.field.widget.attrs.get('class', '') + ' ' + css_class
    return field

@register.filter
def basename(path):
    """Obtiene el nombre del archivo de una ruta"""
    import os
    if path:
        return os.path.basename(path)
    return ''
