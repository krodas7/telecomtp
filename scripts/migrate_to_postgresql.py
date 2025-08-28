#!/usr/bin/env python3
"""
Script para migrar la base de datos de SQLite a PostgreSQL
Sistema ARCA Construcción

Uso:
    python scripts/migrate_to_postgresql.py

Requisitos:
    - PostgreSQL instalado y funcionando
    - psycopg2-binary instalado
    - Base de datos PostgreSQL creada
"""

import os
import sys
import django
from pathlib import Path
import json
from datetime import datetime

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
from django.conf import settings
from django.core.management.base import CommandError

def check_postgresql_connection():
    """Verificar conexión a PostgreSQL"""
    try:
        with connections['postgresql'].cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ Conexión a PostgreSQL exitosa: {version[0]}")
            return True
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return False

def create_postgresql_database():
    """Crear base de datos PostgreSQL si no existe"""
    try:
        # Conectar a PostgreSQL por defecto
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        
        # Configuración de conexión
        db_config = {
            'host': 'localhost',
            'user': 'postgres',
            'password': 'tu-password-postgres',
            'port': '5432'
        }
        
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**db_config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='arca_construccion'")
        exists = cursor.fetchone()
        
        if not exists:
            # Crear base de datos
            cursor.execute("CREATE DATABASE arca_construccion")
            print("✅ Base de datos 'arca_construccion' creada")
        else:
            print("✅ Base de datos 'arca_construccion' ya existe")
        
        # Crear usuario si no existe
        cursor.execute("SELECT 1 FROM pg_user WHERE usename='arca_user'")
        user_exists = cursor.fetchone()
        
        if not user_exists:
            cursor.execute("CREATE USER arca_user WITH PASSWORD 'tu-password-seguro'")
            print("✅ Usuario 'arca_user' creado")
        else:
            print("✅ Usuario 'arca_user' ya existe")
        
        # Otorgar permisos
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE arca_construccion TO arca_user")
        cursor.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO arca_user")
        print("✅ Permisos otorgados al usuario")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def backup_sqlite_data():
    """Crear respaldo de datos SQLite"""
    try:
        backup_dir = BASE_DIR / 'backups'
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = backup_dir / f'sqlite_backup_{timestamp}.json'
        
        print(f"📦 Creando respaldo de SQLite...")
        
        # Exportar datos a JSON
        call_command('dumpdata', 
                    '--natural-foreign', 
                    '--natural-primary',
                    '--exclude', 'contenttypes',
                    '--exclude', 'auth.Permission',
                    '--indent', '2',
                    output=str(backup_file))
        
        print(f"✅ Respaldo creado: {backup_file}")
        return str(backup_file)
        
    except Exception as e:
        print(f"❌ Error creando respaldo: {e}")
        return None

def migrate_to_postgresql():
    """Migrar a PostgreSQL"""
    try:
        print("🔄 Iniciando migración a PostgreSQL...")
        
        # 1. Crear respaldo
        backup_file = backup_sqlite_data()
        if not backup_file:
            return False
        
        # 2. Cambiar configuración temporalmente
        original_db = settings.DATABASES['default'].copy()
        
        # Configurar PostgreSQL temporalmente
        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'arca_construccion',
            'USER': 'arca_user',
            'PASSWORD': 'tu-password-seguro',
            'HOST': 'localhost',
            'PORT': '5432',
        }
        
        # 3. Crear tablas en PostgreSQL
        print("🗄️ Creando tablas en PostgreSQL...")
        call_command('migrate', '--run-syncdb')
        
        # 4. Cargar datos del respaldo
        print("📥 Cargando datos del respaldo...")
        call_command('loaddata', backup_file)
        
        # 5. Restaurar configuración original
        settings.DATABASES['default'] = original_db
        
        print("✅ Migración completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la migración: {e}")
        return False

def verify_migration():
    """Verificar que la migración fue exitosa"""
    try:
        print("🔍 Verificando migración...")
        
        # Cambiar a configuración PostgreSQL
        original_db = settings.DATABASES['default'].copy()
        settings.DATABASES['default'] = {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'arca_construccion',
            'USER': 'arca_user',
            'PASSWORD': 'tu-password-seguro',
            'HOST': 'localhost',
            'PORT': '5432',
        }
        
        # Verificar conexión
        if not check_postgresql_connection():
            return False
        
        # Verificar que las tablas existen
        with connections['default'].cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = [
                'auth_user', 'core_cliente', 'core_proyecto', 
                'core_colaborador', 'core_factura', 'core_pago'
            ]
            
            for table in expected_tables:
                if table in tables:
                    print(f"✅ Tabla {table} encontrada")
                else:
                    print(f"❌ Tabla {table} no encontrada")
                    return False
        
        # Restaurar configuración
        settings.DATABASES['default'] = original_db
        
        print("✅ Verificación completada exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 INICIANDO MIGRACIÓN A POSTGRESQL")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not (BASE_DIR / 'manage.py').exists():
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # 1. Crear base de datos PostgreSQL
    print("\n1️⃣ Creando base de datos PostgreSQL...")
    if not create_postgresql_database():
        print("❌ No se pudo crear la base de datos")
        sys.exit(1)
    
    # 2. Verificar conexión
    print("\n2️⃣ Verificando conexión...")
    if not check_postgresql_connection():
        print("❌ No se pudo conectar a PostgreSQL")
        sys.exit(1)
    
    # 3. Migrar datos
    print("\n3️⃣ Migrando datos...")
    if not migrate_to_postgresql():
        print("❌ Error durante la migración")
        sys.exit(1)
    
    # 4. Verificar migración
    print("\n4️⃣ Verificando migración...")
    if not verify_migration():
        print("❌ La migración no fue exitosa")
        sys.exit(1)
    
    print("\n🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 50)
    print("📋 Próximos pasos:")
    print("1. Actualizar .env.production con las credenciales correctas")
    print("2. Cambiar DJANGO_SETTINGS_MODULE a production_settings")
    print("3. Reiniciar el servidor")
    print("4. Verificar que todo funcione correctamente")

if __name__ == '__main__':
    main()
