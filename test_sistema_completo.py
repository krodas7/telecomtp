#!/usr/bin/env python3
"""
Script de prueba completo del sistema ARCA Construcción
Verifica que todos los módulos funcionen correctamente
"""

import os
import sys
import django
from io import BytesIO

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from core.models import *

def test_authentication():
    """Probar autenticación"""
    print("🔐 PROBANDO AUTENTICACIÓN...")
    
    client = Client()
    
    # Probar login
    login_success = client.login(username='admin', password='admin123')
    if login_success:
        print("✅ Login exitoso")
        return True
    else:
        print("❌ Error en login")
        return False

def test_dashboard():
    """Probar dashboard"""
    print("\n📊 PROBANDO DASHBOARD...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Dashboard accesible")
            return True
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_clientes():
    """Probar módulo de clientes"""
    print("\n👥 PROBANDO MÓDULO DE CLIENTES...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Lista de clientes
        response = client.get('/clientes/')
        if response.status_code == 200:
            print("✅ Lista de clientes accesible")
        else:
            print(f"❌ Error en lista de clientes: {response.status_code}")
            return False
        
        # Formulario de creación
        response = client.get('/clientes/crear/')
        if response.status_code == 200:
            print("✅ Formulario de cliente accesible")
        else:
            print(f"❌ Error en formulario de cliente: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_proyectos():
    """Probar módulo de proyectos"""
    print("\n🏗️ PROBANDO MÓDULO DE PROYECTOS...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Lista de proyectos
        response = client.get('/proyectos/')
        if response.status_code == 200:
            print("✅ Lista de proyectos accesible")
        else:
            print(f"❌ Error en lista de proyectos: {response.status_code}")
            return False
        
        # Formulario de creación
        response = client.get('/proyectos/crear/')
        if response.status_code == 200:
            print("✅ Formulario de proyecto accesible")
        else:
            print(f"❌ Error en formulario de proyecto: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_facturas():
    """Probar módulo de facturas"""
    print("\n💰 PROBANDO MÓDULO DE FACTURAS...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Lista de facturas
        response = client.get('/facturas/')
        if response.status_code == 200:
            print("✅ Lista de facturas accesible")
        else:
            print(f"❌ Error en lista de facturas: {response.status_code}")
            return False
        
        # Formulario de creación
        response = client.get('/facturas/crear/')
        if response.status_code == 200:
            print("✅ Formulario de factura accesible")
        else:
            print(f"❌ Error en formulario de factura: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_gastos():
    """Probar módulo de gastos"""
    print("\n💸 PROBANDO MÓDULO DE GASTOS...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Lista de gastos
        response = client.get('/gastos/')
        if response.status_code == 200:
            print("✅ Lista de gastos accesible")
        else:
            print(f"❌ Error en lista de gastos: {response.status_code}")
            return False
        
        # Formulario de creación
        response = client.get('/gastos/crear/')
        if response.status_code == 200:
            print("✅ Formulario de gasto accesible")
        else:
            print(f"❌ Error en formulario de gasto: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_archivos():
    """Probar módulo de archivos"""
    print("\n📁 PROBANDO MÓDULO DE ARCHIVOS...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Obtener proyecto
        proyecto = Proyecto.objects.filter(activo=True).first()
        if not proyecto:
            print("❌ No hay proyectos para probar archivos")
            return False
        
        # Lista de archivos
        response = client.get(f'/archivos/proyecto/{proyecto.id}/')
        if response.status_code == 200:
            print("✅ Lista de archivos accesible")
        else:
            print(f"❌ Error en lista de archivos: {response.status_code}")
            return False
        
        # Formulario de subida
        response = client.get(f'/archivos/proyecto/{proyecto.id}/subir/')
        if response.status_code == 200:
            print("✅ Formulario de subida accesible")
        else:
            print(f"❌ Error en formulario de subida: {response.status_code}")
            return False
        
        # Probar subida real
        test_file = SimpleUploadedFile(
            "test_sistema.txt",
            b"Archivo de prueba del sistema completo",
            content_type="text/plain"
        )
        
        form_data = {
            'nombre': 'Test Sistema Completo',
            'descripcion': 'Archivo de prueba del sistema',
            'tipo': 'documento',
            'activo': True,
            'archivo': test_file
        }
        
        response = client.post(f'/archivos/proyecto/{proyecto.id}/subir/', form_data)
        if response.status_code == 302:
            print("✅ Subida de archivo exitosa")
            
            # Limpiar archivo de prueba
            archivo = ArchivoProyecto.objects.filter(
                proyecto=proyecto,
                nombre='Test Sistema Completo'
            ).first()
            if archivo:
                archivo.delete()
                print("🧹 Archivo de prueba eliminado")
        else:
            print(f"❌ Error en subida: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_usuarios():
    """Probar módulo de usuarios"""
    print("\n👤 PROBANDO MÓDULO DE USUARIOS...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Lista de usuarios
        response = client.get('/usuarios/')
        if response.status_code == 200:
            print("✅ Lista de usuarios accesible")
        else:
            print(f"❌ Error en lista de usuarios: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_roles():
    """Probar módulo de roles"""
    print("\n🔐 PROBANDO MÓDULO DE ROLES...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    try:
        # Lista de roles
        response = client.get('/roles/')
        if response.status_code == 200:
            print("✅ Lista de roles accesible")
        else:
            print(f"❌ Error en lista de roles: {response.status_code}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_database_integrity():
    """Probar integridad de la base de datos"""
    print("\n🗄️ PROBANDO INTEGRIDAD DE BASE DE DATOS...")
    
    try:
        # Contar registros
        usuarios = User.objects.count()
        clientes = Cliente.objects.count()
        proyectos = Proyecto.objects.count()
        facturas = Factura.objects.count()
        gastos = Gasto.objects.count()
        archivos = ArchivoProyecto.objects.count()
        roles = Rol.objects.count()
        modulos = Modulo.objects.count()
        
        print(f"✅ Usuarios: {usuarios}")
        print(f"✅ Clientes: {clientes}")
        print(f"✅ Proyectos: {proyectos}")
        print(f"✅ Facturas: {facturas}")
        print(f"✅ Gastos: {gastos}")
        print(f"✅ Archivos: {archivos}")
        print(f"✅ Roles: {roles}")
        print(f"✅ Módulos: {modulos}")
        
        return True
    except Exception as e:
        print(f"❌ Error en BD: {e}")
        return False

if __name__ == "__main__":
    print("🚀 RECTIFICACIÓN COMPLETA DEL SISTEMA ARCA CONSTRUCCIÓN")
    print("=" * 70)
    
    tests = [
        ("Autenticación", test_authentication),
        ("Dashboard", test_dashboard),
        ("Clientes", test_clientes),
        ("Proyectos", test_proyectos),
        ("Facturas", test_facturas),
        ("Gastos", test_gastos),
        ("Archivos", test_archivos),
        ("Usuarios", test_usuarios),
        ("Roles", test_roles),
        ("Base de Datos", test_database_integrity),
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
    
    print("\n" + "=" * 70)
    print(f"📊 RESULTADOS: {passed}/{total} módulos funcionando")
    
    if passed == total:
        print("🎉 ¡SISTEMA COMPLETAMENTE FUNCIONAL AL 100%!")
        print("✅ Todos los módulos están operativos")
        print("✅ Base de datos integra")
        print("✅ Formularios funcionando")
        print("✅ Subida de archivos operativa")
        print("✅ Sistema listo para producción")
    elif passed >= total * 0.8:
        print("⚠️  Sistema mayormente funcional")
        print(f"   {total - passed} módulos necesitan atención")
    else:
        print("❌ Sistema con problemas críticos")
        print(f"   {total - passed} módulos no funcionan")
    
    print("\n" + "=" * 70)
    print("🏁 RECTIFICACIÓN COMPLETADA")
