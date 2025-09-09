#!/usr/bin/env python
"""
Script para probar la URL de categorías de gasto
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.urls import reverse
from django.test import Client
from django.contrib.auth.models import User

def test_categoria_urls():
    """Probar las URLs de categorías de gasto"""
    print("🔍 PROBANDO URLs DE CATEGORÍAS DE GASTO")
    print("=" * 50)
    
    try:
        # Crear cliente de prueba
        client = Client()
        
        # Obtener un usuario superusuario
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("❌ No hay superusuarios en el sistema")
            return False
        
        # Autenticar usuario
        client.force_login(user)
        print(f"✅ Usuario autenticado: {user.username}")
        
        # Probar URL de lista de categorías
        print("\n1. PROBANDO LISTA DE CATEGORÍAS...")
        try:
            response = client.get('/categorias-gasto/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Lista de categorías accesible")
                
                # Verificar si el botón está en el HTML
                content = response.content.decode('utf-8')
                if 'btn-nueva-categoria' in content:
                    print("   ✅ Botón 'Nueva Categoría' encontrado en el HTML")
                else:
                    print("   ❌ Botón 'Nueva Categoría' NO encontrado en el HTML")
                
                if 'categoria_gasto_create' in content:
                    print("   ✅ URL de creación encontrada en el HTML")
                else:
                    print("   ❌ URL de creación NO encontrada en el HTML")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error accediendo a lista: {e}")
        
        # Probar URL de creación de categoría
        print("\n2. PROBANDO CREACIÓN DE CATEGORÍA...")
        try:
            response = client.get('/categorias-gasto/crear/')
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ Formulario de creación accesible")
            else:
                print(f"   ❌ Error: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Error accediendo a creación: {e}")
        
        # Probar reverse URL
        print("\n3. PROBANDO REVERSE URLs...")
        try:
            lista_url = reverse('categorias_gasto_list')
            print(f"   ✅ Lista URL: {lista_url}")
        except Exception as e:
            print(f"   ❌ Error reverse lista: {e}")
        
        try:
            crear_url = reverse('categoria_gasto_create')
            print(f"   ✅ Crear URL: {crear_url}")
        except Exception as e:
            print(f"   ❌ Error reverse crear: {e}")
        
        print("\n" + "=" * 50)
        print("✅ PRUEBAS COMPLETADAS")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_categoria_urls()
