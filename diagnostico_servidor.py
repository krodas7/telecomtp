#!/usr/bin/env python3
"""
Script de diagnóstico completo del servidor TelecomTP
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

def run_command(cmd):
    """Ejecutar comando y retornar resultado"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_file_exists(file_path):
    """Verificar si un archivo existe"""
    return os.path.exists(file_path)

def check_service_status(service_name):
    """Verificar estado de un servicio"""
    success, stdout, stderr = run_command(f"systemctl is-active {service_name}")
    return success and "active" in stdout

def check_nginx_config():
    """Verificar configuración de Nginx"""
    success, stdout, stderr = run_command("nginx -t")
    return success

def check_static_files():
    """Verificar archivos estáticos"""
    static_files = [
        "staticfiles/css/sidebar-fix.css",
        "staticfiles/css/neostructure-theme.css",
        "staticfiles/css/sidebar-layout.css",
        "staticfiles/images/LOGO-TELECOM-small.png",
        "staticfiles/images/ISOTIPO-TELECOM-small.png"
    ]
    
    missing_files = []
    for file_path in static_files:
        if not check_file_exists(file_path):
            missing_files.append(file_path)
    
    return missing_files

def check_database_connection():
    """Verificar conexión a la base de datos"""
    try:
        from django.core.management import execute_from_command_line
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
        
        # Intentar conectar a la base de datos
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        return True, "Conexión a BD exitosa"
    except Exception as e:
        return False, f"Error de BD: {str(e)}"

def check_web_accessibility():
    """Verificar accesibilidad web"""
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        return response.status_code == 200, f"Status: {response.status_code}"
    except Exception as e:
        return False, f"Error de conexión: {str(e)}"

def main():
    print("🔍 DIAGNÓSTICO COMPLETO DEL SERVIDOR TELECOMTP")
    print("=" * 50)
    
    # 1. Verificar servicios
    print("\n1. SERVICIOS:")
    telecomtp_status = check_service_status("telecomtp")
    nginx_status = check_service_status("nginx")
    
    print(f"   TelecomTP: {'✅ Activo' if telecomtp_status else '❌ Inactivo'}")
    print(f"   Nginx: {'✅ Activo' if nginx_status else '❌ Inactivo'}")
    
    # 2. Verificar configuración de Nginx
    print("\n2. CONFIGURACIÓN NGINX:")
    nginx_ok = check_nginx_config()
    print(f"   Configuración: {'✅ Válida' if nginx_ok else '❌ Inválida'}")
    
    # 3. Verificar archivos estáticos
    print("\n3. ARCHIVOS ESTÁTICOS:")
    missing_files = check_static_files()
    if missing_files:
        print("   ❌ Archivos faltantes:")
        for file_path in missing_files:
            print(f"      - {file_path}")
    else:
        print("   ✅ Todos los archivos estáticos presentes")
    
    # 4. Verificar base de datos
    print("\n4. BASE DE DATOS:")
    db_ok, db_msg = check_database_connection()
    print(f"   {db_msg}")
    
    # 5. Verificar accesibilidad web
    print("\n5. ACCESIBILIDAD WEB:")
    web_ok, web_msg = check_web_accessibility()
    print(f"   {web_msg}")
    
    # 6. Verificar archivos CSS específicos
    print("\n6. ARCHIVOS CSS CRÍTICOS:")
    css_files = [
        "static/css/sidebar-fix.css",
        "static/css/neostructure-theme.css", 
        "static/css/sidebar-layout.css"
    ]
    
    for css_file in css_files:
        exists = check_file_exists(css_file)
        print(f"   {css_file}: {'✅ Existe' if exists else '❌ No existe'}")
        
        if exists:
            # Verificar contenido del archivo
            try:
                with open(css_file, 'r') as f:
                    content = f.read()
                    if 'sidebar' in content.lower():
                        print(f"      ✅ Contiene estilos de sidebar")
                    else:
                        print(f"      ⚠️  No contiene estilos de sidebar")
            except Exception as e:
                print(f"      ❌ Error al leer archivo: {e}")
    
    # 7. Recomendaciones
    print("\n7. RECOMENDACIONES:")
    
    if not telecomtp_status:
        print("   - Reiniciar servicio: systemctl restart telecomtp")
    
    if not nginx_status:
        print("   - Reiniciar Nginx: systemctl restart nginx")
    
    if missing_files:
        print("   - Recopilar archivos estáticos: python manage.py collectstatic --noinput")
    
    if not nginx_ok:
        print("   - Verificar configuración de Nginx: nginx -t")
    
    if not db_ok:
        print("   - Verificar configuración de base de datos")
    
    if not web_ok:
        print("   - Verificar que el servidor esté escuchando en el puerto correcto")
    
    print("\n" + "=" * 50)
    print("Diagnóstico completado")

if __name__ == "__main__":
    main()

