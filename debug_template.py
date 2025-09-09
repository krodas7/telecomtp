#!/usr/bin/env python
"""
Script para debuggear el template de categorías
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
from django.template.loader import render_to_string
from django.template import Context, Template

def debug_template():
    """Debuggear el template de categorías"""
    print("🔍 DEBUGGEANDO TEMPLATE DE CATEGORÍAS")
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
        print("\n1. OBTENIENDO CONTENIDO DE LA PÁGINA...")
        response = client.get('/categorias-gasto/')
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            print("✅ Página cargada correctamente")
            
            # Buscar el botón en el contenido
            print("\n2. BUSCANDO BOTÓN EN EL CONTENIDO...")
            
            if 'btn-nueva-categoria' in content:
                print("✅ Clase 'btn-nueva-categoria' encontrada")
            else:
                print("❌ Clase 'btn-nueva-categoria' NO encontrada")
            
            if 'btn btn-success btn-lg' in content:
                print("✅ Clase 'btn btn-success btn-lg' encontrada")
            else:
                print("❌ Clase 'btn btn-success btn-lg' NO encontrada")
            
            if 'Nueva Categoría' in content:
                print("✅ Texto 'Nueva Categoría' encontrado")
            else:
                print("❌ Texto 'Nueva Categoría' NO encontrado")
            
            if 'categoria_gasto_create' in content:
                print("✅ URL 'categoria_gasto_create' encontrada")
            else:
                print("❌ URL 'categoria_gasto_create' NO encontrada")
            
            if '/categorias-gasto/crear/' in content:
                print("✅ URL '/categorias-gasto/crear/' encontrada")
            else:
                print("❌ URL '/categorias-gasto/crear/' NO encontrada")
            
            # Buscar la sección específica del botón
            print("\n3. BUSCANDO SECCIÓN DEL BOTÓN...")
            if 'categorias-actions' in content:
                print("✅ Sección 'categorias-actions' encontrada")
                
                # Extraer la sección del botón
                import re
                pattern = r'<div class="categorias-actions">.*?</div>'
                match = re.search(pattern, content, re.DOTALL)
                if match:
                    section = match.group(0)
                    print("✅ Sección de acciones extraída:")
                    print(f"   Longitud: {len(section)} caracteres")
                    
                    if 'Nueva Categoría' in section:
                        print("✅ Botón encontrado en la sección de acciones")
                    else:
                        print("❌ Botón NO encontrado en la sección de acciones")
                        print("   Contenido de la sección:")
                        print(section[:500] + "..." if len(section) > 500 else section)
                else:
                    print("❌ No se pudo extraer la sección de acciones")
            else:
                print("❌ Sección 'categorias-actions' NO encontrada")
            
            # Buscar errores de template
            print("\n4. BUSCANDO ERRORES DE TEMPLATE...")
            if 'TemplateSyntaxError' in content:
                print("❌ Error de sintaxis de template encontrado")
            else:
                print("✅ No hay errores de sintaxis de template")
            
            if 'TemplateDoesNotExist' in content:
                print("❌ Template no encontrado")
            else:
                print("✅ Template encontrado")
            
        else:
            print(f"❌ Error cargando página: {response.status_code}")
            print(f"   Contenido: {response.content.decode('utf-8')[:500]}")
        
        print("\n" + "=" * 50)
        print("✅ DEBUG COMPLETADO")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_template()
