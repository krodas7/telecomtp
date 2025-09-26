#!/usr/bin/env python3
"""
Script de Actualización Rápida para Servidor
Actualiza solo los cambios más recientes sin reinstalar todo
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

def log(message, level="INFO"):
    """Función para logging con colores"""
    colors = {
        "INFO": "\033[94m",    # Azul
        "SUCCESS": "\033[92m", # Verde
        "WARNING": "\033[93m", # Amarillo
        "ERROR": "\033[91m",   # Rojo
        "RESET": "\033[0m"     # Reset
    }
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{colors.get(level, '')}[{timestamp}] {message}{colors['RESET']}")

def check_git_status():
    """Verificar estado de Git"""
    log("Verificando estado de Git...")
    
    try:
        # Verificar si hay cambios sin commitear
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        if result.stdout.strip():
            log("⚠️  Hay cambios sin commitear:", "WARNING")
            print(result.stdout)
            return False
        else:
            log("✓ No hay cambios pendientes", "SUCCESS")
            return True
            
    except subprocess.CalledProcessError as e:
        log(f"✗ Error verificando Git: {e}", "ERROR")
        return False

def get_latest_commit():
    """Obtener información del último commit"""
    try:
        result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                              capture_output=True, text=True, check=True)
        commit_hash = result.stdout.strip().split()[0]
        commit_message = ' '.join(result.stdout.strip().split()[1:])
        
        log(f"Último commit: {commit_hash} - {commit_message}", "INFO")
        return commit_hash, commit_message
        
    except subprocess.CalledProcessError as e:
        log(f"✗ Error obteniendo commit: {e}", "ERROR")
        return None, None

def create_deployment_package():
    """Crear paquete de despliegue con solo los archivos necesarios"""
    log("Creando paquete de despliegue...")
    
    # Archivos y directorios a incluir
    include_patterns = [
        'core/',
        'sistema_construccion/',
        'templates/',
        'static/',
        'media/',
        'manage.py',
        'requirements.txt',
        'requirements_production.txt',
        'requirements_production_simple.txt',
        'production.env',
        'env_production.txt',
        'nginx/',
        'supervisor/',
        'gunicorn/',
        'deploy/',
        '*.py',
        '*.sh',
        '*.conf',
        '*.txt',
        '*.md',
        'web.config',
        'Dockerfile',
        'docker-compose.yml'
    ]
    
    # Archivos y directorios a excluir
    exclude_patterns = [
        '__pycache__/',
        '*.pyc',
        '*.pyo',
        '*.pyd',
        '.git/',
        'venv/',
        'env/',
        '.env',
        'db.sqlite3',
        'logs/',
        'backups/',
        'temp/',
        'staticfiles/',
        '.gitignore',
        '*.log'
    ]
    
    # Crear directorio temporal
    temp_dir = Path('temp_deployment')
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    log("Copiando archivos necesarios...")
    
    # Copiar archivos principales
    for pattern in include_patterns:
        if '*' in pattern:
            # Patrón con wildcard
            import glob
            for file in glob.glob(pattern):
                if os.path.isfile(file):
                    shutil.copy2(file, temp_dir)
                    log(f"  ✓ {file}")
        else:
            # Directorio o archivo específico
            if os.path.exists(pattern):
                if os.path.isdir(pattern):
                    shutil.copytree(pattern, temp_dir / pattern, 
                                  ignore=shutil.ignore_patterns(*exclude_patterns))
                    log(f"  ✓ {pattern}/")
                else:
                    shutil.copy2(pattern, temp_dir)
                    log(f"  ✓ {pattern}")
    
    # Crear archivo de información del despliegue
    commit_hash, commit_message = get_latest_commit()
    deployment_info = f"""# Información del Despliegue
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Commit: {commit_hash}
Mensaje: {commit_message}
Versión: 1.0.0

## Archivos Incluidos
- Código fuente de la aplicación
- Configuraciones de producción
- Scripts de despliegue
- Templates y archivos estáticos
- Configuraciones de Nginx y Supervisor

## Instrucciones de Despliegue
1. Subir todos los archivos al servidor
2. Ejecutar: pip install -r requirements_production.txt
3. Ejecutar: python manage.py migrate --settings=sistema_construccion.production_settings
4. Ejecutar: python manage.py collectstatic --settings=sistema_construccion.production_settings --noinput
5. Reiniciar servicios: supervisorctl restart sistema_construccion
"""
    
    with open(temp_dir / 'DEPLOYMENT_INFO.txt', 'w', encoding='utf-8') as f:
        f.write(deployment_info)
    
    log(f"✓ Paquete creado en: {temp_dir}", "SUCCESS")
    return temp_dir

def create_zip_package(temp_dir):
    """Crear archivo ZIP del paquete de despliegue"""
    log("Creando archivo ZIP...")
    
    zip_name = f"sistema_construccion_deployment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    try:
        shutil.make_archive(zip_name.replace('.zip', ''), 'zip', temp_dir)
        log(f"✓ Archivo ZIP creado: {zip_name}", "SUCCESS")
        return zip_name
    except Exception as e:
        log(f"✗ Error creando ZIP: {e}", "ERROR")
        return None

def create_deployment_script():
    """Crear script de actualización para el servidor"""
    script_content = """#!/bin/bash
