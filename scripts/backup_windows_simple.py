#!/usr/bin/env python3
"""
Script de Respaldo Automático para Windows
==========================================

Script simplificado sin emojis para evitar problemas de codificación en Windows.
"""

import os
import sys
import shutil
import zipfile
import json
from pathlib import Path
from datetime import datetime, timedelta

class BackupWindows:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.backup_root = self.project_root / 'backups' / 'automatico'
        self.logs_dir = self.project_root / 'logs'
        
        # Crear directorios si no existen
        self.backup_root.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def crear_respaldo(self, backup_type='full', compress=True, retention_days=30):
        """Crear respaldo automático"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = self.backup_root / f'backup_{timestamp}'
            backup_dir.mkdir(exist_ok=True)
            
            print(f"[INFO] Iniciando respaldo automático: {backup_type}")
            
            # Respaldo de base de datos
            if backup_type in ['db', 'full']:
                self._backup_database(backup_dir, timestamp)
            
            # Respaldo de archivos media
            if backup_type in ['media', 'full']:
                self._backup_media(backup_dir, timestamp)
            
            # Respaldo de configuración
            if backup_type == 'full':
                self._backup_configuracion(backup_dir, timestamp)
            
            # Comprimir si se solicita
            if compress:
                self._comprimir_respaldo(backup_dir, timestamp)
            
            # Limpiar respaldos antiguos
            self._limpiar_respaldos_antiguos(retention_days)
            
            # Crear reporte de respaldo
            self._crear_reporte_respaldo(timestamp, backup_type, backup_dir)
            
            print(f"[SUCCESS] Respaldo {backup_type} completado exitosamente")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error en respaldo automático: {str(e)}")
            return False
    
    def _backup_database(self, backup_dir, timestamp):
        """Respaldar base de datos SQLite"""
        try:
            db_path = self.project_root / 'db.sqlite3'
            if db_path.exists():
                backup_file = backup_dir / f'db_backup_{timestamp}.sqlite3'
                shutil.copy2(db_path, backup_file)
                print(f"   [INFO] Base de datos respaldada: {backup_file.name}")
                
                # Verificar integridad del respaldo
                if self._verificar_integridad_db(backup_file):
                    print("   [SUCCESS] Integridad de BD verificada")
                else:
                    print("   [WARNING] Problema de integridad en respaldo de BD")
            else:
                print("   [WARNING] Base de datos no encontrada")
        except Exception as e:
            print(f"   [ERROR] Error al respaldar BD: {str(e)}")
    
    def _backup_media(self, backup_dir, timestamp):
        """Respaldar archivos de media"""
        try:
            media_dir = self.project_root / 'media'
            if media_dir.exists() and media_dir.is_dir():
                media_backup = backup_dir / f'media_backup_{timestamp}'
                shutil.copytree(media_dir, media_backup)
                print(f"   [INFO] Archivos media respaldados: {media_backup.name}")
            else:
                print("   [INFO] No hay archivos media para respaldar")
        except Exception as e:
            print(f"   [ERROR] Error al respaldar media: {str(e)}")
    
    def _backup_configuracion(self, backup_dir, timestamp):
        """Respaldar archivos de configuración importantes"""
        try:
            config_backup = backup_dir / f'config_backup_{timestamp}'
            config_backup.mkdir(exist_ok=True)
            
            # Archivos importantes
            important_files = [
                'manage.py',
                'requirements.txt',
                'smartasp.env',
                'gunicorn.conf.py'
            ]
            
            for file_name in important_files:
                file_path = self.project_root / file_name
                if file_path.exists():
                    shutil.copy2(file_path, config_backup / file_name)
                    print(f"   [INFO] Configuración respaldada: {file_name}")
            
            print(f"   [INFO] Archivos de configuración respaldados: {config_backup.name}")
            
        except Exception as e:
            print(f"   [ERROR] Error al respaldar configuración: {str(e)}")
    
    def _comprimir_respaldo(self, backup_dir, timestamp):
        """Comprimir el respaldo completo"""
        try:
            zip_path = self.backup_root / f'backup_{timestamp}.zip'
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_dir)
                        zipf.write(file_path, arcname)
            
            # Eliminar directorio original
            try:
                shutil.rmtree(backup_dir)
            except PermissionError:
                print("   [WARNING] No se pudo eliminar directorio temporal")
            
            print(f"   [INFO] Respaldo comprimido: {zip_path.name}")
            
        except Exception as e:
            print(f"   [ERROR] Error al comprimir: {str(e)}")
    
    def _limpiar_respaldos_antiguos(self, retention_days):
        """Limpiar respaldos antiguos"""
        try:
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            deleted_count = 0
            
            for item in self.backup_root.iterdir():
                if item.is_file() and item.suffix == '.zip':
                    # Obtener fecha del archivo
                    stat = item.stat()
                    file_date = datetime.fromtimestamp(stat.st_mtime)
                    
                    if file_date < cutoff_date:
                        try:
                            item.unlink()
                            deleted_count += 1
                            print(f"   [INFO] Respaldo antiguo eliminado: {item.name}")
                        except PermissionError:
                            print(f"   [WARNING] No se pudo eliminar: {item.name}")
            
            if deleted_count > 0:
                print(f"   [INFO] {deleted_count} respaldos antiguos eliminados")
            else:
                print("   [INFO] No hay respaldos antiguos para eliminar")
                
        except Exception as e:
            print(f"   [ERROR] Error al limpiar respaldos: {str(e)}")
    
    def _verificar_integridad_db(self, backup_file):
        """Verificar integridad de la base de datos respaldada"""
        try:
            import sqlite3
            conn = sqlite3.connect(backup_file)
            cursor = conn.cursor()
            
            # Verificar que se puede acceder a las tablas principales
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            conn.close()
            
            # Verificar que hay al menos algunas tablas
            return len(tables) > 0
            
        except Exception:
            return False
    
    def _crear_reporte_respaldo(self, timestamp, backup_type, backup_dir):
        """Crear reporte del respaldo realizado"""
        try:
            reporte = {
                'fecha_respaldo': timestamp,
                'tipo_respaldo': backup_type,
                'estado': 'completado',
                'archivos_respaldados': [],
                'tamaño_total': 0,
                'errores': []
            }
            
            # Calcular tamaño total
            if backup_dir.exists():
                total_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
                reporte['tamaño_total'] = total_size
                
                # Listar archivos
                for file_path in backup_dir.rglob('*'):
                    if file_path.is_file():
                        reporte['archivos_respaldados'].append({
                            'nombre': str(file_path.relative_to(backup_dir)),
                            'tamaño': file_path.stat().st_size,
                            'fecha_modificacion': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        })
            
            # Guardar reporte
            reporte_file = self.backup_root / f'reporte_respaldo_{timestamp}.json'
            with open(reporte_file, 'w', encoding='utf-8') as f:
                json.dump(reporte, f, indent=2, ensure_ascii=False)
            
            print(f"   [INFO] Reporte de respaldo creado: {reporte_file.name}")
            
        except Exception as e:
            print(f"   [ERROR] Error al crear reporte: {str(e)}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Script de Respaldo Automático para Windows')
    parser.add_argument('--type', choices=['db', 'full', 'media'], default='full',
                       help='Tipo de respaldo (default: full)')
    parser.add_argument('--compress', action='store_true', default=True,
                       help='Comprimir el respaldo (default: True)')
    parser.add_argument('--retention', type=int, default=30,
                       help='Días de retención (default: 30)')
    parser.add_argument('--project-root', type=str, default='.',
                       help='Ruta raíz del proyecto (default: directorio actual)')
    
    args = parser.parse_args()
    
    # Obtener ruta del proyecto
    if args.project_root == '.':
        project_root = os.getcwd()
    else:
        project_root = args.project_root
    
    # Crear instancia de backup
    backup_system = BackupWindows(project_root)
    
    # Ejecutar respaldo
    success = backup_system.crear_respaldo(
        backup_type=args.type,
        compress=args.compress,
        retention_days=args.retention
    )
    
    if success:
        print("[SUCCESS] Respaldo automático completado exitosamente")
        sys.exit(0)
    else:
        print("[ERROR] Error en el respaldo automático")
        sys.exit(1)

if __name__ == '__main__':
    main()
