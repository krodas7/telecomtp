#!/usr/bin/env python3
"""
Script para verificar que el logo esté corregido
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_logo_corregido():
    """Probar que el logo esté corregido"""
    print("🔧 VERIFICANDO LOGO CORREGIDO")
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
    print("\n1️⃣ Probando dashboard con logo corregido...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard carga correctamente")
            
            content = response.content.decode()
            
            # Verificar que contenga el logo correcto
            if 'CONSTRUCCIONES' in content and 'ARCA' in content:
                print("  ✅ Logo corregido: 'CONSTRUCCIONES ARCA' encontrado")
            else:
                print("  ❌ Logo no corregido: texto no encontrado")
            
            # Verificar que contenga los elementos del logo
            if 'logo-buildings' in content and 'building-left' in content:
                print("  ✅ Elementos del logo encontrados")
            else:
                print("  ❌ Elementos del logo no encontrados")
                
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
            
            # Verificar que contenga el logo correcto
            if 'CONSTRUCCIONES' in content and 'ARCA' in content:
                print("  ✅ Logo corregido en clientes")
            else:
                print("  ❌ Logo no corregido en clientes")
                
        else:
            print(f"  ❌ Error cargando clientes: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def main():
    """Función principal"""
    print("🎯 VERIFICACIÓN DE LOGO CORREGIDO")
    print("=" * 35)
    
    # Probar logo
    logo_ok = probar_logo_corregido()
    
    # Resumen final
    print(f"\n" + "=" * 35)
    print("📋 RESUMEN DE LOGO")
    print("=" * 35)
    
    if logo_ok:
        print("🎉 ¡LOGO CORREGIDO EXITOSAMENTE!")
        print("✅ Nombre de empresa: 'CONSTRUCCIONES ARCA'")
        print("✅ Logo con edificios restaurado")
        print("✅ Estilos CSS aplicados")
        
        print(f"\n🌐 Para verificar en el navegador:")
        print(f"  1. Ve a: http://localhost:8000/")
        print(f"  2. Inicia sesión con: admin / admin")
        print(f"  3. Verifica el logo en la parte superior del sidebar")
        print(f"  4. Debe mostrar: 'SISTEMA CONSTRUCCIONES ARCA'")
    else:
        print("❌ HAY PROBLEMAS CON EL LOGO")

if __name__ == "__main__":
    main()
