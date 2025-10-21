#!/usr/bin/env python3
"""
Script de diagnóstico para problemas de generación de PDF en el servidor
"""

import os
import sys
import subprocess
import importlib

def print_header(title):
    """Imprimir encabezado"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def check_python_package(package_name):
    """Verificar si un paquete de Python está instalado"""
    try:
        importlib.import_module(package_name)
        return True, "Instalado"
    except ImportError as e:
        return False, f"No instalado: {str(e)}"

def check_system_package(package_name):
    """Verificar si un paquete del sistema está instalado (Ubuntu/Debian)"""
    try:
        result = subprocess.run(
            ['dpkg', '-l', package_name],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and 'ii' in result.stdout:
            return True, "Instalado"
        else:
            return False, "No instalado"
    except Exception as e:
        return False, f"Error al verificar: {str(e)}"

def test_reportlab_import():
    """Probar importar ReportLab y sus componentes"""
    print_header("PRUEBA DE IMPORTACIÓN DE REPORTLAB")
    
    components = [
        ('reportlab', 'ReportLab base'),
        ('reportlab.lib.pagesizes', 'Tamaños de página'),
        ('reportlab.platypus', 'Platypus'),
        ('reportlab.lib.styles', 'Estilos'),
        ('reportlab.lib.colors', 'Colores'),
        ('reportlab.lib.enums', 'Enumeraciones'),
        ('reportlab.lib.units', 'Unidades'),
    ]
    
    all_ok = True
    for module_name, description in components:
        status, msg = check_python_package(module_name)
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {description:30s} {msg}")
        if not status:
            all_ok = False
    
    return all_ok

def test_pdf_generation():
    """Intentar generar un PDF de prueba"""
    print_header("PRUEBA DE GENERACIÓN DE PDF")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from io import BytesIO
        
        # Crear PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Agregar contenido
        story.append(Paragraph("Prueba de PDF", styles['Heading1']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Este es un PDF de prueba generado para diagnosticar el sistema.", styles['Normal']))
        
        # Generar PDF
        doc.build(story)
        
        pdf_size = len(buffer.getvalue())
        print(f"✅ PDF generado exitosamente ({pdf_size} bytes)")
        
        # Intentar guardar archivo
        test_file = '/tmp/test_pdf_reportlab.pdf'
        try:
            with open(test_file, 'wb') as f:
                f.write(buffer.getvalue())
            print(f"✅ PDF guardado en: {test_file}")
            os.remove(test_file)
            print(f"✅ Archivo de prueba eliminado")
        except Exception as e:
            print(f"❌ Error al guardar PDF: {str(e)}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {str(e)}")
        import traceback
        print("\nDetalles del error:")
        print(traceback.format_exc())
        return False

def check_system_dependencies():
    """Verificar dependencias del sistema necesarias para ReportLab"""
    print_header("DEPENDENCIAS DEL SISTEMA")
    
    system_packages = [
        ('python3-dev', 'Herramientas de desarrollo de Python'),
        ('libfreetype6-dev', 'FreeType (fuentes)'),
        ('libjpeg-dev', 'JPEG'),
        ('libpng-dev', 'PNG'),
        ('zlib1g-dev', 'Compresión zlib'),
        ('liblcms2-dev', 'Color Management'),
        ('libwebp-dev', 'WebP'),
    ]
    
    all_ok = True
    for package, description in system_packages:
        status, msg = check_system_package(package)
        status_icon = "✅" if status else "⚠️"
        print(f"{status_icon} {description:30s} ({package}): {msg}")
        if not status:
            all_ok = False
    
    return all_ok

def check_python_dependencies():
    """Verificar dependencias de Python"""
    print_header("DEPENDENCIAS DE PYTHON")
    
    python_packages = [
        ('reportlab', 'ReportLab'),
        ('pytz', 'Timezone support'),
        ('pillow', 'Pillow (imágenes)'),
        ('openpyxl', 'Excel'),
        ('django', 'Django'),
    ]
    
    all_ok = True
    for package, description in python_packages:
        status, msg = check_python_package(package)
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {description:30s} {msg}")
        if not status:
            all_ok = False
            
        # Si está instalado, mostrar versión
        if status:
            try:
                module = importlib.import_module(package)
                if hasattr(module, '__version__'):
                    print(f"        Versión: {module.__version__}")
            except:
                pass
    
    return all_ok

def check_django_settings():
    """Verificar configuración de Django"""
    print_header("CONFIGURACIÓN DE DJANGO")
    
    try:
        # Configurar Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
        
        import django
        django.setup()
        
        from django.conf import settings
        
        # Verificar MEDIA_ROOT
        print(f"📁 MEDIA_ROOT: {settings.MEDIA_ROOT}")
        if os.path.exists(settings.MEDIA_ROOT):
            print(f"   ✅ Directorio existe")
            if os.access(settings.MEDIA_ROOT, os.W_OK):
                print(f"   ✅ Tiene permisos de escritura")
            else:
                print(f"   ❌ Sin permisos de escritura")
        else:
            print(f"   ❌ Directorio no existe")
        
        # Verificar STATIC_ROOT
        print(f"📁 STATIC_ROOT: {settings.STATIC_ROOT}")
        if os.path.exists(settings.STATIC_ROOT):
            print(f"   ✅ Directorio existe")
        else:
            print(f"   ⚠️  Directorio no existe")
        
        # Verificar DEBUG
        print(f"🔧 DEBUG: {settings.DEBUG}")
        if settings.DEBUG:
            print(f"   ⚠️  DEBUG está activo en producción")
        else:
            print(f"   ✅ DEBUG desactivado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar configuración de Django: {str(e)}")
        return False

def check_disk_space():
    """Verificar espacio en disco"""
    print_header("ESPACIO EN DISCO")
    
    try:
        import shutil
        
        # Verificar espacio en /tmp
        total, used, free = shutil.disk_usage('/tmp')
        total_gb = total / (2**30)
        used_gb = used / (2**30)
        free_gb = free / (2**30)
        percent_used = (used / total) * 100
        
        print(f"💾 /tmp:")
        print(f"   Total: {total_gb:.2f} GB")
        print(f"   Usado: {used_gb:.2f} GB ({percent_used:.1f}%)")
        print(f"   Libre: {free_gb:.2f} GB")
        
        if free_gb < 1:
            print(f"   ⚠️  Poco espacio libre")
            return False
        else:
            print(f"   ✅ Espacio suficiente")
            return True
            
    except Exception as e:
        print(f"❌ Error al verificar espacio: {str(e)}")
        return False

def check_memory():
    """Verificar memoria disponible"""
    print_header("MEMORIA DEL SISTEMA")
    
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        mem_info = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                mem_info[key.strip()] = value.strip()
        
        # Extraer valores en KB
        mem_total = int(mem_info['MemTotal'].split()[0])
        mem_free = int(mem_info['MemFree'].split()[0])
        mem_available = int(mem_info['MemAvailable'].split()[0])
        
        # Convertir a GB
        total_gb = mem_total / (1024 * 1024)
        free_gb = mem_free / (1024 * 1024)
        available_gb = mem_available / (1024 * 1024)
        
        print(f"💾 Memoria:")
        print(f"   Total: {total_gb:.2f} GB")
        print(f"   Libre: {free_gb:.2f} GB")
        print(f"   Disponible: {available_gb:.2f} GB")
        
        if available_gb < 0.5:
            print(f"   ⚠️  Poca memoria disponible")
            return False
        else:
            print(f"   ✅ Memoria suficiente")
            return True
            
    except Exception as e:
        print(f"❌ Error al verificar memoria: {str(e)}")
        return False

def check_logs():
    """Verificar logs recientes de errores"""
    print_header("LOGS DE ERROR RECIENTES")
    
    log_paths = [
        '/var/log/gunicorn/error.log',
        '/var/log/nginx/error.log',
        'logs/error.log',
        'logs/gunicorn.log',
    ]
    
    found_errors = False
    for log_path in log_paths:
        if os.path.exists(log_path):
            try:
                # Leer últimas 20 líneas
                with open(log_path, 'r') as f:
                    lines = f.readlines()
                    last_lines = lines[-20:] if len(lines) > 20 else lines
                
                # Buscar errores de PDF
                pdf_errors = [line for line in last_lines if 'pdf' in line.lower() or 'reportlab' in line.lower()]
                
                if pdf_errors:
                    print(f"\n📋 {log_path}:")
                    for line in pdf_errors[-5:]:  # Últimos 5 errores
                        print(f"   {line.strip()}")
                    found_errors = True
            except Exception as e:
                print(f"⚠️  No se pudo leer {log_path}: {str(e)}")
    
    if not found_errors:
        print("ℹ️  No se encontraron errores de PDF en los logs")

def generate_solution_script():
    """Generar script de solución"""
    print_header("SCRIPT DE SOLUCIÓN")
    
    script_content = """#!/bin/bash
