#!/usr/bin/env python3
"""
Script simple para probar finalizar planilla
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Proyecto, TrabajadorDiario, ArchivoProyecto, CarpetaProyecto
from decimal import Decimal

def test_finalizar_planilla_simple():
    """Probar finalizar planilla de forma simple"""
    print("🔧 PROBANDO FINALIZAR PLANILLA - VERSIÓN SIMPLE")
    print("=" * 60)
    
    try:
        # Obtener proyecto
        proyecto = Proyecto.objects.first()
        if not proyecto:
            print("❌ No hay proyectos")
            return False
        
        print(f"✅ Proyecto: {proyecto.nombre}")
        
        # Crear trabajador de prueba
        trabajador, created = TrabajadorDiario.objects.get_or_create(
            proyecto=proyecto,
            nombre='Test Worker',
            defaults={
                'pago_diario': Decimal('100.00'),
                'activo': True,
                'creado_por': User.objects.filter(is_superuser=True).first()
            }
        )
        
        if created:
            print("✅ Trabajador de prueba creado")
        else:
            print("ℹ️ Trabajador de prueba ya existe")
        
        # Verificar trabajadores antes
        trabajadores_antes = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True).count()
        print(f"📊 Trabajadores activos antes: {trabajadores_antes}")
        
        # Crear cliente
        client = Client()
        admin_user = User.objects.filter(is_superuser=True).first()
        client.force_login(admin_user)
        
        # Probar finalizar planilla
        finalizar_url = f'/proyectos/{proyecto.id}/trabajadores-diarios/finalizar/'
        print(f"🌐 Probando: {finalizar_url}")
        
        response = client.get(finalizar_url)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Redirect exitoso")
            
            # Verificar trabajadores después
            trabajadores_despues = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True).count()
            print(f"📊 Trabajadores activos después: {trabajadores_despues}")
            
            # Verificar carpeta
            carpeta = CarpetaProyecto.objects.filter(
                proyecto=proyecto,
                nombre='Trabajadores Diarios'
            ).first()
            
            if carpeta:
                print("✅ Carpeta 'Trabajadores Diarios' creada")
                
                # Verificar PDF
                pdfs = ArchivoProyecto.objects.filter(
                    proyecto=proyecto,
                    carpeta=carpeta
                )
                
                if pdfs.exists():
                    print(f"✅ PDF creado: {pdfs.first().nombre}")
                else:
                    print("❌ PDF no encontrado")
            else:
                print("❌ Carpeta no encontrada")
            
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"Contenido: {content[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_finalizar_planilla_simple()
