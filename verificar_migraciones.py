#!/usr/bin/env python
"""
Script para verificar y aplicar migraciones en el servidor
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

def verificar_migraciones():
    """Verificar el estado de las migraciones"""
    print("🔍 VERIFICANDO MIGRACIONES...")
    
    try:
        # Mostrar migraciones pendientes
        print("\n1. MIGRACIONES PENDIENTES:")
        execute_from_command_line(['manage.py', 'showmigrations', 'core'])
        
        # Aplicar migraciones
        print("\n2. APLICANDO MIGRACIONES...")
        execute_from_command_line(['manage.py', 'migrate', 'core'])
        
        # Verificar estado final
        print("\n3. ESTADO FINAL:")
        execute_from_command_line(['manage.py', 'showmigrations', 'core'])
        
        print("\n✅ VERIFICACIÓN DE MIGRACIONES COMPLETADA")
        
    except Exception as e:
        print(f"❌ ERROR EN MIGRACIONES: {e}")
        return False
    
    return True

def crear_superusuario():
    """Crear superusuario si no existe"""
    print("\n👤 VERIFICANDO SUPERUSUARIO...")
    
    from django.contrib.auth.models import User
    
    if not User.objects.filter(is_superuser=True).exists():
        print("   ⚠️  No hay superusuarios. Creando uno...")
        try:
            execute_from_command_line(['manage.py', 'createsuperuser'])
            print("   ✅ Superusuario creado")
        except Exception as e:
            print(f"   ❌ Error creando superusuario: {e}")
    else:
        superusuarios = User.objects.filter(is_superuser=True)
        print(f"   ✅ Superusuarios encontrados: {superusuarios.count()}")
        for user in superusuarios:
            print(f"      - {user.username} ({user.email})")

def verificar_tablas():
    """Verificar que las tablas necesarias existen"""
    print("\n🗄️  VERIFICANDO TABLAS...")
    
    from django.db import connection
    
    tablas_requeridas = [
        'auth_user',
        'core_rol',
        'core_permiso',
        'core_rolpermiso',
        'core_perfilusuario'
    ]
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tablas_existentes = [row[0] for row in cursor.fetchall()]
    
    for tabla in tablas_requeridas:
        if tabla in tablas_existentes:
            print(f"   ✅ {tabla}")
        else:
            print(f"   ❌ {tabla} - FALTANTE")

if __name__ == "__main__":
    print("🚀 SCRIPT DE VERIFICACIÓN DE MIGRACIONES")
    print("=" * 50)
    
    try:
        # 1. Verificar tablas
        verificar_tablas()
        
        # 2. Verificar y aplicar migraciones
        if verificar_migraciones():
            # 3. Verificar superusuario
            crear_superusuario()
            
            print("\n" + "=" * 50)
            print("✅ VERIFICACIÓN COMPLETADA")
            print("\n📋 PRÓXIMOS PASOS:")
            print("1. Verifica que puedas acceder a la gestión de usuarios")
            print("2. Si hay problemas, revisa los logs del servidor")
            print("3. Considera reiniciar el servidor web")
        else:
            print("\n❌ VERIFICACIÓN FALLIDA")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
