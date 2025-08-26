#!/usr/bin/env python3
"""
Script de Despliegue para SmartASP
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def log(message):
    """Función para logging"""
    print(f"[SMARTASP] {message}")

def check_requirements():
    """Verificar requisitos para SmartASP"""
    log("Verificando requisitos...")
    
    # Verificar Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        log("ERROR: Se requiere Python 3.8 o superior")
        return False
    
    log(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    return True

def create_directories():
    """Crear directorios necesarios para SmartASP"""
    log("Creando directorios...")
    
    directories = [
        'staticfiles',
        'media',
        'backups',
        'logs',
        'temp'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        log(f"✓ Directorio {directory} creado")

def install_dependencies():
    """Instalar dependencias para SmartASP"""
    log("Instalando dependencias...")
    
    # Dependencias específicas para SmartASP
    smartasp_requirements = [
        'django',
        'sql_server.pyodbc',
        'pyodbc',
        'django-cors-headers',
        'django-crispy-forms',
        'crispy-bootstrap5',
        'openpyxl',
        'xlsxwriter',
        'python-dotenv',
        'Pillow',
        'reportlab',
        'django-extensions',
    ]
    
    for package in smartasp_requirements:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                         check=True, capture_output=True)
            log(f"✓ {package} instalado")
        except subprocess.CalledProcessError:
            log(f"⚠ Error instalando {package}")

def setup_environment():
    """Configurar variables de entorno para SmartASP"""
    log("Configurando entorno...")
    
    env_file = Path('.env')
    if not env_file.exists():
        log("Creando archivo .env...")
        
        env_content = """# Configuración para SmartASP
ENVIRONMENT=smartasp
DEBUG=False

# Base de datos SQL Server
DB_ENGINE=sql_server.pyodbc
DB_NAME=sistema_construccion
DB_USER=tu_usuario
DB_PASSWORD=tu_password
DB_HOST=tu_host
DB_PORT=1433

# Email (Hostinger)
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@tu-dominio.com
EMAIL_HOST_PASSWORD=tu_password_email
DEFAULT_FROM_EMAIL=tu_email@tu-dominio.com

# Dominio
ALLOWED_HOSTS=tu-dominio.com,www.tu-dominio.com

# Secret Key (generar uno nuevo)
SECRET_KEY=tu_secret_key_aqui
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        log("✓ Archivo .env creado")
        log("⚠ IMPORTANTE: Edita el archivo .env con tus credenciales reales")
    else:
        log("✓ Archivo .env ya existe")

def run_migrations():
    """Ejecutar migraciones de Django"""
    log("Ejecutando migraciones...")
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.smartasp_settings')
        
        import django
        django.setup()
        
        # Ejecutar migraciones
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        
        log("✓ Migraciones ejecutadas")
        return True
    except Exception as e:
        log(f"✗ Error en migraciones: {e}")
        return False

