#!/usr/bin/env python
"""
Script para crear datos básicos del sistema
Sistema ARCA Construcción
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Cliente, Proyecto, CategoriaGasto, Gasto
from decimal import Decimal

def crear_usuario_admin():
    """Crear usuario administrador si no existe"""
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@arca.com', 'admin123')
        print("✅ Usuario admin creado: admin/admin123")
    else:
        print("✅ Usuario admin ya existe")

def crear_categorias_gasto():
    """Crear categorías básicas de gastos"""
    categorias = [
        'Materiales',
        'Mano de Obra', 
        'Equipos',
        'Herramientas',
        'Transporte',
        'Administrativos',
        'Servicios',
        'Otros'
    ]
    
    for nombre in categorias:
        categoria, created = CategoriaGasto.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': f'Categoría para gastos de {nombre.lower()}'}
        )
        if created:
            print(f"✅ Categoría creada: {nombre}")
        else:
            print(f"✅ Categoría ya existe: {nombre}")

def crear_cliente_ejemplo():
    """Crear cliente de ejemplo"""
    cliente, created = Cliente.objects.get_or_create(
        razon_social='Cliente Ejemplo S.A.',
        defaults={
            'nombre_contacto': 'Juan Pérez',
            'email': 'juan@cliente.com',
            'telefono': '502-1234-5678',
            'direccion': 'Zona 1, Ciudad de Guatemala',
            'activo': True
        }
    )
    
    if created:
        print("✅ Cliente ejemplo creado")
    else:
        print("✅ Cliente ejemplo ya existe")
    
    return cliente

def crear_proyecto_ejemplo(cliente):
    """Crear proyecto de ejemplo"""
    proyecto, created = Proyecto.objects.get_or_create(
        nombre='Proyecto de Prueba',
        defaults={
            'cliente': cliente,
            'descripcion': 'Proyecto de prueba para el sistema',
            'presupuesto': Decimal('50000.00'),
            'fecha_inicio': '2025-01-01',
            'estado': 'en_progreso',
            'activo': True
        }
    )
    
    if created:
        print("✅ Proyecto ejemplo creado")
    else:
        print("✅ Proyecto ejemplo ya existe")
    
    return proyecto

def crear_gasto_ejemplo(proyecto):
    """Crear gasto de ejemplo"""
    categoria = CategoriaGasto.objects.first()
    
    if not categoria:
        print("❌ No hay categorías de gasto. Creando una...")
        categoria = CategoriaGasto.objects.create(
            nombre='Materiales',
            descripcion='Categoría para materiales'
        )
    
    gasto, created = Gasto.objects.get_or_create(
        descripcion='Compra de materiales de prueba',
        defaults={
            'proyecto': proyecto,
            'categoria': categoria,
            'monto': Decimal('1500.00'),
            'fecha_gasto': '2025-01-15',
            'aprobado': True
        }
    )
    
    if created:
        print("✅ Gasto ejemplo creado")
    else:
        print("✅ Gasto ejemplo ya existe")

def main():
    """Función principal"""
    print("🚀 Creando datos básicos del sistema...")
    print("=" * 50)
    
    try:
        # 1. Crear usuario admin
        crear_usuario_admin()
        print()
        
        # 2. Crear categorías de gasto
        crear_categorias_gasto()
        print()
        
        # 3. Crear cliente ejemplo
        cliente = crear_cliente_ejemplo()
        print()
        
        # 4. Crear proyecto ejemplo
        proyecto = crear_proyecto_ejemplo(cliente)
        print()
        
        # 5. Crear gasto ejemplo
        crear_gasto_ejemplo(proyecto)
        print()
        
        # 6. Mostrar resumen
        print("=" * 50)
        print("📊 RESUMEN DE DATOS CREADOS:")
        print(f"   • Usuarios: {User.objects.count()}")
        print(f"   • Clientes: {Cliente.objects.count()}")
        print(f"   • Proyectos: {Proyecto.objects.count()}")
        print(f"   • Categorías de gasto: {CategoriaGasto.objects.count()}")
        print(f"   • Gastos: {Gasto.objects.count()}")
        print("=" * 50)
        print("✅ ¡Datos básicos creados exitosamente!")
        print("🌐 Ahora puedes acceder al sistema y crear gastos")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
