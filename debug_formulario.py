#!/usr/bin/env python3
"""
Script para debuggear el formulario de archivos
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

def debug_formulario():
    """Debuggear el formulario de archivos"""
    print("🔍 DEBUGGEANDO FORMULARIO DE ARCHIVOS")
    print("=" * 45)
    
    # Obtener proyecto y usuario
    proyecto = Proyecto.objects.filter(activo=True).first()
    admin_user = User.objects.filter(is_superuser=True).first()
    
    if not proyecto or not admin_user:
        print("❌ No hay proyecto o usuario admin")
        return
    
    # Crear carpeta
    carpeta, created = CarpetaProyecto.objects.get_or_create(
        nombre="Debug",
        proyecto=proyecto,
        defaults={
            'descripcion': 'Carpeta para debug',
            'activa': True,
            'creada_por': admin_user
        }
    )
    
    print(f"🏗️ Proyecto: {proyecto.nombre}")
    print(f"📂 Carpeta: {carpeta.nombre}")
    
    # Crear archivo Excel
    def crear_excel(nombre):
        contenido = b'\x50\x4B\x03\x04\x14\x00\x00\x00\x08\x00'
        contenido += b'[Content_Types].xml'
        contenido += b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        contenido += b'<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        contenido += b'<Default Extension="xml" ContentType="application/xml"/>'
        contenido += b'<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
        contenido += b'</Types>'
        contenido += b'Test Excel Content' * 50
        
        return SimpleUploadedFile(
            nombre,
            contenido,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Crear archivo
    archivo = crear_excel("DEBUG_TEST.xlsx")
    print(f"📄 Archivo creado: {archivo.name}")
    
    # Datos del formulario
    form_data = {
        'proyecto': proyecto.id,
        'nombre': 'Test Debug',
        'descripcion': 'Archivo de prueba para debug',
        'carpeta': carpeta.id,
        'tipo': 'documento',
        'activo': True
    }
    
    files = {
        'archivo': archivo
    }
    
    print(f"\n📝 Datos del formulario:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Crear formulario
    print(f"\n🔧 Creando formulario...")
    form = ArchivoProyectoForm(data=form_data, files=files, proyecto=proyecto)
    
    print(f"✅ Formulario creado")
    print(f"📊 Válido: {form.is_valid()}")
    
    if not form.is_valid():
        print(f"\n❌ ERRORES EN EL FORMULARIO:")
        for field, errors in form.errors.items():
            print(f"  {field}: {errors}")
    else:
        print(f"\n✅ FORMULARIO VÁLIDO")
        
        # Intentar guardar
        print(f"\n💾 Intentando guardar...")
        try:
            archivo_obj = form.save(commit=False)
            print(f"✅ Objeto creado: {archivo_obj}")
            
            archivo_obj.proyecto = proyecto
            archivo_obj.subido_por = admin_user
            print(f"✅ Campos asignados")
            
            archivo_obj.save()
            print(f"✅ Archivo guardado en BD: {archivo_obj.id}")
            print(f"   Nombre: {archivo_obj.nombre}")
            print(f"   Archivo: {archivo_obj.archivo.name}")
            
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Función principal"""
    print("🐛 DEBUG DE FORMULARIO DE ARCHIVOS")
    print("=" * 40)
    
    debug_formulario()
    
    print(f"\n✅ DEBUG COMPLETADO")

if __name__ == "__main__":
    main()