def collect_static():
    """Recolectar archivos estáticos"""
    log("Recolectando archivos estáticos...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        log("✓ Archivos estáticos recolectados")
        return True
    except Exception as e:
        log(f"✗ Error recolectando estáticos: {e}")
        return False

def create_superuser():
    """Crear superusuario"""
    log("Creando superusuario...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'createsuperuser', '--noinput'])
        log("✓ Superusuario creado")
        return True
    except Exception as e:
        log(f"⚠ Error creando superusuario: {e}")
        return False

def load_initial_data():
    """Cargar datos iniciales"""
    log("Cargando datos iniciales...")
    
    try:
        # Ejecutar script de datos
        if Path('crear_datos_prueba.py').exists():
            subprocess.run([sys.executable, 'crear_datos_prueba.py'], check=True)
            log("✓ Datos iniciales cargados")
        else:
            log("⚠ Script de datos no encontrado")
        return True
    except Exception as e:
        log(f"⚠ Error cargando datos: {e}")
        return False

def create_web_config():
    """Crear archivo web.config para SmartASP"""
    log("Creando web.config...")
    
    web_config_content = """<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <handlers>
            <add name="Python FastCGI" path="*" verb="*" modules="FastCgiModule" scriptProcessor="C:\\Python39\\python.exe|C:\\Python39\\Lib\\site-packages\\wfastcgi.py" resourceType="Unspecified" requireAccess="Script" />
        </handlers>
        <rewrite>
            <rules>
                <rule name="Static Files" stopProcessing="true">
                    <match url="^(static|media)/.*$" />
                    <action type="Rewrite" url="{R:0}" />
                </rule>
                <rule name="Django" stopProcessing="true">
                    <match url=".*" />
                    <action type="Rewrite" url="sistema_construccion/wsgi_smartasp.py" />
                </rule>
            </rules>
        </rewrite>
        <staticContent>
            <mimeMap fileExtension=".woff" mimeType="application/font-woff" />
            <mimeMap fileExtension=".woff2" mimeType="application/font-woff2" />
        </staticContent>
    </system.webServer>
</configuration>
"""
    
    with open('web.config', 'w', encoding='utf-8') as f:
        f.write(web_config_content)
    
    log("✓ Archivo web.config creado")

def create_deployment_guide():
    """Crear guía de despliegue para SmartASP"""
    log("Creando guía de despliegue...")
    
    guide_content = """# 🚀 Guía de Despliegue para SmartASP

## 📋 Pasos para Desplegar en SmartASP

### 1. Preparación del Proyecto
- ✅ Dependencias instaladas
- ✅ Migraciones ejecutadas
- ✅ Archivos estáticos recolectados
- ✅ Superusuario creado
- ✅ Datos iniciales cargados

### 2. Subir a SmartASP
1. Comprimir el proyecto (excluir venv, __pycache__, .git)
2. Subir via FTP o Panel de Control
3. Extraer en la carpeta raíz del hosting

### 3. Configuración en SmartASP
1. Crear base de datos SQL Server
2. Configurar variables de entorno
3. Actualizar archivo .env con credenciales reales
4. Configurar dominio en Panel de Control

### 4. Verificación
1. Acceder a tu-dominio.com
2. Verificar que el dashboard funcione
3. Probar funcionalidades principales

### 5. Soporte
- Documentación: README.md
- Logs: carpeta logs/
- Backup: carpeta backups/

## 🔧 Configuración de Base de Datos
- Motor: SQL Server
- Puerto: 1433
- Driver: ODBC Driver 17 for SQL Server

## 📧 Configuración de Email
- Host: smtp.hostinger.com
- Puerto: 587
- TLS: Habilitado

## 🌐 Dominio
- Configurar en Panel de Control de Hostinger
- Apuntar a la carpeta del proyecto en SmartASP
"""
    
    with open('SMARTASP_DEPLOY_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    log("✓ Guía de despliegue creada")

def main():
    """Función principal"""
    log("=== INICIANDO DESPLIEGUE PARA SMARTASP ===")
    
    if not check_requirements():
        log("✗ Requisitos no cumplidos")
        return
    
    create_directories()
    install_dependencies()
    setup_environment()
    
    if run_migrations():
        collect_static()
        create_superuser()
        load_initial_data()
    
    create_web_config()
    create_deployment_guide()
    
    log("=== DESPLIEGUE PARA SMARTASP COMPLETADO ===")
    log("📁 Archivos creados:")
    log("  - .env (configurar credenciales)")
    log("  - web.config")
    log("  - SMARTASP_DEPLOY_GUIDE.md")
    log("")
    log("🚀 Próximos pasos:")
    log("1. Editar archivo .env con credenciales reales")
    log("2. Comprimir proyecto (excluir venv, __pycache__)")
    log("3. Subir a SmartASP via FTP")
    log("4. Configurar base de datos SQL Server")
    log("5. Configurar dominio en Hostinger")

if __name__ == '__main__':
    main()
