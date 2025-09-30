#!/usr/bin/env python3
"""
Script para probar la funcionalidad de logout
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_logout():
    """Probar la funcionalidad de logout"""
    print("🔐 PROBANDO FUNCIONALIDAD DE LOGOUT")
    print("=" * 40)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # 1. Autenticar usuario
    print("1️⃣ Autenticando usuario...")
    client.force_login(admin_user)
    
    # Verificar que esté autenticado
    response = client.get('/dashboard/')
    if response.status_code == 200:
        print("  ✅ Usuario autenticado correctamente")
    else:
        print("  ❌ Error al autenticar usuario")
        return False
    
    # 2. Probar logout
    print("\n2️⃣ Probando logout...")
    try:
        response = client.get('/logout/')
        print(f"  📊 Status code: {response.status_code}")
        
        if response.status_code == 302:
            print("  ✅ Logout redirige correctamente (302)")
            
            # Verificar que el usuario ya no esté autenticado
            response = client.get('/dashboard/')
            if response.status_code == 302:
                print("  ✅ Usuario desautenticado correctamente")
                return True
            else:
                print("  ❌ Usuario sigue autenticado después del logout")
                return False
        else:
            print(f"  ❌ Logout no redirige correctamente: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en logout: {e}")
        return False

def probar_urls_logout():
    """Probar que las URLs de logout funcionen"""
    print("\n3️⃣ Probando URLs de logout...")
    
    from django.urls import reverse
    
    try:
        logout_url = reverse('logout')
        print(f"  ✅ URL de logout: {logout_url}")
        return True
    except Exception as e:
        print(f"  ❌ Error en URL de logout: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 PRUEBA DE FUNCIONALIDAD DE LOGOUT")
    print("=" * 45)
    
    try:
        # Probar URLs
        urls_ok = probar_urls_logout()
        
        # Probar logout
        logout_ok = probar_logout()
        
        # Resumen
        print(f"\n" + "=" * 45)
        print("📋 RESUMEN DE PRUEBAS")
        print("=" * 45)
        
        if urls_ok and logout_ok:
            print("🎉 ¡LOGOUT FUNCIONA CORRECTAMENTE!")
            print("✅ URL de logout válida")
            print("✅ Proceso de logout funciona")
            print("✅ Usuario se desautentica correctamente")
        else:
            print("❌ HAY PROBLEMAS CON EL LOGOUT")
            if not urls_ok:
                print("❌ URL de logout no válida")
            if not logout_ok:
                print("❌ Proceso de logout no funciona")
        
        return urls_ok and logout_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
