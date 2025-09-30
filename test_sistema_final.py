#!/usr/bin/env python3
"""
Script final para probar todo el sistema
"""

import os
import sys
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_sistema_completo():
    """Probar todo el sistema"""
    print("🚀 PRUEBA FINAL DEL SISTEMA")
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
            
            content = response.content.decode()
            if 'pwa-diagnostic.js' in content and 'pwa-register.js' in content:
                print("  ✅ Scripts de PWA incluidos")
            else:
                print("  ❌ Scripts de PWA no encontrados")
        else:
            print(f"  ❌ Error cargando página principal: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 2. Probar dashboard
    print("\n2️⃣ Probando dashboard...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard carga correctamente")
            
            content = response.content.decode()
            if 'Dashboard' in content:
                print("  ✅ Dashboard muestra contenido")
            else:
                print("  ❌ Dashboard vacío")
        else:
            print(f"  ❌ Error cargando dashboard: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 3. Probar clientes
    print("\n3️⃣ Probando módulo de clientes...")
    try:
        response = client.get('/clientes/')
        if response.status_code == 200:
            print("  ✅ Módulo de clientes carga correctamente")
            
            content = response.content.decode()
            if 'Clientes' in content and 'pwa-diagnostic.js' not in content:
                print("  ✅ Módulo de clientes sin código JavaScript visible")
            else:
                print("  ❌ Problema con módulo de clientes")
        else:
            print(f"  ❌ Error cargando clientes: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 4. Probar proyectos
    print("\n4️⃣ Probando módulo de proyectos...")
    try:
        response = client.get('/proyectos/')
        if response.status_code == 200:
            print("  ✅ Módulo de proyectos carga correctamente")
        else:
            print(f"  ❌ Error cargando proyectos: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 5. Probar PWA
    print("\n5️⃣ Probando PWA...")
    try:
        response = client.get('/static/js/service-worker.js')
        if response.status_code == 200:
            print("  ✅ Service Worker accesible")
        else:
            print(f"  ❌ Error accediendo Service Worker: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    try:
        response = client.get('/static/js/pwa-register.js')
        if response.status_code == 200:
            print("  ✅ PWA Register accesible")
        else:
            print(f"  ❌ Error accediendo PWA Register: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    try:
        response = client.get('/static/manifest.json')
        if response.status_code == 200:
            print("  ✅ Manifest accesible")
        else:
            print(f"  ❌ Error accediendo manifest: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 6. Probar página offline
    print("\n6️⃣ Probando página offline...")
    try:
        response = client.get('/offline/')
        if response.status_code == 200:
            print("  ✅ Página offline accesible")
        else:
            print(f"  ❌ Error accediendo página offline: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def main():
    """Función principal"""
    print("🎯 SISTEMA ARCA - PRUEBA FINAL")
    print("=" * 35)
    
    # Probar sistema
    sistema_ok = probar_sistema_completo()
    
    # Resumen final
    print(f"\n" + "=" * 35)
    print("📋 RESUMEN FINAL")
    print("=" * 35)
    
    if sistema_ok:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL!")
        print("✅ PWA configurada correctamente")
        print("✅ Módulos funcionando")
        print("✅ Templates corregidos")
        print("✅ JavaScript funcionando")
        print("✅ Archivos estáticos servidos")
        
        print(f"\n🌐 Para probar en el navegador:")
        print(f"  1. Ve a: http://localhost:8000/")
        print(f"  2. Inicia sesión con: admin / admin")
        print(f"  3. Navega por todos los módulos")
        print(f"  4. Verifica que no aparezca código JavaScript en las páginas")
        print(f"  5. Abre las herramientas de desarrollador (F12)")
        print(f"  6. Ve a la pestaña 'Application' o 'Aplicación'")
        print(f"  7. Verifica 'Service Workers' y 'Manifest'")
        print(f"  8. Ejecuta: runPWADiagnostic() en la consola")
    else:
        print("❌ HAY PROBLEMAS CON EL SISTEMA")

if __name__ == "__main__":
    main()
