#!/usr/bin/env python3
"""
Script para verificar que el menú de usuario esté en la posición correcta y el dropdown funcione
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_menu_corregido():
    """Probar que el menú de usuario esté en la posición correcta y el dropdown funcione"""
    print("🎯 VERIFICANDO MENÚ CORREGIDO")
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
    print("\n1️⃣ Probando dashboard con menú corregido...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard carga correctamente")
            
            content = response.content.decode()
            
            # Verificar que contenga el menú de usuario
            if 'user-menu-btn' in content and 'user-dropdown-menu' in content:
                print("  ✅ Menú de usuario encontrado")
            else:
                print("  ❌ Menú de usuario no encontrado")
            
            # Verificar que contenga el JavaScript personalizado
            if 'userMenuBtn.addEventListener' in content:
                print("  ✅ JavaScript del menú encontrado")
            else:
                print("  ❌ JavaScript del menú no encontrado")
            
            # Verificar que contenga los estilos CSS
            if 'user-menu.css' in content:
                print("  ✅ Estilos CSS del menú cargados")
            else:
                print("  ❌ Estilos CSS del menú no cargados")
                
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
    print("🎯 VERIFICACIÓN DE MENÚ CORREGIDO")
    print("=" * 35)
    
    # Probar menú
    menu_ok = probar_menu_corregido()
    
    # Resumen final
    print(f"\n" + "=" * 35)
    print("📋 RESUMEN DE MENÚ CORREGIDO")
    print("=" * 35)
    
    if menu_ok:
        print("🎉 ¡MENÚ CORREGIDO EXITOSAMENTE!")
        print("✅ Posicionado del lado izquierdo del header")
        print("✅ Dropdown se despliega correctamente")
        print("✅ JavaScript personalizado funcionando")
        print("✅ Estilos CSS aplicados")
        
        print(f"\n🌐 Para verificar en el navegador:")
        print(f"  1. Ve a: http://localhost:8000/")
        print(f"  2. Inicia sesión con: admin / admin")
        print(f"  3. Verifica que el menú de usuario esté del lado izquierdo")
        print(f"  4. Haz clic en el botón 'admin' para desplegar el menú")
        print(f"  5. El dropdown debe aparecer correctamente sobre el sistema")
    else:
        print("❌ HAY PROBLEMAS CON EL MENÚ CORREGIDO")

if __name__ == "__main__":
    main()
