#!/usr/bin/env python3
"""
Script de monitoreo de recursos para TelecomTP
Ejecutar con: python monitor_resources.py
"""

import psutil
import time
import os
import sys
import django
from pathlib import Path

# Configurar Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.core.cache import cache
from django.db import connection

def get_system_info():
    """Obtener información del sistema"""
    return {
        'cpu_percent': psutil.cpu_percent(interval=1),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_percent': psutil.disk_usage('/').percent,
        'load_average': os.getloadavg(),
        'processes': len(psutil.pids()),
    }

def get_django_info():
    """Obtener información de Django"""
    try:
        # Información de caché
        cache_info = cache.get('system_info', {})
        
        # Información de base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM django_migrations")
            migrations = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            users = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM core_proyecto")
            proyectos = cursor.fetchone()[0]
        
        return {
            'migrations': migrations,
            'users': users,
            'proyectos': proyectos,
            'cache_working': cache.set('test', 'ok', 10) and cache.get('test') == 'ok'
        }
    except Exception as e:
        return {'error': str(e)}

def check_services():
    """Verificar servicios críticos"""
    services = {
        'nginx': False,
        'gunicorn': False,
        'postgresql': False,
        'redis': False,
    }
    
    try:
        # Verificar nginx
        result = os.popen('systemctl is-active nginx').read().strip()
        services['nginx'] = result == 'active'
        
        # Verificar gunicorn
        result = os.popen('systemctl is-active telecomtp').read().strip()
        services['gunicorn'] = result == 'active'
        
        # Verificar postgresql
        result = os.popen('systemctl is-active postgresql').read().strip()
        services['postgresql'] = result == 'active'
        
        # Verificar redis
        result = os.popen('systemctl is-active redis-server').read().strip()
        services['redis'] = result == 'active'
        
    except Exception as e:
        print(f"Error verificando servicios: {e}")
    
    return services

def print_report():
    """Imprimir reporte de recursos"""
    print("=" * 60)
    print("📊 REPORTE DE RECURSOS TELECOMTP")
    print("=" * 60)
    
    # Información del sistema
    sys_info = get_system_info()
    print(f"\n🖥️  SISTEMA:")
    print(f"   CPU: {sys_info['cpu_percent']:.1f}%")
    print(f"   Memoria: {sys_info['memory_percent']:.1f}%")
    print(f"   Disco: {sys_info['disk_percent']:.1f}%")
    print(f"   Load Average: {sys_info['load_average'][0]:.2f}")
    print(f"   Procesos: {sys_info['processes']}")
    
    # Información de Django
    django_info = get_django_info()
    print(f"\n🐍 DJANGO:")
    if 'error' in django_info:
        print(f"   Error: {django_info['error']}")
    else:
        print(f"   Migraciones: {django_info['migrations']}")
        print(f"   Usuarios: {django_info['users']}")
        print(f"   Proyectos: {django_info['proyectos']}")
        print(f"   Caché: {'✅' if django_info['cache_working'] else '❌'}")
    
    # Servicios
    services = check_services()
    print(f"\n🔧 SERVICIOS:")
    for service, status in services.items():
        status_icon = "✅" if status else "❌"
        print(f"   {service}: {status_icon}")
    
    # Recomendaciones
    print(f"\n💡 RECOMENDACIONES:")
    if sys_info['cpu_percent'] > 80:
        print("   ⚠️  CPU alta - Considerar optimizar consultas")
    if sys_info['memory_percent'] > 85:
        print("   ⚠️  Memoria alta - Considerar reiniciar servicios")
    if sys_info['disk_percent'] > 90:
        print("   ⚠️  Disco lleno - Limpiar logs y archivos temporales")
    
    if not all(services.values()):
        print("   ⚠️  Algunos servicios no están activos")
    
    print("=" * 60)

if __name__ == "__main__":
    print_report()
