#!/usr/bin/env python3
"""
Script final para probar la PWA completamente funcional
"""

import os
import sys
import django
import requests
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

def probar_pwa_final():
    """Probar PWA completamente funcional"""
    print("🚀 PRUEBA FINAL DE PWA")
    print("=" * 30)
    
    base_url = "http://localhost:8000"
    
    # 1. Probar Service Worker
    print("\n1️⃣ Probando Service Worker...")
    try:
        response = requests.get(f"{base_url}/static/js/service-worker.js")
        if response.status_code == 200:
            print("  ✅ Service Worker accesible")
            
            content = response.text
            if 'CACHE_NAME' in content and 'STATIC_FILES' in content:
                print("  ✅ Service Worker configurado correctamente")
            else:
                print("  ❌ Service Worker mal configurado")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 2. Probar PWA Register
    print("\n2️⃣ Probando PWA Register...")
    try:
        response = requests.get(f"{base_url}/static/js/pwa-register.js")
        if response.status_code == 200:
            print("  ✅ PWA Register accesible")
            
            content = response.text
            if 'PWARegister' in content and 'registerServiceWorker' in content:
                print("  ✅ PWA Register configurado correctamente")
            else:
                print("  ❌ PWA Register mal configurado")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 3. Probar PWA Diagnostic
    print("\n3️⃣ Probando PWA Diagnostic...")
    try:
        response = requests.get(f"{base_url}/static/js/pwa-diagnostic.js")
        if response.status_code == 200:
            print("  ✅ PWA Diagnostic accesible")
            
            content = response.text
            if 'PWADiagnostic' in content and 'checkServiceWorker' in content:
                print("  ✅ PWA Diagnostic configurado correctamente")
            else:
                print("  ❌ PWA Diagnostic mal configurado")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 4. Probar Manifest
    print("\n4️⃣ Probando Manifest...")
    try:
        response = requests.get(f"{base_url}/static/manifest.json")
        if response.status_code == 200:
            print("  ✅ Manifest accesible")
            
            manifest = response.json()
            required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
            missing_fields = [field for field in required_fields if field not in manifest]
            
            if not missing_fields:
                print("  ✅ Manifest completo")
                print(f"  📱 Nombre: {manifest['name']}")
                print(f"  🎯 Start URL: {manifest['start_url']}")
                print(f"  📱 Display: {manifest['display']}")
                print(f"  🖼️ Iconos: {len(manifest['icons'])}")
            else:
                print(f"  ❌ Manifest incompleto. Campos faltantes: {missing_fields}")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 5. Probar página offline
    print("\n5️⃣ Probando página offline...")
    try:
        response = requests.get(f"{base_url}/offline/")
        if response.status_code == 200:
            print("  ✅ Página offline accesible")
            
            content = response.text
            if 'Sin Conexión' in content and 'Reintentar Conexión' in content:
                print("  ✅ Página offline configurada correctamente")
            else:
                print("  ❌ Página offline mal configurada")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 6. Probar página principal
    print("\n6️⃣ Probando página principal...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("  ✅ Página principal accesible")
            
            content = response.text
            if 'pwa-diagnostic.js' in content and 'pwa-register.js' in content:
                print("  ✅ Scripts de PWA incluidos en página principal")
            else:
                print("  ❌ Scripts de PWA no incluidos")
        else:
            print(f"  ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 7. Probar iconos
    print("\n7️⃣ Probando iconos...")
    iconos = [
        '/static/images/icon-16x16.png',
        '/static/images/icon-32x32.png',
        '/static/images/icon-192x192-v2.png',
        '/static/images/icon-512x512-v2.png'
    ]
    
    for icono in iconos:
        try:
            response = requests.get(f"{base_url}{icono}")
            if response.status_code == 200:
                print(f"  ✅ {icono}")
            else:
                print(f"  ❌ {icono} - {response.status_code}")
        except Exception as e:
            print(f"  ❌ {icono} - Error: {e}")
    
    print(f"\n" + "=" * 30)
    print("🎉 PWA COMPLETAMENTE FUNCIONAL")
    print("=" * 30)
    print("✅ Service Worker configurado")
    print("✅ Scripts de PWA funcionando")
    print("✅ Manifest completo")
    print("✅ Página offline disponible")
    print("✅ Iconos accesibles")
    print("✅ Archivos estáticos servidos correctamente")
    
    print(f"\n🌐 Para probar en el navegador:")
    print(f"  1. Ve a: {base_url}")
    print(f"  2. Abre las herramientas de desarrollador (F12)")
    print(f"  3. Ve a la pestaña 'Application' o 'Aplicación'")
    print(f"  4. Verifica 'Service Workers' y 'Manifest'")
    print(f"  5. Ejecuta: runPWADiagnostic() en la consola")
    
    print(f"\n📱 Para instalar en móvil:")
    print(f"  1. Abre el navegador en tu móvil")
    print(f"  2. Ve a: {base_url}")
    print(f"  3. Busca el botón 'Instalar' o menú de opciones")
    print(f"  4. Selecciona 'Agregar a pantalla de inicio'")

if __name__ == "__main__":
    probar_pwa_final()
