#!/usr/bin/env python3
"""
Script de prueba para verificar el módulo de archivos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Proyecto, Cliente, ArchivoProyecto, CarpetaProyecto

def test_archivos_module():
    """Probar el módulo de archivos"""
    print("🔍 PROBANDO MÓDULO DE ARCHIVOS...")
    
    # Crear cliente de prueba
    client = Client()
    
    # Obtener usuario admin
    try:
        admin_user = User.objects.get(username='admin')
        print(f"✅ Usuario admin encontrado: {admin_user.username}")
    except User.DoesNotExist:
        print("❌ Usuario admin no encontrado")
        return False
    
    # Obtener proyecto de prueba
    try:
        proyecto = Proyecto.objects.filter(activo=True).first()
        if not proyecto:
            print("❌ No hay proyectos activos")
            return False
        print(f"✅ Proyecto encontrado: {proyecto.nombre}")
    except Exception as e:
        print(f"❌ Error obteniendo proyecto: {e}")
        return False
    
    # Probar login
    login_success = client.login(username='admin', password='admin123')
    if not login_success:
        print("❌ Error en login")
        return False
    print("✅ Login exitoso")
    
    # Probar acceso a lista de archivos
    try:
        response = client.get(f'/archivos/proyecto/{proyecto.id}/')
        if response.status_code == 200:
            print("✅ Lista de archivos accesible")
        else:
            print(f"❌ Error en lista de archivos: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accediendo a lista de archivos: {e}")
        return False
    
    # Probar acceso a formulario de subida
    try:
        response = client.get(f'/archivos/proyecto/{proyecto.id}/subir/')
        if response.status_code == 200:
            print("✅ Formulario de subida accesible")
        else:
            print(f"❌ Error en formulario de subida: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accediendo a formulario de subida: {e}")
        return False
    
    # Probar creación de carpeta
    try:
        response = client.get(f'/archivos/proyecto/{proyecto.id}/carpeta/crear/')
        if response.status_code == 200:
            print("✅ Formulario de carpeta accesible")
        else:
            print(f"❌ Error en formulario de carpeta: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accediendo a formulario de carpeta: {e}")
        return False
    
    print("✅ MÓDULO DE ARCHIVOS FUNCIONANDO CORRECTAMENTE")
    return True

def test_upload_file():
    """Probar subida de archivo"""
    print("\n📁 PROBANDO SUBIDA DE ARCHIVO...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    # Obtener proyecto
    proyecto = Proyecto.objects.filter(activo=True).first()
    if not proyecto:
        print("❌ No hay proyectos para probar")
        return False
    
    # Crear archivo de prueba
    test_file_content = b"Este es un archivo de prueba"
    test_file = {
        'archivo': ('test.txt', test_file_content, 'text/plain')
    }
    
    # Datos del formulario
    form_data = {
        'nombre': 'Archivo de Prueba',
        'descripcion': 'Archivo creado para probar el sistema',
        'tipo': 'documento',
        'activo': True
    }
    
    try:
        response = client.post(f'/archivos/proyecto/{proyecto.id}/subir/', {
            **form_data,
            **test_file
        })
        
        if response.status_code == 302:  # Redirect after successful upload
            print("✅ Archivo subido exitosamente")
            
            # Verificar que el archivo se creó en la base de datos
            archivo = ArchivoProyecto.objects.filter(
                proyecto=proyecto,
                nombre='Archivo de Prueba'
            ).first()
            
            if archivo:
                print(f"✅ Archivo guardado en BD: {archivo.nombre}")
                return True
            else:
                print("❌ Archivo no encontrado en BD")
                return False
        else:
            print(f"❌ Error en subida: {response.status_code}")
            if hasattr(response, 'content'):
                print(f"Contenido de respuesta: {response.content.decode()[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error en subida de archivo: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS DEL MÓDULO DE ARCHIVOS")
    print("=" * 50)
    
    # Probar módulo básico
    if test_archivos_module():
        print("\n" + "=" * 50)
        # Probar subida de archivo
        if test_upload_file():
            print("\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
            print("✅ El módulo de archivos está funcionando al 100%")
        else:
            print("\n⚠️  Hay problemas con la subida de archivos")
    else:
        print("\n❌ HAY PROBLEMAS CRÍTICOS EN EL MÓDULO DE ARCHIVOS")
    
    print("\n" + "=" * 50)
    print("🏁 PRUEBAS COMPLETADAS")
