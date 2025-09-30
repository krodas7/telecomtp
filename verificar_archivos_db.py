#!/usr/bin/env python3
"""
Script para verificar archivos en la base de datos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import ArchivoProyecto, Proyecto
from django.db.models import Count

def verificar_archivos():
    """Verificar archivos en la base de datos"""
    print("🔍 VERIFICANDO ARCHIVOS EN LA BASE DE DATOS")
    print("=" * 50)
    
    # Contar archivos totales
    total_archivos = ArchivoProyecto.objects.count()
    print(f"📁 Total de archivos en BD: {total_archivos}")
    
    # Archivos por proyecto
    proyectos_con_archivos = Proyecto.objects.annotate(
        num_archivos=Count('archivos')
    ).filter(num_archivos__gt=0)
    
    print(f"\n📊 ARCHIVOS POR PROYECTO:")
    for proyecto in proyectos_con_archivos:
        print(f"  🏗️ {proyecto.nombre}: {proyecto.num_archivos} archivos")
        
        # Mostrar archivos del proyecto
        archivos = ArchivoProyecto.objects.filter(proyecto=proyecto, activo=True)
        for archivo in archivos:
            print(f"    📄 {archivo.nombre} ({archivo.archivo.name})")
            print(f"       Tipo: {archivo.tipo}")
            print(f"       Subido por: {archivo.subido_por}")
            print(f"       Fecha: {archivo.fecha_subida}")
            print(f"       Activo: {archivo.activo}")
            print()
    
    # Verificar archivos recientes
    print(f"🕒 ARCHIVOS RECIENTES (últimos 5):")
    archivos_recientes = ArchivoProyecto.objects.filter(activo=True).order_by('-fecha_subida')[:5]
    for archivo in archivos_recientes:
        print(f"  📄 {archivo.nombre}")
        print(f"     Proyecto: {archivo.proyecto.nombre}")
        print(f"     Archivo: {archivo.archivo.name}")
        print(f"     Fecha: {archivo.fecha_subida}")
        print()

def verificar_archivos_fisicos():
    """Verificar archivos físicos en el servidor"""
    print(f"\n💾 VERIFICANDO ARCHIVOS FÍSICOS")
    print("=" * 35)
    
    import os
    from django.conf import settings
    
    media_root = settings.MEDIA_ROOT
    print(f"📁 Directorio media: {media_root}")
    
    # Verificar si existe
    if os.path.exists(media_root):
        print("✅ Directorio media existe")
        
        # Contar archivos
        archivos_fisicos = []
        for root, dirs, files in os.walk(media_root):
            for file in files:
                archivos_fisicos.append(os.path.join(root, file))
        
        print(f"📊 Total archivos físicos: {len(archivos_fisicos)}")
        
        # Mostrar algunos archivos
        print(f"\n📄 Algunos archivos físicos:")
        for archivo in archivos_fisicos[:10]:  # Mostrar solo los primeros 10
            print(f"  {archivo}")
    else:
        print("❌ Directorio media no existe")

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO DE ARCHIVOS")
    print("=" * 30)
    
    verificar_archivos()
    verificar_archivos_fisicos()
    
    print(f"\n✅ DIAGNÓSTICO COMPLETADO")

if __name__ == "__main__":
    main()
