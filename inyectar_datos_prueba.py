#!/usr/bin/env python3
"""
Script para inyectar datos de prueba al sistema ARCA Construcción
Incluye: 7 clientes, 10 proyectos, 10 colaboradores y 5 anticipos
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import (
    Cliente, Proyecto, Colaborador, Factura, Pago, Gasto, CategoriaGasto,
    Anticipo, AplicacionAnticipo, ArchivoProyecto, Presupuesto, PartidaPresupuesto,
    ItemInventario, CategoriaInventario, AsignacionInventario,
    Rol, PerfilUsuario, Modulo, Permiso, RolPermiso, AnticipoProyecto,
    CarpetaProyecto, ConfiguracionSistema, EventoCalendario,
    TrabajadorDiario, RegistroTrabajo, AnticipoTrabajadorDiario
)

def crear_clientes():
    """Crear 7 clientes de prueba"""
    print("🏢 Creando clientes...")
    
    clientes_data = [
        {
            'razon_social': 'Constructora Maya S.A.',
            'codigo_fiscal': '12345678-9',
            'direccion': 'Zona 10, Ciudad de Guatemala',
            'telefono': '+502 2234-5678',
            'email': 'contacto@constructora-maya.com',
            'activo': True
        },
        {
            'razon_social': 'Inmobiliaria del Valle',
            'codigo_fiscal': '87654321-0',
            'direccion': 'Zona 15, Ciudad de Guatemala',
            'telefono': '+502 2234-5679',
            'email': 'ventas@inmobiliaria-valle.com',
            'activo': True
        },
        {
            'razon_social': 'Desarrollos Urbanos S.A.',
            'codigo_fiscal': '11223344-5',
            'direccion': 'Zona 4, Ciudad de Guatemala',
            'telefono': '+502 2234-5680',
            'email': 'info@desarrollos-urbanos.com',
            'activo': True
        },
        {
            'razon_social': 'Constructora del Pacífico',
            'codigo_fiscal': '55667788-9',
            'direccion': 'Escuintla, Guatemala',
            'telefono': '+502 2234-5681',
            'email': 'construccion@pacifico.com',
            'activo': True
        },
        {
            'razon_social': 'Inversiones Inmobiliarias GT',
            'codigo_fiscal': '99887766-5',
            'direccion': 'Zona 9, Ciudad de Guatemala',
            'telefono': '+502 2234-5682',
            'email': 'inversiones@gt.com',
            'activo': True
        },
        {
            'razon_social': 'Constructora del Norte',
            'codigo_fiscal': '44332211-0',
            'direccion': 'Quetzaltenango, Guatemala',
            'telefono': '+502 2234-5683',
            'email': 'norte@constructora.com',
            'activo': True
        },
        {
            'razon_social': 'Desarrollos Residenciales',
            'codigo_fiscal': '77889900-1',
            'direccion': 'Zona 16, Ciudad de Guatemala',
            'telefono': '+502 2234-5684',
            'email': 'residencial@desarrollos.com',
            'activo': True
        }
    ]
    
    clientes_creados = []
    for cliente_data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            codigo_fiscal=cliente_data['codigo_fiscal'],
            defaults=cliente_data
        )
        clientes_creados.append(cliente)  # Agregar tanto los creados como los existentes
        if created:
            print(f"  ✅ Cliente creado: {cliente.razon_social}")
        else:
            print(f"  ⚠️  Cliente ya existe: {cliente.razon_social}")
    
    return clientes_creados

def crear_proyectos(clientes):
    """Crear 10 proyectos de prueba"""
    print("\n🏗️ Creando proyectos...")
    
    proyectos_data = [
        {
            'nombre': 'Torre Residencial Vista Hermosa',
            'descripcion': 'Edificio residencial de 15 pisos con 120 apartamentos',
            'cliente': clientes[0],
            'fecha_inicio': datetime.now() - timedelta(days=180),
            'fecha_fin': datetime.now() + timedelta(days=90),
            'presupuesto': Decimal('2500000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Centro Comercial Plaza Central',
            'descripcion': 'Centro comercial de 3 niveles con 50 locales comerciales',
            'cliente': clientes[1],
            'fecha_inicio': datetime.now() - timedelta(days=120),
            'fecha_fin': datetime.now() + timedelta(days=60),
            'presupuesto': Decimal('1800000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Conjunto Habitacional Los Pinos',
            'descripcion': 'Conjunto de 80 casas unifamiliares',
            'cliente': clientes[2],
            'fecha_inicio': datetime.now() - timedelta(days=90),
            'fecha_fin': datetime.now() + timedelta(days=120),
            'presupuesto': Decimal('3200000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Oficinas Corporativas Zona 10',
            'descripcion': 'Edificio de oficinas de 8 pisos',
            'cliente': clientes[3],
            'fecha_inicio': datetime.now() - timedelta(days=60),
            'fecha_fin': datetime.now() + timedelta(days=180),
            'presupuesto': Decimal('1500000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Residencial Las Flores',
            'descripcion': 'Conjunto residencial de 60 apartamentos',
            'cliente': clientes[4],
            'fecha_inicio': datetime.now() - timedelta(days=30),
            'fecha_fin': datetime.now() + timedelta(days=210),
            'presupuesto': Decimal('2800000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Centro de Convenciones',
            'descripcion': 'Centro de convenciones con capacidad para 500 personas',
            'cliente': clientes[5],
            'fecha_inicio': datetime.now() - timedelta(days=15),
            'fecha_fin': datetime.now() + timedelta(days=300),
            'presupuesto': Decimal('4200000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Torre Mixta Comercial-Residencial',
            'descripcion': 'Edificio de 20 pisos con locales comerciales y apartamentos',
            'cliente': clientes[6],
            'fecha_inicio': datetime.now() - timedelta(days=45),
            'fecha_fin': datetime.now() + timedelta(days=240),
            'presupuesto': Decimal('3500000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Conjunto Habitacional El Roble',
            'descripcion': 'Conjunto de 100 casas unifamiliares',
            'cliente': clientes[0],
            'fecha_inicio': datetime.now() - timedelta(days=200),
            'fecha_fin': datetime.now() + timedelta(days=30),
            'presupuesto': Decimal('4000000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Edificio de Oficinas Zona 4',
            'descripcion': 'Edificio de oficinas de 12 pisos',
            'cliente': clientes[1],
            'fecha_inicio': datetime.now() - timedelta(days=100),
            'fecha_fin': datetime.now() + timedelta(days=150),
            'presupuesto': Decimal('2200000.00'),
            'estado': 'en_progreso',
            'activo': True
        },
        {
            'nombre': 'Residencial Los Laureles',
            'descripcion': 'Conjunto residencial de 90 apartamentos',
            'cliente': clientes[2],
            'fecha_inicio': datetime.now() - timedelta(days=75),
            'fecha_fin': datetime.now() + timedelta(days=165),
            'presupuesto': Decimal('3100000.00'),
            'estado': 'en_progreso',
            'activo': True
        }
    ]
    
    proyectos_creados = []
    for proyecto_data in proyectos_data:
        proyecto, created = Proyecto.objects.get_or_create(
            nombre=proyecto_data['nombre'],
            defaults=proyecto_data
        )
        proyectos_creados.append(proyecto)  # Agregar tanto los creados como los existentes
        if created:
            print(f"  ✅ Proyecto creado: {proyecto.nombre}")
        else:
            print(f"  ⚠️  Proyecto ya existe: {proyecto.nombre}")
    
    return proyectos_creados

def crear_colaboradores(proyectos):
    """Crear 10 colaboradores de prueba"""
    print("\n👷 Creando colaboradores...")
    
    colaboradores_data = [
        {
            'nombre': 'Juan Carlos Pérez',
            'dpi': '1234567890101',
            'direccion': 'Zona 10, Ciudad de Guatemala',
            'telefono': '+502 1234-5678',
            'email': 'juan.perez@arca.com',
            'salario': Decimal('8000.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=365)).date(),
            'activo': True
        },
        {
            'nombre': 'María Elena Rodríguez',
            'dpi': '1234567890102',
            'direccion': 'Zona 15, Ciudad de Guatemala',
            'telefono': '+502 1234-5679',
            'email': 'maria.rodriguez@arca.com',
            'salario': Decimal('7500.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=300)).date(),
            'activo': True
        },
        {
            'nombre': 'Carlos Alberto López',
            'dpi': '1234567890103',
            'direccion': 'Zona 4, Ciudad de Guatemala',
            'telefono': '+502 1234-5680',
            'email': 'carlos.lopez@arca.com',
            'salario': Decimal('6000.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=250)).date(),
            'activo': True
        },
        {
            'nombre': 'Ana Patricia Martínez',
            'dpi': '1234567890104',
            'direccion': 'Zona 9, Ciudad de Guatemala',
            'telefono': '+502 1234-5681',
            'email': 'ana.martinez@arca.com',
            'salario': Decimal('7000.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=200)).date(),
            'activo': True
        },
        {
            'nombre': 'Roberto José González',
            'dpi': '1234567890105',
            'direccion': 'Zona 11, Ciudad de Guatemala',
            'telefono': '+502 1234-5682',
            'email': 'roberto.gonzalez@arca.com',
            'salario': Decimal('5500.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=180)).date(),
            'activo': True
        },
        {
            'nombre': 'Carmen Leticia Herrera',
            'dpi': '1234567890106',
            'direccion': 'Zona 12, Ciudad de Guatemala',
            'telefono': '+502 1234-5683',
            'email': 'carmen.herrera@arca.com',
            'salario': Decimal('5000.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=150)).date(),
            'activo': True
        },
        {
            'nombre': 'Diego Alejandro Morales',
            'dpi': '1234567890107',
            'direccion': 'Zona 13, Ciudad de Guatemala',
            'telefono': '+502 1234-5684',
            'email': 'diego.morales@arca.com',
            'salario': Decimal('6500.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=120)).date(),
            'activo': True
        },
        {
            'nombre': 'Luis Fernando Ramírez',
            'dpi': '1234567890108',
            'direccion': 'Zona 14, Ciudad de Guatemala',
            'telefono': '+502 1234-5685',
            'email': 'luis.ramirez@arca.com',
            'salario': Decimal('5800.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=100)).date(),
            'activo': True
        },
        {
            'nombre': 'Patricia Alejandra Vásquez',
            'dpi': '1234567890109',
            'direccion': 'Zona 16, Ciudad de Guatemala',
            'telefono': '+502 1234-5686',
            'email': 'patricia.vasquez@arca.com',
            'salario': Decimal('5200.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=80)).date(),
            'activo': True
        },
        {
            'nombre': 'Miguel Ángel Castillo',
            'dpi': '1234567890110',
            'direccion': 'Zona 17, Ciudad de Guatemala',
            'telefono': '+502 1234-5687',
            'email': 'miguel.castillo@arca.com',
            'salario': Decimal('7200.00'),
            'fecha_contratacion': (datetime.now() - timedelta(days=60)).date(),
            'activo': True
        }
    ]
    
    colaboradores_creados = []
    for colaborador_data in colaboradores_data:
        colaborador, created = Colaborador.objects.get_or_create(
            email=colaborador_data['email'],
            defaults=colaborador_data
        )
        colaboradores_creados.append(colaborador)  # Agregar tanto los creados como los existentes
        if created:
            print(f"  ✅ Colaborador creado: {colaborador.nombre}")
        else:
            print(f"  ⚠️  Colaborador ya existe: {colaborador.nombre}")
    
    return colaboradores_creados

def crear_anticipos(clientes, proyectos):
    """Crear 5 anticipos de prueba"""
    print("\n💰 Creando anticipos...")
    
    anticipos_data = [
        {
            'cliente': clientes[0],
            'proyecto': proyectos[0],
            'monto': Decimal('500000.00'),
            'tipo': 'inicial',
            'estado': 'recibido',
            'fecha_recepcion': datetime.now() - timedelta(days=30),
            'observaciones': 'Anticipo inicial para Torre Residencial Vista Hermosa'
        },
        {
            'cliente': clientes[1],
            'proyecto': proyectos[1],
            'monto': Decimal('300000.00'),
            'tipo': 'inicial',
            'estado': 'recibido',
            'fecha_recepcion': datetime.now() - timedelta(days=25),
            'observaciones': 'Anticipo inicial para Centro Comercial Plaza Central'
        },
        {
            'cliente': clientes[2],
            'proyecto': proyectos[2],
            'monto': Decimal('800000.00'),
            'tipo': 'inicial',
            'estado': 'recibido',
            'fecha_recepcion': datetime.now() - timedelta(days=20),
            'observaciones': 'Anticipo inicial para Conjunto Habitacional Los Pinos'
        },
        {
            'cliente': clientes[3],
            'proyecto': proyectos[3],
            'monto': Decimal('250000.00'),
            'tipo': 'inicial',
            'estado': 'recibido',
            'fecha_recepcion': datetime.now() - timedelta(days=15),
            'observaciones': 'Anticipo inicial para Oficinas Corporativas Zona 10'
        },
        {
            'cliente': clientes[4],
            'proyecto': proyectos[4],
            'monto': Decimal('600000.00'),
            'tipo': 'inicial',
            'estado': 'recibido',
            'fecha_recepcion': datetime.now() - timedelta(days=10),
            'observaciones': 'Anticipo inicial para Residencial Las Flores'
        }
    ]
    
    anticipos_creados = []
    for anticipo_data in anticipos_data:
        anticipo, created = Anticipo.objects.get_or_create(
            cliente=anticipo_data['cliente'],
            proyecto=anticipo_data['proyecto'],
            defaults=anticipo_data
        )
        anticipos_creados.append(anticipo)  # Agregar tanto los creados como los existentes
        if created:
            print(f"  ✅ Anticipo creado: {anticipo.cliente.razon_social} - {anticipo.proyecto.nombre}")
        else:
            print(f"  ⚠️  Anticipo ya existe: {anticipo.cliente.razon_social} - {anticipo.proyecto.nombre}")
    
    return anticipos_creados

def asignar_colaboradores_a_proyectos(proyectos, colaboradores):
    """Asignar colaboradores a proyectos"""
    print("\n🔗 Asignando colaboradores a proyectos...")
    
    # Asignar colaboradores aleatoriamente a proyectos
    for proyecto in proyectos:
        # Seleccionar 2-4 colaboradores aleatoriamente para cada proyecto
        num_colaboradores = random.randint(2, 4)
        colaboradores_asignados = random.sample(colaboradores, min(num_colaboradores, len(colaboradores)))
        
        for colaborador in colaboradores_asignados:
            # Verificar si ya está asignado
            if not proyecto.colaboradores.filter(id=colaborador.id).exists():
                proyecto.colaboradores.add(colaborador)
                print(f"  ✅ {colaborador.nombre} asignado a {proyecto.nombre}")

def crear_categorias_gastos():
    """Crear categorías de gastos básicas"""
    print("\n📋 Creando categorías de gastos...")
    
    categorias_data = [
        {'nombre': 'Materiales de Construcción', 'descripcion': 'Cemento, ladrillos, varillas, etc.'},
        {'nombre': 'Mano de Obra', 'descripcion': 'Salarios de trabajadores'},
        {'nombre': 'Equipos y Herramientas', 'descripcion': 'Alquiler de maquinaria'},
        {'nombre': 'Transporte', 'descripcion': 'Fletes y transporte de materiales'},
        {'nombre': 'Servicios Básicos', 'descripcion': 'Agua, luz, teléfono'},
        {'nombre': 'Permisos y Licencias', 'descripcion': 'Permisos municipales y licencias'},
        {'nombre': 'Otros', 'descripcion': 'Gastos varios'}
    ]
    
    for categoria_data in categorias_data:
        categoria, created = CategoriaGasto.objects.get_or_create(
            nombre=categoria_data['nombre'],
            defaults=categoria_data
        )
        if created:
            print(f"  ✅ Categoría creada: {categoria.nombre}")

def main():
    """Función principal"""
    print("🚀 INICIANDO INYECCIÓN DE DATOS DE PRUEBA")
    print("=" * 50)
    
    try:
        # Crear categorías de gastos
        crear_categorias_gastos()
        
        # Crear clientes
        clientes = crear_clientes()
        
        # Crear proyectos
        proyectos = crear_proyectos(clientes)
        
        # Crear colaboradores
        colaboradores = crear_colaboradores(proyectos)
        
        # Crear anticipos
        anticipos = crear_anticipos(clientes, proyectos)
        
        # Asignar colaboradores a proyectos
        asignar_colaboradores_a_proyectos(proyectos, colaboradores)
        
        print("\n" + "=" * 50)
        print("✅ INYECCIÓN DE DATOS COMPLETADA EXITOSAMENTE")
        print("=" * 50)
        print(f"📊 RESUMEN:")
        print(f"  🏢 Clientes: {len(clientes)}")
        print(f"  🏗️ Proyectos: {len(proyectos)}")
        print(f"  👷 Colaboradores: {len(colaboradores)}")
        print(f"  💰 Anticipos: {len(anticipos)}")
        print(f"  📋 Categorías de gastos: 7")
        print("\n🎉 El sistema ahora tiene datos de prueba para trabajar!")
        
    except Exception as e:
        print(f"\n❌ ERROR durante la inyección de datos: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
