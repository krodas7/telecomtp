"""
Servicios para el sistema de construcción
"""
import os
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from .models import (
    NotificacionSistema, ConfiguracionNotificaciones, 
    HistorialNotificaciones, Factura, Gasto, Proyecto, Presupuesto
)
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class NotificacionService:
    """Servicio para manejar notificaciones del sistema"""
    
    @staticmethod
    def crear_notificacion(usuario, tipo, titulo, mensaje, prioridad='media', 
                          proyecto=None, factura=None, gasto=None):
        """Crea una nueva notificación"""
        try:
            # Verificar si el usuario quiere recibir este tipo de notificación
            config = ConfiguracionNotificaciones.objects.get_or_create(usuario=usuario)[0]
            
            if not getattr(config, f"{tipo.split('_')[0]}s", True):
                return None
            
            # Crear la notificación
            notificacion = NotificacionSistema.objects.create(
                usuario=usuario,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                prioridad=prioridad,
                proyecto=proyecto,
                factura=factura,
                gasto=gasto
            )
            
            # Registrar en el historial
            HistorialNotificaciones.objects.create(
                usuario=usuario,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                metodo_envio='sistema',
                estado='enviada'
            )
            
            return notificacion
            
        except Exception as e:
            print(f"Error creando notificación: {e}")
            return None
    
    @staticmethod
    def notificar_factura_vencida(factura):
        """Notifica sobre facturas vencidas"""
        if factura.estado == 'vencida':
            usuarios = User.objects.filter(is_active=True)
            for usuario in usuarios:
                NotificacionService.crear_notificacion(
                    usuario=usuario,
                    tipo='factura_vencida',
                    titulo=f'Factura Vencida: {factura.numero_factura}',
                    mensaje=f'La factura {factura.numero_factura} del proyecto {factura.proyecto.nombre} está vencida desde {factura.fecha_vencimiento.strftime("%d/%m/%Y")}',
                    prioridad='alta',
                    factura=factura,
                    proyecto=factura.proyecto
                )
    
    @staticmethod
    def notificar_pago_pendiente(factura):
        """Notifica sobre pagos pendientes"""
        if factura.monto_pendiente > 0:
            usuarios = User.objects.filter(is_active=True)
            for usuario in usuarios:
                NotificacionService.crear_notificacion(
                    usuario=usuario,
                    tipo='pago_pendiente',
                    titulo=f'Pago Pendiente: {factura.numero_factura}',
                    mensaje=f'La factura {factura.numero_factura} tiene un pago pendiente de Q{factura.monto_pendiente}',
                    prioridad='media',
                    factura=factura,
                    proyecto=factura.proyecto
                )
    
    @staticmethod
    def notificar_gasto_aprobacion(gasto):
        """Notifica sobre gastos que requieren aprobación"""
        if not gasto.aprobado:
            usuarios = User.objects.filter(is_active=True, is_superuser=True)
            for usuario in usuarios:
                NotificacionService.crear_notificacion(
                    usuario=usuario,
                    tipo='gasto_aprobacion',
                    titulo=f'Gasto Requiere Aprobación: {gasto.descripcion}',
                    mensaje=f'El gasto "{gasto.descripcion}" por Q{gasto.monto} requiere aprobación',
                    prioridad='media',
                    gasto=gasto,
                    proyecto=gasto.proyecto
                )
    
    @staticmethod
    def notificar_cambio_proyecto(proyecto, estado_anterior, estado_nuevo):
        """Notifica sobre cambios de estado en proyectos"""
        usuarios = User.objects.filter(is_active=True)
        for usuario in usuarios:
            NotificacionService.crear_notificacion(
                usuario=usuario,
                tipo='proyecto_estado',
                titulo=f'Cambio de Estado: {proyecto.nombre}',
                mensaje=f'El proyecto {proyecto.nombre} cambió de estado de {estado_anterior} a {estado_nuevo}',
                prioridad='baja',
                proyecto=proyecto
            )
    
    @staticmethod
    def notificar_anticipo_disponible(anticipo):
        """Notifica sobre anticipos disponibles"""
        usuarios = User.objects.filter(is_active=True)
        for usuario in usuarios:
            NotificacionService.crear_notificacion(
                usuario=usuario,
                tipo='anticipo_disponible',
                titulo=f'Anticipo Disponible: {anticipo.numero_anticipo}',
                mensaje=f'El anticipo {anticipo.numero_anticipo} por Q{anticipo.monto_disponible} está disponible para aplicar',
                prioridad='media',
                proyecto=anticipo.proyecto
            )
    
    @staticmethod
    def notificar_presupuesto_revision(presupuesto):
        """Notifica sobre presupuestos que requieren revisión"""
        if presupuesto.estado == 'en_revision':
            usuarios = User.objects.filter(is_active=True, is_superuser=True)
            for usuario in usuarios:
                NotificacionService.crear_notificacion(
                    usuario=usuario,
                    tipo='presupuesto_revision',
                    titulo=f'Presupuesto Requiere Revisión: {presupuesto.nombre}',
                    mensaje=f'El presupuesto {presupuesto.nombre} del proyecto {presupuesto.proyecto.nombre} requiere revisión',
                    prioridad='media',
                    proyecto=presupuesto.proyecto
                )
    
    @staticmethod
    def notificar_archivo_subido(archivo):
        """Notifica sobre nuevos archivos subidos"""
        usuarios = User.objects.filter(is_active=True)
        for usuario in usuarios:
            NotificacionService.crear_notificacion(
                usuario=usuario,
                tipo='archivo_subido',
                titulo=f'Nuevo Archivo: {archivo.nombre}',
                mensaje=f'Se subió el archivo "{archivo.nombre}" al proyecto {archivo.proyecto.nombre}',
                prioridad='baja',
                proyecto=archivo.proyecto
            )
    
    @staticmethod
    def limpiar_notificaciones_antiguas(dias=30):
        """Limpia notificaciones antiguas"""
        fecha_limite = timezone.now() - timedelta(days=dias)
        NotificacionSistema.objects.filter(
            fecha_creacion__lt=fecha_limite,
            leida=True
        ).delete()
    
    @staticmethod
    def obtener_notificaciones_no_leidas(usuario):
        """Obtiene las notificaciones no leídas de un usuario"""
        return NotificacionSistema.objects.filter(
            usuario=usuario,
            leida=False
        ).order_by('-fecha_creacion')
    
    @staticmethod
    def marcar_como_leida(notificacion_id, usuario):
        """Marca una notificación como leída"""
        try:
            notificacion = NotificacionSistema.objects.get(
                id=notificacion_id,
                usuario=usuario
            )
            notificacion.marcar_como_leida()
            return True
        except NotificacionSistema.DoesNotExist:
            return False
    
    @staticmethod
    def enviar_email_notificacion(notificacion, usuario_destino=None):
        """
        Envía una notificación por email con plantilla HTML personalizada
        """
        try:
            if not usuario_destino:
                usuario_destino = notificacion.usuario
            
            # Obtener configuración del usuario
            config = ConfiguracionNotificaciones.objects.filter(usuario=usuario_destino).first()
            if not config or not config.email_habilitado:
                return False
            
            # Verificar horario de notificaciones
            hora_actual = timezone.now().time()
            if config.horario_inicio and config.horario_fin:
                if not (config.horario_inicio <= hora_actual <= config.horario_fin):
                    return False
            
            # Renderizar plantilla HTML
            context = {
                'notificacion': notificacion,
                'usuario': usuario_destino,
                'fecha': timezone.now(),
                'base_url': settings.BASE_URL if hasattr(settings, 'BASE_URL') else 'http://localhost:8000'
            }
            
            html_content = render_to_string('notificaciones/email_template.html', context)
            text_content = strip_tags(html_content)
            
            # Crear email
            subject = f"🔔 {notificacion.titulo}"
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = usuario_destino.email
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[to_email]
            )
            email.attach_alternative(html_content, "text/html")
            
            # Enviar email
            email.send()
            
            # Registrar en historial
            HistorialNotificaciones.objects.create(
                usuario=usuario_destino,
                tipo=notificacion.tipo,
                titulo=notificacion.titulo,
                mensaje=notificacion.mensaje,
                fecha_envio=timezone.now(),
                metodo_envio='email',
                estado='enviado'
            )
            
            logger.info(f"Email enviado exitosamente a {usuario_destino.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error enviando email: {str(e)}")
            
            # Registrar error en historial
            if usuario_destino:
                HistorialNotificaciones.objects.create(
                    usuario=usuario_destino,
                    tipo=notificacion.tipo if notificacion else 'sistema',
                    titulo=notificacion.titulo if notificacion else 'Error de Email',
                    mensaje=f"Error enviando email: {str(e)}",
                    fecha_envio=timezone.now(),
                    metodo_envio='email',
                    estado='error'
                )
            
            return False
    
    @staticmethod
    def enviar_notificacion_masiva(tipo, titulo, mensaje, usuarios=None, prioridad='normal'):
        """
        Envía una notificación masiva a múltiples usuarios
        """
        if not usuarios:
            usuarios = User.objects.filter(is_active=True)
        
        notificaciones_creadas = []
        for usuario in usuarios:
            notificacion = NotificacionSistema.objects.create(
                usuario=usuario,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                prioridad=prioridad
            )
            notificaciones_creadas.append(notificacion)
            
            # Enviar email si está habilitado
            NotificacionService.enviar_email_notificacion(notificacion, usuario)
        
        return notificaciones_creadas
    
    @staticmethod
    def programar_notificacion(tipo, titulo, mensaje, usuario, fecha_envio, prioridad='normal'):
        """
        Programa una notificación para ser enviada en una fecha específica
        """
        from .models import NotificacionProgramada
        
        notificacion = NotificacionProgramada.objects.create(
            usuario=usuario,
            tipo=tipo,
            titulo=titulo,
            mensaje=mensaje,
            fecha_envio=fecha_envio,
            prioridad=prioridad,
            estado='programada'
        )
        
        return notificacion
    
    @staticmethod
    def procesar_notificaciones_programadas():
        """
        Procesa y envía las notificaciones programadas
        """
        from .models import NotificacionProgramada
        
        ahora = timezone.now()
        notificaciones_pendientes = NotificacionProgramada.objects.filter(
            fecha_envio__lte=ahora,
            estado='programada'
        )
        
        for notif_programada in notificaciones_pendientes:
            # Crear notificación del sistema
            notificacion = NotificacionSistema.objects.create(
                usuario=notif_programada.usuario,
                tipo=notif_programada.tipo,
                titulo=notif_programada.titulo,
                mensaje=notif_programada.mensaje,
                prioridad=notif_programada.prioridad
            )
            
            # Enviar email
            NotificacionService.enviar_email_notificacion(notificacion)
            
            # Marcar como procesada
            notif_programada.estado = 'enviada'
            notif_programada.fecha_envio_real = ahora
            notif_programada.save()
            
            logger.info(f"Notificación programada procesada: {notif_programada.id}")

    @staticmethod
    def enviar_notificacion_push(notificacion):
        """
        Envía una notificación push al navegador del usuario
        """
        try:
            # En un entorno real, aquí se enviaría la notificación push
            # usando Web Push API o servicios como Firebase Cloud Messaging
            
            logger.info(f"Notificación push enviada: {notificacion.titulo} a {notificacion.usuario.username}")
            return True
        except Exception as e:
            logger.error(f"Error enviando notificación push: {str(e)}")
            return False

    @staticmethod
    def enviar_notificacion_push_masiva(notificaciones, usuarios=None):
        """
        Envía notificaciones push masivas a múltiples usuarios
        """
        try:
            if usuarios is None:
                usuarios = User.objects.filter(is_active=True)
            
            for usuario in usuarios:
                for notificacion in notificaciones:
                    if notificacion.usuario == usuario:
                        NotificacionService.enviar_notificacion_push(notificacion)
            
            logger.info(f"Notificaciones push masivas enviadas a {usuarios.count()} usuarios")
            return True
        except Exception as e:
            logger.error(f"Error enviando notificaciones push masivas: {str(e)}")
            return False


