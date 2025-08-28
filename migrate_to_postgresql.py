#!/usr/bin/env python3
"""
Script para migrar la base de datos de SQLite a PostgreSQL
Sistema ARCA Construcción - Migración a Producción
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.production_settings')

django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database():
    """Crear base de datos PostgreSQL si no existe"""
    try:
        # Conectar a PostgreSQL como superusuario
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=os.environ.get('DB_PORT', '5432'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', ''),
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Crear base de datos si no existe
        db_name = os.environ.get('DB_NAME', 'arca_construccion')
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creando base de datos '{db_name}'...")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Base de datos '{db_name}' creada exitosamente")
        else:
            print(f"✅ Base de datos '{db_name}' ya existe")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False
    
    return True

def create_user():
    """Crear usuario de base de datos si no existe"""
    try:
        # Conectar a la base de datos específica
        conn = psycopg2.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            port=os.environ.get('DB_PORT', '5432'),
            user=os.environ.get('DB_USER', 'postgres'),
            password=os.environ.get('DB_PASSWORD', ''),
            database=os.environ.get('DB_NAME', 'arca_construccion')
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Crear usuario si no existe
        db_user = os.environ.get('DB_USER', 'arca_user')
        db_password = os.environ.get('DB_PASSWORD', '')
        
        cursor.execute(f"SELECT 1 FROM pg_user WHERE usename = '{db_user}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creando usuario '{db_user}'...")
            cursor.execute(f"CREATE USER {db_user} WITH PASSWORD '{db_password}'")
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {os.environ.get('DB_NAME', 'arca_construccion')} TO {db_user}")
            print(f"✅ Usuario '{db_user}' creado exitosamente")
        else:
            print(f"✅ Usuario '{db_user}' ya existe")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error creando usuario: {e}")
        return False
    
    return True

def migrate_database():
    """Migrar la base de datos"""
    try:
        print("🔄 Ejecutando migraciones...")
        call_command('migrate', verbosity=2)
        print("✅ Migraciones completadas")
        return True
    except Exception as e:
        print(f"❌ Error en migraciones: {e}")
        return False

def collect_static():
    """Recolectar archivos estáticos"""
    try:
        print("📁 Recolectando archivos estáticos...")
        call_command('collectstatic', '--noinput', verbosity=2)
        print("✅ Archivos estáticos recolectados")
        return True
    except Exception as e:
        print(f"❌ Error recolectando estáticos: {e}")
        return False

def create_superuser():
    """Crear superusuario si no existe"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creando superusuario...")
            username = input("Nombre de usuario para superusuario: ")
            email = input("Email para superusuario: ")
            password = input("Contraseña para superusuario: ")
            
            User.objects.create_superuser(username, email, password)
            print("✅ Superusuario creado exitosamente")
        else:
            print("✅ Superusuario ya existe")
        
        return True
    except Exception as e:
        print(f"❌ Error creando superusuario: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO MIGRACIÓN A POSTGRESQL")
    print("=" * 50)
    
    # Verificar variables de entorno
    required_vars = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Variables de entorno faltantes:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n💡 Asegúrate de configurar el archivo .env o production.env")
        return False
    
    # Crear base de datos
    if not create_database():
        return False
    
    # Crear usuario
    if not create_user():
        return False
    
    # Ejecutar migraciones
    if not migrate_database():
        return False
    
    # Recolectar archivos estáticos
    if not collect_static():
        return False
    
    # Crear superusuario
    if not create_superuser():
        return False
    
    print("\n🎉 ¡MIGRACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("✅ Base de datos PostgreSQL configurada")
    print("✅ Usuario de base de datos creado")
    print("✅ Migraciones aplicadas")
    print("✅ Archivos estáticos recolectados")
    print("✅ Superusuario configurado")
    print("\n🚀 El sistema está listo para producción!")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
