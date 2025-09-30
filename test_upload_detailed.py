#!/usr/bin/env python3
"""
Script de prueba detallado para subida de archivos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Proyecto, ArchivoProyecto
from core.forms_simple import ArchivoProyectoForm

def test_form_validation():
    """Probar validación del formulario"""
    print("🔍 PROBANDO VALIDACIÓN DEL FORMULARIO...")
    
    proyecto = Proyecto.objects.filter(activo=True).first()
    if not proyecto:
        print("❌ No hay proyectos")
        return False
    
    # Probar formulario vacío
    form = ArchivoProyectoForm(proyecto=proyecto)
    print(f"✅ Formulario creado: {form}")
    
    # Probar con datos válidos
    form_data = {
        'nombre': 'Test File',
        'descripcion': 'Test Description',
        'tipo': 'documento',
        'activo': True
    }
    
    form = ArchivoProyectoForm(data=form_data, proyecto=proyecto)
    print(f"✅ Formulario con datos: {form}")
    print(f"✅ Válido: {form.is_valid()}")
    
    if not form.is_valid():
        print(f"❌ Errores del formulario: {form.errors}")
        return False
    
    return True

def test_upload_with_client():
    """Probar subida con cliente de prueba"""
    print("\n📁 PROBANDO SUBIDA CON CLIENTE...")
    
    client = Client()
    client.login(username='admin', password='admin123')
    
    proyecto = Proyecto.objects.filter(activo=True).first()
    if not proyecto:
        print("❌ No hay proyectos")
        return False
    
    # Crear archivo de prueba
    test_file_content = b"Este es un archivo de prueba"
    
    # Datos del formulario
    form_data = {
        'nombre': 'Archivo de Prueba Detallado',
        'descripcion': 'Archivo creado para probar el sistema detalladamente',
        'tipo': 'documento',
        'activo': True
    }
    
    try:
        # Primero obtener el formulario GET
        response = client.get(f'/archivos/proyecto/{proyecto.id}/subir/')
        print(f"✅ GET response: {response.status_code}")
        
        # Luego hacer POST con archivo
        with open('/tmp/test_file.txt', 'wb') as f:
            f.write(test_file_content)
        
        with open('/tmp/test_file.txt', 'rb') as f:
            response = client.post(f'/archivos/proyecto/{proyecto.id}/subir/', {
                **form_data,
                'archivo': f
            })
        
        print(f"✅ POST response: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Redirección exitosa (archivo subido)")
            
            # Verificar en BD
            archivo = ArchivoProyecto.objects.filter(
                proyecto=proyecto,
                nombre='Archivo de Prueba Detallado'
            ).first()
            
            if archivo:
                print(f"✅ Archivo en BD: {archivo.nombre}")
                return True
            else:
                print("❌ Archivo no encontrado en BD")
                return False
        else:
            print(f"❌ Error en POST: {response.status_code}")
            print(f"Contenido: {response.content.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Limpiar archivo temporal
        if os.path.exists('/tmp/test_file.txt'):
            os.remove('/tmp/test_file.txt')

if __name__ == "__main__":
    print("🚀 PRUEBA DETALLADA DE SUBIDA DE ARCHIVOS")
    print("=" * 50)
    
    if test_form_validation():
        print("\n" + "=" * 30)
        if test_upload_with_client():
            print("\n🎉 SUBIDA DE ARCHIVOS FUNCIONANDO")
        else:
            print("\n❌ PROBLEMAS EN SUBIDA DE ARCHIVOS")
    else:
        print("\n❌ PROBLEMAS EN VALIDACIÓN DE FORMULARIO")
    
    print("\n" + "=" * 50)
    print("🏁 PRUEBA COMPLETADA")
