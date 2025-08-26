from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from core.services import SistemaNotificacionesAutomaticas, NotificacionService
from core.models import NotificacionProgramada, ConfiguracionNotificaciones
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Envía notificaciones programadas y ejecuta verificaciones automáticas'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--tipo',
            type=str,
            choices=['programadas', 'automaticas', 'resumenes', 'todas'],
            default='todas',
            help='Tipo de notificaciones a procesar'
        )
        
        parser.add_argument(
            '--usuario',
            type=str,
            help='Username específico para procesar notificaciones'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Ejecutar sin enviar realmente las notificaciones'
        )
    
    def handle(self, *args, **options):
        tipo = options['tipo']
        usuario_especifico = options['usuario']
        dry_run = options['dry_run']
        
        self.stdout.write(
            self.style.SUCCESS(f'🚀 Iniciando procesamiento de notificaciones: {tipo}')
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('⚠️  MODO DRY-RUN: No se enviarán notificaciones reales')
            )
        
        try:
            if tipo in ['programadas', 'todas']:
                self.procesar_notificaciones_programadas(dry_run, usuario_especifico)
            
            if tipo in ['automaticas', 'todas']:
                self.ejecutar_verificaciones_automaticas(dry_run, usuario_especifico)
            
            if tipo in ['resumenes', 'todas']:
                self.enviar_resumenes_diarios(dry_run, usuario_especifico)
            
            self.stdout.write(
                self.style.SUCCESS('✅ Procesamiento de notificaciones completado exitosamente')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error durante el procesamiento: {str(e)}')
            )
            logger.error(f"Error en comando enviar_notificaciones: {str(e)}")
    
    def procesar_notificaciones_programadas(self, dry_run, usuario_especifico):
        """Procesa las notificaciones programadas"""
        self.stdout.write('📅 Procesando notificaciones programadas...')
        
        # Filtrar notificaciones programadas
        queryset = NotificacionProgramada.objects.filter(
            estado='programada',
            fecha_envio__lte=timezone.now()
        )
        
        if usuario_especifico:
            try:
                usuario = User.objects.get(username=usuario_especifico)
                queryset = queryset.filter(usuario=usuario)
                self.stdout.write(f'   Usuario específico: {usuario.username}')
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Usuario no encontrado: {usuario_especifico}')
                )
                return
        
        notificaciones = list(queryset)
        
        if not notificaciones:
            self.stdout.write('   No hay notificaciones programadas para procesar')
            return
        
        self.stdout.write(f'   Encontradas {len(notificaciones)} notificaciones programadas')
        
        for notif_programada in notificaciones:
            try:
                self.stdout.write(f'   📤 Procesando: {notif_programada.titulo} para {notif_programada.usuario.username}')
                
                if not dry_run:
                    # Crear notificación del sistema
                    notificacion = NotificacionService.crear_notificacion(
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
                    notif_programada.fecha_envio_real = timezone.now()
                    notif_programada.save()
                    
                    self.stdout.write(f'      ✅ Enviada exitosamente')
                else:
                    self.stdout.write(f'      🔍 DRY-RUN: Se habría enviado')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'      ❌ Error: {str(e)}')
                )
                logger.error(f"Error procesando notificación programada {notif_programada.id}: {str(e)}")
                
                if not dry_run:
                    notif_programada.estado = 'error'
                    notif_programada.save()
    
    def ejecutar_verificaciones_automaticas(self, dry_run, usuario_especifico):
        """Ejecuta las verificaciones automáticas del sistema"""
        self.stdout.write('🔍 Ejecutando verificaciones automáticas...')
        
        if not dry_run:
            try:
                SistemaNotificacionesAutomaticas.ejecutar_verificaciones_diarias()
                self.stdout.write('   ✅ Verificaciones automáticas ejecutadas')
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'   ❌ Error en verificaciones automáticas: {str(e)}')
                )
                logger.error(f"Error en verificaciones automáticas: {str(e)}")
        else:
            self.stdout.write('   🔍 DRY-RUN: Se habrían ejecutado las verificaciones')
    
    def enviar_resumenes_diarios(self, dry_run, usuario_especifico):
        """Envía resúmenes diarios a usuarios que lo tengan habilitado"""
        self.stdout.write('📊 Enviando resúmenes diarios...')
        
        # Filtrar configuraciones
        queryset = ConfiguracionNotificaciones.objects.filter(
            email_habilitado=True,
            resumen_diario=True
        )
        
        if usuario_especifico:
            try:
                usuario = User.objects.get(username=usuario_especifico)
                queryset = queryset.filter(usuario=usuario)
                self.stdout.write(f'   Usuario específico: {usuario.username}')
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Usuario no encontrado: {usuario_especifico}')
                )
                return
        
        configuraciones = list(queryset)
        
        if not configuraciones:
            self.stdout.write('   No hay usuarios con resúmenes diarios habilitados')
            return
        
        self.stdout.write(f'   Encontrados {len(configuraciones)} usuarios para resúmenes')
        
        for config in configuraciones:
            try:
                self.stdout.write(f'   📧 Enviando resumen a: {config.usuario.username}')
                
                if not dry_run:
                    SistemaNotificacionesAutomaticas.enviar_resumen_diario(config.usuario)
                    self.stdout.write(f'      ✅ Resumen enviado exitosamente')
                else:
                    self.stdout.write(f'      🔍 DRY-RUN: Se habría enviado el resumen')
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'      ❌ Error: {str(e)}')
                )
                logger.error(f"Error enviando resumen diario a {config.usuario.username}: {str(e)}")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del sistema de notificaciones"""
        total_notificaciones = NotificacionProgramada.objects.count()
        pendientes = NotificacionProgramada.objects.filter(estado='programada').count()
        enviadas = NotificacionProgramada.objects.filter(estado='enviada').count()
        errores = NotificacionProgramada.objects.filter(estado='error').count()
        
        self.stdout.write('\n📊 ESTADÍSTICAS DEL SISTEMA:')
        self.stdout.write(f'   Total de notificaciones programadas: {total_notificaciones}')
        self.stdout.write(f'   Pendientes de envío: {pendientes}')
        self.stdout.write(f'   Enviadas exitosamente: {enviadas}')
        self.stdout.write(f'   Con errores: {errores}')
        
        if total_notificaciones > 0:
            porcentaje_exito = (enviadas / total_notificaciones) * 100
            self.stdout.write(f'   Porcentaje de éxito: {porcentaje_exito:.1f}%')
