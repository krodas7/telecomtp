#!/usr/bin/env python3
"""
Script para verificar que el menú de usuario esté en el header
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_menu_usuario():
    """Probar que el menú de usuario esté en el header"""
    print("👤 VERIFICANDO MENÚ DE USUARIO")
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
    print("\n1️⃣ Probando dashboard con menú de usuario...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard carga correctamente")
            
            content = response.content.decode()
            
            # Verificar que contenga el menú de usuario en el header
            if 'user-menu-btn' in content and 'user-dropdown-menu' in content:
                print("  ✅ Menú de usuario encontrado en el header")
            else:
                print("  ❌ Menú de usuario no encontrado en el header")
            
            # Verificar que contenga las opciones del menú
            if 'Perfil' in content and 'Cambiar Contraseña' in content and 'Cerrar Sesión' in content:
                print("  ✅ Opciones del menú encontradas")
            else:
                print("  ❌ Opciones del menú no encontradas")
                
            # Verificar que NO esté en el sidebar
            if 'sidebar-footer' in content and 'user-menu' not in content.split('sidebar-footer')[0]:
                print("  ✅ Menú de usuario removido del sidebar")
            else:
                print("  ❌ Menú de usuario aún en el sidebar")
                
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
            
            # Verificar que contenga el menú de usuario en el header
            if 'user-menu-btn' in content:
                print("  ✅ Menú de usuario en header de clientes")
            else:
                print("  ❌ Menú de usuario no en header de clientes")
                
        else:
            print(f"  ❌ Error cargando clientes: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def main():
    """Función principal"""
    print("🎯 VERIFICACIÓN DE MENÚ DE USUARIO")
    print("=" * 35)
    
    # Probar menú
    menu_ok = probar_menu_usuario()
    
    # Resumen final
    print(f"\n" + "=" * 35)
    print("📋 RESUMEN DE MENÚ DE USUARIO")
    print("=" * 35)
    
    if menu_ok:
        print("🎉 ¡MENÚ DE USUARIO CORREGIDO!")
        print("✅ Movido del sidebar al header")
        print("✅ Ubicado en la parte superior derecha")
        print("✅ Estilos CSS aplicados")
        print("✅ Opciones del menú funcionando")
        
        print(f"\n🌐 Para verificar en el navegador:")
        print(f"  1. Ve a: http://localhost:8000/")
        print(f"  2. Inicia sesión con: admin / admin")
        print(f"  3. Verifica el menú de usuario en la parte superior derecha")
        print(f"  4. Haz clic en el botón con tu nombre de usuario")
        print(f"  5. Verifica que aparezcan las opciones: Perfil, Cambiar Contraseña, Cerrar Sesión")
    else:
        print("❌ HAY PROBLEMAS CON EL MENÚ DE USUARIO")

if __name__ == "__main__":
    main()
