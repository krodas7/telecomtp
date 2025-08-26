#!/usr/bin/env python3
"""
Script de Backup Automático para Sistema ARCA Construcción en Producción
Ejecutar diariamente con cron para mantener respaldos automáticos
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración
BACKUP_DIR = "/var/backups/sistema-arca"
RETENTION_DAYS = 30
DB_NAME = "arca_construccion"
DB_USER = "arca_user"
MEDIA_DIR = "/var/www/sistema-arca/media"
STATIC_DIR = "/var/www/sistema-arca/staticfiles"
LOG_DIR = "/var/log/sistema-arca"

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/backup.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def crear_directorios():
    """Crear directorios necesarios para backups"""
    try:
        Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        logger.info("✅ Directorios de backup creados/verificados")
    except Exception as e:
        logger.error(f"❌ Error creando directorios: {e}")
        raise

def backup_base_datos():
    """Crear backup de la base de datos PostgreSQL"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{BACKUP_DIR}/db_backup_{timestamp}.sql"
        
        # Comando pg_dump
        cmd = [
            "sudo", "-u", "postgres", "pg_dump",
            "-h", "localhost",
            "-U", DB_USER,
            "-d", DB_NAME,
            "-f", backup_file,
            "--verbose"
        ]
        
        # Ejecutar backup
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            # Comprimir backup
            compressed_file = f"{backup_file}.gz"
            subprocess.run(["gzip", backup_file], check=True)
            
            file_size = os.path.getsize(compressed_file)
            logger.info(f"✅ Backup de BD creado: {compressed_file} ({file_size} bytes)")
            return compressed_file
        else:
            logger.error(f"❌ Error en backup de BD: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error en backup de BD: {e}")
        return None

def backup_archivos():
    """Crear backup de archivos media y static"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{BACKUP_DIR}/files_backup_{timestamp}.tar.gz"
        
        # Crear tar.gz con archivos
        cmd = [
            "tar", "-czf", backup_file,
            "-C", "/var/www/sistema-arca",
            "media", "staticfiles"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            file_size = os.path.getsize(backup_file)
            logger.info(f"✅ Backup de archivos creado: {backup_file} ({file_size} bytes)")
            return backup_file
        else:
            logger.error(f"❌ Error en backup de archivos: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error en backup de archivos: {e}")
        return None

def backup_configuracion():
    """Crear backup de archivos de configuración"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{BACKUP_DIR}/config_backup_{timestamp}.tar.gz"
        
        # Archivos importantes a respaldar
        config_files = [
            "/etc/nginx/sites-available/sistema-arca",
            "/etc/systemd/system/sistema-arca.service",
            "/var/www/sistema-arca/gunicorn.conf.py",
            "/var/www/sistema-arca/requirements.txt"
        ]
        
        # Crear tar.gz con archivos de configuración
        cmd = ["tar", "-czf", backup_file] + config_files
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            file_size = os.path.getsize(backup_file)
            logger.info(f"✅ Backup de configuración creado: {backup_file} ({file_size} bytes)")
            return backup_file
        else:
            logger.error(f"❌ Error en backup de configuración: {result.stderr}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Error en backup de configuración: {e}")
        return None

def limpiar_backups_antiguos():
    """Eliminar backups más antiguos que RETENTION_DAYS"""
    try:
        cutoff_date = datetime.now() - timedelta(days=RETENTION_DAYS)
        deleted_count = 0
        
        for backup_file in Path(BACKUP_DIR).glob("*"):
            if backup_file.is_file():
                file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
                if file_time < cutoff_date:
                    backup_file.unlink()
                    deleted_count += 1
                    logger.info(f"🗑️ Backup eliminado: {backup_file}")
        
        logger.info(f"✅ {deleted_count} backups antiguos eliminados")
        
    except Exception as e:
        logger.error(f"❌ Error limpiando backups antiguos: {e}")

def generar_reporte():
    """Generar reporte de backup"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"{BACKUP_DIR}/reporte_backup_{timestamp}.json"
        
        # Obtener información de backups
        backup_files = []
        total_size = 0
        
        for backup_file in Path(BACKUP_DIR).glob("*"):
            if backup_file.is_file():
                file_info = {
                    "nombre": backup_file.name,
                    "tamaño_bytes": backup_file.stat().st_size,
                    "fecha_modificacion": datetime.fromtimestamp(backup_file.stat().st_mtime).isoformat()
                }
                backup_files.append(file_info)
                total_size += file_info["tamaño_bytes"]
        
        # Crear reporte
        reporte = {
            "fecha_backup": datetime.now().isoformat(),
            "total_archivos": len(backup_files),
            "tamaño_total_bytes": total_size,
            "tamaño_total_mb": round(total_size / (1024 * 1024), 2),
            "archivos": backup_files,
            "configuracion": {
                "directorio_backup": BACKUP_DIR,
                "retencion_dias": RETENTION_DAYS,
                "base_datos": DB_NAME
            }
        }
        
        # Guardar reporte
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Reporte generado: {report_file}")
        return reporte
        
    except Exception as e:
        logger.error(f"❌ Error generando reporte: {e}")
        return None

def enviar_notificacion(reporte):
    """Enviar notificación por email del backup"""
    try:
        # Configuración de email (cambiar según tu proveedor)
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_user = os.environ.get('SMTP_USER', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        
        if not all([smtp_user, smtp_password]):
            logger.warning("⚠️ Configuración de email incompleta, saltando notificación")
            return
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = smtp_user  # Enviar a ti mismo
        msg['Subject'] = f"✅ Backup Sistema ARCA - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Cuerpo del mensaje
        body = f"""
        🚀 Backup del Sistema ARCA Construcción completado exitosamente
        
        📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        📊 Total archivos: {reporte['total_archivos']}
        💾 Tamaño total: {reporte['tamaño_total_mb']} MB
        
        📁 Directorio: {BACKUP_DIR}
        🔄 Retención: {RETENTION_DAYS} días
        
        ¡El sistema está respaldado y seguro! 🎉
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Enviar email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        logger.info("✅ Notificación por email enviada")
        
    except Exception as e:
        logger.error(f"❌ Error enviando notificación: {e}")

def main():
    """Función principal del script de backup"""
    try:
        logger.info("🚀 Iniciando backup automático del Sistema ARCA Construcción")
        
        # Crear directorios
        crear_directorios()
        
        # Crear backups
        db_backup = backup_base_datos()
        files_backup = backup_archivos()
        config_backup = backup_configuracion()
        
        # Verificar que se crearon los backups principales
        if not db_backup:
            logger.error("❌ Falló backup de base de datos")
            return False
        
        # Limpiar backups antiguos
        limpiar_backups_antiguos()
        
        # Generar reporte
        reporte = generar_reporte()
        
        # Enviar notificación
        if reporte:
            enviar_notificacion(reporte)
        
        logger.info("🎉 Backup automático completado exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error crítico en backup: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
