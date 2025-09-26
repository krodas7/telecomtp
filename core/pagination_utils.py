
"""
Utilidades de paginación para listas largas
"""

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.template.loader import render_to_string
from typing import Any, Dict, List, Optional
import math

class CustomPaginator:
    """
    Paginador personalizado con funcionalidades avanzadas
    """
    
    def __init__(self, object_list, per_page=25, orphans=0, allow_empty_first_page=True):
        self.paginator = Paginator(object_list, per_page, orphans, allow_empty_first_page)
        self.per_page = per_page
        self.count = self.paginator.count
        self.num_pages = self.paginator.num_pages
    
    def get_page(self, page_number):
        """Obtiene una página específica"""
        try:
            return self.paginator.page(page_number)
        except PageNotAnInteger:
            return self.paginator.page(1)
        except EmptyPage:
            return self.paginator.page(self.paginator.num_pages)
    
    def get_page_info(self, page_number):
        """Obtiene información detallada de la página"""
        page = self.get_page(page_number)
        
        return {
            'page_number': page.number,
            'has_previous': page.has_previous(),
            'has_next': page.has_next(),
            'previous_page_number': page.previous_page_number() if page.has_previous() else None,
            'next_page_number': page.next_page_number() if page.has_next() else None,
            'start_index': page.start_index(),
            'end_index': page.end_index(),
            'total_count': self.count,
            'total_pages': self.num_pages,
            'per_page': self.per_page,
            'object_list': list(page.object_list),
        }
    
    def get_pagination_range(self, page_number, delta=2):
        """
        Obtiene el rango de páginas a mostrar en la navegación
        
        Args:
            page_number: Número de página actual
            delta: Número de páginas a mostrar antes y después de la actual
        """
        page_number = int(page_number)
        delta = int(delta)
        
        start = max(1, page_number - delta)
        end = min(self.num_pages, page_number + delta + 1)
        
        # Asegurar que siempre se muestren al menos 5 páginas si es posible
        if end - start < 5 and self.num_pages >= 5:
            if start == 1:
                end = min(5, self.num_pages)
            elif end == self.num_pages:
                start = max(1, self.num_pages - 4)
        
        return range(start, end + 1)

def paginate_queryset(queryset, page, per_page=25, orphans=0):
    """
    Función de conveniencia para paginar un queryset
    
    Args:
        queryset: QuerySet a paginar
        page: Número de página solicitada
        per_page: Elementos por página
        orphans: Elementos huérfanos permitidos
    
    Returns:
        Tupla (page_obj, paginator)
    """
    paginator = CustomPaginator(queryset, per_page, orphans)
    page_obj = paginator.get_page(page)
    return page_obj, paginator

def get_pagination_context(page_obj, paginator, request=None):
    """
    Genera el contexto completo para la paginación en templates
    
    Args:
        page_obj: Objeto de página actual
        paginator: Instancia del paginador
        request: Request HTTP (opcional)
    
    Returns:
        Diccionario con contexto de paginación
    """
    page_number = page_obj.number
    
    # Obtener parámetros de la URL para mantener filtros
    url_params = {}
    if request:
        for key, value in request.GET.items():
            if key != 'page':  # Excluir el parámetro de página
                url_params[key] = value
    
    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': paginator.num_pages > 1,
        'page_range': paginator.get_pagination_range(page_number),
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'start_index': page_obj.start_index(),
        'end_index': page_obj.end_index(),
        'total_count': paginator.count,
        'total_pages': paginator.num_pages,
        'per_page': paginator.per_page,
        'current_page': page_number,
        'url_params': url_params,
        'page_info': paginator.get_page_info(page_number),
    }
    
    return context

