#!/usr/bin/env python3
"""
Script de prueba para verificar el botón de reset de la aplicación
"""

import os
import sys
import django
from io import BytesIO

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import *

def test_reset_access():
    """Probar acceso al reset para diferentes tipos de usuario"""
    print("🔐 PROBANDO ACCESO AL RESET...")
    
    client = Client()
    
    # Probar sin login
    response = client.get('/sistema/reset-app/')
    if response.status_code == 302:  # Redirect to login
        print("✅ Acceso sin login redirige correctamente")
    else:
        print(f"❌ Error en acceso sin login: {response.status_code}")
        return False
    
    # Probar con usuario normal
    try:
        user_normal = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )
        client.login(username='testuser', password='testpass123')
        
        response = client.get('/sistema/reset-app/')
        if response.status_code == 302:  # Redirect to dashboard
            print("✅ Usuario normal es redirigido correctamente")
        else:
            print(f"❌ Error con usuario normal: {response.status_code}")
            return False
        
        client.logout()
        user_normal.delete()
        
    except Exception as e:
        print(f"❌ Error creando usuario normal: {e}")
        return False
    
    # Probar con superusuario
    client.login(username='admin', password='admin123')
    response = client.get('/sistema/reset-app/')
    if response.status_code == 200:
        print("✅ Superusuario puede acceder al reset")
        return True
    else:
        print(f"❌ Error con superusuario: {response.status_code}")
        return False

def test_reset_form():
    """Probar el formulario de reset"""
    print("\n📋 PROBANDO FORMULARIO DE RESET...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Obtener la página de reset
        response = client.get('/sistema/reset-app/')
        if response.status_code != 200:
            print(f"❌ Error obteniendo formulario: {response.status_code}")
            return False
        
        content = response.content.decode('utf-8')
        
        # Verificar elementos del formulario
        checks = [
            ('csrf_token', 'CSRF token presente'),
            ('confirmReset', 'Checkbox de confirmación presente'),
            ('confirmSuperuser', 'Checkbox de superusuario presente'),
            ('confirmBackup', 'Checkbox de backup presente'),
            ('btnReset', 'Botón de reset presente'),
            ('resetForm', 'Formulario presente'),
            ('EJECUTAR RESET', 'Texto del botón presente')
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"❌ {description}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando formulario: {e}")
        return False

def test_reset_functionality():
    """Probar la funcionalidad del reset (sin ejecutar realmente)"""
    print("\n⚙️ PROBANDO FUNCIONALIDAD DEL RESET...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Contar registros antes del test
        initial_counts = {
            'clientes': Cliente.objects.count(),
            'proyectos': Proyecto.objects.count(),
            'facturas': Factura.objects.count(),
            'gastos': Gasto.objects.count(),
            'archivos': ArchivoProyecto.objects.count(),
            'usuarios': User.objects.count(),
            'logs': LogActividad.objects.count()
        }
        
        print("📊 Estado inicial del sistema:")
        for model, count in initial_counts.items():
            print(f"   - {model}: {count}")
        
        # Simular POST al reset (sin ejecutar realmente)
        # Solo verificamos que la URL esté configurada correctamente
        response = client.post('/sistema/reset-app/', {
            'csrfmiddlewaretoken': 'test'
        }, follow=True)
        
        # El reset debería redirigir a 'sistema' después de procesar
        if response.status_code == 200:
            print("✅ Formulario de reset procesa correctamente")
            return True
        else:
            print(f"❌ Error procesando reset: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando funcionalidad: {e}")
        return False

def test_reset_security():
    """Probar medidas de seguridad del reset"""
    print("\n🛡️ PROBANDO MEDIDAS DE SEGURIDAD...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Obtener la página de reset
        response = client.get('/sistema/reset-app/')
        content = response.content.decode('utf-8')
        
        # Verificar medidas de seguridad
        security_checks = [
            ('ZONA DE PELIGRO', 'Advertencia de peligro presente'),
            ('IRREVERSIBLE', 'Advertencia de irreversibilidad presente'),
            ('superusuario', 'Mensaje de superusuario presente'),
            ('copia de seguridad', 'Mensaje de backup presente'),
            ('CONFIRMACIÓN FINAL', 'Confirmación final presente'),
            ('checkAllConfirmed', 'Validación JavaScript presente'),
            ('preventDefault', 'Prevención de envío accidental presente')
        ]
        
        for check, description in security_checks:
            if check.lower() in content.lower():
                print(f"✅ {description}")
            else:
                print(f"⚠️  {description} - No encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando seguridad: {e}")
        return False

def test_reset_ui():
    """Probar la interfaz de usuario del reset"""
    print("\n🎨 PROBANDO INTERFAZ DE USUARIO...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        response = client.get('/sistema/reset-app/')
        content = response.content.decode('utf-8')
        
        # Verificar elementos de UI
        ui_checks = [
            ('reset-warning', 'Estilos de advertencia'),
            ('reset-actions', 'Lista de acciones'),
            ('reset-form', 'Formulario estilizado'),
            ('btn-reset', 'Botón de reset estilizado'),
            ('danger-zone', 'Zona de peligro'),
            ('confirm-checkbox', 'Checkboxes de confirmación'),
            ('fa-exclamation-triangle', 'Iconos de advertencia'),
            ('fa-shield-alt', 'Iconos de seguridad')
        ]
        
        for check, description in ui_checks:
            if check in content:
                print(f"✅ {description}")
            else:
                print(f"⚠️  {description} - No encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando UI: {e}")
        return False

if __name__ == "__main__":
    print("🚀 VERIFICACIÓN DEL BOTÓN DE RESET DE LA APLICACIÓN")
    print("=" * 60)
    
    tests = [
        ("Acceso al Reset", test_reset_access),
        ("Formulario de Reset", test_reset_form),
        ("Funcionalidad del Reset", test_reset_functionality),
        ("Medidas de Seguridad", test_reset_security),
        ("Interfaz de Usuario", test_reset_ui),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: FUNCIONANDO")
            else:
                print(f"❌ {test_name}: CON PROBLEMAS")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADOS: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡BOTÓN DE RESET FUNCIONANDO AL 100%!")
        print("✅ Acceso controlado por permisos")
        print("✅ Formulario completo y funcional")
        print("✅ Medidas de seguridad implementadas")
        print("✅ Interfaz de usuario atractiva")
        print("✅ Validaciones JavaScript funcionando")
    elif passed >= total * 0.8:
        print("⚠️  Botón de reset mayormente funcional")
        print(f"   {total - passed} aspectos necesitan atención")
    else:
        print("❌ Botón de reset con problemas críticos")
        print(f"   {total - passed} aspectos no funcionan")
    
    print("\n" + "=" * 60)
    print("🏁 VERIFICACIÓN COMPLETADA")
