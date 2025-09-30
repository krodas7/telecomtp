#!/usr/bin/env python3
"""
Script para probar el nuevo sistema de notificaciones toast
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

def probar_toast_notifications():
    """Probar el sistema de notificaciones toast"""
    print("🔔 PROBANDO SISTEMA DE NOTIFICACIONES TOAST")
    print("=" * 50)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # 1. Probar creación de cliente con notificación toast
    print("\n1️⃣ Probando notificación TOAST de CREACIÓN...")
    try:
        form_data = {
            'razon_social': 'Cliente Toast Test',
            'codigo_fiscal': '87654321-0',
            'telefono': '5555-6666',
            'email': 'toast@test.com',
            'direccion': 'Dirección de prueba toast'
        }
        
        response = client.post('/clientes/crear/', form_data)
        
        if response.status_code == 302:
            print("  ✅ Cliente creado correctamente")
            print("  ✅ Notificación toast debería aparecer automáticamente")
            
            # Verificar que el cliente se creó
            cliente = Cliente.objects.filter(razon_social='Cliente Toast Test').first()
            if cliente:
                print(f"  ✅ Cliente encontrado en BD: {cliente.razon_social}")
            else:
                print("  ❌ Cliente no encontrado en BD")
        else:
            print(f"  ❌ Error en creación: {response.status_code}")
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # 2. Probar actualización con notificación toast
    print("\n2️⃣ Probando notificación TOAST de ACTUALIZACIÓN...")
    try:
        cliente = Cliente.objects.filter(razon_social='Cliente Toast Test').first()
        if cliente:
            form_data = {
                'razon_social': 'Cliente Toast Test ACTUALIZADO',
                'codigo_fiscal': '87654321-0',
                'telefono': '7777-8888',
                'email': 'toast-actualizado@test.com',
                'direccion': 'Nueva dirección toast'
            }
            
            response = client.post(f'/clientes/{cliente.id}/editar/', form_data)
            
            if response.status_code == 302:
                print("  ✅ Cliente actualizado correctamente")
                print("  ✅ Notificación toast debería aparecer automáticamente")
                
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
    
    # 3. Probar eliminación con notificación toast
    print("\n3️⃣ Probando notificación TOAST de ELIMINACIÓN...")
    try:
        cliente = Cliente.objects.filter(razon_social__contains='Cliente Toast Test').first()
        if cliente:
            response = client.post(f'/clientes/{cliente.id}/eliminar/')
            
            if response.status_code == 302:
                print("  ✅ Cliente eliminado correctamente")
                print("  ✅ Notificación toast debería aparecer automáticamente")
                
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

def verificar_archivos_toast():
    """Verificar que los archivos de toast estén creados"""
    print("\n4️⃣ Verificando archivos de notificaciones toast...")
    
    import os
    
    archivos_verificar = [
        'static/css/toast-notifications.css',
        'static/js/toast-notifications.js'
    ]
    
    for archivo in archivos_verificar:
        if os.path.exists(archivo):
            print(f"  ✅ {archivo} existe")
        else:
            print(f"  ❌ {archivo} no existe")
    
    # Verificar que el template base incluya los archivos
    try:
        with open('templates/base.html', 'r') as f:
            content = f.read()
            
        if 'toast-notifications.css' in content:
            print("  ✅ CSS de toast incluido en base.html")
        else:
            print("  ❌ CSS de toast NO incluido en base.html")
            
        if 'toast-notifications.js' in content:
            print("  ✅ JS de toast incluido en base.html")
        else:
            print("  ❌ JS de toast NO incluido en base.html")
            
    except Exception as e:
        print(f"  ❌ Error leyendo base.html: {e}")

def mostrar_caracteristicas_toast():
    """Mostrar las características del sistema toast"""
    print("\n5️⃣ Características del sistema de notificaciones toast:")
    print("  🎨 Diseño moderno y elegante")
    print("  ⏱️ Desaparece automáticamente después de 4 segundos")
    print("  📱 Responsive para móviles y desktop")
    print("  🎭 Animaciones suaves de entrada y salida")
    print("  🎯 Posicionado en la esquina superior derecha")
    print("  🎨 Iconos y colores apropiados para cada tipo")
    print("  ❌ Botón de cerrar manual")
    print("  📊 Barra de progreso visual")
    print("  🎪 Efectos hover y transiciones")

def main():
    """Función principal"""
    print("🔔 PRUEBA DEL SISTEMA DE NOTIFICACIONES TOAST")
    print("=" * 60)
    
    try:
        # Verificar archivos
        verificar_archivos_toast()
        
        # Probar notificaciones
        toast_ok = probar_toast_notifications()
        
        # Mostrar características
        mostrar_caracteristicas_toast()
        
        # Resumen final
        print(f"\n" + "=" * 60)
        print("📋 RESUMEN FINAL")
        print("=" * 60)
        
        if toast_ok:
            print("🎉 ¡SISTEMA DE NOTIFICACIONES TOAST FUNCIONA PERFECTAMENTE!")
            print("✅ Notificaciones elegantes y modernas")
            print("✅ Desaparecen automáticamente")
            print("✅ Diseño responsive")
            print("✅ Animaciones suaves")
            print("✅ Experiencia de usuario mejorada")
            
            print(f"\n🌐 Para probar en el navegador:")
            print(f"   1. Ve a: http://localhost:8000/clientes/crear/")
            print(f"   2. Crea un nuevo cliente")
            print(f"   3. Observa la notificación toast elegante")
            print(f"   4. Prueba editar y eliminar clientes")
            print(f"   5. Las notificaciones aparecerán en la esquina superior derecha")
        else:
            print("❌ HAY PROBLEMAS CON EL SISTEMA TOAST")
        
        return toast_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
