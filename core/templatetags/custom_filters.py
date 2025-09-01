from django import template

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
