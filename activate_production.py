#!/usr/bin/env python3
"""
Script para activar la configuración de producción
Sistema ARCA Construcción - Activación de Producción
"""

import os
import sys
import shutil
from pathlib import Path
import subprocess

def load_env_file(env_file):
    """Cargar variables de entorno desde archivo"""
    if not os.path.exists(env_file):
        print(f"❌ Archivo {env_file} no encontrado")
        return False
    
    print(f"📁 Cargando variables de entorno desde {env_file}...")
    
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()
    
    print("✅ Variables de entorno cargadas")
    return True

def install_production_dependencies():
    """Instalar dependencias de producción"""
    try:
        print("📦 Instalando dependencias de producción...")
        
        # Verificar si requirements_production.txt existe
        if not os.path.exists('requirements_production.txt'):
            print("❌ requirements_production.txt no encontrado")
            return False
        
        # Instalar dependencias
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements_production.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependencias de producción instaladas")
            return True
        else:
            print(f"❌ Error instalando dependencias: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_directories():
    """Crear directorios necesarios para producción"""
    directories = [
        'staticfiles',
        'media',
        'logs',
        'backups',
        'temp'
    ]
    
    print("📁 Creando directorios de producción...")
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def backup_sqlite():
    """Hacer backup de la base de datos SQLite"""
    try:
        if os.path.exists('db.sqlite3'):
            print("💾 Haciendo backup de base de datos SQLite...")
            backup_file = f"backups/db_backup_{os.path.basename(os.getcwd())}_{os.environ.get('ENVIRONMENT', 'production')}.sqlite3"
            shutil.copy2('db.sqlite3', backup_file)
            print(f"✅ Backup creado: {backup_file}")
        else:
            print("ℹ️ No hay base de datos SQLite para hacer backup")
        
        return True
    except Exception as e:
        print(f"❌ Error haciendo backup: {e}")
        return False

def test_production_settings():
    """Probar configuración de producción"""
    try:
        print("🧪 Probando configuración de producción...")
        
        # Cambiar a configuración de producción
        os.environ['DJANGO_SETTINGS_MODULE'] = 'sistema_construccion.production_settings'
        
        # Importar Django y verificar configuración
        import django
        django.setup()
        
        from django.conf import settings
        
        # Verificar configuraciones críticas
        checks = [
            ('DEBUG', settings.DEBUG, False),
            ('SECRET_KEY', bool(settings.SECRET_KEY), True),
            ('DATABASES', settings.DATABASES['default']['ENGINE'], 'django.db.backends.postgresql'),
            ('STATIC_ROOT', bool(settings.STATIC_ROOT), True),
            ('MEDIA_ROOT', bool(settings.MEDIA_ROOT), True),
        ]
        
        all_good = True
        for name, value, expected in checks:
            if value == expected:
                print(f"   ✅ {name}: {value}")
            else:
                print(f"   ❌ {name}: {value} (esperado: {expected})")
                all_good = False
        
        if all_good:
            print("✅ Configuración de producción verificada")
            return True
        else:
            print("❌ Configuración de producción tiene problemas")
            return False
            
    except Exception as e:
        print(f"❌ Error probando configuración: {e}")
        return False

def create_production_wsgi():
    """Crear archivo WSGI para producción"""
    try:
        print("🔧 Configurando WSGI para producción...")
        
        wsgi_content = '''"""
WSGI config for sistema_construccion project.
Configuración para producción
"""

import os
import sys
from pathlib import Path

# Agregar el directorio del proyecto al path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configurar variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.production_settings')

# Cargar archivo .env si existe
env_file = BASE_DIR / '.env'
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
'''
        
        with open('sistema_construccion/wsgi_production.py', 'w') as f:
            f.write(wsgi_content)
        
        print("✅ Archivo WSGI de producción creado")
        return True
        
    except Exception as e:
        print(f"❌ Error creando WSGI: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 ACTIVANDO CONFIGURACIÓN DE PRODUCCIÓN")
    print("=" * 50)
    
    # Cargar variables de entorno
    env_files = ['.env', 'production.env']
    env_loaded = False
    
    for env_file in env_files:
        if os.path.exists(env_file):
            if load_env_file(env_file):
                env_loaded = True
                break
    
    if not env_loaded:
        print("❌ No se pudo cargar archivo de variables de entorno")
        print("💡 Crea un archivo .env o production.env con la configuración")
        return False
    
    # Crear directorios
    if not create_directories():
        return False
    
    # Hacer backup de SQLite
    if not backup_sqlite():
        return False
    
    # Instalar dependencias de producción
    if not install_production_dependencies():
        return False
    
    # Crear WSGI de producción
    if not create_production_wsgi():
        return False
    
    # Probar configuración
    if not test_production_settings():
        return False
    
    print("\n🎉 ¡CONFIGURACIÓN DE PRODUCCIÓN ACTIVADA!")
    print("=" * 50)
    print("✅ Variables de entorno cargadas")
    print("✅ Directorios de producción creados")
    print("✅ Backup de SQLite realizado")
    print("✅ Dependencias de producción instaladas")
    print("✅ WSGI de producción configurado")
    print("✅ Configuración verificada")
    print("\n📋 PRÓXIMOS PASOS:")
    print("1. Configurar base de datos PostgreSQL")
    print("2. Ejecutar: python migrate_to_postgresql.py")
    print("3. Configurar servidor web (Nginx)")
    print("4. Configurar Gunicorn")
    print("5. Configurar SSL/HTTPS")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
