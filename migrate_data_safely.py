#!/usr/bin/env python3
"""
Script para migrar datos de SQLite a PostgreSQL de forma segura
Ejecutar con: python migrate_data_safely.py
"""

import os
import sys
import django
from pathlib import Path
import json
from datetime import datetime

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.core.management import call_command
from django.db import connections
from django.contrib.auth.models import User
from core.models import *

def backup_sqlite_data():
    """Crear respaldo completo de datos SQLite"""
    print("📦 Creando respaldo de datos SQLite...")
    
    backup_data = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Respaldo de usuarios
    users = list(User.objects.values())
    backup_data['users'] = users
    print(f"   ✅ Usuarios: {len(users)} registros")
    
    # Respaldo de proyectos
    try:
        proyectos = list(Proyecto.objects.values())
        backup_data['proyectos'] = proyectos
        print(f"   ✅ Proyectos: {len(proyectos)} registros")
    except:
        print("   ⚠️  No hay proyectos")
        backup_data['proyectos'] = []
    
    # Respaldo de clientes
    try:
        clientes = list(Cliente.objects.values())
        backup_data['clientes'] = clientes
        print(f"   ✅ Clientes: {len(clientes)} registros")
    except:
        print("   ⚠️  No hay clientes")
        backup_data['clientes'] = []
    
    # Respaldo de colaboradores
    try:
        colaboradores = list(Colaborador.objects.values())
        backup_data['colaboradores'] = colaboradores
        print(f"   ✅ Colaboradores: {len(colaboradores)} registros")
    except:
        print("   ⚠️  No hay colaboradores")
        backup_data['colaboradores'] = []
    
    # Respaldo de facturas
    try:
        facturas = list(Factura.objects.values())
        backup_data['facturas'] = facturas
        print(f"   ✅ Facturas: {len(facturas)} registros")
    except:
        print("   ⚠️  No hay facturas")
        backup_data['facturas'] = []
    
    # Respaldo de gastos
    try:
        gastos = list(Gasto.objects.values())
        backup_data['gastos'] = gastos
        print(f"   ✅ Gastos: {len(gastos)} registros")
    except:
        print("   ⚠️  No hay gastos")
        backup_data['gastos'] = []
    
    # Guardar respaldo
    backup_file = f"backup_sqlite_{timestamp}.json"
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, default=str)
    
    print(f"   💾 Respaldo guardado: {backup_file}")
    return backup_file, backup_data

def check_postgresql_connection():
    """Verificar conexión a PostgreSQL"""
    print("🔍 Verificando conexión a PostgreSQL...")
    
    try:
        # Cambiar temporalmente a configuración de producción
        os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema_construccion.settings_production'
        django.setup()
        
        # Probar conexión
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
        
        print("   ✅ Conexión a PostgreSQL exitosa")
        return True
    except Exception as e:
        print(f"   ❌ Error conectando a PostgreSQL: {e}")
        return False

def migrate_to_postgresql(backup_data):
    """Migrar datos a PostgreSQL"""
    print("🔄 Migrando datos a PostgreSQL...")
    
    try:
        # Cambiar a configuración de producción
        os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema_construccion.settings_production'
        django.setup()
        
        # Ejecutar migraciones
        print("   📋 Ejecutando migraciones...")
        call_command('migrate', verbosity=0)
        
        # Restaurar usuarios
        if backup_data['users']:
            print("   👥 Restaurando usuarios...")
            for user_data in backup_data['users']:
                # Remover campos que no se pueden crear directamente
                user_data.pop('id', None)
                user_data.pop('last_login', None)
                user_data.pop('date_joined', None)
                
                try:
                    User.objects.get_or_create(
                        username=user_data['username'],
                        defaults=user_data
                    )
                except Exception as e:
                    print(f"     ⚠️  Error con usuario {user_data.get('username', 'unknown')}: {e}")
        
        # Restaurar proyectos
        if backup_data['proyectos']:
            print("   🏗️  Restaurando proyectos...")
            for proyecto_data in backup_data['proyectos']:
                proyecto_data.pop('id', None)
                try:
                    Proyecto.objects.get_or_create(
                        nombre=proyecto_data['nombre'],
                        defaults=proyecto_data
                    )
                except Exception as e:
                    print(f"     ⚠️  Error con proyecto {proyecto_data.get('nombre', 'unknown')}: {e}")
        
        # Restaurar clientes
        if backup_data['clientes']:
            print("   👤 Restaurando clientes...")
            for cliente_data in backup_data['clientes']:
                cliente_data.pop('id', None)
                try:
                    Cliente.objects.get_or_create(
                        nombre=cliente_data['nombre'],
                        defaults=cliente_data
                    )
                except Exception as e:
                    print(f"     ⚠️  Error con cliente {cliente_data.get('nombre', 'unknown')}: {e}")
        
        print("   ✅ Migración completada")
        return True
        
    except Exception as e:
        print(f"   ❌ Error en migración: {e}")
        return False

def verify_migration():
    """Verificar que la migración fue exitosa"""
    print("🔍 Verificando migración...")
    
    try:
        # Cambiar a configuración de producción
        os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema_construccion.settings_production'
        django.setup()
        
        # Contar registros
        user_count = User.objects.count()
        proyecto_count = Proyecto.objects.count()
        cliente_count = Cliente.objects.count()
        
        print(f"   👥 Usuarios: {user_count}")
        print(f"   🏗️  Proyectos: {proyecto_count}")
        print(f"   👤 Clientes: {cliente_count}")
        
        if user_count > 0:
            print("   ✅ Migración exitosa")
            return True
        else:
            print("   ❌ No se encontraron datos migrados")
            return False
            
    except Exception as e:
        print(f"   ❌ Error verificando migración: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 MIGRACIÓN SEGURA DE DATOS TELECOMTP")
    print("=" * 50)
    
    # Paso 1: Respaldo de datos
    backup_file, backup_data = backup_sqlite_data()
    
    # Paso 2: Verificar PostgreSQL
    if not check_postgresql_connection():
        print("❌ No se puede continuar sin PostgreSQL")
        return
    
    # Paso 3: Migrar datos
    if migrate_to_postgresql(backup_data):
        # Paso 4: Verificar migración
        if verify_migration():
            print("\n✅ MIGRACIÓN COMPLETADA EXITOSAMENTE")
            print(f"📦 Respaldo guardado en: {backup_file}")
            print("🔄 Ahora puedes usar la configuración de producción")
        else:
            print("\n❌ ERROR EN LA MIGRACIÓN")
            print("🔄 Restaurar desde respaldo si es necesario")
    else:
        print("\n❌ ERROR EN LA MIGRACIÓN")
        print("🔄 Los datos originales están seguros en SQLite")

if __name__ == "__main__":
    main()
