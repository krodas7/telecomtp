#!/usr/bin/env python3
"""
Script para probar que el PDF se guarde correctamente en archivos
"""

import os
import sys
import django
import requests
from io import BytesIO

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, ArchivoProyecto, CarpetaProyecto, TrabajadorDiario
from django.contrib.auth.models import User

def test_pdf_guardado():
    print("🧪 Probando guardado automático de PDF...")
    
    # Obtener proyecto y trabajadores
    proyecto = Proyecto.objects.first()
    if not proyecto:
        print("❌ No hay proyectos en la base de datos")
        return
    
    trabajadores = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True)
    if not trabajadores.exists():
        print("❌ No hay trabajadores diarios activos")
        return
    
    print(f"✅ Proyecto: {proyecto.nombre}")
    print(f"✅ Trabajadores activos: {trabajadores.count()}")
    
    # Simular datos de días trabajados
    dias_data = {}
    for trabajador in trabajadores:
        dias_data[f'dias_trabajador_{trabajador.id}'] = 5  # 5 días para cada uno
    
    # Hacer petición POST para generar PDF
    url = f"http://localhost:8000/proyectos/{proyecto.id}/trabajadores-diarios/pdf/"
    
    try:
        response = requests.post(url, data=dias_data, timeout=30)
        
        if response.status_code == 200:
            print("✅ PDF generado exitosamente")
            
            # Verificar que se guardó en archivos
            carpeta = CarpetaProyecto.objects.filter(
                proyecto=proyecto, 
                nombre='Trabajadores Diarios'
            ).first()
            
            if carpeta:
                archivos = ArchivoProyecto.objects.filter(
                    proyecto=proyecto, 
                    carpeta=carpeta
                ).order_by('-fecha_subida')
                
                print(f"📁 Archivos en carpeta: {archivos.count()}")
                
                # Verificar el último archivo
                if archivos.exists():
                    ultimo_archivo = archivos.first()
                    print(f"📄 Último archivo: {ultimo_archivo.nombre}")
                    print(f"📄 Extensión: {ultimo_archivo.get_extension()}")
                    print(f"📄 Tiene archivo físico: {'✅' if ultimo_archivo.archivo else '❌'}")
                    
                    if ultimo_archivo.archivo:
                        print(f"📄 Tamaño: {ultimo_archivo.archivo.size} bytes")
                        print(f"📄 Ruta: {ultimo_archivo.archivo.path}")
                        
                        # Verificar que es realmente un PDF
                        try:
                            with open(ultimo_archivo.archivo.path, 'rb') as f:
                                header = f.read(4)
                                if header == b'%PDF':
                                    print("✅ Es un archivo PDF válido")
                                else:
                                    print("❌ No es un archivo PDF válido")
                        except Exception as e:
                            print(f"❌ Error leyendo archivo: {e}")
                    else:
                        print("❌ El archivo no tiene contenido físico")
                else:
                    print("❌ No hay archivos en la carpeta")
            else:
                print("❌ No se encontró la carpeta 'Trabajadores Diarios'")
        else:
            print(f"❌ Error generando PDF: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_pdf_guardado()