# Script de Actualización Rápida para Servidor
# Ejecutar en el servidor después de subir los archivos

set -e

# Colores
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"
}

# Configuración
PROJECT_DIR="/var/www/sistema_construccion"
VENV_DIR="$PROJECT_DIR/venv"

log "=== INICIANDO ACTUALIZACIÓN RÁPIDA ==="

# Verificar que estamos en el directorio correcto
if [ ! -f "manage.py" ]; then
    error "No se encontró manage.py. Ejecutar desde el directorio del proyecto."
fi

# Activar entorno virtual
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    log "Entorno virtual activado"
else
    warn "No se encontró entorno virtual en $VENV_DIR"
fi

# Instalar/actualizar dependencias
log "Instalando dependencias..."
pip install -r requirements_production.txt

# Aplicar migraciones
log "Aplicando migraciones..."
python manage.py migrate --settings=sistema_construccion.production_settings

# Recolectar archivos estáticos
log "Recolectando archivos estáticos..."
python manage.py collectstatic --settings=sistema_construccion.production_settings --noinput

# Verificar configuración
log "Verificando configuración..."
python manage.py check --settings=sistema_construccion.production_settings

# Reiniciar servicios
log "Reiniciando servicios..."
if command -v supervisorctl &> /dev/null; then
    supervisorctl restart sistema_construccion
    log "✓ Aplicación reiniciada"
else
    warn "Supervisor no encontrado, reiniciar manualmente"
fi

# Verificar que todo funcione
log "Verificando aplicación..."
if curl -s http://localhost/health/ | grep -q "healthy"; then
    log "✓ Aplicación funcionando correctamente"
else
    warn "No se pudo verificar el estado de la aplicación"
fi

log "=== ACTUALIZACIÓN COMPLETADA ==="
log "El sistema ha sido actualizado con los cambios más recientes"
"""
    
    with open('actualizar_servidor.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # Hacer ejecutable
    os.chmod('actualizar_servidor.sh', 0o755)
    log("✓ Script de actualización creado: actualizar_servidor.sh", "SUCCESS")

def main():
    """Función principal"""
    log("=== SCRIPT DE ACTUALIZACIÓN RÁPIDA ===")
    
    # Verificar que estamos en un repositorio Git
    if not os.path.exists('.git'):
        log("✗ No se encontró repositorio Git", "ERROR")
        return
    
    # Verificar estado de Git
    if not check_git_status():
        log("⚠️  Hay cambios sin commitear. ¿Deseas continuar? (y/n): ", "WARNING")
        response = input().lower()
        if response != 'y':
            log("Operación cancelada", "INFO")
            return
    
    # Obtener información del commit
    commit_hash, commit_message = get_latest_commit()
    if not commit_hash:
        log("✗ No se pudo obtener información del commit", "ERROR")
        return
    
    # Crear paquete de despliegue
    temp_dir = create_deployment_package()
    if not temp_dir:
        log("✗ Error creando paquete de despliegue", "ERROR")
        return
    
    # Crear archivo ZIP
    zip_file = create_zip_package(temp_dir)
    if not zip_file:
        log("✗ Error creando archivo ZIP", "ERROR")
        return
    
    # Crear script de actualización
    create_deployment_script()
    
    # Limpiar directorio temporal
    shutil.rmtree(temp_dir)
    
    log("=== ACTUALIZACIÓN PREPARADA ===", "SUCCESS")
    log("Archivos creados:", "SUCCESS")
    log(f"  📦 {zip_file} - Paquete de despliegue", "SUCCESS")
    log(f"  🔧 actualizar_servidor.sh - Script de actualización", "SUCCESS")
    log("", "INFO")
    log("Próximos pasos:", "INFO")
    log("1. Subir el archivo ZIP al servidor", "INFO")
    log("2. Extraer en el directorio del proyecto", "INFO")
    log("3. Ejecutar: chmod +x actualizar_servidor.sh", "INFO")
    log("4. Ejecutar: ./actualizar_servidor.sh", "INFO")
    log("", "INFO")
    log("¡Listo para desplegar! 🚀", "SUCCESS")

if __name__ == '__main__':
    main()







