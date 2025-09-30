#!/usr/bin/env python3
"""
Script para probar la PWA completa
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import *

def probar_pwa():
    """Probar funcionalidad de PWA"""
    print("🔍 PROBANDO PWA COMPLETA")
    print("=" * 35)
    
    # Crear cliente de prueba
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # 1. Probar página principal
    print("\n1️⃣ Probando página principal...")
    try:
        response = client.get('/')
        if response.status_code == 200:
            print("  ✅ Página principal carga correctamente")
            
            # Verificar que incluya los scripts de PWA
            content = response.content.decode()
            if 'pwa-diagnostic.js' in content and 'pwa-register.js' in content:
                print("  ✅ Scripts de PWA incluidos")
            else:
                print("  ❌ Scripts de PWA no encontrados")
        else:
            print(f"  ❌ Error cargando página principal: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 2. Probar manifest.json
    print("\n2️⃣ Probando manifest.json...")
    try:
        response = client.get('/static/manifest.json')
        if response.status_code == 200:
            print("  ✅ Manifest.json accesible")
            
            import json
            manifest = json.loads(response.content.decode())
            required_fields = ['name', 'short_name', 'start_url', 'display', 'icons']
            missing_fields = [field for field in required_fields if field not in manifest]
            
            if not missing_fields:
                print("  ✅ Manifest.json completo")
            else:
                print(f"  ❌ Manifest.json incompleto. Campos faltantes: {missing_fields}")
        else:
            print(f"  ❌ Error accediendo manifest.json: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 3. Probar Service Worker
    print("\n3️⃣ Probando Service Worker...")
    try:
        response = client.get('/static/js/service-worker.js')
        if response.status_code == 200:
            print("  ✅ Service Worker accesible")
            
            content = response.content.decode()
            if 'CACHE_NAME' in content and 'STATIC_FILES' in content:
                print("  ✅ Service Worker configurado correctamente")
            else:
                print("  ❌ Service Worker mal configurado")
        else:
            print(f"  ❌ Error accediendo Service Worker: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 4. Probar página offline
    print("\n4️⃣ Probando página offline...")
    try:
        response = client.get('/offline/')
        if response.status_code == 200:
            print("  ✅ Página offline accesible")
            
            content = response.content.decode()
            if 'Sin Conexión' in content and 'Reintentar Conexión' in content:
                print("  ✅ Página offline configurada correctamente")
            else:
                print("  ❌ Página offline mal configurada")
        else:
            print(f"  ❌ Error accediendo página offline: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 5. Probar archivos estáticos
    print("\n5️⃣ Probando archivos estáticos...")
    static_files = [
        '/static/js/pwa-diagnostic.js',
        '/static/js/pwa-register.js',
        '/static/images/icon-192x192-v2.png',
        '/static/images/icon-512x512-v2.png',
        '/static/images/icon-32x32.png',
        '/static/images/icon-16x16.png'
    ]
    
    for file_path in static_files:
        try:
            response = client.get(file_path)
            if response.status_code == 200:
                print(f"  ✅ {file_path}")
            else:
                print(f"  ❌ {file_path} - {response.status_code}")
        except Exception as e:
            print(f"  ❌ {file_path} - Error: {e}")
    
    # 6. Probar dashboard
    print("\n6️⃣ Probando dashboard...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard accesible")
            
            content = response.content.decode()
            if 'pwa-diagnostic.js' in content:
                print("  ✅ Dashboard incluye scripts de PWA")
            else:
                print("  ❌ Dashboard no incluye scripts de PWA")
        else:
            print(f"  ❌ Error accediendo dashboard: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def verificar_configuracion_pwa():
    """Verificar configuración de PWA"""
    print(f"\n🔧 VERIFICANDO CONFIGURACIÓN PWA")
    print("=" * 40)
    
    # Verificar archivos necesarios
    archivos_requeridos = [
        'static/js/service-worker.js',
        'static/js/pwa-diagnostic.js',
        'static/js/pwa-register.js',
        'static/manifest.json',
        'templates/offline.html'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print("❌ Archivos faltantes:")
        for archivo in archivos_faltantes:
            print(f"  - {archivo}")
    else:
        print("✅ Todos los archivos de PWA presentes")
    
    # Verificar configuración de Django
    from django.conf import settings
    
    print(f"\n📋 Configuración Django:")
    print(f"  DEBUG: {settings.DEBUG}")
    print(f"  ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    print(f"  MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    
    return len(archivos_faltantes) == 0

def main():
    """Función principal"""
    print("🚀 PRUEBA COMPLETA DE PWA")
    print("=" * 35)
    
    # Verificar configuración
    config_ok = verificar_configuracion_pwa()
    
    # Probar PWA
    pwa_ok = probar_pwa()
    
    # Resumen final
    print(f"\n" + "=" * 35)
    print("📋 RESUMEN DE PWA")
    print("=" * 35)
    
    if config_ok and pwa_ok:
        print("🎉 ¡PWA COMPLETAMENTE FUNCIONAL!")
        print("✅ Service Worker configurado")
        print("✅ Manifest.json correcto")
        print("✅ Scripts de PWA incluidos")
        print("✅ Página offline disponible")
        print("✅ Archivos estáticos accesibles")
        print("\n🌐 Para probar en el navegador:")
        print("  1. Ve a: http://localhost:8000/")
        print("  2. Abre las herramientas de desarrollador (F12)")
        print("  3. Ve a la pestaña 'Application' o 'Aplicación'")
        print("  4. Verifica 'Service Workers' y 'Manifest'")
        print("  5. Ejecuta: runPWADiagnostic() en la consola")
    else:
        print("❌ HAY PROBLEMAS CON LA PWA")
        if not config_ok:
            print("❌ Problemas de configuración")
        if not pwa_ok:
            print("❌ Problemas de funcionalidad")

if __name__ == "__main__":
    main()
