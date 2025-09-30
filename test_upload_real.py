#!/usr/bin/env python3
"""
Script para simular la subida real de archivos desde el navegador
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
from core.models import Proyecto, CarpetaProyecto
from django.core.files.uploadedfile import SimpleUploadedFile

def simular_upload_navegador():
    """Simular exactamente lo que hace el navegador"""
    print("🌐 SIMULANDO SUBIDA DESDE NAVEGADOR")
    print("=" * 45)
    
    # Crear cliente de prueba
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # Obtener proyecto
    proyecto = Proyecto.objects.filter(activo=True).first()
    if not proyecto:
        print("❌ No hay proyectos")
        return
    
    print(f"🏗️ Proyecto: {proyecto.nombre}")
    
    # Crear carpeta si no existe
    carpeta, created = CarpetaProyecto.objects.get_or_create(
        nombre="Archivos Generales",
        proyecto=proyecto,
        defaults={
            'descripcion': 'Carpeta para archivos generales',
            'activa': True,
            'creada_por': admin_user
        }
    )
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
        contenido += b'Test Excel Content' * 100  # Más contenido
        
        return SimpleUploadedFile(
            nombre,
            contenido,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Simular POST request como el navegador
    archivo = crear_excel_realista("PRUEBA_NAVEGADOR.xlsx")
    
    print(f"\n📤 Simulando subida de: {archivo.name}")
    
    # Datos del formulario
    form_data = {
        'proyecto': proyecto.id,
        'nombre': 'Archivo desde Navegador',
        'descripcion': 'Archivo subido simulando el navegador',
        'carpeta': carpeta.id,
        'tipo': 'documento',
        'activo': True
    }
    
    # Archivo
    files = {
        'archivo': archivo
    }
    
    # Hacer la petición POST
    url = f'/archivos/proyecto/{proyecto.id}/subir/'
    print(f"🌐 URL: {url}")
    
    try:
        response = client.post(url, data=form_data, files=files, follow=True)
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Petición exitosa")
            
            # Verificar si se guardó en la BD
            from core.models import ArchivoProyecto
            archivos_ahora = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
            print(f"📁 Archivos en BD ahora: {archivos_ahora}")
            
            # Buscar el archivo específico
            archivo_guardado = ArchivoProyecto.objects.filter(
                proyecto=proyecto,
                nombre='Archivo desde Navegador'
            ).first()
            
            if archivo_guardado:
                print(f"✅ Archivo guardado en BD: {archivo_guardado.nombre}")
                print(f"   Archivo físico: {archivo_guardado.archivo.name}")
                print(f"   Subido por: {archivo_guardado.subido_por}")
            else:
                print("❌ Archivo NO guardado en BD")
                
        else:
            print(f"❌ Error en petición: {response.status_code}")
            print(f"Contenido: {response.content.decode()[:500]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def verificar_archivos_despues():
    """Verificar archivos después de la subida"""
    print(f"\n🔍 VERIFICACIÓN POST-SUBIDA")
    print("=" * 30)
    
    from core.models import ArchivoProyecto, Proyecto
    
    # Contar archivos
    total_archivos = ArchivoProyecto.objects.count()
    print(f"📁 Total archivos en BD: {total_archivos}")
    
    # Archivos del proyecto
    proyecto = Proyecto.objects.filter(activo=True).first()
    if proyecto:
        archivos_proyecto = ArchivoProyecto.objects.filter(proyecto=proyecto, activo=True)
        print(f"🏗️ Archivos en proyecto '{proyecto.nombre}': {archivos_proyecto.count()}")
        
        for archivo in archivos_proyecto:
            print(f"  📄 {archivo.nombre} ({archivo.archivo.name})")

def main():
    """Función principal"""
    print("🧪 SIMULACIÓN DE SUBIDA DESDE NAVEGADOR")
    print("=" * 50)
    
    simular_upload_navegador()
    verificar_archivos_despues()
    
    print(f"\n✅ SIMULACIÓN COMPLETADA")

if __name__ == "__main__":
    main()
