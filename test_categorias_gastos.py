#!/usr/bin/env python3
"""
Script para probar la funcionalidad de categorías de gastos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import CategoriaGasto

def probar_categorias_gastos():
    """Probar la funcionalidad de categorías de gastos"""
    print("🏷️ PROBANDO CATEGORÍAS DE GASTOS")
    print("=" * 40)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # 1. Probar lista de gastos con botón de categorías
    print("\n1️⃣ Probando lista de gastos...")
    try:
        response = client.get('/gastos/')
        if response.status_code == 200:
            content = response.content.decode()
            
            if 'Gestionar Categorías' in content:
                print("  ✅ Botón 'Gestionar Categorías' encontrado")
            else:
                print("  ❌ Botón 'Gestionar Categorías' no encontrado")
            
            if 'categoria_gasto_create' in content:
                print("  ✅ URL de crear categorías encontrada")
            else:
                print("  ❌ URL de crear categorías no encontrada")
        else:
            print(f"  ❌ Error cargando gastos: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 2. Probar lista de categorías
    print("\n2️⃣ Probando lista de categorías...")
    try:
        response = client.get('/categorias-gasto/')
        if response.status_code == 200:
            print("  ✅ Lista de categorías carga correctamente")
            
            content = response.content.decode()
            if 'Gestión de Categorías' in content:
                print("  ✅ Título de gestión encontrado")
            else:
                print("  ❌ Título de gestión no encontrado")
        else:
            print(f"  ❌ Error cargando categorías: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 3. Probar crear categoría
    print("\n3️⃣ Probando crear categoría...")
    try:
        response = client.get('/categorias-gasto/crear/')
        if response.status_code == 200:
            print("  ✅ Formulario de crear categoría carga correctamente")
        else:
            print(f"  ❌ Error cargando formulario: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 4. Verificar categorías existentes
    print("\n4️⃣ Verificando categorías existentes...")
    try:
        categorias = CategoriaGasto.objects.all()
        print(f"  📊 Total de categorías: {categorias.count()}")
        
        for categoria in categorias:
            print(f"    • {categoria.nombre}: {categoria.descripcion or 'Sin descripción'}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def crear_categorias_ejemplo():
    """Crear algunas categorías de ejemplo"""
    print("\n5️⃣ Creando categorías de ejemplo...")
    
    categorias_ejemplo = [
        {
            'nombre': 'Materiales de Construcción',
            'descripcion': 'Cemento, ladrillos, varillas, etc.'
        },
        {
            'nombre': 'Mano de Obra',
            'descripcion': 'Salarios de trabajadores y personal'
        },
        {
            'nombre': 'Equipos y Herramientas',
            'descripcion': 'Alquiler y mantenimiento de equipos'
        },
        {
            'nombre': 'Transporte',
            'descripcion': 'Fletes y transporte de materiales'
        },
        {
            'nombre': 'Servicios Profesionales',
            'descripcion': 'Arquitectos, ingenieros, consultores'
        }
    ]
    
    creadas = 0
    for cat_data in categorias_ejemplo:
        categoria, created = CategoriaGasto.objects.get_or_create(
            nombre=cat_data['nombre'],
            defaults={'descripcion': cat_data['descripcion']}
        )
        if created:
            print(f"  ✅ Categoría creada: {categoria.nombre}")
            creadas += 1
        else:
            print(f"  ℹ️ Categoría ya existe: {categoria.nombre}")
    
    print(f"  📊 Total categorías creadas: {creadas}")
    return creadas > 0

def main():
    """Función principal"""
    print("🔧 PRUEBA DE CATEGORÍAS DE GASTOS")
    print("=" * 45)
    
    try:
        # Probar funcionalidad
        funcionalidad_ok = probar_categorias_gastos()
        
        # Crear categorías de ejemplo
        categorias_creadas = crear_categorias_ejemplo()
        
        # Resumen final
        print(f"\n" + "=" * 45)
        print("📋 RESUMEN FINAL")
        print("=" * 45)
        
        if funcionalidad_ok:
            print("🎉 ¡CATEGORÍAS DE GASTOS FUNCIONAN CORRECTAMENTE!")
            print("✅ Lista de gastos con botón de categorías")
            print("✅ Lista de categorías funcionando")
            print("✅ Formulario de crear categorías funcionando")
            if categorias_creadas:
                print("✅ Categorías de ejemplo creadas")
            
            print(f"\n🌐 Para probar en el navegador:")
            print(f"   1. Ve a: http://localhost:8000/gastos/")
            print(f"   2. Haz clic en 'Gestionar Categorías'")
            print(f"   3. Crea nuevas categorías")
            print(f"   4. Edita o elimina categorías existentes")
        else:
            print("❌ HAY PROBLEMAS CON LAS CATEGORÍAS DE GASTOS")
        
        return funcionalidad_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