class SistemaNotificacionesAutomaticas:
    """Sistema para enviar notificaciones automáticas basadas en eventos"""
    
    @staticmethod
    def verificar_facturas_vencidas():
        """Verifica y notifica sobre facturas vencidas"""
        hoy = timezone.now().date()
        facturas_vencidas = Factura.objects.filter(
            fecha_vencimiento__lt=hoy,
            estado__in=['emitida', 'enviada']
        )
        
        for factura in facturas_vencidas:
            factura.estado = 'vencida'
            factura.save()
            NotificacionService.notificar_factura_vencida(factura)
    
    @staticmethod
    def verificar_pagos_pendientes():
        """Verifica y notifica sobre pagos pendientes"""
        facturas_con_pendiente = Factura.objects.filter(
            monto_pendiente__gt=0,
            estado__in=['emitida', 'enviada', 'vencida']
        )
        
        for factura in facturas_con_pendiente:
            NotificacionService.notificar_pago_pendiente(factura)
    
    @staticmethod
    def verificar_gastos_pendientes():
        """Verifica y notifica sobre gastos pendientes de aprobación"""
        gastos_pendientes = Gasto.objects.filter(
            aprobado=False,
            fecha_gasto__gte=timezone.now() - timedelta(days=7)
        )
        
        for gasto in gastos_pendientes:
            NotificacionService.notificar_gasto_aprobacion(gasto)
    
    @staticmethod
    def verificar_presupuestos_revision():
        """Verifica y notifica sobre presupuestos en revisión"""
        presupuestos_revision = Presupuesto.objects.filter(
            estado='en_revision',
            fecha_creacion__gte=timezone.now() - timedelta(days=3)
        )
        
        for presupuesto in presupuestos_revision:
            NotificacionService.notificar_presupuesto_revision(presupuesto)
    
    @staticmethod
    def verificar_y_enviar_recordatorios():
        """
        Verifica y envía recordatorios automáticos por email
        """
        # Recordatorios de facturas próximas a vencer
        fecha_limite = timezone.now() + timedelta(days=7)
        facturas_proximas = Factura.objects.filter(
            fecha_vencimiento__lte=fecha_limite,
            estado='pendiente'
        )
        
        for factura in facturas_proximas:
            dias_restantes = (factura.fecha_vencimiento - timezone.now().date()).days
            
            if dias_restantes <= 3:
                prioridad = 'alta'
            elif dias_restantes <= 7:
                prioridad = 'normal'
            else:
                continue
            
            titulo = f"⚠️ Factura próxima a vencer"
            mensaje = f"La factura #{factura.numero} vence en {dias_restantes} días. Monto: ${factura.monto_total}"
            
            notificacion = NotificacionSistema.objects.create(
                usuario=factura.proyecto.cliente,
                tipo='factura',
                factura=factura,
                titulo=titulo,
                mensaje=mensaje,
                prioridad=prioridad
            )
            
            # Enviar email
            NotificacionService.enviar_email_notificacion(notificacion)
    
    @staticmethod
    def enviar_resumen_diario(usuario):
        """
        Envía un resumen diario de notificaciones por email
        """
        hoy = timezone.now().date()
        notificaciones_hoy = NotificacionSistema.objects.filter(
            usuario=usuario,
            fecha_creacion__date=hoy
        ).order_by('-fecha_creacion')
        
        if not notificaciones_hoy.exists():
            return
        
        # Contar por tipo
        resumen = {}
        for notif in notificaciones_hoy:
            if notif.tipo not in resumen:
                resumen[notif.tipo] = 0
            resumen[notif.tipo] += 1
        
        # Crear mensaje de resumen
        titulo = "📊 Resumen Diario de Notificaciones"
        mensaje = f"Tienes {notificaciones_hoy.count()} notificaciones hoy:\n\n"
        
        for tipo, cantidad in resumen.items():
            mensaje += f"• {tipo.title()}: {cantidad}\n"
        
        # Crear notificación de resumen
        notificacion = NotificacionSistema.objects.create(
            usuario=usuario,
            tipo='sistema',
            titulo=titulo,
            mensaje=mensaje,
            prioridad='baja'
        )
        
        # Enviar email de resumen
        NotificacionService.enviar_email_notificacion(notificacion)
    
    @staticmethod
    def ejecutar_verificaciones_diarias():
        """
        Ejecuta todas las verificaciones automáticas diarias
        """
        logger.info("Iniciando verificaciones automáticas diarias...")
        
        # Verificaciones existentes
        SistemaNotificacionesAutomaticas.verificar_facturas_vencidas()
        SistemaNotificacionesAutomaticas.verificar_pagos_pendientes()
        SistemaNotificacionesAutomaticas.verificar_archivos_recientes()
        
        # Nuevas verificaciones
        SistemaNotificacionesAutomaticas.verificar_y_enviar_recordatorios()
        
        # Procesar notificaciones programadas
        NotificacionService.procesar_notificaciones_programadas()
        
        # Enviar resúmenes diarios a usuarios que lo tengan habilitado
        configuraciones = ConfiguracionNotificaciones.objects.filter(
            email_habilitado=True,
            resumen_diario=True
        )
        
        for config in configuraciones:
            SistemaNotificacionesAutomaticas.enviar_resumen_diario(config.usuario)
        
        logger.info("Verificaciones automáticas diarias completadas")


class EmailTemplateService:
    """
    Servicio para gestionar plantillas de email
    """
    
    @staticmethod
    def generar_plantilla_personalizada(tipo_notificacion, datos_personalizados):
        """
        Genera una plantilla HTML personalizada basada en el tipo de notificación
        """
        plantillas_base = {
            'factura': {
                'color_principal': '#dc3545',
                'icono': '📄',
                'estilo_boton': 'background-color: #dc3545;'
            },
            'proyecto': {
                'color_principal': '#007bff',
                'icono': '🏗️',
                'estilo_boton': 'background-color: #007bff;'
            },
            'gasto': {
                'color_principal': '#ffc107',
                'icono': '💰',
                'estilo_boton': 'background-color: #ffc107;'
            },
            'archivo': {
                'color_principal': '#28a745',
                'icono': '📁',
                'estilo_boton': 'background-color: #28a745;'
            },
            'sistema': {
                'color_principal': '#6c757d',
                'icono': '🔔',
                'estilo_boton': 'background-color: #6c757d;'
            }
        }
        
        plantilla = plantillas_base.get(tipo_notificacion, plantillas_base['sistema'])
        plantilla.update(datos_personalizados)
        
        return plantilla
