#!/usr/bin/env python3
"""
Script para actualizar las categorías existentes con colores e iconos únicos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import CategoriaGasto

def actualizar_categorias():
    """Actualizar categorías con colores e iconos únicos"""
    print("🎨 ACTUALIZANDO CATEGORÍAS CON COLORES E ICONOS ÚNICOS")
    print("=" * 60)
    
    # Configuración de colores e iconos para cada categoría
    configuraciones = {
        'Mano de Obra': {'color': '#28a745', 'icono': 'fas fa-users'},
        'Equipos y Maquinaria': {'color': '#007bff', 'icono': 'fas fa-truck'},
        'Seguridad Industrial': {'color': '#ffc107', 'icono': 'fas fa-hard-hat'},
        'Servicios Públicos': {'color': '#6f42c1', 'icono': 'fas fa-bolt'},
        'Mantenimiento': {'color': '#fd7e14', 'icono': 'fas fa-wrench'},
        'Permisos y Licencias': {'color': '#17a2b8', 'icono': 'fas fa-file-alt'},
        'Materiales de Construcción': {'color': '#dc3545', 'icono': 'fas fa-hammer'},
        'Transporte y Logística': {'color': '#20c997', 'icono': 'fas fa-shipping-fast'},
        'Consultoría Técnica': {'color': '#6c757d', 'icono': 'fas fa-calculator'},
        'Administrativos': {'color': '#e83e8c', 'icono': 'fas fa-clipboard'},
        'gastos': {'color': '#343a40', 'icono': 'fas fa-receipt'},
        'Prueba Color Icono': {'color': '#e83e8c', 'icono': 'fas fa-paint-brush'}
    }
    
    categorias_actualizadas = 0
    
    for nombre, config in configuraciones.items():
        try:
            categoria = CategoriaGasto.objects.get(nombre=nombre)
            categoria.color = config['color']
            categoria.icono = config['icono']
            categoria.save()
            
            print(f"✅ {nombre}: {config['color']} - {config['icono']}")
            categorias_actualizadas += 1
            
        except CategoriaGasto.DoesNotExist:
            print(f"⚠️  Categoría '{nombre}' no encontrada")
        except Exception as e:
            print(f"❌ Error actualizando '{nombre}': {e}")
    
    print(f"\n📊 RESUMEN:")
    print(f"  ✅ Categorías actualizadas: {categorias_actualizadas}")
    print(f"  ✅ Total categorías en BD: {CategoriaGasto.objects.count()}")
    
    return categorias_actualizadas > 0

def mostrar_categorias_actualizadas():
    """Mostrar todas las categorías con sus nuevos colores e iconos"""
    print("\n🎨 CATEGORÍAS ACTUALIZADAS")
    print("=" * 60)
    
    categorias = CategoriaGasto.objects.all().order_by('nombre')
    
    for i, cat in enumerate(categorias, 1):
        print(f"{i:2d}. {cat.nombre}")
        print(f"     🎨 Color: {cat.color}")
        print(f"     🔧 Icono: {cat.icono}")
        print(f"     📝 Descripción: {cat.descripcion}")
        print()

def main():
    """Función principal"""
    print("🎨 ACTUALIZACIÓN DE COLORES E ICONOS EN CATEGORÍAS")
    print("=" * 70)
    
    # Actualizar categorías
    success = actualizar_categorias()
    
    if success:
        # Mostrar resultado
        mostrar_categorias_actualizadas()
        
        print("\n🎉 ¡CATEGORÍAS ACTUALIZADAS EXITOSAMENTE!")
        print("✅ Todas las categorías ahora tienen colores e iconos únicos")
        print("✅ El dashboard mostrará las categorías con sus colores e iconos")
        
        print(f"\n🌐 PARA VER LOS CAMBIOS:")
        print("  1. Ve a: http://localhost:8000/gastos/dashboard/")
        print("  2. Observa las categorías con sus colores e iconos únicos")
        print("  3. Ve a: http://localhost:8000/categorias-gasto/")
        print("  4. Edita cualquier categoría para cambiar color e icono")
    else:
        print("\n❌ ERROR ACTUALIZANDO CATEGORÍAS")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
