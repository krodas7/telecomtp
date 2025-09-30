#!/usr/bin/env python3
"""
Script para debuggear la vista de upload
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
from core.models import Proyecto, CarpetaProyecto, ArchivoProyecto
from django.core.files.uploadedfile import SimpleUploadedFile

def debug_vista_upload():
    """Debuggear la vista de upload paso a paso"""
    print("🔍 DEBUGGEANDO VISTA DE UPLOAD")
    print("=" * 40)
    
    # Crear cliente
    client = Client()
    
    # Obtener usuario y proyecto
    admin_user = User.objects.filter(is_superuser=True).first()
    proyecto = Proyecto.objects.filter(activo=True).first()
    
    if not admin_user or not proyecto:
        print("❌ No hay usuario o proyecto")
        return
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario: {admin_user.username}")
    print(f"🏗️ Proyecto: {proyecto.nombre}")
    
    # Crear carpeta
    carpeta, created = CarpetaProyecto.objects.get_or_create(
        nombre="Debug Vista",
        proyecto=proyecto,
        defaults={
            'descripcion': 'Carpeta para debug de vista',
            'activa': True,
            'creada_por': admin_user
        }
    )
    print(f"📂 Carpeta: {carpeta.nombre}")
    
    # Contar archivos antes
    archivos_antes = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
    print(f"📁 Archivos antes: {archivos_antes}")
    
    # Crear archivo
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
    
    archivo = crear_excel("DEBUG_VISTA.xlsx")
    print(f"📄 Archivo: {archivo.name}")
    
    # Datos del formulario
    form_data = {
        'proyecto': proyecto.id,
        'nombre': 'Debug Vista Upload',
        'descripcion': 'Archivo para debug de vista',
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
    
    # Hacer petición POST
    url = f'/archivos/proyecto/{proyecto.id}/subir/'
    print(f"\n🌐 URL: {url}")
    
    try:
        response = client.post(url, data=form_data, files=files, follow=True)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Petición exitosa")
            
            # Verificar si se guardó
            archivos_despues = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
            print(f"📁 Archivos después: {archivos_despues}")
            
            if archivos_despues > archivos_antes:
                print("✅ Archivo guardado en BD")
                
                # Buscar el archivo específico
                archivo_guardado = ArchivoProyecto.objects.filter(
                    proyecto=proyecto,
                    nombre='Debug Vista Upload'
                ).first()
                
                if archivo_guardado:
                    print(f"✅ Archivo encontrado: {archivo_guardado.nombre}")
                    print(f"   ID: {archivo_guardado.id}")
                    print(f"   Archivo: {archivo_guardado.archivo.name}")
                    print(f"   Subido por: {archivo_guardado.subido_por}")
                else:
                    print("❌ Archivo no encontrado por nombre")
            else:
                print("❌ Archivo NO guardado en BD")
                
                # Verificar si hay errores en el formulario
                print(f"\n🔍 Verificando formulario...")
                from core.forms_simple import ArchivoProyectoForm
                
                form = ArchivoProyectoForm(data=form_data, files=files, proyecto=proyecto)
                print(f"📊 Formulario válido: {form.is_valid()}")
                
                if not form.is_valid():
                    print(f"❌ Errores en formulario:")
                    for field, errors in form.errors.items():
                        print(f"  {field}: {errors}")
                else:
                    print("✅ Formulario es válido")
                    
                    # Intentar guardar manualmente
                    try:
                        archivo_obj = form.save(commit=False)
                        archivo_obj.subido_por = admin_user
                        archivo_obj.save()
                        print(f"✅ Guardado manualmente: {archivo_obj.id}")
                    except Exception as e:
                        print(f"❌ Error al guardar manualmente: {e}")
        else:
            print(f"❌ Error en petición: {response.status_code}")
            print(f"Contenido: {response.content.decode()[:500]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Función principal"""
    print("🐛 DEBUG DE VISTA DE UPLOAD")
    print("=" * 35)
    
    debug_vista_upload()
    
    print(f"\n✅ DEBUG COMPLETADO")

if __name__ == "__main__":
    main()
