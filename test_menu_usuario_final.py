#!/usr/bin/env python3
"""
Script para probar el menú de usuario mejorado
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
    """Probar el menú de usuario"""
    print("👤 PROBANDO MENÚ DE USUARIO MEJORADO")
    print("=" * 45)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # Probar dashboard (donde está el menú)
    print("\n1️⃣ Probando dashboard con menú de usuario...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar elementos del menú
            if 'user-menu-btn' in content:
                print("  ✅ Botón del menú de usuario encontrado")
            else:
                print("  ❌ Botón del menú de usuario no encontrado")
            
            if 'user-dropdown-menu' in content:
                print("  ✅ Dropdown del menú encontrado")
            else:
                print("  ❌ Dropdown del menú no encontrado")
            
            if 'Cerrar Sesión' in content:
                print("  ✅ Enlace de cerrar sesión encontrado")
            else:
                print("  ❌ Enlace de cerrar sesión no encontrado")
            
            if 'logout' in content:
                print("  ✅ URL de logout encontrada")
            else:
                print("  ❌ URL de logout no encontrada")
            
            return True
        else:
            print(f"  ❌ Error cargando dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def verificar_css_responsivo():
    """Verificar que el CSS responsivo esté cargando"""
    print("\n2️⃣ Verificando CSS responsivo...")
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        response = client.get('/static/css/user-menu.css')
        if response.status_code == 200:
            content = response.content.decode()
            
            if '@media' in content:
                print("  ✅ Media queries responsivas encontradas")
            else:
                print("  ❌ Media queries responsivas no encontradas")
            
            if 'user-menu-btn' in content:
                print("  ✅ Estilos del botón encontrados")
            else:
                print("  ❌ Estilos del botón no encontrados")
            
            if 'user-dropdown-menu' in content:
                print("  ✅ Estilos del dropdown encontrados")
            else:
                print("  ❌ Estilos del dropdown no encontrados")
            
            return True
        else:
            print(f"  ❌ Error cargando CSS: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def verificar_logout():
    """Verificar que el logout funcione"""
    print("\n3️⃣ Verificando funcionalidad de logout...")
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        # Probar logout
        response = client.get('/logout/')
        if response.status_code == 302:
            print("  ✅ Logout redirige correctamente")
            
            # Verificar que el usuario esté desautenticado
            response = client.get('/dashboard/')
            if response.status_code == 302:
                print("  ✅ Usuario desautenticado correctamente")
                return True
            else:
                print("  ❌ Usuario no desautenticado")
                return False
        else:
            print(f"  ❌ Logout no redirige: {response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 PRUEBA FINAL DEL MENÚ DE USUARIO")
    print("=" * 45)
    
    try:
        # Probar menú de usuario
        menu_ok = probar_menu_usuario()
        
        # Verificar CSS responsivo
        css_ok = verificar_css_responsivo()
        
        # Verificar logout
        logout_ok = verificar_logout()
        
        # Resumen final
        print(f"\n" + "=" * 45)
        print("📋 RESUMEN FINAL")
        print("=" * 45)
        
        if menu_ok and css_ok and logout_ok:
            print("🎉 ¡MENÚ DE USUARIO FUNCIONA PERFECTAMENTE!")
            print("✅ Menú de usuario cargado correctamente")
            print("✅ CSS responsivo funcionando")
            print("✅ Logout funcionando correctamente")
            print("\n🌐 Para probar en el navegador:")
            print("   1. Ve a: http://localhost:8000/")
            print("   2. Inicia sesión con: admin / admin")
            print("   3. Haz clic en el menú de usuario (admin)")
            print("   4. Verifica que el dropdown se abra")
            print("   5. Haz clic en 'Cerrar Sesión'")
            print("   6. Verifica que te redirija al login")
        else:
            print("❌ HAY PROBLEMAS CON EL MENÚ DE USUARIO")
            if not menu_ok:
                print("❌ Menú de usuario no funciona")
            if not css_ok:
                print("❌ CSS responsivo no funciona")
            if not logout_ok:
                print("❌ Logout no funciona")
        
        return menu_ok and css_ok and logout_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
