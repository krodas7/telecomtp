#!/usr/bin/env python3
"""
Script para probar la funcionalidad de trabajadores diarios
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Proyecto, TrabajadorDiario
from decimal import Decimal

def test_trabajadores_diarios():
    """Probar funcionalidad completa de trabajadores diarios"""
    print("🔧 PROBANDO FUNCIONALIDAD DE TRABAJADORES DIARIOS")
    print("=" * 60)
    
    try:
        # Obtener un proyecto existente
        proyecto = Proyecto.objects.first()
        if not proyecto:
            print("❌ No hay proyectos en la base de datos")
            return False
        
        print(f"✅ Proyecto encontrado: {proyecto.nombre} (ID: {proyecto.id})")
        
        # Crear cliente de prueba
        client = Client()
        
        # Obtener usuario admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No hay usuario admin")
            return False
        
        # Autenticar
        client.force_login(admin_user)
        print(f"✅ Usuario autenticado: {admin_user.username}")
        
        # 1. Probar acceso a la lista de trabajadores diarios
        print("\n📋 1. PROBANDO LISTA DE TRABAJADORES DIARIOS")
        print("-" * 50)
        
        lista_url = f'/proyectos/{proyecto.id}/trabajadores-diarios/'
        print(f"🌐 URL: {lista_url}")
        
        response = client.get(lista_url)
        if response.status_code == 200:
            print("✅ Lista de trabajadores diarios carga correctamente")
        else:
            print(f"❌ Error en lista: {response.status_code}")
            return False
        
        # 2. Probar acceso al formulario de creación
        print("\n📝 2. PROBANDO FORMULARIO DE CREACIÓN")
        print("-" * 50)
        
        crear_url = f'/proyectos/{proyecto.id}/trabajadores-diarios/crear/'
        print(f"🌐 URL: {crear_url}")
        
        response = client.get(crear_url)
        if response.status_code == 200:
            print("✅ Formulario de creación carga correctamente")
        else:
            print(f"❌ Error en formulario: {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                if 'TemplateSyntaxError' in content:
                    print("❌ Error de sintaxis en template")
                print(f"Contenido del error: {content[:500]}...")
            return False
        
        # 3. Probar creación de trabajador diario
        print("\n👷 3. PROBANDO CREACIÓN DE TRABAJADOR DIARIO")
        print("-" * 50)
        
        # Contar trabajadores antes
        trabajadores_antes = TrabajadorDiario.objects.filter(proyecto=proyecto).count()
        print(f"📊 Trabajadores antes: {trabajadores_antes}")
        
        # Datos del formulario
        form_data = {
            'nombre': 'Juan Pérez',
            'pago_diario': '150.00',
            'activo': True
        }
        
        print(f"📝 Datos del formulario: {form_data}")
        
        # Enviar POST
        response = client.post(crear_url, form_data)
        
        if response.status_code == 302:  # Redirect
            print("✅ Trabajador diario creado exitosamente (redirect)")
            
            # Verificar que se guardó en la BD
            trabajadores_despues = TrabajadorDiario.objects.filter(proyecto=proyecto).count()
            print(f"📊 Trabajadores después: {trabajadores_despues}")
            
            if trabajadores_despues > trabajadores_antes:
                print("✅ Trabajador guardado en la base de datos")
                
                # Verificar datos específicos
                trabajador = TrabajadorDiario.objects.filter(
                    proyecto=proyecto, 
                    nombre='Juan Pérez'
                ).first()
                
                if trabajador:
                    print(f"✅ Datos verificados:")
                    print(f"   - Nombre: {trabajador.nombre}")
                    print(f"   - Pago diario: Q{trabajador.pago_diario}")
                    print(f"   - Proyecto: {trabajador.proyecto.nombre}")
                    print(f"   - Activo: {trabajador.activo}")
                    print(f"   - Creado por: {trabajador.creado_por.username}")
                else:
                    print("❌ Trabajador no encontrado en la BD")
                    return False
            else:
                print("❌ Trabajador no se guardó en la BD")
                return False
        else:
            print(f"❌ Error en creación: {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"Contenido del error: {content[:500]}...")
            return False
        
        # 4. Verificar redirección
        print("\n🔄 4. VERIFICANDO REDIRECCIÓN")
        print("-" * 50)
        
        if response.status_code == 302:
            redirect_url = response.url
            print(f"📍 URL de redirección: {redirect_url}")
            
            if f'/proyectos/{proyecto.id}/trabajadores-diarios/' in redirect_url:
                print("✅ Redirección correcta a la lista de trabajadores")
            else:
                print("⚠️ Redirección no va a la lista esperada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_verificar_bd():
    """Verificar que los datos se guardan correctamente en la BD"""
    print("\n🗄️ VERIFICANDO BASE DE DATOS")
    print("=" * 40)
    
    try:
        # Contar trabajadores por proyecto
        proyectos = Proyecto.objects.all()
        
        for proyecto in proyectos:
            trabajadores = TrabajadorDiario.objects.filter(proyecto=proyecto)
            print(f"📁 Proyecto: {proyecto.nombre}")
            print(f"   👷 Trabajadores: {trabajadores.count()}")
            
            for trabajador in trabajadores:
                print(f"   - {trabajador.nombre}: Q{trabajador.pago_diario} {'✅' if trabajador.activo else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verificando BD: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO PRUEBAS DE TRABAJADORES DIARIOS")
    print("=" * 60)
    
    # Ejecutar pruebas
    test1 = test_trabajadores_diarios()
    test2 = test_verificar_bd()
    
    print("\n📊 RESUMEN DE PRUEBAS")
    print("=" * 30)
    print(f"Funcionalidad: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Base de datos: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if all([test1, test2]):
        print("\n🎉 TODAS LAS PRUEBAS PASARON")
        print("✅ Trabajadores diarios funcionando correctamente")
    else:
        print("\n⚠️ ALGUNAS PRUEBAS FALLARON")
        print("❌ Revisar los errores mostrados arriba")

if __name__ == '__main__':
    main()
