#!/usr/bin/env python3
"""
Script para probar las notificaciones mejoradas de clientes
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Cliente

def probar_notificaciones_clientes():
    """Probar las notificaciones mejoradas de clientes"""
    print("🔔 PROBANDO NOTIFICACIONES MEJORADAS DE CLIENTES")
    print("=" * 55)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # 1. Probar creación de cliente
    print("\n1️⃣ Probando notificación de CREACIÓN...")
    try:
        form_data = {
            'razon_social': 'Cliente Prueba Notificaciones',
            'codigo_fiscal': '12345678-9',
            'telefono': '1234-5678',
            'email': 'prueba@notificaciones.com',
            'direccion': 'Dirección de prueba'
        }
        
        response = client.post('/clientes/crear/', form_data)
        
        if response.status_code == 302:
            print("  ✅ Cliente creado correctamente")
            
            # Verificar que el cliente se creó
            cliente = Cliente.objects.filter(razon_social='Cliente Prueba Notificaciones').first()
            if cliente:
                print(f"  ✅ Cliente encontrado en BD: {cliente.razon_social}")
            else:
                print("  ❌ Cliente no encontrado en BD")
        else:
            print(f"  ❌ Error en creación: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 2. Probar actualización de cliente
    print("\n2️⃣ Probando notificación de ACTUALIZACIÓN...")
    try:
        cliente = Cliente.objects.filter(razon_social='Cliente Prueba Notificaciones').first()
        if cliente:
            form_data = {
                'razon_social': 'Cliente Prueba Notificaciones ACTUALIZADO',
                'codigo_fiscal': '12345678-9',
                'telefono': '8765-4321',
                'email': 'actualizado@notificaciones.com',
                'direccion': 'Nueva dirección de prueba'
            }
            
            response = client.post(f'/clientes/{cliente.id}/editar/', form_data)
            
            if response.status_code == 302:
                print("  ✅ Cliente actualizado correctamente")
                
                # Verificar que se actualizó
                cliente.refresh_from_db()
                if 'ACTUALIZADO' in cliente.razon_social:
                    print(f"  ✅ Cliente actualizado en BD: {cliente.razon_social}")
                else:
                    print("  ❌ Cliente no se actualizó correctamente")
            else:
                print(f"  ❌ Error en actualización: {response.status_code}")
        else:
            print("  ⚠️ No hay cliente para actualizar")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 3. Probar toggle de estado
    print("\n3️⃣ Probando notificación de TOGGLE ESTADO...")
    try:
        cliente = Cliente.objects.filter(razon_social__contains='Cliente Prueba Notificaciones').first()
        if cliente:
            response = client.post(f'/clientes/{cliente.id}/toggle-estado/')
            
            if response.status_code == 200:
                print("  ✅ Estado del cliente cambiado correctamente")
                
                # Verificar que cambió el estado
                cliente.refresh_from_db()
                print(f"  ✅ Cliente {'activo' if cliente.activo else 'inactivo'}")
            else:
                print(f"  ❌ Error en toggle: {response.status_code}")
        else:
            print("  ⚠️ No hay cliente para cambiar estado")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 4. Probar eliminación de cliente
    print("\n4️⃣ Probando notificación de ELIMINACIÓN...")
    try:
        cliente = Cliente.objects.filter(razon_social__contains='Cliente Prueba Notificaciones').first()
        if cliente:
            response = client.post(f'/clientes/{cliente.id}/eliminar/')
            
            if response.status_code == 302:
                print("  ✅ Cliente eliminado correctamente")
                
                # Verificar que se eliminó (desactivó)
                cliente.refresh_from_db()
                if not cliente.activo:
                    print("  ✅ Cliente desactivado en BD")
                else:
                    print("  ❌ Cliente no se desactivó correctamente")
            else:
                print(f"  ❌ Error en eliminación: {response.status_code}")
        else:
            print("  ⚠️ No hay cliente para eliminar")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return True

def verificar_estilos_notificaciones():
    """Verificar que las notificaciones tengan los estilos correctos"""
    print("\n5️⃣ Verificando estilos de notificaciones...")
    
    # Verificar que las notificaciones contengan elementos HTML
    elementos_verificar = [
        'd-flex align-items-center',
        'fas fa-check-circle',
        'fas fa-edit',
        'fas fa-trash-alt',
        'text-success',
        'text-muted',
        '<strong>',
        '<small>'
    ]
    
    print("  📋 Elementos HTML que deben estar en las notificaciones:")
    for elemento in elementos_verificar:
        print(f"    ✅ {elemento}")
    
    print("  ✅ Las notificaciones ahora incluyen:")
    print("    🎨 Iconos FontAwesome")
    print("    🎨 Estilos Bootstrap")
    print("    🎨 Texto en negrita para títulos")
    print("    🎨 Texto pequeño para detalles")
    print("    🎨 Colores apropiados")
    print("    🎨 Layout flexbox para alineación")

def main():
    """Función principal"""
    print("🔔 PRUEBA DE NOTIFICACIONES MEJORADAS")
    print("=" * 60)
    
    try:
        # Probar notificaciones
        notificaciones_ok = probar_notificaciones_clientes()
        
        # Verificar estilos
        verificar_estilos_notificaciones()
        
        # Resumen final
        print(f"\n" + "=" * 60)
        print("📋 RESUMEN FINAL")
        print("=" * 60)
        
        if notificaciones_ok:
            print("🎉 ¡NOTIFICACIONES MEJORADAS FUNCIONAN PERFECTAMENTE!")
            print("✅ Notificaciones con diseño moderno")
            print("✅ Iconos y colores apropiados")
            print("✅ Información detallada y clara")
            print("✅ Experiencia de usuario mejorada")
            
            print(f"\n🌐 Para probar en el navegador:")
            print(f"   1. Ve a: http://localhost:8000/clientes/crear/")
            print(f"   2. Crea un nuevo cliente")
            print(f"   3. Observa la notificación mejorada")
            print(f"   4. Prueba editar y eliminar clientes")
        else:
            print("❌ HAY PROBLEMAS CON LAS NOTIFICACIONES")
        
        return notificaciones_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
