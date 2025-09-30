#!/usr/bin/env python3
"""
Script final para probar la subida de archivos Excel
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

def probar_excel_final():
    """Prueba final de archivos Excel"""
    print("🧪 PRUEBA FINAL DE ARCHIVOS EXCEL")
    print("=" * 40)
    
    # Obtener proyecto y usuario
    proyecto = Proyecto.objects.filter(activo=True).first()
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not proyecto or not admin_user:
        print("❌ No hay proyecto o usuario admin disponible")
        return
    
    # Crear carpeta
    carpeta, created = CarpetaProyecto.objects.get_or_create(
        nombre="Pruebas Excel",
        proyecto=proyecto,
        defaults={
            'descripcion': 'Carpeta para pruebas de Excel', 
            'activa': True,
            'creada_por': admin_user
        }
    )
    
    print(f"📁 Proyecto: {proyecto.nombre}")
    print(f"📂 Carpeta: {carpeta.nombre}")
    
    # Crear archivo Excel realista
    def crear_excel_realista(nombre):
        # Crear un archivo Excel más realista
        contenido = b'\x50\x4B\x03\x04\x14\x00\x00\x00\x08\x00'  # Cabecera ZIP
        contenido += b'[Content_Types].xml'  # Contenido típico de Excel
        contenido += b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        contenido += b'<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        contenido += b'<Default Extension="xml" ContentType="application/xml"/>'
        contenido += b'<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        contenido += b'</Types>'
        contenido += b'Test Excel Content' * 50  # Más contenido
        
        return SimpleUploadedFile(
            nombre,
            contenido,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Probar archivos Excel
    archivos_excel = [
        'planilla_trabajo.xlsx',
        'presupuesto_materiales.xls',
        'cronograma_proyecto.XLSX',
        'lista_precios.XLS'
    ]
    
    print(f"\n🔍 PROBANDO ARCHIVOS EXCEL:")
    for nombre_archivo in archivos_excel:
        print(f"\n📄 Probando: {nombre_archivo}")
        
        # Crear archivo
        archivo = crear_excel_realista(nombre_archivo)
        
        # Crear formulario
        form_data = {
            'nombre': f'Test {nombre_archivo}',
            'descripcion': f'Archivo Excel de prueba: {nombre_archivo}',
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
            
            # Intentar guardar
            try:
                archivo_obj = form.save(commit=False)
                archivo_obj.proyecto = proyecto
                archivo_obj.subido_por = admin_user
                archivo_obj.save()
                print(f"  💾 GUARDADO: {archivo_obj.nombre}")
            except Exception as e:
                print(f"  ❌ ERROR AL GUARDAR: {e}")
        else:
            print(f"  ❌ INVÁLIDO: {nombre_archivo}")
            for field, errors in form.errors.items():
                print(f"    {field}: {errors}")
    
    print(f"\n✅ PRUEBA FINAL COMPLETADA")
    print("🌐 Ahora puedes probar en el navegador:")
    print(f"   1. Ve a: http://localhost:8000/archivos/proyecto/{proyecto.id}/")
    print(f"   2. Haz clic en 'Subir Archivo'")
    print(f"   3. Selecciona un archivo Excel (.xls o .xlsx)")
    print(f"   4. ¡Debería funcionar correctamente!")

if __name__ == "__main__":
    probar_excel_final()
