#!/usr/bin/env python3
"""
Script para crear datos de prueba para el dashboard de gastos
"""

import os
import sys
import django
from datetime import datetime, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.models import Sum
from core.models import Gasto, CategoriaGasto, Proyecto, Cliente

def crear_datos_gastos():
    """Crear datos de prueba para gastos"""
    print("📊 CREANDO DATOS DE PRUEBA PARA GASTOS")
    print("=" * 50)
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Crear categorías de gastos si no existen
    categorias_data = [
        {'nombre': 'Mano de Obra', 'descripcion': 'Gastos relacionados con personal'},
        {'nombre': 'Equipos y Maquinaria', 'descripcion': 'Alquiler y mantenimiento de equipos'},
        {'nombre': 'Seguridad Industrial', 'descripcion': 'Equipos y medidas de seguridad'},
        {'nombre': 'Servicios Públicos', 'descripcion': 'Electricidad, agua, teléfono'},
        {'nombre': 'Mantenimiento', 'descripcion': 'Mantenimiento de instalaciones'},
        {'nombre': 'Permisos y Licencias', 'descripcion': 'Permisos municipales y licencias'},
        {'nombre': 'Materiales de Construcción', 'descripcion': 'Cemento, ladrillos, etc.'},
        {'nombre': 'Transporte y Logística', 'descripcion': 'Transporte de materiales'},
        {'nombre': 'Consultoría Técnica', 'descripcion': 'Servicios de consultoría'},
        {'nombre': 'Administrativos', 'descripcion': 'Gastos administrativos generales'},
    ]
    
    categorias = []
    for cat_data in categorias_data:
        categoria, created = CategoriaGasto.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion']}
        )
        categorias.append(categoria)
        if created:
            print(f"  ✅ Categoría creada: {categoria.nombre}")
        else:
            print(f"  ℹ️  Categoría existente: {categoria.nombre}")
    
    # Crear cliente si no existe
    cliente, created = Cliente.objects.get_or_create(
        razon_social="Cliente de Prueba",
        defaults={
            'codigo_fiscal': '12345678-9',
            'telefono': '5555-5555',
            'email': 'cliente@prueba.com',
            'direccion': 'Dirección de prueba'
        }
    )
    if created:
        print(f"  ✅ Clyecto creado: {cliente.razon_social}")
    else:
        print(f"  ℹ️  Cliente existente: {cliente.razon_social}")
    
    # Crear proyecto si no existe
    proyecto, created = Proyecto.objects.get_or_create(
        nombre="Proyecto de Prueba",
        defaults={
            'cliente': cliente,
            'descripcion': 'Proyecto para pruebas del dashboard',
            'fecha_inicio': datetime.now().date(),
            'fecha_fin': (datetime.now() + timedelta(days=365)).date(),
            'presupuesto': 1000000.00,
            'activo': True
        }
    )
    if created:
        print(f"  ✅ Proyecto creado: {proyecto.nombre}")
    else:
        print(f"  ℹ️  Proyecto existente: {proyecto.nombre}")
    
    # Crear gastos de prueba
    gastos_data = [
        # Mano de Obra
        {'descripcion': 'Pago de albañiles - Semana 1', 'monto': 15000.00, 'categoria': 'Mano de Obra', 'aprobado': True},
        {'descripcion': 'Pago de albañiles - Semana 2', 'monto': 18000.00, 'categoria': 'Mano de Obra', 'aprobado': True},
        {'descripcion': 'Pago de albañiles - Semana 3', 'monto': 16500.00, 'categoria': 'Mano de Obra', 'aprobado': True},
        {'descripcion': 'Pago de albañiles - Semana 4', 'monto': 17200.00, 'categoria': 'Mano de Obra', 'aprobado': False},
        {'descripcion': 'Pago de albañiles - Semana 5', 'monto': 15800.00, 'categoria': 'Mano de Obra', 'aprobado': False},
        
        # Equipos y Maquinaria
        {'descripcion': 'Alquiler de excavadora', 'monto': 25000.00, 'categoria': 'Equipos y Maquinaria', 'aprobado': True},
        {'descripcion': 'Alquiler de grúa', 'monto': 18000.00, 'categoria': 'Equipos y Maquinaria', 'aprobado': True},
        {'descripcion': 'Alquiler de compactadora', 'monto': 8500.00, 'categoria': 'Equipos y Maquinaria', 'aprobado': True},
        {'descripcion': 'Alquiler de mezcladora', 'monto': 12000.00, 'categoria': 'Equipos y Maquinaria', 'aprobado': True},
        {'descripcion': 'Alquiler de andamios', 'monto': 15000.00, 'categoria': 'Equipos y Maquinaria', 'aprobado': True},
        {'descripcion': 'Alquiler de martillo neumático', 'monto': 8000.00, 'categoria': 'Equipos y Maquinaria', 'aprobado': False},
        {'descripcion': 'Alquiler de soldadora', 'monto': 9500.00, 'categoria': 'Equipos y Maquinaria', 'aprobado': False},
        
        # Seguridad Industrial
        {'descripcion': 'Cascos de seguridad', 'monto': 2500.00, 'categoria': 'Seguridad Industrial', 'aprobado': True},
        {'descripcion': 'Chalecos reflectivos', 'monto': 1800.00, 'categoria': 'Seguridad Industrial', 'aprobado': True},
        {'descripcion': 'Botas de seguridad', 'monto': 3200.00, 'categoria': 'Seguridad Industrial', 'aprobado': True},
        {'descripcion': 'Guantes de protección', 'monto': 1200.00, 'categoria': 'Seguridad Industrial', 'aprobado': True},
        {'descripcion': 'Señalización de obra', 'monto': 1500.00, 'categoria': 'Seguridad Industrial', 'aprobado': False},
        
        # Servicios Públicos
        {'descripcion': 'Factura de electricidad', 'monto': 8500.00, 'categoria': 'Servicios Públicos', 'aprobado': True},
        {'descripcion': 'Factura de agua', 'monto': 3200.00, 'categoria': 'Servicios Públicos', 'aprobado': True},
        {'descripcion': 'Factura de teléfono', 'monto': 1500.00, 'categoria': 'Servicios Públicos', 'aprobado': True},
        {'descripcion': 'Factura de internet', 'monto': 800.00, 'categoria': 'Servicios Públicos', 'aprobado': True},
        {'descripcion': 'Factura de gas', 'monto': 2200.00, 'categoria': 'Servicios Públicos', 'aprobado': False},
        
        # Mantenimiento
        {'descripcion': 'Mantenimiento de equipos', 'monto': 12000.00, 'categoria': 'Mantenimiento', 'aprobado': True},
        {'descripcion': 'Reparación de herramientas', 'monto': 3500.00, 'categoria': 'Mantenimiento', 'aprobado': True},
        {'descripcion': 'Limpieza de obra', 'monto': 2500.00, 'categoria': 'Mantenimiento', 'aprobado': False},
        
        # Permisos y Licencias
        {'descripcion': 'Permiso municipal', 'monto': 5000.00, 'categoria': 'Permisos y Licencias', 'aprobado': True},
        {'descripcion': 'Licencia ambiental', 'monto': 3500.00, 'categoria': 'Permisos y Licencias', 'aprobado': True},
        {'descripcion': 'Permiso de construcción', 'monto': 8000.00, 'categoria': 'Permisos y Licencias', 'aprobado': False},
        
        # Materiales de Construcción
        {'descripcion': 'Cemento', 'monto': 15000.00, 'categoria': 'Materiales de Construcción', 'aprobado': True},
        {'descripcion': 'Ladrillos', 'monto': 12000.00, 'categoria': 'Materiales de Construcción', 'aprobado': True},
        
        # Transporte y Logística
        {'descripcion': 'Transporte de materiales', 'monto': 8000.00, 'categoria': 'Transporte y Logística', 'aprobado': True},
        
        # Consultoría Técnica
        {'descripcion': 'Consultoría estructural', 'monto': 15000.00, 'categoria': 'Consultoría Técnica', 'aprobado': True},
        
        # Administrativos
        {'descripcion': 'Papelería y oficina', 'monto': 2500.00, 'categoria': 'Administrativos', 'aprobado': True},
    ]
    
    gastos_creados = 0
    for gasto_data in gastos_data:
        # Buscar la categoría
        categoria = next((c for c in categorias if c.nombre == gasto_data['categoria']), None)
        if not categoria:
            print(f"  ❌ Categoría no encontrada: {gasto_data['categoria']}")
            continue
        
        # Crear gasto
        gasto, created = Gasto.objects.get_or_create(
            descripcion=gasto_data['descripcion'],
            defaults={
                'monto': gasto_data['monto'],
                'categoria': categoria,
                'proyecto': proyecto,
                'fecha_gasto': datetime.now().date() - timedelta(days=random.randint(1, 30)),
                'aprobado': gasto_data['aprobado'],
                'aprobado_por': admin_user if gasto_data['aprobado'] else None
            }
        )
        
        if created:
            gastos_creados += 1
            print(f"  ✅ Gasto creado: {gasto.descripcion} - Q{gasto.monto:,.2f}")
        else:
            print(f"  ℹ️  Gasto existente: {gasto.descripcion}")
    
    print(f"\n📊 RESUMEN:")
    print(f"  ✅ Gastos creados: {gastos_creados}")
    print(f"  ✅ Total gastos en BD: {Gasto.objects.count()}")
    print(f"  ✅ Total monto: Q{Gasto.objects.aggregate(total=Sum('monto'))['total'] or 0:,.2f}")
    print(f"  ✅ Gastos aprobados: {Gasto.objects.filter(aprobado=True).count()}")
    print(f"  ✅ Gastos pendientes: {Gasto.objects.filter(aprobado=False).count()}")
    
    return True

def main():
    """Función principal"""
    print("📊 CREACIÓN DE DATOS DE PRUEBA PARA GASTOS")
    print("=" * 60)
    
    try:
        success = crear_datos_gastos()
        
        if success:
            print(f"\n🎉 ¡DATOS DE PRUEBA CREADOS EXITOSAMENTE!")
            print("✅ Categorías de gastos creadas")
            print("✅ Gastos de prueba creados")
            print("✅ Dashboard ahora mostrará datos reales")
            
            print(f"\n🌐 PARA VER LOS DATOS:")
            print("  1. Ve a: http://localhost:8000/gastos/dashboard/")
            print("  2. Observa las estadísticas actualizadas")
            print("  3. Revisa las categorías con datos")
            print("  4. Verifica los montos y cantidades")
        else:
            print("❌ ERROR CREANDO DATOS DE PRUEBA")
        
        return success
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
