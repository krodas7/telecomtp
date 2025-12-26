"""
Utilidades para optimización de consultas del Telecom Technology
"""

from django.db.models import Prefetch, Q
from .models import *


class QueryOptimizer:
    """Clase para optimizar consultas comunes del sistema"""
    
    @staticmethod
    def proyectos_con_relaciones():
        """Optimiza consultas de proyectos con todas las relaciones necesarias"""
        return Proyecto.objects.select_related(
            'cliente'
        ).prefetch_related(
            'colaboradores',
            'facturas',
            'gastos',
            'anticipos',
            'archivos',
            'carpetas'
        )
    
    @staticmethod
    def clientes_con_estadisticas():
        """Optimiza consultas de clientes con estadísticas"""
        return Cliente.objects.prefetch_related(
            Prefetch('proyectos', queryset=Proyecto.objects.filter(activo=True)),
            Prefetch('facturas', queryset=Factura.objects.all()),
            'anticipos'
        )
    
    @staticmethod
    def facturas_con_relaciones():
        """Optimiza consultas de facturas con relaciones"""
        return Factura.objects.select_related(
            'cliente',
            'proyecto',
            'creado_por'
        ).prefetch_related(
            'pagos',
            'aplicaciones_anticipo'
        )
    
    @staticmethod
    def gastos_con_relaciones():
        """Optimiza consultas de gastos con relaciones"""
        return Gasto.objects.select_related(
            'proyecto',
            'categoria',
            'aprobado_por'
        )
    
    @staticmethod
    def colaboradores_con_proyectos():
        """Optimiza consultas de colaboradores con proyectos"""
        return Colaborador.objects.prefetch_related(
            'proyectos',
            'anticipos_proyecto'
        )
    
    @staticmethod
    def usuarios_con_perfiles():
        """Optimiza consultas de usuarios con perfiles"""
        return User.objects.select_related(
            'perfilusuario__rol'
        ).prefetch_related(
            'perfilusuario__rol__rolpermiso__permiso__modulo'
        )
    
    @staticmethod
    def notificaciones_con_relaciones():
        """Optimiza consultas de notificaciones con relaciones"""
        return NotificacionSistema.objects.select_related(
            'usuario',
            'proyecto',
            'factura',
            'gasto'
        )


class DashboardQueries:
    """Consultas optimizadas para el dashboard"""
    
    @staticmethod
    def estadisticas_generales():
        """Obtiene estadísticas generales optimizadas"""
        from django.db.models import Sum, Count
        
        return {
            'proyectos': Proyecto.objects.filter(activo=True).aggregate(
                total=Count('id'),
                en_progreso=Count('id', filter=Q(estado='en_progreso')),
                completados=Count('id', filter=Q(estado='completado'))
            ),
            'facturas': Factura.objects.aggregate(
                total=Count('id'),
                pagadas=Count('id', filter=Q(estado='pagada')),
                total_facturado=Sum('monto_total'),
                total_pagado=Sum('monto_pagado')
            ),
            'gastos': Gasto.objects.filter(aprobado=True).aggregate(
                total=Sum('monto'),
                cantidad=Count('id')
            )
        }
    
    @staticmethod
    def proyectos_recientes(limite=5):
        """Obtiene proyectos recientes optimizados"""
        return QueryOptimizer.proyectos_con_relaciones().order_by('-creado_en')[:limite]
    
    @staticmethod
    def gastos_recientes(limite=5):
        """Obtiene gastos recientes optimizados"""
        return QueryOptimizer.gastos_con_relaciones().order_by('-creado_en')[:limite]
    
    @staticmethod
    def facturas_vencidas():
        """Obtiene facturas vencidas optimizadas"""
        from django.utils import timezone
        hoy = timezone.now().date()
        
        return Factura.objects.filter(
            fecha_vencimiento__lt=hoy,
            estado__in=['emitida', 'enviada']
        ).select_related('cliente', 'proyecto').order_by('fecha_vencimiento')
    
    @staticmethod
    def gastos_pendientes_aprobacion():
        """Obtiene gastos pendientes de aprobación optimizados"""
        return QueryOptimizer.gastos_con_relaciones().filter(
            aprobado=False
        ).order_by('-creado_en')


class ReporteQueries:
    """Consultas optimizadas para reportes"""
    
    @staticmethod
    def gastos_por_categoria(fecha_inicio=None, fecha_fin=None, proyecto_id=None):
        """Obtiene gastos agrupados por categoría optimizados"""
        from django.db.models import Sum, Count
        
        queryset = Gasto.objects.filter(aprobado=True).select_related('categoria')
        
        if proyecto_id:
            queryset = queryset.filter(proyecto_id=proyecto_id)
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_gasto__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(fecha_gasto__lte=fecha_fin)
        
        return queryset.values('categoria__nombre', 'categoria__color').annotate(
            total=Sum('monto'),
            cantidad=Count('id')
        ).order_by('-total')
    
    @staticmethod
    def facturas_por_estado():
        """Obtiene facturas agrupadas por estado optimizadas"""
        from django.db.models import Count, Sum
        
        return Factura.objects.values('estado').annotate(
            cantidad=Count('id'),
            monto_total=Sum('monto_total')
        ).order_by('-cantidad')
    
    @staticmethod
    def proyectos_por_estado():
        """Obtiene proyectos agrupados por estado optimizados"""
        from django.db.models import Count, Sum
        
        return Proyecto.objects.filter(activo=True).values('estado').annotate(
            cantidad=Count('id'),
            presupuesto_total=Sum('presupuesto')
        ).order_by('-cantidad')
    
    @staticmethod
    def rentabilidad_por_proyecto():
        """Calcula rentabilidad por proyecto optimizada"""
        from django.db.models import Sum
        
        proyectos = Proyecto.objects.filter(
            activo=True,
            presupuesto__gt=0
        ).select_related('cliente')
        
        resultados = []
        for proyecto in proyectos:
            gastos = Gasto.objects.filter(
                proyecto=proyecto,
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            facturas = Factura.objects.filter(
                proyecto=proyecto,
                estado='pagada'
            ).aggregate(total=Sum('monto_total'))['total'] or 0
            
            if proyecto.presupuesto > 0:
                rentabilidad = ((facturas - gastos) / proyecto.presupuesto) * 100
            else:
                rentabilidad = 0
            
            resultados.append({
                'proyecto': proyecto,
                'presupuesto': proyecto.presupuesto,
                'gastos': gastos,
                'ingresos': facturas,
                'utilidad': facturas - gastos,
                'rentabilidad': round(rentabilidad, 2)
            })
        
        return sorted(resultados, key=lambda x: x['rentabilidad'], reverse=True)


class CacheKeys:
    """Claves para el sistema de caché"""
    
    DASHBOARD_STATS = 'dashboard_stats'
    PROYECTOS_RECIENTES = 'proyectos_recientes'
    GASTOS_RECIENTES = 'gastos_recientes'
    FACTURAS_VENCIDAS = 'facturas_vencidas'
    GASTOS_PENDIENTES = 'gastos_pendientes'
    USUARIOS_ACTIVOS = 'usuarios_activos'
    CATEGORIAS_GASTO = 'categorias_gasto'
    ROLES_PERMISOS = 'roles_permisos'
    
    @staticmethod
    def get_user_key(user_id, key):
        """Genera clave de caché específica para usuario"""
        return f"user_{user_id}_{key}"
    
    @staticmethod
    def get_project_key(project_id, key):
        """Genera clave de caché específica para proyecto"""
        return f"project_{project_id}_{key}"
