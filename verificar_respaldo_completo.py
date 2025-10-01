#!/usr/bin/env python3
"""
Script de Verificación de Respaldo Completo del Sistema ARCA
============================================================

Este script verifica que el sistema de respaldos esté funcionando correctamente
y que incluya todos los componentes del sistema.

Uso:
    python verificar_respaldo_completo.py
    python verificar_respaldo_completo.py --test-backup
"""

import os
import sys
import json
import sqlite3
import zipfile
from pathlib import Path
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class VerificadorRespaldo:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / 'backups' / 'automatico'
        self.media_dir = self.project_root / 'media'
        self.db_path = self.project_root / 'db.sqlite3'
        
    def verificar_sistema_completo(self):
        """Verificar que el sistema esté completo y funcional"""
        logger.info("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA ARCA")
        logger.info("=" * 50)
        
        resultados = {
            'base_datos': self.verificar_base_datos(),
            'archivos_media': self.verificar_archivos_media(),
            'configuracion': self.verificar_configuracion(),
            'templates': self.verificar_templates(),
            'static_files': self.verificar_static_files(),
            'scripts': self.verificar_scripts(),
            'modelos': self.verificar_modelos(),
            'respaldos_existentes': self.verificar_respaldos_existentes()
        }
        
        # Resumen
        logger.info("\n📊 RESUMEN DE VERIFICACIÓN")
        logger.info("=" * 30)
        
        total_verificaciones = len(resultados)
        verificaciones_exitosas = sum(1 for resultado in resultados.values() if resultado['estado'] == 'OK')
        
        for nombre, resultado in resultados.items():
            estado_icono = "✅" if resultado['estado'] == 'OK' else "❌"
            logger.info(f"{estado_icono} {nombre.replace('_', ' ').title()}: {resultado['estado']}")
            if resultado['detalles']:
                for detalle in resultado['detalles']:
                    logger.info(f"   - {detalle}")
        
        logger.info(f"\n🎯 RESULTADO FINAL: {verificaciones_exitosas}/{total_verificaciones} verificaciones exitosas")
        
        if verificaciones_exitosas == total_verificaciones:
            logger.info("🎉 ¡SISTEMA COMPLETO Y FUNCIONAL!")
            return True
        else:
            logger.warning("⚠️ ALGUNAS VERIFICACIONES FALLARON")
            return False
    
    def verificar_base_datos(self):
        """Verificar que la base de datos esté completa y funcional"""
        try:
            if not self.db_path.exists():
                return {'estado': 'ERROR', 'detalles': ['Base de datos no encontrada']}
            
            # Conectar a la base de datos
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar tablas principales
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tablas = [row[0] for row in cursor.fetchall()]
            
            tablas_esperadas = [
                'core_proyecto', 'core_cliente', 'core_colaborador', 'core_factura',
                'core_gasto', 'core_categoriagasto', 'core_anticipo', 'core_archivoproyecto',
                'core_trabajadordiario', 'core_registrotrabajo', 'core_anticipotrabajadordiario',
                'core_planillatrabajadoresdiarios', 'core_planillaliquidada'
            ]
            
            tablas_faltantes = [tabla for tabla in tablas_esperadas if tabla not in tablas]
            tablas_extra = [tabla for tabla in tablas if tabla not in tablas_esperadas and not tabla.startswith('django_')]
            
            detalles = []
            if tablas_faltantes:
                detalles.append(f"Tablas faltantes: {', '.join(tablas_faltantes)}")
            if tablas_extra:
                detalles.append(f"Tablas adicionales: {', '.join(tablas_extra)}")
            
            # Verificar datos en tablas principales
            cursor.execute("SELECT COUNT(*) FROM core_proyecto")
            proyectos_count = cursor.fetchone()[0]
            detalles.append(f"Proyectos: {proyectos_count}")
            
            cursor.execute("SELECT COUNT(*) FROM core_cliente")
            clientes_count = cursor.fetchone()[0]
            detalles.append(f"Clientes: {clientes_count}")
            
            cursor.execute("SELECT COUNT(*) FROM core_trabajadordiario")
            trabajadores_count = cursor.fetchone()[0]
            detalles.append(f"Trabajadores diarios: {trabajadores_count}")
            
            cursor.execute("SELECT COUNT(*) FROM core_planillatrabajadoresdiarios")
            planillas_count = cursor.fetchone()[0]
            detalles.append(f"Planillas: {planillas_count}")
            
            conn.close()
            
            if tablas_faltantes:
                return {'estado': 'ERROR', 'detalles': detalles}
            else:
                return {'estado': 'OK', 'detalles': detalles}
                
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando BD: {str(e)}']}
    
    def verificar_archivos_media(self):
        """Verificar archivos de media"""
        try:
            if not self.media_dir.exists():
                return {'estado': 'WARNING', 'detalles': ['Directorio media no existe']}
            
            # Contar archivos por tipo
            archivos = list(self.media_dir.rglob('*'))
            archivos_archivo = [f for f in archivos if f.is_file()]
            
            tipos_archivo = {}
            for archivo in archivos_archivo:
                extension = archivo.suffix.lower()
                tipos_archivo[extension] = tipos_archivo.get(extension, 0) + 1
            
            detalles = [f"Total archivos: {len(archivos_archivo)}"]
            for tipo, cantidad in sorted(tipos_archivo.items()):
                detalles.append(f"{tipo}: {cantidad}")
            
            return {'estado': 'OK', 'detalles': detalles}
            
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando media: {str(e)}']}
    
    def verificar_configuracion(self):
        """Verificar archivos de configuración"""
        try:
            archivos_config = [
                'manage.py',
                'requirements.txt',
                'sistema_construccion/settings.py',
                'core/urls.py',
                'core/models.py',
                'core/views.py',
                'core/forms_simple.py'
            ]
            
            archivos_faltantes = []
            archivos_presentes = []
            
            for archivo in archivos_config:
                archivo_path = self.project_root / archivo
                if archivo_path.exists():
                    archivos_presentes.append(archivo)
                else:
                    archivos_faltantes.append(archivo)
            
            detalles = [f"Archivos presentes: {len(archivos_presentes)}"]
            if archivos_faltantes:
                detalles.append(f"Archivos faltantes: {', '.join(archivos_faltantes)}")
            
            estado = 'OK' if not archivos_faltantes else 'ERROR'
            return {'estado': estado, 'detalles': detalles}
            
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando configuración: {str(e)}']}
    
    def verificar_templates(self):
        """Verificar templates del sistema"""
        try:
            templates_dir = self.project_root / 'templates'
            if not templates_dir.exists():
                return {'estado': 'ERROR', 'detalles': ['Directorio templates no existe']}
            
            # Contar templates por módulo
            modulos = {}
            for template_path in templates_dir.rglob('*.html'):
                modulo = template_path.parent.name
                modulos[modulo] = modulos.get(modulo, 0) + 1
            
            detalles = []
            total_templates = sum(modulos.values())
            detalles.append(f"Total templates: {total_templates}")
            
            for modulo, cantidad in sorted(modulos.items()):
                detalles.append(f"{modulo}: {cantidad}")
            
            return {'estado': 'OK', 'detalles': detalles}
            
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando templates: {str(e)}']}
    
    def verificar_static_files(self):
        """Verificar archivos estáticos"""
        try:
            static_dir = self.project_root / 'static'
            if not static_dir.exists():
                return {'estado': 'WARNING', 'detalles': ['Directorio static no existe']}
            
            archivos_static = list(static_dir.rglob('*'))
            archivos_archivo = [f for f in archivos_static if f.is_file()]
            
            tipos_archivo = {}
            for archivo in archivos_archivo:
                extension = archivo.suffix.lower()
                tipos_archivo[extension] = tipos_archivo.get(extension, 0) + 1
            
            detalles = [f"Total archivos estáticos: {len(archivos_archivo)}"]
            for tipo, cantidad in sorted(tipos_archivo.items()):
                detalles.append(f"{tipo}: {cantidad}")
            
            return {'estado': 'OK', 'detalles': detalles}
            
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando static files: {str(e)}']}
    
    def verificar_scripts(self):
        """Verificar scripts de respaldo y utilidades"""
        try:
            scripts_dir = self.project_root / 'scripts'
            if not scripts_dir.exists():
                return {'estado': 'WARNING', 'detalles': ['Directorio scripts no existe']}
            
            scripts = list(scripts_dir.glob('*.py'))
            scripts_backup = [s for s in scripts if 'backup' in s.name.lower()]
            
            detalles = [f"Total scripts: {len(scripts)}"]
            detalles.append(f"Scripts de respaldo: {len(scripts_backup)}")
            
            for script in scripts_backup:
                detalles.append(f"- {script.name}")
            
            return {'estado': 'OK', 'detalles': detalles}
            
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando scripts: {str(e)}']}
    
    def verificar_modelos(self):
        """Verificar que los modelos estén correctamente definidos"""
        try:
            models_file = self.project_root / 'core' / 'models.py'
            if not models_file.exists():
                return {'estado': 'ERROR', 'detalles': ['Archivo models.py no encontrado']}
            
            with open(models_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            modelos_esperados = [
                'class Proyecto', 'class Cliente', 'class Colaborador', 'class Factura',
                'class Gasto', 'class CategoriaGasto', 'class Anticipo', 'class ArchivoProyecto',
                'class TrabajadorDiario', 'class RegistroTrabajo', 'class AnticipoTrabajadorDiario',
                'class PlanillaTrabajadoresDiarios', 'class PlanillaLiquidada'
            ]
            
            modelos_presentes = [modelo for modelo in modelos_esperados if modelo in content]
            modelos_faltantes = [modelo for modelo in modelos_esperados if modelo not in content]
            
            detalles = [f"Modelos presentes: {len(modelos_presentes)}"]
            if modelos_faltantes:
                detalles.append(f"Modelos faltantes: {', '.join(modelos_faltantes)}")
            
            estado = 'OK' if not modelos_faltantes else 'ERROR'
            return {'estado': estado, 'detalles': detalles}
            
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando modelos: {str(e)}']}
    
    def verificar_respaldos_existentes(self):
        """Verificar respaldos existentes"""
        try:
            if not self.backup_dir.exists():
                return {'estado': 'WARNING', 'detalles': ['Directorio de respaldos no existe']}
            
            respaldos = list(self.backup_dir.glob('*.zip'))
            respaldos_recientes = [r for r in respaldos if (datetime.now() - datetime.fromtimestamp(r.stat().st_mtime)).days < 7]
            
            detalles = [f"Total respaldos: {len(respaldos)}"]
            detalles.append(f"Respaldos recientes (últimos 7 días): {len(respaldos_recientes)}")
            
            if respaldos:
                ultimo_respaldo = max(respaldos, key=lambda x: x.stat().st_mtime)
                fecha_ultimo = datetime.fromtimestamp(ultimo_respaldo.stat().st_mtime)
                detalles.append(f"Último respaldo: {fecha_ultimo.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return {'estado': 'OK', 'detalles': detalles}
            
        except Exception as e:
            return {'estado': 'ERROR', 'detalles': [f'Error verificando respaldos: {str(e)}']}
    
    def crear_respaldo_prueba(self):
        """Crear un respaldo de prueba para verificar funcionalidad"""
        try:
            logger.info("🧪 CREANDO RESPALDO DE PRUEBA")
            logger.info("=" * 30)
            
            # Importar y ejecutar el script de respaldo
            sys.path.append(str(self.project_root))
            from scripts.backup_automatico import BackupAutomatico
            
            backup = BackupAutomatico(str(self.project_root))
            resultado = backup.crear_respaldo(backup_type='full', compress=True, retention_days=1)
            
            if resultado:
                logger.info("✅ Respaldo de prueba creado exitosamente")
                return True
            else:
                logger.error("❌ Error creando respaldo de prueba")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error en respaldo de prueba: {str(e)}")
            return False

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Verificar sistema de respaldos ARCA')
    parser.add_argument('--test-backup', action='store_true', help='Crear respaldo de prueba')
    parser.add_argument('--project-root', default='.', help='Ruta del proyecto')
    
    args = parser.parse_args()
    
    verificador = VerificadorRespaldo(args.project_root)
    
    # Verificar sistema completo
    sistema_ok = verificador.verificar_sistema_completo()
    
    # Crear respaldo de prueba si se solicita
    if args.test_backup:
        logger.info("\n" + "="*50)
        respaldo_ok = verificador.crear_respaldo_prueba()
        
        if respaldo_ok:
            logger.info("🎉 ¡SISTEMA DE RESPALDOS FUNCIONANDO CORRECTAMENTE!")
        else:
            logger.error("❌ PROBLEMA CON EL SISTEMA DE RESPALDOS")
    
    return 0 if sistema_ok else 1

if __name__ == '__main__':
    sys.exit(main())
