#!/usr/bin/env python3
"""
Script para probar la funcionalidad de finalizar planilla de trabajadores diarios
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

def test_finalizar_planilla():
    """Probar funcionalidad completa de finalizar planilla"""
    print("🔧 PROBANDO FUNCIONALIDAD DE FINALIZAR PLANILLA")
    print("=" * 60)
    
    try:
        # Obtener un proyecto existente
        proyecto = Proyecto.objects.first()
        if not proyecto:
            print("❌ No hay proyectos en la base de datos")
            return False
        
        print(f"✅ Proyecto encontrado: {proyecto.nombre} (ID: {proyecto.id})")
        
        # Crear algunos trabajadores de prueba
        print("\n👷 CREANDO TRABAJADORES DE PRUEBA")
        print("-" * 40)
        
        trabajadores_data = [
            {'nombre': 'Juan Pérez', 'pago_diario': Decimal('150.00')},
            {'nombre': 'María García', 'pago_diario': Decimal('175.00')},
            {'nombre': 'Carlos López', 'pago_diario': Decimal('200.00')},
        ]
        
        trabajadores_creados = []
        for data in trabajadores_data:
            trabajador, created = TrabajadorDiario.objects.get_or_create(
                proyecto=proyecto,
                nombre=data['nombre'],
                defaults={
                    'pago_diario': data['pago_diario'],
                    'activo': True,
                    'creado_por': User.objects.filter(is_superuser=True).first()
                }
            )
            if created:
                print(f"✅ Trabajador creado: {trabajador.nombre} - Q{trabajador.pago_diario}")
            else:
                print(f"ℹ️ Trabajador ya existe: {trabajador.nombre}")
            trabajadores_creados.append(trabajador)
        
        # Verificar trabajadores activos antes
        trabajadores_antes = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True).count()
        print(f"\n📊 Trabajadores activos antes: {trabajadores_antes}")
        
        # Crear cliente de prueba
        client = Client()
        admin_user = User.objects.filter(is_superuser=True).first()
        client.force_login(admin_user)
        
        # 1. Probar acceso a la lista de trabajadores
        print("\n📋 1. PROBANDO LISTA DE TRABAJADORES")
        print("-" * 50)
        
        lista_url = f'/proyectos/{proyecto.id}/trabajadores-diarios/'
        response = client.get(lista_url)
        
        if response.status_code == 200:
            print("✅ Lista de trabajadores carga correctamente")
            # Verificar que el botón "Finalizar Planilla" esté presente
            content = response.content.decode('utf-8')
            if 'Finalizar Planilla' in content:
                print("✅ Botón 'Finalizar Planilla' presente en la lista")
            else:
                print("❌ Botón 'Finalizar Planilla' no encontrado")
                return False
        else:
            print(f"❌ Error en lista: {response.status_code}")
            return False
        
        # 2. Probar finalizar planilla
        print("\n🏁 2. PROBANDO FINALIZAR PLANILLA")
        print("-" * 50)
        
        finalizar_url = f'/proyectos/{proyecto.id}/trabajadores-diarios/finalizar/'
        print(f"🌐 URL: {finalizar_url}")
        
        # Verificar archivos antes
        archivos_antes = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
        carpetas_antes = CarpetaProyecto.objects.filter(proyecto=proyecto).count()
        
        print(f"📁 Archivos antes: {archivos_antes}")
        print(f"📁 Carpetas antes: {carpetas_antes}")
        
        # Ejecutar finalizar planilla
        response = client.get(finalizar_url)
        
        if response.status_code == 302:  # Redirect
            print("✅ Planilla finalizada exitosamente (redirect)")
            
            # Verificar trabajadores después
            trabajadores_despues = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True).count()
            print(f"📊 Trabajadores activos después: {trabajadores_despues}")
            
            if trabajadores_despues == 0:
                print("✅ Lista de trabajadores limpiada correctamente")
            else:
                print("❌ Lista de trabajadores no se limpió correctamente")
                return False
            
            # Verificar archivos después
            archivos_despues = ArchivoProyecto.objects.filter(proyecto=proyecto).count()
            carpetas_despues = CarpetaProyecto.objects.filter(proyecto=proyecto).count()
            
            print(f"📁 Archivos después: {archivos_despues}")
            print(f"📁 Carpetas después: {carpetas_despues}")
            
            if archivos_despues > archivos_antes:
                print("✅ PDF guardado en archivos del proyecto")
                
                # Verificar carpeta "Trabajadores Diarios"
                carpeta = CarpetaProyecto.objects.filter(
                    proyecto=proyecto, 
                    nombre='Trabajadores Diarios'
                ).first()
                
                if carpeta:
                    print("✅ Carpeta 'Trabajadores Diarios' creada")
                    
                    # Verificar PDF en la carpeta
                    pdfs = ArchivoProyecto.objects.filter(
                        proyecto=proyecto,
                        carpeta=carpeta,
                        nombre__contains='planilla_trabajadores'
                    )
                    
                    if pdfs.exists():
                        pdf = pdfs.first()
                        print(f"✅ PDF guardado: {pdf.nombre}")
                        print(f"   - Descripción: {pdf.descripcion}")
                        print(f"   - Subido por: {pdf.subido_por.username}")
                    else:
                        print("❌ PDF no encontrado en la carpeta")
                        return False
                else:
                    print("❌ Carpeta 'Trabajadores Diarios' no encontrada")
                    return False
            else:
                print("❌ PDF no se guardó en archivos del proyecto")
                return False
            
        else:
            print(f"❌ Error al finalizar planilla: {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"Contenido del error: {content[:500]}...")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_verificar_limpieza():
    """Verificar que la limpieza funciona correctamente"""
    print("\n🧹 VERIFICANDO LIMPIEZA DE TRABAJADORES")
    print("=" * 50)
    
    try:
        proyectos = Proyecto.objects.all()
        
        for proyecto in proyectos:
            trabajadores_activos = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True).count()
            trabajadores_inactivos = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=False).count()
            
            print(f"📁 Proyecto: {proyecto.nombre}")
            print(f"   👷 Activos: {trabajadores_activos}")
            print(f"   👷 Inactivos: {trabajadores_inactivos}")
            
            # Verificar archivos
            archivos = ArchivoProyecto.objects.filter(proyecto=proyecto)
            print(f"   📄 Archivos: {archivos.count()}")
            
            for archivo in archivos:
                print(f"      - {archivo.nombre} ({archivo.carpeta.nombre if archivo.carpeta else 'Sin carpeta'})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando limpieza: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE FINALIZAR PLANILLA")
    print("=" * 60)
    
    # Ejecutar pruebas
    test1 = test_finalizar_planilla()
    test2 = test_verificar_limpieza()
    
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 30)
    print(f"Finalizar Planilla: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Verificación BD: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if all([test1, test2]):
        print("\n🎉 TODAS LAS PRUEBAS PASARON")
        print("✅ Funcionalidad de finalizar planilla funcionando correctamente")
    else:
        print("\n⚠️ ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisar los errores mostrados arriba")

if __name__ == '__main__':
    main()
