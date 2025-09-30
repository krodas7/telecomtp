#!/usr/bin/env python3
"""
Script para probar la subida de archivos Excel
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

def test_excel_upload():
    """Probar la subida de archivos Excel"""
    print("🧪 PROBANDO SUBIDA DE ARCHIVOS EXCEL")
    print("=" * 50)
    
    # Obtener un proyecto para la prueba
    proyecto = Proyecto.objects.first()
    if not proyecto:
        print("❌ No hay proyectos disponibles para la prueba")
        return
    
    print(f"📁 Proyecto seleccionado: {proyecto.nombre}")
    
    # Crear un archivo Excel simulado
    excel_content = b"PK\x03\x04\x14\x00\x00\x00\x08\x00"  # Cabecera de archivo Excel
    excel_file = SimpleUploadedFile(
        "test_excel.xlsx",
        excel_content,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    # Datos del formulario
    form_data = {
        'nombre': 'Archivo de Prueba Excel',
        'descripcion': 'Archivo Excel de prueba para verificar la funcionalidad',
        'tipo': 'excel',
        'activo': True
    }
    
    # Crear el formulario
    form = ArchivoProyectoForm(data=form_data, files={'archivo': excel_file}, proyecto=proyecto)
    
    print("🔍 Validando formulario...")
    if form.is_valid():
        print("✅ Formulario válido - Los archivos Excel son aceptados")
        
        # Intentar guardar
        try:
            archivo = form.save(commit=False)
            archivo.proyecto = proyecto
            archivo.save()
            print(f"✅ Archivo Excel guardado exitosamente: {archivo.nombre}")
            print(f"   Tipo: {archivo.tipo}")
            print(f"   Extensión: {archivo.get_extension()}")
            print(f"   Es Excel: {archivo.es_excel()}")
            
            # Limpiar archivo de prueba
            archivo.delete()
            print("🧹 Archivo de prueba eliminado")
            
        except Exception as e:
            print(f"❌ Error al guardar: {str(e)}")
    else:
        print("❌ Formulario inválido:")
        for field, errors in form.errors.items():
            print(f"   {field}: {errors}")
    
    # Probar con diferentes extensiones de Excel
    print("\n🔍 Probando diferentes extensiones de Excel...")
    
    extensiones_excel = ['.xlsx', '.xls']
    for ext in extensiones_excel:
        excel_file = SimpleUploadedFile(
            f"test{ext}",
            excel_content,
            content_type="application/vnd.ms-excel" if ext == '.xls' else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        form_data['nombre'] = f'Archivo Excel {ext}'
        form = ArchivoProyectoForm(data=form_data, files={'archivo': excel_file}, proyecto=proyecto)
        
        if form.is_valid():
            print(f"✅ Extensión {ext} aceptada")
        else:
            print(f"❌ Extensión {ext} rechazada: {form.errors}")
    
    print("\n" + "=" * 50)
    print("✅ PRUEBA COMPLETADA")

if __name__ == "__main__":
    test_excel_upload()