# Script de solución para problemas de PDF en el servidor

echo "🔧 Iniciando solución de problemas de PDF..."

# 1. Instalar dependencias del sistema
echo "📦 Instalando dependencias del sistema..."
sudo apt-get update
sudo apt-get install -y \\
    python3-dev \\
    libfreetype6-dev \\
    libjpeg-dev \\
    libpng-dev \\
    zlib1g-dev \\
    liblcms2-dev \\
    libwebp-dev \\
    build-essential

# 2. Activar entorno virtual
if [ -d "venv" ]; then
    echo "🐍 Activando entorno virtual..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# 3. Reinstalar reportlab
echo "📚 Reinstalando reportlab..."
pip uninstall -y reportlab
pip install --no-cache-dir reportlab>=4.0.0

# 4. Instalar pytz si no está
echo "🌍 Verificando pytz..."
pip install --upgrade pytz>=2023.3

# 5. Verificar permisos de media
echo "🔒 Verificando permisos..."
if [ -d "media" ]; then
    chmod -R 755 media/
    chown -R www-data:www-data media/ 2>/dev/null || chown -R $USER:$USER media/
fi

# 6. Crear directorio temporal si no existe
mkdir -p /tmp/django_pdf
chmod 777 /tmp/django_pdf

# 7. Reiniciar servicios
echo "🔄 Reiniciando servicios..."
sudo systemctl restart gunicorn 2>/dev/null || sudo systemctl restart telecomtp
sudo systemctl restart nginx

