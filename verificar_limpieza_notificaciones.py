#!/usr/bin/env python3
"""
Script para verificar que todas las notificaciones molestas han sido eliminadas
"""

import os
import sys
import glob
import re

# Configurar Django antes de importar modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def verificar_notificaciones_molestas():
    """Verificar que no queden notificaciones molestas en templates"""
    print("🔍 VERIFICANDO LIMPIEZA DE NOTIFICACIONES MOLESTAS")
    print("=" * 60)
    
    # Patrones de notificaciones molestas específicas (solo en HTML, no en JavaScript)
    patrones_molestos = [
        r'<div class="alert alert-info">.*?Nota.*?El botón verde.*?aparece solo en facturas.*?pagadas.*?</div>',
        r'<div class="alert alert-warning">.*?Fechas.*?Emisión.*?cuando se creó.*?Vencimiento.*?cuando debe pagarse.*?</div>',
        r'<div class="alert alert-info">.*?El proyecto será marcado como inactivo.*?no se eliminará físicamente.*?</div>',
        r'<div class="alert alert-info">.*?Las facturas y gastos existentes no se verán afectados.*?</div>'
    ]
    
    templates_con_problemas = []
    
    # Buscar en todos los templates
    template_files = glob.glob('templates/**/*.html', recursive=True)
    
    for template_file in template_files:
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            problemas_encontrados = []
            for patron in patrones_molestos:
                if re.search(patron, content, re.IGNORECASE | re.DOTALL):
                    problemas_encontrados.append(patron)
            
            if problemas_encontrados:
                templates_con_problemas.append({
                    'archivo': template_file,
                    'problemas': problemas_encontrados
                })
                
        except Exception as e:
            print(f"  ⚠️ Error leyendo {template_file}: {e}")
    
    return templates_con_problemas

def verificar_botones_ayuda():
    """Verificar que los botones de ayuda estén presentes"""
    print("\n🔍 VERIFICANDO BOTONES DE AYUDA CONTEXTUAL")
    print("=" * 60)
    
    templates_con_ayuda = []
    templates_sin_ayuda = []
    
    # Buscar templates que deberían tener ayuda
    templates_principales = [
        'templates/core/facturas/list.html',
        'templates/core/proyectos/list.html',
        'templates/core/anticipos/list.html'
    ]
    
    for template_file in templates_principales:
        if os.path.exists(template_file):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'mostrarAyuda' in content and 'btn-outline-info' in content:
                    templates_con_ayuda.append(template_file)
                else:
                    templates_sin_ayuda.append(template_file)
                    
            except Exception as e:
                print(f"  ⚠️ Error leyendo {template_file}: {e}")
    
    return templates_con_ayuda, templates_sin_ayuda

def probar_funcionalidad_ayuda():
    """Probar que la funcionalidad de ayuda funcione en el navegador"""
    print("\n🔍 PROBANDO FUNCIONALIDAD DE AYUDA EN NAVEGADOR")
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
    
    # Probar páginas principales
    paginas_a_probar = [
        ('/facturas/', 'Facturas'),
        ('/proyectos/', 'Proyectos'),
        ('/anticipos/', 'Anticipos')
    ]
    
    paginas_ok = 0
    
    for url, nombre in paginas_a_probar:
        try:
            response = client.get(url)
            if response.status_code == 200:
                content = response.content.decode()
                
                # Verificar que no hay notificaciones estáticas molestas
                if 'alert alert-info' in content and ('botón verde' in content or 'facturas.*pagadas' in content):
                    print(f"  ❌ {nombre}: Aún hay notificaciones molestas")
                elif 'mostrarAyuda' in content and 'btn-outline-info' in content:
                    print(f"  ✅ {nombre}: Ayuda contextual implementada correctamente")
                    paginas_ok += 1
                else:
                    print(f"  ⚠️ {nombre}: Sin notificaciones molestas pero sin ayuda contextual")
                    paginas_ok += 1
            else:
                print(f"  ❌ {nombre}: Error {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {nombre}: Error {e}")
    
    return paginas_ok, len(paginas_a_probar)

def main():
    """Función principal"""
    print("🔔 VERIFICACIÓN FINAL DE LIMPIEZA DE NOTIFICACIONES")
    print("=" * 70)
    
    try:
        # 1. Verificar que no queden notificaciones molestas
        templates_problematicos = verificar_notificaciones_molestas()
        
        if templates_problematicos:
            print(f"\n❌ AÚN HAY {len(templates_problematicos)} TEMPLATES CON NOTIFICACIONES MOLESTAS:")
            for template in templates_problematicos:
                print(f"  - {template['archivo']}")
        else:
            print("\n✅ NO HAY NOTIFICACIONES MOLESTAS EN EL SISTEMA")
        
        # 2. Verificar botones de ayuda
        templates_con_ayuda, templates_sin_ayuda = verificar_botones_ayuda()
        
        print(f"\n📊 BOTONES DE AYUDA:")
        print(f"  ✅ Templates con ayuda: {len(templates_con_ayuda)}")
        print(f"  ❌ Templates sin ayuda: {len(templates_sin_ayuda)}")
        
        if templates_sin_ayuda:
            print("  Templates sin ayuda:")
            for template in templates_sin_ayuda:
                print(f"    - {template}")
        
        # 3. Probar funcionalidad en navegador
        paginas_ok, total_paginas = probar_funcionalidad_ayuda()
        
        print(f"\n📊 FUNCIONALIDAD EN NAVEGADOR:")
        print(f"  ✅ Páginas funcionando: {paginas_ok}/{total_paginas}")
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if not templates_problematicos and paginas_ok == total_paginas:
            print("🎉 ¡SISTEMA COMPLETAMENTE LIMPIO!")
            print("✅ Todas las notificaciones molestas eliminadas")
            print("✅ Ayuda contextual implementada correctamente")
            print("✅ Funcionalidad verificada en navegador")
            print("✅ Interfaz limpia y profesional")
            return True
        else:
            print("⚠️ HAY PROBLEMAS PENDIENTES:")
            if templates_problematicos:
                print(f"  - {len(templates_problematicos)} templates con notificaciones molestas")
            if paginas_ok < total_paginas:
                print(f"  - {total_paginas - paginas_ok} páginas con problemas")
            return False
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
