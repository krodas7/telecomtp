#!/usr/bin/env python
"""
Script para probar el renderizado del template directamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.template.loader import render_to_string
from django.contrib.auth.models import User
from core.models import CategoriaGasto

def test_template_render():
    """Probar el renderizado del template directamente"""
    print("🔍 PROBANDO RENDERIZADO DEL TEMPLATE")
    print("=" * 50)
    
    try:
        # Obtener un usuario superusuario
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("❌ No hay superusuarios en el sistema")
            return False
        
        print(f"✅ Usuario: {user.username}")
        
        # Obtener categorías
        categorias = CategoriaGasto.objects.all()
        print(f"✅ Categorías encontradas: {categorias.count()}")
        
        # Crear contexto
        context = {
            'categorias': categorias,
            'user': user,
        }
        
        # Renderizar template
        print("\n1. RENDERIZANDO TEMPLATE...")
        try:
            html = render_to_string('core/categorias_gasto/list.html', context)
            print("✅ Template renderizado correctamente")
            print(f"   Longitud del HTML: {len(html)} caracteres")
            
            # Buscar el botón en el HTML renderizado
            print("\n2. BUSCANDO BOTÓN EN HTML RENDERIZADO...")
            
            if 'Nueva Categoría' in html:
                print("✅ Texto 'Nueva Categoría' encontrado")
            else:
                print("❌ Texto 'Nueva Categoría' NO encontrado")
            
            if 'btn btn-success btn-lg' in html:
                print("✅ Clase 'btn btn-success btn-lg' encontrada")
            else:
                print("❌ Clase 'btn btn-success btn-lg' NO encontrada")
            
            if '/categorias-gasto/crear/' in html:
                print("✅ URL '/categorias-gasto/crear/' encontrada")
            else:
                print("❌ URL '/categorias-gasto/crear/' NO encontrada")
            
            # Buscar la sección específica
            print("\n3. BUSCANDO SECCIÓN DEL BOTÓN...")
            if 'categorias-actions' in html:
                print("✅ Sección 'categorias-actions' encontrada")
                
                # Extraer la sección del botón
                import re
                pattern = r'<div class="categorias-actions">.*?</div>'
                match = re.search(pattern, html, re.DOTALL)
                if match:
                    section = match.group(0)
                    print("✅ Sección de acciones extraída:")
                    print(f"   Longitud: {len(section)} caracteres")
                    
                    if 'Nueva Categoría' in section:
                        print("✅ Botón encontrado en la sección de acciones")
                        print("   Contenido completo de la sección:")
                        print(section)
                    else:
                        print("❌ Botón NO encontrado en la sección de acciones")
                        print("   Contenido de la sección:")
                        print(section)
                else:
                    print("❌ No se pudo extraer la sección de acciones")
            else:
                print("❌ Sección 'categorias-actions' NO encontrada")
            
            # Guardar HTML para inspección
            with open('debug_output.html', 'w', encoding='utf-8') as f:
                f.write(html)
            print("\n✅ HTML guardado en 'debug_output.html' para inspección")
            
        except Exception as e:
            print(f"❌ Error renderizando template: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        print("\n" + "=" * 50)
        print("✅ PRUEBA COMPLETADA")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_template_render()