echo "✅ Solución completada. Prueba generar un PDF nuevamente."
"""
    
    script_path = 'fix_pdf_servidor.sh'
    try:
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        print(f"✅ Script de solución creado: {script_path}")
        print(f"\nPara ejecutar:")
        print(f"   chmod +x {script_path}")
        print(f"   ./{script_path}")
        return True
    except Exception as e:
        print(f"❌ Error al crear script: {str(e)}")
        return False

def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("  🔍 DIAGNÓSTICO DE PROBLEMAS DE PDF EN EL SERVIDOR")
    print("=" * 70)
    
    results = {}
    
    # 1. Verificar dependencias de Python
    results['python_deps'] = check_python_dependencies()
    
    # 2. Verificar dependencias del sistema
    results['system_deps'] = check_system_dependencies()
    
    # 3. Probar importación de ReportLab
    results['reportlab_import'] = test_reportlab_import()
    
    # 4. Probar generación de PDF
    if results['reportlab_import']:
        results['pdf_generation'] = test_pdf_generation()
    else:
        results['pdf_generation'] = False
        print_header("PRUEBA DE GENERACIÓN DE PDF")
        print("⏭️  Omitida (ReportLab no disponible)")
    
    # 5. Verificar configuración de Django
    results['django_config'] = check_django_settings()
    
    # 6. Verificar espacio en disco
    results['disk_space'] = check_disk_space()
    
    # 7. Verificar memoria
    results['memory'] = check_memory()
    
    # 8. Verificar logs
    check_logs()
    
    # Resumen
    print_header("RESUMEN DEL DIAGNÓSTICO")
    
    total_checks = len(results)
    passed_checks = sum(1 for v in results.values() if v)
    
    for check_name, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name.replace('_', ' ').title()}")
    
    print(f"\nResultado: {passed_checks}/{total_checks} verificaciones exitosas")
    
    # Generar script de solución
    generate_solution_script()
    
    # Recomendaciones
    print_header("RECOMENDACIONES")
    
    if not results['python_deps']:
        print("❌ Faltan dependencias de Python")
        print("   → Ejecutar: pip install -r requirements_production_simple.txt")
    
    if not results['system_deps']:
        print("❌ Faltan dependencias del sistema")
        print("   → Ejecutar el script: ./fix_pdf_servidor.sh")
    
    if not results['reportlab_import']:
        print("❌ ReportLab no se puede importar")
        print("   → Reinstalar: pip uninstall reportlab && pip install reportlab>=4.0.0")
    
    if not results['pdf_generation']:
        print("❌ La generación de PDF falla")
        print("   → Verificar logs y ejecutar: ./fix_pdf_servidor.sh")
    
    if not results['disk_space']:
        print("⚠️  Poco espacio en disco")
        print("   → Liberar espacio en /tmp")
    
    if not results['memory']:
        print("⚠️  Poca memoria disponible")
        print("   → Considerar ampliar memoria del servidor")
    
    print("\n" + "=" * 70)
    print("Diagnóstico completado")
    print("=" * 70 + "\n")
    
    return all(results.values())

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Diagnóstico interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

