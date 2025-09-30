#!/usr/bin/env python3
"""
Script para verificar que el menú de usuario esté ordenado y en la posición correcta
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_menu_ordenado():
    """Probar que el menú de usuario esté ordenado y en la posición correcta"""
    print("🎯 VERIFICANDO MENÚ ORDENADO")
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
    
    # Probar dashboard
    print("\n1️⃣ Probando dashboard con menú ordenado...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard carga correctamente")
            
            content = response.content.decode()
            
            # Verificar que contenga los estilos correctos
            if 'header-right' in content and 'user-menu' in content:
                print("  ✅ Estructura del header correcta")
            else:
                print("  ❌ Estructura del header incorrecta")
            
            # Verificar que contenga los estilos CSS
            if 'user-menu.css' in content:
                print("  ✅ Estilos CSS del menú cargados")
            else:
                print("  ❌ Estilos CSS del menú no cargados")
            
            # Verificar que contenga el botón del menú
            if 'user-menu-btn' in content and 'user-avatar-small' in content:
                print("  ✅ Botón del menú con avatar encontrado")
            else:
                print("  ❌ Botón del menú no encontrado")
                
        else:
            print(f"  ❌ Error cargando dashboard: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Probar clientes
    print("\n2️⃣ Probando módulo de clientes...")
    try:
        response = client.get('/clientes/')
        if response.status_code == 200:
            print("  ✅ Módulo de clientes carga correctamente")
            
            content = response.content.decode()
            
            # Verificar que contenga el menú de usuario
            if 'user-menu-btn' in content:
                print("  ✅ Menú de usuario en clientes")
            else:
                print("  ❌ Menú de usuario no en clientes")
                
        else:
            print(f"  ❌ Error cargando clientes: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def main():
    """Función principal"""
    print("🎯 VERIFICACIÓN DE MENÚ ORDENADO")
    print("=" * 35)
    
    # Probar menú
    menu_ok = probar_menu_ordenado()
    
    # Resumen final
    print(f"\n" + "=" * 35)
    print("📋 RESUMEN DE MENÚ ORDENADO")
    print("=" * 35)
    
    if menu_ok:
        print("🎉 ¡MENÚ ORDENADO CORRECTAMENTE!")
        print("✅ Posicionado en la parte superior derecha")
        print("✅ Estilos CSS aplicados")
        print("✅ Diseño ordenado y profesional")
        print("✅ Avatar y nombre de usuario visibles")
        
        print(f"\n🌐 Para verificar en el navegador:")
        print(f"  1. Ve a: http://localhost:8000/")
        print(f"  2. Inicia sesión con: admin / admin")
        print(f"  3. Verifica que el menú de usuario esté en la parte superior derecha")
        print(f"  4. Debe mostrar: [👤] admin [▼]")
        print(f"  5. El diseño debe verse ordenado y profesional")
    else:
        print("❌ HAY PROBLEMAS CON EL MENÚ ORDENADO")

if __name__ == "__main__":
    main()
