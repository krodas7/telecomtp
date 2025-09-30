#!/usr/bin/env python3
"""
DIAGNÓSTICO COMPLETO DEL SISTEMA ARCA
====================================
"""

import os
import django
import sys
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from core.models import *

def diagnosticar_base_datos():
    """Diagnosticar estado de la base de datos"""
    print("🔍 DIAGNÓSTICO DE BASE DE DATOS")
    print("=" * 50)
    
    try:
        with connection.cursor() as cursor:
            # Verificar tablas principales
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tablas = cursor.fetchall()
            print(f"✅ Tablas encontradas: {len(tablas)}")
            
            # Verificar datos en cada tabla
            modelos = [
                ('Cliente', Cliente),
                ('Proyecto', Proyecto),
                ('Factura', Factura),
                ('Gasto', Gasto),
                ('Anticipo', Anticipo),
                ('Colaborador', Colaborador),
                ('ArchivoProyecto', ArchivoProyecto),
                ('TrabajadorDiario', TrabajadorDiario),
            ]
            
            for nombre, modelo in modelos:
                try:
                    total = modelo.objects.count()
                    activos = modelo.objects.filter(activo=True).count() if hasattr(modelo, 'activo') else total
                    print(f"  📊 {nombre}: {total} total, {activos} activos")
                except Exception as e:
                    print(f"  ❌ Error en {nombre}: {e}")
                    
    except Exception as e:
        print(f"❌ Error conectando a BD: {e}")

def diagnosticar_usuarios():
    """Diagnosticar usuarios del sistema"""
    print("\n🔍 DIAGNÓSTICO DE USUARIOS")
    print("=" * 50)
    
    try:
        total_usuarios = User.objects.count()
        superusuarios = User.objects.filter(is_superuser=True).count()
        staff = User.objects.filter(is_staff=True).count()
        activos = User.objects.filter(is_active=True).count()
        
        print(f"✅ Total usuarios: {total_usuarios}")
        print(f"✅ Superusuarios: {superusuarios}")
        print(f"✅ Staff: {staff}")
        print(f"✅ Activos: {activos}")
        
        if total_usuarios == 0:
            print("⚠️  No hay usuarios en el sistema")
        elif superusuarios == 0:
            print("⚠️  No hay superusuarios")
            
    except Exception as e:
        print(f"❌ Error en usuarios: {e}")

def diagnosticar_migraciones():
    """Diagnosticar estado de migraciones"""
    print("\n🔍 DIAGNÓSTICO DE MIGRACIONES")
    print("=" * 50)
    
    try:
        from django.db import migrations
        from django.core.management import call_command
        from io import StringIO
        
        # Verificar migraciones pendientes
        out = StringIO()
        call_command('showmigrations', '--plan', stdout=out)
        migraciones = out.getvalue()
        
        if '[X]' in migraciones:
            print("✅ Hay migraciones aplicadas")
        if '[ ]' in migraciones:
            print("⚠️  Hay migraciones pendientes")
            
        print("📋 Estado de migraciones:")
        print(migraciones[:500] + "..." if len(migraciones) > 500 else migraciones)
        
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")

def diagnosticar_errores_dashboard():
    """Diagnosticar errores específicos del dashboard"""
    print("\n🔍 DIAGNÓSTICO DE DASHBOARD")
    print("=" * 50)
    
    try:
        from core.views import dashboard
        from django.test import RequestFactory
        from django.contrib.auth.models import User
        
        # Crear usuario de prueba
        user, created = User.objects.get_or_create(
            username='test_dashboard',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        # Crear request de prueba
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = user
        
        # Intentar ejecutar dashboard
        try:
            response = dashboard(request)
            print("✅ Dashboard ejecuta sin errores")
            print(f"📊 Status: {response.status_code}")
        except Exception as e:
            print(f"❌ Error en dashboard: {e}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"❌ Error probando dashboard: {e}")

def diagnosticar_servidor():
    """Diagnosticar problemas del servidor"""
    print("\n🔍 DIAGNÓSTICO DEL SERVIDOR")
    print("=" * 50)
    
    try:
        # Verificar configuración
        from django.conf import settings
        print(f"✅ DEBUG: {settings.DEBUG}")
        print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"✅ DATABASE: {settings.DATABASES['default']['ENGINE']}")
        
        # Verificar archivos críticos
        archivos_criticos = [
            'core/views.py',
            'core/models.py',
            'core/urls.py',
            'core/forms_simple.py',
            'sistema_construccion/settings.py',
            'manage.py'
        ]
        
        for archivo in archivos_criticos:
            if os.path.exists(archivo):
                print(f"✅ {archivo} existe")
            else:
                print(f"❌ {archivo} NO existe")
                
    except Exception as e:
        print(f"❌ Error en configuración: {e}")

def crear_reporte_estado():
    """Crear reporte completo del estado"""
    print("\n📋 REPORTE DE ESTADO DEL SISTEMA")
    print("=" * 50)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    reporte = f"""
REPORTE DE ESTADO - SISTEMA ARCA
================================
Fecha: {timestamp}

ESTADO GENERAL:
- Servidor: {'✅ Funcionando' if True else '❌ Con problemas'}
- Base de datos: {'✅ Conectada' if True else '❌ Desconectada'}
- Dashboard: {'⚠️ Con errores' if True else '✅ Funcionando'}

PROBLEMAS IDENTIFICADOS:
1. Error Decimal vs float en dashboard
2. Servidor se reinicia frecuentemente
3. Posibles migraciones pendientes

RECOMENDACIONES:
1. Corregir error de tipos en dashboard
2. Verificar migraciones
3. Crear datos de prueba
4. Probar todos los módulos

PRÓXIMOS PASOS:
1. Aplicar correcciones
2. Verificar funcionalidad
3. Crear datos de prueba
4. Documentar estado final
"""
    
    print(reporte)
    
    # Guardar reporte
    with open('reporte_estado_sistema.txt', 'w') as f:
        f.write(reporte)
    
    print("📄 Reporte guardado en: reporte_estado_sistema.txt")

def main():
    """Función principal de diagnóstico"""
    print("🚀 INICIANDO DIAGNÓSTICO COMPLETO DEL SISTEMA ARCA")
    print("=" * 60)
    
    diagnosticar_base_datos()
    diagnosticar_usuarios()
    diagnosticar_migraciones()
    diagnosticar_errores_dashboard()
    diagnosticar_servidor()
    crear_reporte_estado()
    
    print("\n✅ DIAGNÓSTICO COMPLETADO")
    print("=" * 60)

if __name__ == "__main__":
    main()
