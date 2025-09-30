#!/usr/bin/env python3
"""
Script simple para probar la creación de categorías
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import CategoriaGasto

def crear_categoria_directamente():
    """Crear categoría directamente en la BD"""
    print("🎨 CREANDO CATEGORÍA DIRECTAMENTE EN LA BD")
    print("=" * 50)
    
    try:
        # Crear categoría con color e icono personalizados
        categoria = CategoriaGasto.objects.create(
            nombre='Prueba Color Icono',
            descripcion='Categoría de prueba con color e icono personalizados',
            color='#e83e8c',
            icono='fas fa-paint-brush'
        )
        
        print(f"✅ Categoría creada exitosamente:")
        print(f"  📝 Nombre: {categoria.nombre}")
        print(f"  🎨 Color: {categoria.color}")
        print(f"  🔧 Icono: {categoria.icono}")
        print(f"  📅 Creada: {categoria.creado_en}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando categoría: {e}")
        return False

def mostrar_todas_categorias():
    """Mostrar todas las categorías"""
    print("\n📋 TODAS LAS CATEGORÍAS EN LA BD")
    print("=" * 50)
    
    categorias = CategoriaGasto.objects.all()
    
    for i, cat in enumerate(categorias, 1):
        print(f"{i}. {cat.nombre}")
        print(f"   🎨 Color: {cat.color}")
        print(f"   🔧 Icono: {cat.icono}")
        print(f"   📝 Descripción: {cat.descripcion}")
        print()

def main():
    """Función principal"""
    print("🎨 PRUEBA SIMPLE DE CATEGORÍAS")
    print("=" * 40)
    
    # Mostrar categorías existentes
    mostrar_todas_categorias()
    
    # Crear nueva categoría
    success = crear_categoria_directamente()
    
    if success:
        print("\n✅ ¡CATEGORÍA CREADA EXITOSAMENTE!")
        print("🎨 La funcionalidad de color e icono está funcionando")
    else:
        print("\n❌ ERROR CREANDO CATEGORÍA")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
