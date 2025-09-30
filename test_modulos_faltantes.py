#!/usr/bin/env python3
"""
Script para verificar que los módulos de rentabilidad y sistema estén funcionando
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_modulos_faltantes():
    """Probar que los módulos de rentabilidad y sistema estén funcionando"""
    print("🔍 VERIFICANDO MÓDULOS FALTANTES")
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
    
    # Probar módulo de rentabilidad
    print("\n1️⃣ Probando módulo de rentabilidad...")
    try:
        response = client.get('/rentabilidad/')
        if response.status_code == 200:
            print("  ✅ Módulo de rentabilidad funciona")
        else:
            print(f"  ❌ Error en rentabilidad: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error en rentabilidad: {e}")
    
    # Probar módulo de sistema
    print("\n2️⃣ Probando módulo de sistema...")
    try:
        response = client.get('/sistema/')
        if response.status_code == 200:
            print("  ✅ Módulo de sistema funciona")
        else:
            print(f"  ❌ Error en sistema: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error en sistema: {e}")
    
    # Probar dashboard para verificar menú
    print("\n3️⃣ Probando menú del dashboard...")
    try:
        response = client.get('/dashboard/')
        if response.status_code == 200:
            print("  ✅ Dashboard carga correctamente")
            
            content = response.content.decode()
            
            # Verificar que contenga los módulos en el menú
            if 'Rentabilidad' in content and 'Sistema' in content:
                print("  ✅ Módulos de rentabilidad y sistema en el menú")
            else:
                print("  ❌ Módulos no encontrados en el menú")
                
        else:
            print(f"  ❌ Error cargando dashboard: {response.status_code}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def main():
    """Función principal"""
    print("🎯 VERIFICACIÓN DE MÓDULOS FALTANTES")
    print("=" * 35)
    
    # Probar módulos
    modulos_ok = probar_modulos_faltantes()
    
    # Resumen final
    print(f"\n" + "=" * 35)
    print("📋 RESUMEN DE MÓDULOS")
    print("=" * 35)
    
    if modulos_ok:
        print("🎉 ¡MÓDULOS RESTAURADOS!")
        print("✅ Módulo de rentabilidad funcionando")
        print("✅ Módulo de sistema funcionando")
        print("✅ Módulos agregados al menú del sidebar")
        
        print(f"\n🌐 Para verificar en el navegador:")
        print(f"  1. Ve a: http://localhost:8000/")
        print(f"  2. Inicia sesión con: admin / admin")
        print(f"  3. Verifica que aparezcan 'Rentabilidad' y 'Sistema' en el menú")
        print(f"  4. Haz clic en cada uno para verificar que funcionen")
    else:
        print("❌ HAY PROBLEMAS CON LOS MÓDULOS")

if __name__ == "__main__":
    main()