def paginate_with_filters(queryset, request, per_page=25, filters=None):
    """
    Pagina un queryset aplicando filtros y manteniendo la paginación
    
    Args:
        queryset: QuerySet base
        request: Request HTTP
        per_page: Elementos por página
        filters: Diccionario de filtros a aplicar
    
    Returns:
        Tupla (page_obj, paginator, filtered_queryset)
    """
    # Aplicar filtros si se proporcionan
    if filters:
        for field, value in filters.items():
            if value and hasattr(queryset.model, field):
                if isinstance(value, str) and value.strip():
                    queryset = queryset.filter(**{f"{field}__icontains": value.strip()})
                elif value is not None:
                    queryset = queryset.filter(**{field: value})
    
    # Obtener página de la request
    page = request.GET.get('page', 1)
    
    # Paginar
    page_obj, paginator = paginate_queryset(queryset, page, per_page)
    
    return page_obj, paginator, queryset

def render_pagination_ajax(page_obj, paginator, template_name='core/includes/pagination.html'):
    """
    Renderiza la paginación para respuestas AJAX
    
    Args:
        page_obj: Objeto de página actual
        paginator: Instancia del paginador
        template_name: Template a usar para renderizar
    
    Returns:
        HTML renderizado de la paginación
    """
    context = get_pagination_context(page_obj, paginator)
    return render_to_string(template_name, context)

def pagination_response(page_obj, paginator, data_key='objects'):
    """
    Genera una respuesta JSON con datos paginados
    
    Args:
        page_obj: Objeto de página actual
        paginator: Instancia del paginador
        data_key: Clave para los datos en la respuesta
    
    Returns:
        JsonResponse con datos paginados
    """
    page_info = paginator.get_page_info(page_obj.number)
    
    response_data = {
        'success': True,
        'pagination': {
            'current_page': page_info['page_number'],
            'total_pages': page_info['total_pages'],
            'total_count': page_info['total_count'],
            'per_page': page_info['per_page'],
            'has_previous': page_info['has_previous'],
            'has_next': page_info['has_next'],
            'previous_page': page_info['previous_page_number'],
            'next_page': page_info['next_page_number'],
            'start_index': page_info['start_index'],
            'end_index': page_info['end_index'],
        },
        data_key: page_info['object_list'],
    }
    
    return JsonResponse(response_data)

def get_page_size_options():
    """
    Retorna opciones de tamaño de página para el usuario
    
    Returns:
        Lista de opciones de tamaño de página
    """
    return [
        {'value': 10, 'label': '10 por página'},
        {'value': 25, 'label': '25 por página'},
        {'value': 50, 'label': '50 por página'},
        {'value': 100, 'label': '100 por página'},
    ]

def calculate_optimal_page_size(total_count, target_pages=10):
    """
    Calcula el tamaño de página óptimo basado en el total de elementos
    
    Args:
        total_count: Total de elementos
        target_pages: Número objetivo de páginas
    
    Returns:
        Tamaño de página óptimo
    """
    if total_count <= 0:
        return 25
    
    optimal_size = math.ceil(total_count / target_pages)
    
    # Redondear a opciones estándar
    standard_sizes = [10, 25, 50, 100]
    for size in standard_sizes:
        if optimal_size <= size:
            return size
    
    return 100

class PaginationMixin:
    """
    Mixin para vistas que requieren paginación
    """
    
    paginate_by = 25
    paginate_orphans = 0
    page_kwarg = 'page'
    
    def get_paginate_by(self, queryset):
        """Obtiene el número de elementos por página"""
        return self.paginate_by
    
    def get_paginate_orphans(self):
        """Obtiene el número de elementos huérfanos permitidos"""
        return self.paginate_orphans
    
    def paginate_queryset(self, queryset, page_size):
        """Pagina el queryset"""
        paginator = CustomPaginator(
            queryset, 
            page_size, 
            self.get_paginate_orphans(),
            allow_empty_first_page=True
        )
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except (TypeError, ValueError):
            page_number = 1
        
        page_obj = paginator.get_page(page_number)
        return page_obj, paginator
    
    def get_pagination_context(self, page_obj, paginator):
        """Obtiene el contexto de paginación"""
        return get_pagination_context(page_obj, paginator, self.request)
