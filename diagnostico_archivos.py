#!/usr/bin/env python3
"""
Diagnóstico de archivos en la base de datos
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, ArchivoProyecto, CarpetaProyecto

def diagnosticar():
    print("🔍 Diagnóstico de archivos...")
    
    # Verificar proyectos
    proyectos = Proyecto.objects.all()
    print(f"📊 Proyectos: {proyectos.count()}")
    
    if proyectos.exists():
        proyecto = proyectos.first()
        print(f"📁 Proyecto principal: {proyecto.nombre}")
        
        # Verificar carpetas
        carpetas = CarpetaProyecto.objects.filter(proyecto=proyecto)
        print(f"📁 Carpetas: {carpetas.count()}")
        
        for carpeta in carpetas:
            print(f"  - {carpeta.nombre}")
            
            # Verificar archivos en cada carpeta
            archivos = ArchivoProyecto.objects.filter(proyecto=proyecto, carpeta=carpeta)
            print(f"    📄 Archivos: {archivos.count()}")
            
            for archivo in archivos:
                print(f"      - {archivo.nombre}")
                print(f"        ID: {archivo.id}")
                print(f"        Tiene archivo físico: {'✅' if archivo.archivo else '❌'}")
                if archivo.archivo:
                    print(f"        Tamaño: {archivo.archivo.size} bytes")
                    print(f"        Ruta: {archivo.archivo.path}")
                    print(f"        Existe archivo: {'✅' if os.path.exists(archivo.archivo.path) else '❌'}")
                    print(f"        Extensión: {archivo.get_extension()}")
                print(f"        Fecha: {archivo.fecha_subida}")
                print()

if __name__ == "__main__":
    diagnosticar()
