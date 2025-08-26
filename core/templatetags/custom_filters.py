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
