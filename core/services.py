"""
Servicios del Telecom Technology
Contiene la lógica de negocio separada de las vistas
"""

from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
from .models import *
from .query_utils import QueryOptimizer, DashboardQueries, ReporteQueries


class ProyectoService:
    """Servicio para operaciones relacionadas con proyectos"""
    
    @staticmethod
    def calcular_rentabilidad(proyecto):
        """Calcula la rentabilidad de un proyecto"""
        try:
            # Obtener gastos aprobados del proyecto
            gastos_totales = Gasto.objects.filter(
                proyecto=proyecto,
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            # Obtener facturas pagadas
            facturas_pagadas = Factura.objects.filter(
                proyecto=proyecto,
                estado='pagada'
            ).aggregate(total=Sum('monto_total'))['total'] or 0
            
            # Calcular rentabilidad
            presupuesto = proyecto.presupuesto or 0
            ingresos = facturas_pagadas
            gastos = gastos_totales
            
            if presupuesto > 0:
                rentabilidad_porcentaje = ((ingresos - gastos) / presupuesto) * 100
            else:
                rentabilidad_porcentaje = 0
            
            return {
                'presupuesto': presupuesto,
                'ingresos': ingresos,
                'gastos': gastos,
                'utilidad': ingresos - gastos,
                'rentabilidad_porcentaje': round(rentabilidad_porcentaje, 2)
            }
        except Exception as e:
            return {
                'presupuesto': 0,
                'ingresos': 0,
                'gastos': 0,
                'utilidad': 0,
                'rentabilidad_porcentaje': 0,
                'error': str(e)
            }
    
    @staticmethod
    def obtener_estadisticas_proyecto(proyecto):
        """Obtiene estadísticas detalladas de un proyecto"""
        try:
            # Estadísticas básicas
            total_gastos = Gasto.objects.filter(proyecto=proyecto).aggregate(
                total=Sum('monto')
            )['total'] or 0
            
            gastos_aprobados = Gasto.objects.filter(
                proyecto=proyecto,
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            gastos_pendientes = Gasto.objects.filter(
                proyecto=proyecto,
                aprobado=False
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            # Estadísticas de facturas
            total_facturas = Factura.objects.filter(proyecto=proyecto).count()
            facturas_pagadas = Factura.objects.filter(
                proyecto=proyecto,
                estado='pagada'
            ).count()
            
            monto_facturado = Factura.objects.filter(proyecto=proyecto).aggregate(
                total=Sum('monto_total')
            )['total'] or 0
            
            monto_pagado = Factura.objects.filter(proyecto=proyecto).aggregate(
                total=Sum('monto_pagado')
            )['total'] or 0
            
            # Estadísticas de colaboradores
            total_colaboradores = proyecto.colaboradores.count()
            
            return {
                'gastos': {
                    'total': total_gastos,
                    'aprobados': gastos_aprobados,
                    'pendientes': gastos_pendientes,
                    'por_aprobar': gastos_pendientes
                },
                'facturas': {
                    'total': total_facturas,
                    'pagadas': facturas_pagadas,
                    'pendientes': total_facturas - facturas_pagadas,
                    'monto_facturado': monto_facturado,
                    'monto_pagado': monto_pagado,
                    'monto_pendiente': monto_facturado - monto_pagado
                },
                'colaboradores': {
                    'total': total_colaboradores
                }
            }
        except Exception as e:
            return {'error': str(e)}


class FacturaService:
    """Servicio para operaciones relacionadas con facturas"""
    
    @staticmethod
    def generar_numero_factura():
        """Genera un número de factura único"""
        try:
            # Obtener el último número de factura
            ultima_factura = Factura.objects.order_by('-id').first()
            if ultima_factura and ultima_factura.numero_factura:
                # Extraer el número y incrementar
                try:
                    numero = int(ultima_factura.numero_factura.split('-')[-1])
                    nuevo_numero = numero + 1
                except (ValueError, IndexError):
                    nuevo_numero = 1
            else:
                nuevo_numero = 1
            
            # Formatear como F001-2025
            return f"F{nuevo_numero:03d}-{timezone.now().year}"
        except Exception:
            return f"F001-{timezone.now().year}"
    
    @staticmethod
    def calcular_montos_factura(monto_subtotal, porcentaje_iva=12):
        """Calcula los montos de una factura"""
        monto_iva = monto_subtotal * (porcentaje_iva / 100)
        monto_total = monto_subtotal + monto_iva
        
        return {
            'monto_subtotal': monto_subtotal,
            'monto_iva': monto_iva,
            'monto_total': monto_total,
            'porcentaje_iva': porcentaje_iva
        }
    
    @staticmethod
    def obtener_facturas_vencidas():
        """Obtiene facturas vencidas"""
        hoy = timezone.now().date()
        return Factura.objects.filter(
            fecha_vencimiento__lt=hoy,
            estado__in=['emitida', 'enviada']
        ).order_by('fecha_vencimiento')


class GastoService:
    """Servicio para operaciones relacionadas con gastos"""
    
    @staticmethod
    def obtener_gastos_por_categoria(proyecto_id=None, fecha_inicio=None, fecha_fin=None):
        """Obtiene gastos agrupados por categoría"""
        queryset = Gasto.objects.filter(aprobado=True)
        
        if proyecto_id:
            queryset = queryset.filter(proyecto_id=proyecto_id)
        
        if fecha_inicio:
            queryset = queryset.filter(fecha_gasto__gte=fecha_inicio)
        
        if fecha_fin:
            queryset = queryset.filter(fecha_gasto__lte=fecha_fin)
        
        return queryset.values('categoria__nombre').annotate(
            total=Sum('monto'),
            cantidad=Count('id')
        ).order_by('-total')
    
    @staticmethod
    def obtener_gastos_pendientes_aprobacion():
        """Obtiene gastos pendientes de aprobación"""
        return Gasto.objects.filter(aprobado=False).order_by('-creado_en')


class DashboardService:
    """Servicio para datos del dashboard"""
    
    @staticmethod
    def obtener_estadisticas_generales():
        """Obtiene estadísticas generales para el dashboard"""
        try:
            # Usar consultas optimizadas
            stats = DashboardQueries.estadisticas_generales()
            
            # Facturas vencidas
            facturas_vencidas = DashboardQueries.facturas_vencidas().count()
            
            # Gastos pendientes
            gastos_pendientes = DashboardQueries.gastos_pendientes_aprobacion().count()
            
            return {
                'proyectos': {
                    'total': stats['proyectos']['total'],
                    'en_progreso': stats['proyectos']['en_progreso'],
                    'completados': stats['proyectos']['completados'],
                    'pendientes': stats['proyectos']['total'] - stats['proyectos']['en_progreso'] - stats['proyectos']['completados']
                },
                'financiero': {
                    'total_facturado': stats['facturas']['total_facturado'] or 0,
                    'total_pagado': stats['facturas']['total_pagado'] or 0,
                    'total_gastos': stats['gastos']['total'] or 0,
                    'utilidad': (stats['facturas']['total_pagado'] or 0) - (stats['gastos']['total'] or 0)
                },
                'alertas': {
                    'facturas_vencidas': facturas_vencidas,
                    'gastos_pendientes': gastos_pendientes
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def obtener_proyectos_recientes(limite=5):
        """Obtiene los proyectos más recientes"""
        return Proyecto.objects.filter(activo=True).order_by('-creado_en')[:limite]
    
    @staticmethod
    def obtener_gastos_recientes(limite=5):
        """Obtiene los gastos más recientes"""
        return Gasto.objects.filter(aprobado=True).order_by('-creado_en')[:limite]


class NotificacionService:
    """Servicio para manejo de notificaciones"""
    
    @staticmethod
    def crear_notificacion(usuario, tipo, titulo, mensaje, **kwargs):
        """Crea una nueva notificación"""
        return NotificacionSistema.objects.create(
            usuario=usuario,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            **kwargs
        )
    
    @staticmethod
    def verificar_facturas_vencidas():
        """Verifica y crea notificaciones para facturas vencidas"""
        facturas_vencidas = FacturaService.obtener_facturas_vencidas()
        
        for factura in facturas_vencidas:
            # Crear notificación para el usuario que creó la factura
            if factura.creado_por:
                NotificacionService.crear_notificacion(
                    usuario=factura.creado_por,
                    tipo='factura_vencida',
                    titulo=f'Factura vencida: {factura.numero_factura}',
                    mensaje=f'La factura {factura.numero_factura} está vencida desde {factura.fecha_vencimiento}',
                    factura=factura,
                    prioridad='alta'
                )
    
    @staticmethod
    def verificar_gastos_pendientes():
        """Verifica y crea notificaciones para gastos pendientes"""
        gastos_pendientes = GastoService.obtener_gastos_pendientes_aprobacion()
        
        # Obtener usuarios con permisos de aprobación
        usuarios_aprobacion = User.objects.filter(
            perfilusuario__rol__rolpermiso__permiso__codigo='gastos_editar',
            perfilusuario__rol__rolpermiso__activo=True
        ).distinct()
        
        for gasto in gastos_pendientes:
            for usuario in usuarios_aprobacion:
                NotificacionService.crear_notificacion(
                    usuario=usuario,
                    tipo='gasto_aprobacion',
                    titulo=f'Gasto pendiente de aprobación',
                    mensaje=f'Gasto por Q{gasto.monto:,.2f} requiere aprobación',
                    gasto=gasto,
                    prioridad='media'
                )


class ArchivoService:
    """Servicio para manejo de archivos"""
    
    @staticmethod
    def obtener_archivos_por_proyecto(proyecto_id):
        """Obtiene archivos organizados por carpetas para un proyecto"""
        proyecto = Proyecto.objects.get(id=proyecto_id)
        
        # Obtener carpetas raíz
        carpetas_raiz = CarpetaProyecto.objects.filter(
            proyecto=proyecto,
            carpeta_padre__isnull=True,
            activa=True
        ).order_by('nombre')
        
        # Obtener archivos sin carpeta
        archivos_sin_carpeta = ArchivoProyecto.objects.filter(
            proyecto=proyecto,
            carpeta__isnull=True,
            activo=True
        ).order_by('-fecha_subida')
        
        return {
            'carpetas': carpetas_raiz,
            'archivos_sin_carpeta': archivos_sin_carpeta
        }
    
    @staticmethod
    def crear_carpeta(proyecto, nombre, carpeta_padre=None, creado_por=None):
        """Crea una nueva carpeta en un proyecto"""
        return CarpetaProyecto.objects.create(
            proyecto=proyecto,
            carpeta_padre=carpeta_padre,
            nombre=nombre,
            creada_por=creado_por
        )