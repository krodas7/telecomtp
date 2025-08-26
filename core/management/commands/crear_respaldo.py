from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
import os
import shutil
import zipfile
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Crea un respaldo completo de la base de datos y archivos del sistema'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--type',
            type=str,
            choices=['db', 'full', 'media'],
            default='full',
            help='Tipo de respaldo: db (solo base de datos), full (completo), media (solo archivos)'
        )
        parser.add_argument(
            '--compress',
            action='store_true',
            help='Comprimir el respaldo'
        )
        parser.add_argument(
            '--retention',
            type=int,
            default=30,
            help='Días de retención para respaldos antiguos'
        )
    
    def handle(self, *args, **options):
        backup_type = options['type']
        compress = options['compress']
        retention_days = options['retention']
        
        try:
            # Crear directorio de respaldos si no existe
            backup_dir = Path(settings.BASE_DIR) / 'backups' / 'manual'
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Timestamp para el nombre del archivo
            timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
            
            if backup_type in ['db', 'full']:
                self.backup_database(backup_dir, timestamp)
            
            if backup_type in ['media', 'full']:
                self.backup_media_files(backup_dir, timestamp)
            
            if backup_type == 'full':
                self.backup_settings_files(backup_dir, timestamp)
            
            # Comprimir si se solicita
            if compress:
                self.compress_backup(backup_dir, timestamp)
            
            # Limpiar respaldos antiguos
            self.cleanup_old_backups(backup_dir, retention_days)
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✅ Respaldo {backup_type} creado exitosamente en {backup_dir}'
                )
            )
            
        except Exception as e:
            logger.error(f"Error al crear respaldo: {str(e)}")
            self.stdout.write(
                self.style.ERROR(f'❌ Error al crear respaldo: {str(e)}')
            )
    
    def backup_database(self, backup_dir, timestamp):
        """Respaldar la base de datos SQLite"""
        try:
                    db_path = Path(settings.DATABASES['default']['NAME'])
        if str(db_path).endswith('db.sqlite3'):
                backup_file = backup_dir / f'db_backup_{timestamp}.sqlite3'
                shutil.copy2(db_path, backup_file)
                self.stdout.write(f'   📊 Base de datos respaldada: {backup_file}')
            else:
                self.stdout.write(self.style.WARNING('   ⚠️ Base de datos no es SQLite, respaldo manual requerido'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error al respaldar BD: {str(e)}'))
    
    def backup_media_files(self, backup_dir, timestamp):
        """Respaldar archivos de media"""
        try:
            media_dir = settings.MEDIA_ROOT
            if os.path.exists(media_dir):
                media_backup = backup_dir / f'media_backup_{timestamp}'
                if os.path.isdir(media_dir):
                    shutil.copytree(media_dir, media_backup)
                    self.stdout.write(f'   📁 Archivos media respaldados: {media_backup}')
                else:
                    self.stdout.write(self.style.WARNING('   ⚠️ Directorio media no encontrado'))
            else:
                self.stdout.write(self.style.WARNING('   ⚠️ Directorio media no configurado'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error al respaldar media: {str(e)}'))
    
    def backup_settings_files(self, backup_dir, timestamp):
        """Respaldar archivos de configuración importantes"""
        try:
            settings_backup = backup_dir / f'settings_backup_{timestamp}'
            settings_backup.mkdir(exist_ok=True)
            
            # Archivos importantes a respaldar
            important_files = [
                'manage.py',
                'requirements.txt',
                'smartasp.env',
                'gunicorn.conf.py'
            ]
            
            for file_name in important_files:
                file_path = Path(settings.BASE_DIR) / file_name
                if file_path.exists():
                    shutil.copy2(file_path, settings_backup / file_name)
                    self.stdout.write(f'   ⚙️ Configuración respaldada: {file_name}')
            
            self.stdout.write(f'   ⚙️ Archivos de configuración respaldados: {settings_backup}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error al respaldar configuración: {str(e)}'))
    
    def compress_backup(self, backup_dir, timestamp):
        """Comprimir el respaldo completo"""
        try:
            backup_name = f'backup_{timestamp}'
            backup_path = backup_dir / backup_name
            zip_path = backup_dir / f'{backup_name}.zip'
            
            # Crear archivo ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_dir):
                    for file in files:
                        if file.endswith(timestamp) or file.startswith(f'backup_{timestamp}'):
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, backup_dir)
                            zipf.write(file_path, arcname)
            
            # Eliminar archivos originales
            for item in backup_dir.iterdir():
                if item.name.startswith(f'backup_{timestamp}') and item.is_dir():
                    shutil.rmtree(item)
                elif item.name.startswith(f'backup_{timestamp}') and item.suffix != '.zip':
                    item.unlink()
            
            self.stdout.write(f'   📦 Respaldo comprimido: {zip_path}')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error al comprimir: {str(e)}'))
    
    def cleanup_old_backups(self, backup_dir, retention_days):
        """Limpiar respaldos antiguos"""
        try:
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            deleted_count = 0
            for item in backup_dir.iterdir():
                if item.is_file():
                    # Obtener fecha del archivo
                    stat = item.stat()
                    file_date = datetime.fromtimestamp(stat.st_mtime)
                    
                    if file_date < cutoff_date:
                        item.unlink()
                        deleted_count += 1
                        self.stdout.write(f'   🗑️ Respaldo antiguo eliminado: {item.name}')
            
            if deleted_count > 0:
                self.stdout.write(f'   🧹 {deleted_count} respaldos antiguos eliminados')
            else:
                self.stdout.write('   🧹 No hay respaldos antiguos para eliminar')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'   ❌ Error al limpiar respaldos: {str(e)}'))
