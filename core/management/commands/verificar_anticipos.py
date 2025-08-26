from django.core.management.base import BaseCommand
from core.models import AnticipoProyecto
from django.db import transaction


class Command(BaseCommand):
    help = 'Verifica y corrige el estado de los anticipos del proyecto'

    def add_arguments(self, parser):
        parser.add_argument(
            '--proyecto_id',
            type=int,
            help='ID del proyecto específico a verificar',
        )
        parser.add_argument(
            '--corregir',
            action='store_true',
            help='Corregir automáticamente los anticipos con estado incorrecto',
        )

    def handle(self, *args, **options):
        proyecto_id = options.get('proyecto_id')
        corregir = options.get('corregir')

        if proyecto_id:
            anticipos = AnticipoProyecto.objects.filter(proyecto_id=proyecto_id)
            self.stdout.write(f'Verificando anticipos del proyecto {proyecto_id}')
        else:
            anticipos = AnticipoProyecto.objects.all()
            self.stdout.write('Verificando todos los anticipos del sistema')

        # Contar por estado
        estados = {}
        for anticipo in anticipos:
            estado = anticipo.estado
            if estado not in estados:
                estados[estado] = []
            estados[estado].append(anticipo)

        self.stdout.write('\n📊 RESUMEN DE ANTICIPOS:')
        self.stdout.write('=' * 50)
        
        for estado, lista_anticipos in estados.items():
            self.stdout.write(f'{estado.upper()}: {len(lista_anticipos)} anticipos')
            
            if estado == 'liquidado':
                self.stdout.write('  Detalles de anticipos liquidados:')
                for anticipo in lista_anticipos[:5]:  # Mostrar solo los primeros 5
                    self.stdout.write(f'    - {anticipo.colaborador.nombre}: Q{anticipo.monto} - {anticipo.fecha_anticipo}')
                    if anticipo.fecha_liquidacion:
                        self.stdout.write(f'      Liquidado el: {anticipo.fecha_liquidacion}')
                    if anticipo.liquidado_por:
                        self.stdout.write(f'      Por: {anticipo.liquidado_por.username}')
                if len(lista_anticipos) > 5:
                    self.stdout.write(f'    ... y {len(lista_anticipos) - 5} más')

        # Verificar inconsistencias
        self.stdout.write('\n🔍 VERIFICANDO INCONSISTENCIAS:')
        self.stdout.write('=' * 50)
        
        inconsistencias = []
        
        for anticipo in anticipos:
            if anticipo.estado == 'liquidado':
                if not anticipo.fecha_liquidacion:
                    inconsistencias.append(f'Anticipo {anticipo.id}: Liquidado sin fecha de liquidación')
                if not anticipo.liquidado_por:
                    inconsistencias.append(f'Anticipo {anticipo.id}: Liquidado sin usuario que liquide')
            elif anticipo.estado == 'pendiente':
                if anticipo.fecha_liquidacion:
                    inconsistencias.append(f'Anticipo {anticipo.id}: Pendiente con fecha de liquidación')
                if anticipo.liquidado_por:
                    inconsistencias.append(f'Anticipo {anticipo.id}: Pendiente con usuario que liquide')

        if inconsistencias:
            self.stdout.write(self.style.WARNING(f'Se encontraron {len(inconsistencias)} inconsistencias:'))
            for inc in inconsistencias:
                self.stdout.write(f'  ⚠️  {inc}')
        else:
            self.stdout.write(self.style.SUCCESS('✅ No se encontraron inconsistencias'))

        # Corregir si se solicita
        if corregir and inconsistencias:
            self.stdout.write('\n🔧 CORRIGIENDO INCONSISTENCIAS...')
            self.stdout.write('=' * 50)
            
            with transaction.atomic():
                corregidos = 0
                
                for anticipo in anticipos:
                    if anticipo.estado == 'liquidado':
                        if not anticipo.fecha_liquidacion:
                            anticipo.fecha_liquidacion = anticipo.fecha_anticipo
                            anticipo.save()
                            corregidos += 1
                        if not anticipo.liquidado_por:
                            # Asignar al primer usuario del sistema o crear uno dummy
                            from django.contrib.auth.models import User
                            try:
                                usuario = User.objects.first()
                                if usuario:
                                    anticipo.liquidado_por = usuario
                                    anticipo.save()
                                    corregidos += 1
                            except:
                                pass
                    elif anticipo.estado == 'pendiente':
                        if anticipo.fecha_liquidacion:
                            anticipo.fecha_liquidacion = None
                            anticipo.save()
                            corregidos += 1
                        if anticipo.liquidado_por:
                            anticipo.liquidado_por = None
                            anticipo.save()
                            corregidos += 1

                self.stdout.write(self.style.SUCCESS(f'✅ Se corrigieron {corregidos} inconsistencias'))

        # Opción para resetear todos los anticipos a pendiente
        if corregir:
            self.stdout.write('\n🔄 OPCIONES ADICIONALES:')
            self.stdout.write('=' * 50)
            self.stdout.write('Para resetear todos los anticipos a estado "pendiente":')
            self.stdout.write('  python manage.py verificar_anticipos --corregir --resetear')
            
            if '--resetear' in str(options):
                self.stdout.write('\n🔄 RESETEANDO TODOS LOS ANTICIPOS A PENDIENTE...')
                with transaction.atomic():
                    AnticipoProyecto.objects.all().update(
                        estado='pendiente',
                        fecha_liquidacion=None,
                        liquidado_por=None
                    )
                    self.stdout.write(self.style.SUCCESS('✅ Todos los anticipos han sido reseteados a "pendiente"'))

        self.stdout.write('\n✅ Verificación completada')
