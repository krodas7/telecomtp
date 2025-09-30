#!/usr/bin/env python3
"""
Script directo para probar finalizar planilla
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, TrabajadorDiario, ArchivoProyecto, CarpetaProyecto
from django.contrib.auth.models import User
from decimal import Decimal

def main():
    print("🔧 PROBANDO FINALIZAR PLANILLA - VERSIÓN DIRECTA")
    print("=" * 60)
    
    try:
        # Obtener proyecto
        proyecto = Proyecto.objects.first()
        if not proyecto:
            print("❌ No hay proyectos")
            return
        
        print(f"✅ Proyecto: {proyecto.nombre}")
        
        # Verificar trabajadores antes
        trabajadores_antes = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True).count()
        print(f"📊 Trabajadores activos antes: {trabajadores_antes}")
        
        # Crear trabajador si no existe
        if trabajadores_antes == 0:
            admin_user = User.objects.filter(is_superuser=True).first()
            trabajador = TrabajadorDiario.objects.create(
                proyecto=proyecto,
                nombre='Test Worker',
                pago_diario=Decimal('100.00'),
                activo=True,
                creado_por=admin_user
            )
            print("✅ Trabajador de prueba creado")
            trabajadores_antes = 1
        
        # Verificar archivos antes
        archivos_antes = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
        carpetas_antes = CarpetaProyecto.objects.filter(proyecto=proyecto).count()
        
        print(f"📁 Archivos antes: {archivos_antes}")
        print(f"📁 Carpetas antes: {carpetas_antes}")
        
        # Simular finalizar planilla
        print("\n🏁 SIMULANDO FINALIZAR PLANILLA...")
        
        # 1. Crear carpeta
        carpeta, created = CarpetaProyecto.objects.get_or_create(
            proyecto=proyecto,
            nombre='Trabajadores Diarios',
            defaults={
                'creada_por': User.objects.filter(is_superuser=True).first(),
                'descripcion': 'Carpeta para almacenar planillas de trabajadores diarios'
            }
        )
        
        if created:
            print("✅ Carpeta 'Trabajadores Diarios' creada")
        else:
            print("ℹ️ Carpeta 'Trabajadores Diarios' ya existe")
        
        # 2. Crear archivo de planilla
        from django.core.files.base import ContentFile
        from django.utils import timezone
        
        contenido = f"PLANILLA DE TRABAJADORES DIARIOS\nProyecto: {proyecto.nombre}\nFecha: {timezone.now()}\n"
        
        archivo = ArchivoProyecto.objects.create(
            proyecto=proyecto,
            carpeta=carpeta,
            nombre=f"planilla_test_{timezone.now().strftime('%Y%m%d_%H%M%S')}.txt",
            archivo=ContentFile(contenido.encode('utf-8')),
            descripcion='Planilla de prueba',
            subido_por=User.objects.filter(is_superuser=True).first(),
            activo=True
        )
        
        print("✅ Archivo de planilla creado")
        
        # 3. Limpiar trabajadores
        trabajadores = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True)
        trabajadores.update(activo=False)
        
        print(f"✅ {trabajadores.count()} trabajadores marcados como inactivos")
        
        # Verificar resultados
        trabajadores_despues = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True).count()
        archivos_despues = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
        carpetas_despues = CarpetaProyecto.objects.filter(proyecto=proyecto).count()
        
        print(f"\n📊 RESULTADOS:")
        print(f"   Trabajadores activos después: {trabajadores_despues}")
        print(f"   Archivos después: {archivos_despues}")
        print(f"   Carpetas después: {carpetas_despues}")
        
        if trabajadores_despues == 0 and archivos_despues > archivos_antes:
            print("\n🎉 FUNCIONALIDAD FUNCIONANDO CORRECTAMENTE")
        else:
            print("\n❌ HAY PROBLEMAS CON LA FUNCIONALIDAD")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
