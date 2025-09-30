#!/usr/bin/env python3
"""
Script para probar la subida de archivos Excel
"""

import os
import sys
import django
from io import BytesIO

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.forms_simple import ArchivoProyectoForm
from core.models import Proyecto, CarpetaProyecto
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

def crear_archivo_excel_falso():
    """Crear un archivo Excel falso para probar"""
    # Crear contenido falso de Excel (solo para prueba)
    contenido = b'\x50\x4B\x03\x04\x14\x00\x00\x00\x08\x00'  # Cabecera ZIP/Excel
    contenido += b'Test Excel File Content' * 100  # Contenido de prueba
    
    archivo = SimpleUploadedFile(
        "test_excel.xlsx",
        contenido,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    return archivo

def probar_validacion_excel():
    """Probar la validación de archivos Excel"""
    print("🧪 PROBANDO VALIDACIÓN DE ARCHIVOS EXCEL")
    print("=" * 50)
    
    # Obtener un proyecto
    proyecto = Proyecto.objects.filter(activo=True).first()
    if not proyecto:
        print("❌ No hay proyectos disponibles")
        return
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin disponible")
        return
    
    # Crear carpeta de prueba
    carpeta, created = CarpetaProyecto.objects.get_or_create(
        nombre="Pruebas",
        proyecto=proyecto,
        defaults={
            'descripcion': 'Carpeta para pruebas', 
            'activa': True,
            'creada_por': admin_user
        }
    )
    
    print(f"📁 Proyecto: {proyecto.nombre}")
    print(f"📂 Carpeta: {carpeta.nombre}")
    
    # Probar diferentes extensiones de Excel
    extensiones_excel = [
        'test.xlsx',
        'test.xls', 
        'test.XLSX',  # Mayúsculas
        'test.XLS',   # Mayúsculas
        'documento_excel.xlsx',
        'planilla_trabajo.xls'
    ]
    
    for nombre_archivo in extensiones_excel:
        print(f"\n🔍 Probando: {nombre_archivo}")
        
        # Crear archivo falso
        archivo = crear_archivo_excel_falso()
        archivo.name = nombre_archivo
        
        # Crear formulario
        form_data = {
            'nombre': f'Test {nombre_archivo}',
            'descripcion': 'Archivo de prueba',
            'carpeta': carpeta.id,
            'tipo': 'documento',
            'activo': True
        }
        
        form = ArchivoProyectoForm(
            data=form_data,
            files={'archivo': archivo},
            proyecto=proyecto
        )
        
        if form.is_valid():
            print(f"  ✅ VÁLIDO: {nombre_archivo}")
        else:
            print(f"  ❌ INVÁLIDO: {nombre_archivo}")
            for field, errors in form.errors.items():
                print(f"    {field}: {errors}")
    
    # Probar archivos no permitidos
    print(f"\n🚫 PROBANDO ARCHIVOS NO PERMITIDOS:")
    archivos_no_permitidos = [
        'test.exe',
        'test.bat',
        'test.com',
        'test.scr'
    ]
    
    for nombre_archivo in archivos_no_permitidos:
        print(f"\n🔍 Probando: {nombre_archivo}")
        
        archivo = crear_archivo_excel_falso()
        archivo.name = nombre_archivo
        
        form_data = {
            'nombre': f'Test {nombre_archivo}',
            'descripcion': 'Archivo de prueba',
            'carpeta': carpeta.id,
            'tipo': 'documento',
            'activo': True
        }
        
        form = ArchivoProyectoForm(
            data=form_data,
            files={'archivo': archivo},
            proyecto=proyecto
        )
        
        if form.is_valid():
            print(f"  ⚠️ VÁLIDO (no debería serlo): {nombre_archivo}")
        else:
            print(f"  ✅ CORRECTAMENTE RECHAZADO: {nombre_archivo}")

def verificar_configuracion_archivos():
    """Verificar la configuración de archivos en settings"""
    print(f"\n⚙️ VERIFICANDO CONFIGURACIÓN DE ARCHIVOS")
    print("=" * 45)
    
    from django.conf import settings
    
    # Verificar FILE_UPLOAD_MAX_MEMORY_SIZE
    max_memory = getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 'No configurado')
    print(f"📏 FILE_UPLOAD_MAX_MEMORY_SIZE: {max_memory}")
    
    # Verificar DATA_UPLOAD_MAX_MEMORY_SIZE
    data_max = getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 'No configurado')
    print(f"📏 DATA_UPLOAD_MAX_MEMORY_SIZE: {data_max}")
    
    # Verificar MEDIA_ROOT
    media_root = getattr(settings, 'MEDIA_ROOT', 'No configurado')
    print(f"📁 MEDIA_ROOT: {media_root}")
    
    # Verificar MEDIA_URL
    media_url = getattr(settings, 'MEDIA_URL', 'No configurado')
    print(f"🌐 MEDIA_URL: {media_url}")

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO DE SUBIDA DE ARCHIVOS EXCEL")
    print("=" * 55)
    
    verificar_configuracion_archivos()
    probar_validacion_excel()
    
    print(f"\n✅ DIAGNÓSTICO COMPLETADO")
    print("💡 Si los archivos Excel son válidos pero no se suben,")
    print("   el problema puede estar en la vista o en la configuración del servidor")

if __name__ == "__main__":
    main()
