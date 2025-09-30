#!/usr/bin/env python3
"""
Script para probar la funcionalidad de colores e iconos en categorías de gastos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import CategoriaGasto, Gasto, Proyecto, Cliente
from django.db.models import Sum, Count

def probar_creacion_categoria_con_color_icono():
    """Probar la creación de categorías con color e icono"""
    print("🎨 PROBANDO CREACIÓN DE CATEGORÍAS CON COLOR E ICONO")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # Datos de prueba para categorías
    categorias_prueba = [
        {
            'nombre': 'Materiales de Construcción',
            'descripcion': 'Cemento, ladrillos, arena, etc.',
            'color': '#dc3545',
            'icono': 'fas fa-hammer'
        },
        {
            'nombre': 'Equipos y Maquinaria',
            'descripcion': 'Alquiler de equipos pesados',
            'color': '#007bff',
            'icono': 'fas fa-truck'
        },
        {
            'nombre': 'Mano de Obra',
            'descripcion': 'Salarios y pagos a trabajadores',
            'color': '#28a745',
            'icono': 'fas fa-users'
        },
        {
            'nombre': 'Seguridad Industrial',
            'descripcion': 'Equipos de protección personal',
            'color': '#ffc107',
            'icono': 'fas fa-hard-hat'
        },
        {
            'nombre': 'Servicios Públicos',
            'descripcion': 'Electricidad, agua, teléfono',
            'color': '#6f42c1',
            'icono': 'fas fa-bolt'
        }
    ]
    
    categorias_creadas = 0
    
    for cat_data in categorias_prueba:
        print(f"\n📝 Creando categoría: {cat_data['nombre']}")
        
        # Crear categoría via POST
        response = client.post('/categorias-gasto/crear/', {
            'nombre': cat_data['nombre'],
            'descripcion': cat_data['descripcion'],
            'color': cat_data['color'],
            'icono': cat_data['icono']
        })
        
        if response.status_code == 302:
            print(f"  ✅ Categoría creada exitosamente")
            categorias_creadas += 1
        else:
            print(f"  ❌ Error creando categoría: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"  📄 Respuesta: {response.content.decode()[:200]}...")
    
    print(f"\n📊 RESUMEN DE CREACIÓN:")
    print(f"  ✅ Categorías creadas: {categorias_creadas}")
    print(f"  ✅ Total categorías en BD: {CategoriaGasto.objects.count()}")
    
    return categorias_creadas > 0

def verificar_categorias_en_dashboard():
    """Verificar que las categorías se muestren correctamente en el dashboard"""
    print("\n📊 VERIFICANDO CATEGORÍAS EN DASHBOARD")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    
    try:
        # Acceder al dashboard
        response = client.get('/gastos/dashboard/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar que se muestren las categorías con color e icono
            if 'categoria-icon' in content and 'categoria-header' in content:
                print("  ✅ Estructura de categorías con iconos presente")
            else:
                print("  ❌ Estructura de categorías con iconos faltante")
                return False
            
            # Verificar que haya categorías en la BD
            categorias_con_datos = CategoriaGasto.objects.annotate(
                total_gastos=Count('gasto')
            ).filter(total_gastos__gt=0)
            
            if categorias_con_datos.exists():
                print(f"  ✅ {categorias_con_datos.count()} categorías con gastos encontradas")
                
                # Verificar colores e iconos
                for categoria in categorias_con_datos:
                    print(f"    📋 {categoria.nombre}:")
                    print(f"      🎨 Color: {categoria.color}")
                    print(f"      🔧 Icono: {categoria.icono}")
            else:
                print("  ⚠️  No hay categorías con gastos")
            
            return True
        else:
            print(f"  ❌ Error accediendo al dashboard: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def probar_edicion_categoria():
    """Probar la edición de categorías con color e icono"""
    print("\n✏️ PROBANDO EDICIÓN DE CATEGORÍAS")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    
    # Obtener una categoría existente
    categoria = CategoriaGasto.objects.first()
    if not categoria:
        print("  ❌ No hay categorías para editar")
        return False
    
    print(f"  📝 Editando categoría: {categoria.nombre}")
    
    # Datos de edición
    nuevos_datos = {
        'nombre': f"{categoria.nombre} (Editada)",
        'descripcion': f"Descripción editada para {categoria.nombre}",
        'color': '#e83e8c',
        'icono': 'fas fa-paint-brush'
    }
    
    # Editar categoría
    response = client.post(f'/categorias-gasto/{categoria.id}/editar/', nuevos_datos)
    
    if response.status_code == 302:
        print("  ✅ Categoría editada exitosamente")
        
        # Verificar cambios en la BD
        categoria.refresh_from_db()
        if categoria.nombre == nuevos_datos['nombre'] and categoria.color == nuevos_datos['color']:
            print("  ✅ Cambios guardados correctamente en la BD")
            return True
        else:
            print("  ❌ Los cambios no se guardaron correctamente")
            return False
    else:
        print(f"  ❌ Error editando categoría: {response.status_code}")
        return False

def mostrar_categorias_existentes():
    """Mostrar todas las categorías existentes con sus colores e iconos"""
    print("\n📋 CATEGORÍAS EXISTENTES EN LA BASE DE DATOS")
    print("=" * 60)
    
    categorias = CategoriaGasto.objects.all()
    
    if not categorias.exists():
        print("  ❌ No hay categorías en la base de datos")
        return
    
    for i, categoria in enumerate(categorias, 1):
        print(f"  {i}. {categoria.nombre}")
        print(f"     🎨 Color: {categoria.color}")
        print(f"     🔧 Icono: {categoria.icono}")
        print(f"     📝 Descripción: {categoria.descripcion}")
        print(f"     📅 Creada: {categoria.creado_en.strftime('%d/%m/%Y %H:%M')}")
        print()

def main():
    """Función principal"""
    print("🎨 PRUEBA DE COLORES E ICONOS EN CATEGORÍAS DE GASTOS")
    print("=" * 70)
    
    try:
        # Mostrar categorías existentes
        mostrar_categorias_existentes()
        
        # Probar creación de categorías
        creacion_ok = probar_creacion_categoria_con_color_icono()
        
        # Verificar en dashboard
        dashboard_ok = verificar_categorias_en_dashboard()
        
        # Probar edición
        edicion_ok = probar_edicion_categoria()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if creacion_ok and dashboard_ok and edicion_ok:
            print("🎉 ¡FUNCIONALIDAD DE COLORES E ICONOS FUNCIONANDO PERFECTAMENTE!")
            print("✅ Creación de categorías con color e icono: OK")
            print("✅ Visualización en dashboard: OK")
            print("✅ Edición de categorías: OK")
            print("✅ Persistencia en base de datos: OK")
            
            print(f"\n🌐 PARA PROBAR:")
            print("  1. Ve a: http://localhost:8000/categorias-gasto/crear/")
            print("  2. Crea una categoría con color e icono personalizados")
            print("  3. Ve al dashboard: http://localhost:8000/gastos/dashboard/")
            print("  4. Observa las categorías con sus colores e iconos")
        else:
            print("❌ HAY PROBLEMAS CON LA FUNCIONALIDAD")
            if not creacion_ok:
                print("  - Problemas con creación de categorías")
            if not dashboard_ok:
                print("  - Problemas con visualización en dashboard")
            if not edicion_ok:
                print("  - Problemas con edición de categorías")
        
        return creacion_ok and dashboard_ok and edicion_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
