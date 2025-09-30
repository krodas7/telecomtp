#!/usr/bin/env python3
"""
Script para probar la eliminación de archivos
"""

import os
import sys
import django
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, ArchivoProyecto
from core.forms_simple import ArchivoProyectoForm
from django.contrib.auth.models import User

def test_file_deletion():
    """Probar la eliminación de archivos"""
    print("🧪 PROBANDO ELIMINACIÓN DE ARCHIVOS")
    print("=" * 50)
    
    # Obtener un proyecto y usuario para la prueba
    proyecto = Proyecto.objects.first()
    user = User.objects.first()
    
    if not proyecto or not user:
        print("❌ No hay proyectos o usuarios disponibles para la prueba")
        return
    
    print(f"📁 Proyecto: {proyecto.nombre}")
    print(f"👤 Usuario: {user.username}")
    
    # Crear un archivo de prueba
    excel_content = b"PK\x03\x04\x14\x00\x00\x00\x08\x00"  # Cabecera de archivo Excel
    excel_file = SimpleUploadedFile(
        "test_delete.xlsx",
        excel_content,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # Datos del formulario
    form_data = {
        'nombre': 'Archivo para Eliminar',
        'descripcion': 'Archivo de prueba para verificar eliminación',
        'tipo': 'excel',
        'activo': True
    }
    
    # Crear el formulario y guardar archivo
    form = ArchivoProyectoForm(data=form_data, files={'archivo': excel_file}, proyecto=proyecto)
    
    if form.is_valid():
        archivo = form.save(commit=False)
        archivo.proyecto = proyecto
        archivo.subido_por = user
        archivo.save()
        
        print(f"✅ Archivo creado: {archivo.nombre} (ID: {archivo.id})")
        
        # Verificar que el archivo existe
        archivos_antes = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
        print(f"📊 Archivos antes de eliminar: {archivos_antes}")
        
        # Simular la eliminación
        print("🗑️  Eliminando archivo...")
        try:
            # Obtener el ID del proyecto antes de eliminar
            proyecto_id = archivo.proyecto.id
            
            # Eliminar el archivo
            archivo.delete()
            
            # Verificar que se eliminó
            archivos_despues = ArchivoProyecto.objects.filter(proyecto_id=proyecto_id).count()
            print(f"📊 Archivos después de eliminar: {archivos_despues}")
            
            if archivos_despues < archivos_antes:
                print("✅ Archivo eliminado exitosamente")
            else:
                print("❌ El archivo no se eliminó correctamente")
                
        except Exception as e:
            print(f"❌ Error al eliminar: {str(e)}")
    else:
        print("❌ Error creando archivo de prueba:")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")

def test_confirmation_validation():
    """Probar la validación de confirmación"""
    print("\n🔍 PROBANDO VALIDACIÓN DE CONFIRMACIÓN")
    print("=" * 50)
    
    # Simular diferentes valores de confirmación
    test_cases = [
        ("ELIMINAR", True, "Confirmación correcta"),
        ("eliminar", True, "Confirmación en minúsculas"),
        ("Eliminar", True, "Confirmación con mayúscula inicial"),
        ("ELIMINAR ", True, "Confirmación con espacio al final"),
        (" ELIMINAR", True, "Confirmación con espacio al inicio"),
        ("BORRAR", False, "Palabra incorrecta"),
        ("", False, "Campo vacío"),
        ("ELIMINAR123", False, "Confirmación con números"),
    ]
    
    for confirmacion, esperado, descripcion in test_cases:
        # Simular la validación
        confirmacion_clean = confirmacion.strip().upper()
        es_valido = confirmacion_clean == 'ELIMINAR'
        
        status = "✅" if es_valido == esperado else "❌"
        resultado = "VÁLIDO" if es_valido else "INVÁLIDO"
        
        print(f"{status} {descripcion}: '{confirmacion}' -> {resultado}")

if __name__ == "__main__":
    test_file_deletion()
    test_confirmation_validation()
    
    print("\n" + "=" * 50)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 50)
    print("🌐 Para probar en el navegador:")
    print("  1. Ve a: http://localhost:8000/")
    print("  2. Inicia sesión con: admin / admin123")
    print("  3. Ve a Archivos → Selecciona un proyecto")
    print("  4. Intenta eliminar un archivo")
    print("  5. Escribe 'ELIMINAR' para confirmar")
