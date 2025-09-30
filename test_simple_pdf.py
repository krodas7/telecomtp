#!/usr/bin/env python3
"""
Script simple para probar el guardado de PDF
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, ArchivoProyecto, CarpetaProyecto
from django.core.files.base import ContentFile
from django.utils import timezone

def test_simple():
    print("🧪 Probando guardado simple de PDF...")
    
    # Obtener proyecto
    proyecto = Proyecto.objects.first()
    if not proyecto:
        print("❌ No hay proyectos")
        return
    
    print(f"✅ Proyecto: {proyecto.nombre}")
    
    # Crear carpeta si no existe
    carpeta, created = CarpetaProyecto.objects.get_or_create(
        proyecto=proyecto,
        nombre='Trabajadores Diarios',
        defaults={
            'creada_por_id': 1,
            'descripcion': 'Carpeta para almacenar planillas de trabajadores diarios'
        }
    )
    
    print(f"✅ Carpeta: {carpeta.nombre} ({'creada' if created else 'existente'})")
    
    # Crear contenido PDF simple
    pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF'
    
    # Crear archivo PDF
    nombre_archivo = f'test_pdf_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    archivo_pdf = ContentFile(pdf_content, name=nombre_archivo)
    
    # Asegurar que el nombre sea correcto
    archivo_pdf.name = nombre_archivo
    
    print(f"📄 Creando archivo: {nombre_archivo}")
    print(f"📄 Tamaño contenido: {len(pdf_content)} bytes")
    print(f"📄 Nombre ContentFile: {archivo_pdf.name}")
    
    try:
        archivo = ArchivoProyecto.objects.create(
            proyecto=proyecto,
            carpeta=carpeta,
            nombre=nombre_archivo,
            archivo=archivo_pdf,
            descripcion=f'PDF de prueba generado el {timezone.now().strftime("%d/%m/%Y %H:%M")}',
            subido_por_id=1,
            activo=True
        )
        
        print(f"✅ Archivo creado con ID: {archivo.id}")
        print(f"✅ Nombre en BD: {archivo.nombre}")
        print(f"✅ Tiene archivo físico: {'Sí' if archivo.archivo else 'No'}")
        
        if archivo.archivo:
            print(f"✅ Tamaño archivo: {archivo.archivo.size} bytes")
            print(f"✅ Ruta archivo: {archivo.archivo.path}")
            print(f"✅ Nombre archivo: {archivo.archivo.name}")
            print(f"✅ Extensión detectada: {archivo.get_extension()}")
            
            # Verificar que es PDF
            try:
                with open(archivo.archivo.path, 'rb') as f:
                    header = f.read(4)
                    print(f"✅ Header archivo: {header}")
                    if header == b'%PDF':
                        print("✅ Es un archivo PDF válido")
                    else:
                        print("❌ No es un archivo PDF válido")
            except Exception as e:
                print(f"❌ Error leyendo archivo: {e}")
        else:
            print("❌ El archivo no tiene contenido físico")
            
    except Exception as e:
        print(f"❌ Error creando archivo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_simple()
