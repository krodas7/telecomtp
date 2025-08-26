#!/usr/bin/env python
import os
import django
from decimal import Decimal
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import (
    Cliente, Proyecto, Colaborador, Factura, Gasto, CategoriaGasto, 
    NotificacionSistema, Pago, Anticipo, Presupuesto, PartidaPresupuesto,
    ArchivoProyecto, LogActividad
)
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta

print("=== CREANDO DATOS COMPLETOS DE PRUEBA ===")
print("=" * 50)

try:
    # Obtener o crear usuario de prueba
    user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'Test',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        user.set_password('admin123')
        user.save()
        print("✅ Usuario admin creado")
    else:
        print("✅ Usuario admin ya existe")

    # Crear múltiples clientes
    clientes_data = [
        {
            'razon_social': 'Constructora Metropolitana S.A.',
            'codigo_fiscal': 'CM001-2025',
            'email': 'info@metropolitana.com',
            'telefono': '+502 2222-1111',
            'direccion': 'Av. Principal #100, Zona 1, Ciudad'
        },
        {
            'razon_social': 'Ingeniería Civil del Norte',
            'codigo_fiscal': 'ICN002-2025',
            'email': 'contacto@ingenierianorte.com',
            'telefono': '+502 3333-2222',
            'direccion': 'Calle Norte #200, Zona 2, Ciudad'
        },
        {
            'razon_social': 'Desarrollos Urbanos del Sur',
            'codigo_fiscal': 'DUS003-2025',
            'email': 'ventas@desarrollossur.com',
            'telefono': '+502 4444-3333',
            'direccion': 'Boulevard Sur #300, Zona 3, Ciudad'
        },
        {
            'razon_social': 'Infraestructura Nacional Ltda.',
            'codigo_fiscal': 'INL004-2025',
            'email': 'proyectos@infraestructura.com',
            'telefono': '+502 5555-4444',
            'direccion': 'Carretera Nacional Km 15, Zona 4'
        },
        {
            'razon_social': 'Construcciones Residenciales Plus',
            'codigo_fiscal': 'CRP005-2025',
            'email': 'info@residencialesplus.com',
            'telefono': '+502 6666-5555',
            'direccion': 'Residencial Los Pinos #500, Zona 5'
        }
    ]

    clientes_creados = []
    for cliente_data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            razon_social=cliente_data['razon_social'],
            defaults={
                'codigo_fiscal': cliente_data['codigo_fiscal'],
                'direccion': cliente_data['direccion'],
                'telefono': cliente_data['telefono'],
                'email': cliente_data['email'],
                'activo': True
            }
        )
        if created:
            print(f"✅ Cliente '{cliente.razon_social}' creado")
        else:
            print(f"✅ Cliente '{cliente.razon_social}' ya existe")
        clientes_creados.append(cliente)

    # Crear categorías de gasto
    categorias_data = [
        'Materiales de Construcción',
        'Mano de Obra',
        'Equipos y Maquinaria',
        'Transporte y Logística',
        'Administrativos',
        'Servicios Públicos',
        'Seguridad Industrial',
        'Mantenimiento',
        'Permisos y Licencias',
        'Consultoría Técnica'
    ]

    categorias_creadas = []
    for nombre_categoria in categorias_data:
        categoria, created = CategoriaGasto.objects.get_or_create(
            nombre=nombre_categoria,
            defaults={'descripcion': f'Categoría para gastos de {nombre_categoria.lower()}'}
        )
        if created:
            print(f"✅ Categoría '{categoria.nombre}' creada")
        else:
            print(f"✅ Categoría '{categoria.nombre}' ya existe")
        categorias_creadas.append(categoria)

    # Crear colaboradores
    colaboradores_data = [
        {
            'nombre': 'Carlos Méndez López',
            'dpi': '1234567890101',
            'telefono': '+502 7777-6666',
            'email': 'carlos.mendez@empresa.com',
            'salario': Decimal('4500.00'),
            'fecha_contratacion': (timezone.now() - timedelta(days=365)).date()
        },
        {
            'nombre': 'Ana María González',
            'dpi': '2345678901012',
            'telefono': '+502 8888-7777',
            'email': 'ana.gonzalez@empresa.com',
            'salario': Decimal('5200.00'),
            'fecha_contratacion': (timezone.now() - timedelta(days=300)).date()
        },
        {
            'nombre': 'Roberto Jiménez',
            'dpi': '3456789010123',
            'telefono': '+502 9999-8888',
            'email': 'roberto.jimenez@empresa.com',
            'salario': Decimal('3800.00'),
            'fecha_contratacion': (timezone.now() - timedelta(days=200)).date()
        },
        {
            'nombre': 'María Elena Ramírez',
            'dpi': '4567890101234',
            'telefono': '+502 1111-9999',
            'email': 'maria.ramirez@empresa.com',
            'salario': Decimal('4800.00'),
            'fecha_contratacion': (timezone.now() - timedelta(days=150)).date()
        },
        {
            'nombre': 'Luis Fernando Torres',
            'dpi': '5678901012345',
            'telefono': '+502 2222-1111',
            'email': 'luis.torres@empresa.com',
            'salario': Decimal('4100.00'),
            'fecha_contratacion': (timezone.now() - timedelta(days=100)).date()
        }
    ]

    colaboradores_creados = []
    for colaborador_data in colaboradores_data:
        colaborador, created = Colaborador.objects.get_or_create(
            nombre=colaborador_data['nombre'],
            defaults={
                'dpi': colaborador_data['dpi'],
                'telefono': colaborador_data['telefono'],
                'email': colaborador_data['email'],
                'salario': colaborador_data['salario'],
                'fecha_contratacion': colaborador_data['fecha_contratacion'],
                'activo': True
            }
        )
        if created:
            print(f"✅ Colaborador '{colaborador.nombre}' creado")
        else:
            print(f"✅ Colaborador '{colaborador.nombre}' ya existe")
        colaboradores_creados.append(colaborador)

    # Crear múltiples proyectos
    proyectos_data = [
        {
            'nombre': 'Edificio Residencial Centro Histórico',
            'descripcion': 'Construcción de edificio residencial de 20 pisos en el centro histórico de la ciudad',
            'estado': 'en_progreso',
            'fecha_inicio': (timezone.now() - timedelta(days=180)).date(),
            'fecha_fin': (timezone.now() + timedelta(days=180)).date(),
            'presupuesto': Decimal('8500000.00'),
            'cliente': clientes_creados[0]
        },
        {
            'nombre': 'Carretera Interurbana Norte-Sur',
            'descripcion': 'Construcción de carretera de 45 km entre dos ciudades principales',
            'estado': 'en_progreso',
            'fecha_inicio': (timezone.now() - timedelta(days=120)).date(),
            'fecha_fin': (timezone.now() + timedelta(days=300)).date(),
            'presupuesto': Decimal('15000000.00'),
            'cliente': clientes_creados[1]
        },
        {
            'nombre': 'Centro Comercial Plaza Norte',
            'descripcion': 'Construcción de centro comercial de 4 pisos con estacionamiento subterráneo',
            'estado': 'completado',
            'fecha_inicio': (timezone.now() - timedelta(days=400)).date(),
            'fecha_fin': (timezone.now() - timedelta(days=30)).date(),
            'presupuesto': Decimal('12000000.00'),
            'cliente': clientes_creados[2]
        },
        {
            'nombre': 'Puente sobre Río Principal',
            'descripcion': 'Construcción de puente vehicular de 200 metros sobre el río principal',
            'estado': 'pendiente',
            'fecha_inicio': (timezone.now() + timedelta(days=30)).date(),
            'fecha_fin': (timezone.now() + timedelta(days=240)).date(),
            'presupuesto': Decimal('8000000.00'),
            'cliente': clientes_creados[3]
        },
        {
            'nombre': 'Residencial Los Pinos',
            'descripcion': 'Construcción de 50 casas residenciales en urbanización privada',
            'estado': 'en_progreso',
            'fecha_inicio': (timezone.now() - timedelta(days=90)).date(),
            'fecha_fin': (timezone.now() + timedelta(days=150)).date(),
            'presupuesto': Decimal('6000000.00'),
            'cliente': clientes_creados[4]
        },
        {
            'nombre': 'Hospital Regional del Norte',
            'descripcion': 'Construcción de hospital de 3 pisos con 200 camas',
            'estado': 'pendiente',
            'fecha_inicio': (timezone.now() + timedelta(days=60)).date(),
            'fecha_fin': (timezone.now() + timedelta(days=480)).date(),
            'presupuesto': Decimal('25000000.00'),
            'cliente': clientes_creados[0]
        },
        {
            'nombre': 'Aeropuerto Internacional',
            'descripcion': 'Ampliación de pista y terminal del aeropuerto internacional',
            'estado': 'en_progreso',
            'fecha_inicio': (timezone.now() - timedelta(days=240)).date(),
            'fecha_fin': (timezone.now() + timedelta(days=120)).date(),
            'presupuesto': Decimal('35000000.00'),
            'cliente': clientes_creados[1]
        },
        {
            'nombre': 'Centro de Convenciones',
            'descripcion': 'Construcción de centro de convenciones con capacidad para 2000 personas',
            'estado': 'completado',
            'fecha_inicio': (timezone.now() - timedelta(days=500)).date(),
            'fecha_fin': (timezone.now() - timedelta(days=60)).date(),
            'presupuesto': Decimal('18000000.00'),
            'cliente': clientes_creados[2]
        }
    ]

    proyectos_creados = []
    for proyecto_data in proyectos_data:
        proyecto, created = Proyecto.objects.get_or_create(
            nombre=proyecto_data['nombre'],
            defaults={
                'cliente': proyecto_data['cliente'],
                'descripcion': proyecto_data['descripcion'],
                'estado': proyecto_data['estado'],
                'fecha_inicio': proyecto_data['fecha_inicio'],
                'fecha_fin': proyecto_data['fecha_fin'],
                'presupuesto': proyecto_data['presupuesto'],
                'activo': True
            }
        )
        if created:
            print(f"✅ Proyecto '{proyecto.nombre}' creado")
        else:
            print(f"✅ Proyecto '{proyecto.nombre}' ya existe")
        proyectos_creados.append(proyecto)

    # Crear múltiples facturas
    facturas_creadas = []
    for i, proyecto in enumerate(proyectos_creados):
        # Crear 2-4 facturas por proyecto
        num_facturas = random.randint(2, 4)
        for j in range(num_facturas):
            monto_total = Decimal(random.randint(100000, 2000000))
            monto_pagado = Decimal(random.randint(0, int(monto_total)))
            estado = 'pagada' if monto_pagado >= monto_total else 'emitida'
            
            factura, created = Factura.objects.get_or_create(
                numero_factura=f'F{i+1:03d}-{j+1:03d}-2025',
                defaults={
                    'cliente': proyecto.cliente,
                    'proyecto': proyecto,
                    'monto_total': monto_total,
                    'monto_pagado': monto_pagado,
                    'estado': estado,
                    'fecha_emision': (timezone.now() - timedelta(days=random.randint(10, 90))).date(),
                    'fecha_vencimiento': (timezone.now() + timedelta(days=random.randint(10, 60))).date(),
                    'creado_por': user
                }
            )
            if created:
                print(f"✅ Factura '{factura.numero_factura}' creada")
                facturas_creadas.append(factura)
            else:
                print(f"✅ Factura '{factura.numero_factura}' ya existe")

    # Crear múltiples gastos
    gastos_creados = []
    for proyecto in proyectos_creados:
        # Crear 3-6 gastos por proyecto
        num_gastos = random.randint(3, 6)
        for j in range(num_gastos):
            categoria = random.choice(categorias_creadas)
            monto = Decimal(random.randint(5000, 150000))
            
            gasto, created = Gasto.objects.get_or_create(
                descripcion=f'Gasto {j+1} - {categoria.nombre} - {proyecto.nombre}',
                proyecto=proyecto,
                fecha_gasto=(timezone.now() - timedelta(days=random.randint(1, 120))).date(),
                defaults={
                    'categoria': categoria,
                    'monto': monto,
                    'aprobado': random.choice([True, True, True, False])  # 75% aprobados
                }
            )
            if created:
                print(f"✅ Gasto '{gasto.descripcion}' creado")
                gastos_creados.append(gasto)
            else:
                print(f"✅ Gasto ya existe")

    # Crear múltiples pagos
    pagos_creados = []
    for factura in facturas_creadas:
        if factura.estado == 'pagada':
            # Crear 1-3 pagos por factura pagada
            num_pagos = random.randint(1, 3)
            monto_restante = factura.monto_total - factura.monto_pagado
            
            for j in range(num_pagos):
                if monto_restante <= 0:
                    break
                    
                monto_pago = min(monto_restante, Decimal(random.randint(50000, 200000)))
                monto_restante -= monto_pago
                
                pago, created = Pago.objects.get_or_create(
                    factura=factura,
                    monto=monto_pago,
                    fecha_pago=(timezone.now() - timedelta(days=random.randint(1, 60))).date(),
                    defaults={
                        'metodo_pago': random.choice(['efectivo', 'transferencia', 'cheque']),
                        'estado': 'confirmado',
                        'registrado_por': user
                    }
                )
                if created:
                    print(f"✅ Pago de Q{monto_pago:,.2f} para factura {factura.numero_factura} creado")
                    pagos_creados.append(pago)
                else:
                    print(f"✅ Pago ya existe")

    # Crear múltiples anticipos
    anticipos_creados = []
    for i, proyecto in enumerate(proyectos_creados):
        if random.choice([True, False]):  # 50% de proyectos tienen anticipos
            monto = Decimal(random.randint(100000, 500000))
            
            anticipo, created = Anticipo.objects.get_or_create(
                numero_anticipo=f'ANT{i+1:03d}-2025',
                proyecto=proyecto,
                defaults={
                    'cliente': proyecto.cliente,
                    'monto': monto,
                    'tipo': random.choice(['anticipo', 'materiales', 'gastos', 'otros']),
                    'estado': random.choice(['pendiente', 'aplicado', 'devuelto', 'cancelado']),
                    'fecha_recepcion': (timezone.now() - timedelta(days=random.randint(30, 180))).date(),
                    'creado_por': user
                }
            )
            if created:
                print(f"✅ Anticipo '{anticipo.numero_anticipo}' por Q{monto:,.2f} creado")
                anticipos_creados.append(anticipo)
            else:
                print(f"✅ Anticipo ya existe")

    # Crear múltiples notificaciones
    notificaciones_creadas = []
    tipos_notificacion = ['factura_vencida', 'proyecto_progreso', 'sistema', 'gasto_aprobacion', 'anticipo_disponible']
    prioridades = ['baja', 'normal', 'alta', 'urgente']
    
    for i in range(20):  # Crear 20 notificaciones
        tipo = random.choice(tipos_notificacion)
        prioridad = random.choice(prioridades)
        
        if tipo == 'factura_vencida':
            titulo = f'Factura próxima a vencer - {random.choice(facturas_creadas).numero_factura}'
            mensaje = f'La factura vence en {random.randint(1, 30)} días'
        elif tipo == 'proyecto_progreso':
            proyecto = random.choice(proyectos_creados)
            titulo = f'Proyecto en progreso - {proyecto.nombre}'
            mensaje = f'El proyecto está al {random.randint(20, 80)}% de avance'
        elif tipo == 'sistema':
            titulo = 'Actualización del sistema'
            mensaje = 'Se han aplicado mejoras en el sistema de construcción'
        elif tipo == 'gasto_aprobacion':
            gasto = random.choice(gastos_creados)
            titulo = f'Gasto pendiente de aprobación - {gasto.descripcion[:30]}...'
            mensaje = f'Gasto por Q{gasto.monto:,.2f} requiere aprobación'
        else:  # anticipo_disponible
            anticipo = random.choice(anticipos_creados) if anticipos_creados else None
            if anticipo:
                titulo = f'Anticipo disponible - {anticipo.numero_anticipo}'
                mensaje = f'Anticipo por Q{anticipo.monto:,.2f} disponible para aplicación'
            else:
                titulo = 'Sistema de anticipos'
                mensaje = 'Los anticipos están funcionando correctamente'
        
        notif, created = NotificacionSistema.objects.get_or_create(
            titulo=titulo,
            mensaje=mensaje,
            defaults={
                'usuario': user,
                'tipo': tipo,
                'prioridad': prioridad,
                'leida': random.choice([True, False]),
                'fecha_creacion': timezone.now() - timedelta(days=random.randint(0, 30))
            }
        )
        if created:
            print(f"✅ Notificación '{notif.titulo[:30]}...' creada")
            notificaciones_creadas.append(notif)
        else:
            print(f"✅ Notificación ya existe")

    # Crear presupuestos
    presupuestos_creados = []
    for proyecto in proyectos_creados:
        if random.choice([True, False]):  # 50% de proyectos tienen presupuesto
            presupuesto, created = Presupuesto.objects.get_or_create(
                proyecto=proyecto,
                defaults={
                    'nombre': f'Presupuesto {proyecto.nombre}',
                    'descripcion': f'Presupuesto detallado para el proyecto {proyecto.nombre}',
                    'estado': random.choice(['borrador', 'en_revision', 'aprobado']),
                    'monto_total': proyecto.presupuesto or Decimal('1000000.00'),
                    'creado_por': user
                }
            )
            if created:
                print(f"✅ Presupuesto para '{proyecto.nombre}' creado")
                presupuestos_creados.append(presupuesto)
                
                # Crear partidas del presupuesto
                for j in range(random.randint(3, 8)):
                    partida, created = PartidaPresupuesto.objects.get_or_create(
                        presupuesto=presupuesto,
                        descripcion=f'Partida {j+1} - {random.choice(categorias_creadas).nombre}',
                        defaults={
                            'monto_estimado': Decimal(random.randint(50000, 200000)),
                            'monto_real': Decimal(random.randint(30000, 250000))
                        }
                    )
                    if created:
                        print(f"  ✅ Partida '{partida.descripcion[:30]}...' creada")
            else:
                print(f"✅ Presupuesto ya existe")

    # Crear archivos de proyecto
    archivos_creados = []
    tipos_archivo = ['plano', 'documento', 'imagen', 'contrato', 'especificacion']
    
    for proyecto in proyectos_creados:
        num_archivos = random.randint(2, 5)
        for j in range(num_archivos):
            archivo, created = ArchivoProyecto.objects.get_or_create(
                nombre=f'Archivo {j+1} - {proyecto.nombre}',
                proyecto=proyecto,
                defaults={
                    'tipo': random.choice(tipos_archivo),
                    'descripcion': f'Archivo {j+1} del proyecto {proyecto.nombre}',
                    'subido_por': user,
                    'activo': True
                }
            )
            if created:
                print(f"✅ Archivo '{archivo.nombre[:30]}...' creado")
                archivos_creados.append(archivo)
            else:
                print(f"✅ Archivo ya existe")

    # Crear logs de actividad
    actividades = [
        'Login', 'Logout', 'Crear', 'Editar', 'Eliminar', 'Subir Archivo',
        'Descargar Archivo', 'Aprobar Gasto', 'Crear Factura', 'Registrar Pago'
    ]
    modulos = ['Sistema', 'Proyectos', 'Clientes', 'Facturas', 'Gastos', 'Archivos']
    
    for i in range(50):  # Crear 50 logs de actividad
        log, created = LogActividad.objects.get_or_create(
            usuario=user,
            accion=random.choice(actividades),
            modulo=random.choice(modulos),
            descripcion=f'Actividad de prueba {i+1} - {random.choice(actividades)} en {random.choice(modulos)}',
            fecha_actividad=timezone.now() - timedelta(days=random.randint(0, 90)),
            defaults={
                'ip_address': f'192.168.1.{random.randint(1, 255)}',
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        if created:
            print(f"✅ Log de actividad {i+1} creado")

    print("\n" + "=" * 50)
    print("✅ DATOS COMPLETOS DE PRUEBA CREADOS EXITOSAMENTE")
    print("=" * 50)
    
    # Mostrar resumen completo
    print(f"\n📊 RESUMEN COMPLETO:")
    print(f"  • Clientes activos: {Cliente.objects.filter(activo=True).count()}")
    print(f"  • Proyectos activos: {Proyecto.objects.filter(activo=True).count()}")
    print(f"  • Proyectos en progreso: {Proyecto.objects.filter(activo=True, estado='en_progreso').count()}")
    print(f"  • Proyectos pendientes: {Proyecto.objects.filter(activo=True, estado='pendiente').count()}")
    print(f"  • Proyectos completados: {Proyecto.objects.filter(activo=True, estado='completado').count()}")
    print(f"  • Colaboradores activos: {Colaborador.objects.filter(activo=True).count()}")
    print(f"  • Categorías de gasto: {CategoriaGasto.objects.count()}")
    print(f"  • Facturas totales: {Factura.objects.count()}")
    print(f"  • Gastos totales: {Gasto.objects.count()}")
    print(f"  • Pagos registrados: {Pago.objects.count()}")
    print(f"  • Anticipos: {Anticipo.objects.count()}")
    print(f"  • Presupuestos: {Presupuesto.objects.count()}")
    print(f"  • Archivos: {ArchivoProyecto.objects.count()}")
    print(f"  • Notificaciones: {NotificacionSistema.objects.count()}")
    print(f"  • Logs de actividad: {LogActividad.objects.count()}")
    
    print(f"\n🔑 Credenciales de acceso:")
    print(f"  • Usuario: admin")
    print(f"  • Contraseña: admin123")
    
    print(f"\n🌐 Accede a: http://127.0.0.1:8000/")
    print(f"\n💡 Ahora puedes probar todas las funcionalidades del sistema con datos realistas!")

except Exception as e:
    print(f"❌ Error creando datos: {e}")
    import traceback
    traceback.print_exc()
