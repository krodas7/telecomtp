#!/usr/bin/env python3
"""
Script para sincronizar migraciones entre local y servidor
Soluciona el problema de tablas que ya existen
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.db import connection
from django.core.management import call_command

def main():
    print("🔧 Sincronizando migraciones...")
    print("=" * 60)
    
    # Verificar qué tablas existen
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            ORDER BY name;
        """)
        tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n📊 Tablas existentes en la BD: {len(tables)}")
    
    # Verificar si core_colaborador tiene las columnas nuevas
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(core_colaborador)")
        columns = [row[1] for row in cursor.fetchall()]
    
    print(f"\n👤 Columnas en core_colaborador: {len(columns)}")
    
    # Verificar columnas específicas
    columnas_necesarias = [
        'aplica_bono_general',
        'aplica_bono_produccion', 
        'aplica_retenciones'
    ]
    
    columnas_faltantes = [col for col in columnas_necesarias if col not in columns]
    
    if columnas_faltantes:
        print(f"\n❌ Columnas faltantes: {columnas_faltantes}")
        print("\n🔨 Agregando columnas faltantes manualmente...")
        
        with connection.cursor() as cursor:
            for columna in columnas_faltantes:
                try:
                    sql = f"ALTER TABLE core_colaborador ADD COLUMN {columna} BOOLEAN DEFAULT 1 NOT NULL"
                    print(f"   Ejecutando: {sql}")
                    cursor.execute(sql)
                    print(f"   ✅ Columna {columna} agregada")
                except Exception as e:
                    print(f"   ⚠️  Error en {columna}: {e}")
        
        print("\n✅ Columnas agregadas exitosamente")
    else:
        print(f"\n✅ Todas las columnas necesarias existen")
    
    # Verificar tabla core_configuracionplanilla
    if 'core_configuracionplanilla' not in tables:
        print("\n⚠️  Tabla core_configuracionplanilla no existe, se creará en migrate")
    
    # Verificar tabla core_notapostit
    if 'core_notapostit' not in tables:
        print("\n⚠️  Tabla core_notapostit no existe, se creará en migrate")
    
    print("\n" + "=" * 60)
    print("✅ Sincronización completada")
    print("\nAhora puedes ejecutar:")
    print("  python3 manage.py migrate --fake")
    print("  python3 manage.py migrate")

if __name__ == '__main__':
    main()

