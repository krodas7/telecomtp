from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Factura


class Command(BaseCommand):
    help = 'Actualizar estados de vencimiento de facturas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mostrar qué se haría sin ejecutar cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('🔍 MODO SIMULACIÓN - No se harán cambios'))
        
        # Obtener facturas que podrían estar vencidas
        facturas_por_vencer = Factura.objects.filter(
            estado__in=['borrador', 'emitida', 'enviada'],
            fecha_vencimiento__lt=timezone.now().date()
        ).exclude(
            estado__in=['pagada', 'cancelada']
        )
        
        self.stdout.write(f"📊 Total de facturas a revisar: {facturas_por_vencer.count()}")
        
        if facturas_por_vencer.count() == 0:
            self.stdout.write(self.style.SUCCESS('✅ No hay facturas que requieran actualización'))
            return
        
        # Mostrar facturas que se actualizarían
        self.stdout.write("\n📋 Facturas que se marcarían como vencidas:")
        for factura in facturas_por_vencer:
            dias_vencida = (timezone.now().date() - factura.fecha_vencimiento).days
            self.stdout.write(
                f"  • {factura.numero_factura} - {factura.cliente.razon_social} "
                f"- Vencida hace {dias_vencida} días"
            )
        
        if not dry_run:
            # Actualizar estados
            actualizadas = 0
            for factura in facturas_por_vencer:
                estado_anterior = factura.estado
                factura.estado = 'vencida'
                factura.save(update_fields=['estado'])
                actualizadas += 1
                
                self.stdout.write(
                    f"✅ {factura.numero_factura}: {estado_anterior} → vencida"
                )
            
            self.stdout.write(
                self.style.SUCCESS(f"\n🎉 Actualización completada: {actualizadas} facturas actualizadas")
            )
        else:
            self.stdout.write(
                self.style.WARNING(f"\n⚠️ En modo simulación se marcarían {facturas_por_vencer.count()} facturas como vencidas")
            )
