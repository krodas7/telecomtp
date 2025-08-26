#!/usr/bin/env python
"""
Script de diagnóstico del sistema para identificar problemas
con AJAX, Gunicorn y el dashboard
"""

import os
import sys
import django
from pathlib import Path

def configurar_django():
    """Configura Django para el script"""
    try:
        # Agregar el directorio del proyecto al path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        # Configurar variables de entorno
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
        
        # Configurar Django
        django.setup()
        
        print("✓ Django configurado correctamente")
        return True
        
    except Exception as e:
        print(f"✗ Error configurando Django: {e}")
        return False

def verificar_dependencias():
    """Verifica las dependencias del sistema"""
    print("\n=== VERIFICACIÓN DE DEPENDENCIAS ===")
    
    # Verificar Django
    try:
        import django
        print(f"✓ Django {django.get_version()} instalado")
    except ImportError:
        print("✗ Django no está instalado")
        return False
    
    # Verificar dependencias de cache
    try:
        import django_redis
        print("✓ django-redis instalado")
    except ImportError:
        print("⚠ django-redis no está instalado (cache en memoria)")
    
    # Verificar dependencias de gráficos
    try:
        import numpy
        print("✓ NumPy instalado")
    except ImportError:
        print("✗ NumPy no está instalado")
    
    try:
        import pandas
        print("✓ Pandas instalado")
    except ImportError:
        print("✗ Pandas no está instalado")
    
    try:
        import sklearn
        print("✓ Scikit-learn instalado")
    except ImportError:
        print("✗ Scikit-learn no está instalado")
    
    # Verificar Gunicorn
    try:
        import gunicorn
        print("✓ Gunicorn instalado")
    except ImportError:
        print("⚠ Gunicorn no está instalado (servidor de desarrollo)")
    
    return True

def verificar_configuracion():
    """Verifica la configuración del sistema"""
    print("\n=== VERIFICACIÓN DE CONFIGURACIÓN ===")
    
    try:
        from django.conf import settings
        
        # Verificar configuración de cache
        print(f"✓ Cache backend: {settings.CACHES['default']['BACKEND']}")
        
        # Verificar configuración de base de datos
        print(f"✓ Base de datos: {settings.DATABASES['default']['ENGINE']}")
        
        # Verificar configuración de archivos estáticos
        print(f"✓ Archivos estáticos: {settings.STATIC_URL}")
        print(f"✓ Directorio estático: {settings.STATICFILES_DIRS}")
        
        # Verificar configuración de media
        print(f"✓ Media URL: {settings.MEDIA_URL}")
        print(f"✓ Media root: {settings.MEDIA_ROOT}")
        
        # Verificar configuración de templates
        print(f"✓ Directorio de templates: {settings.TEMPLATES[0]['DIRS']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verificando configuración: {e}")
        return False

def verificar_modelos():
    """Verifica que los modelos estén funcionando correctamente"""
    print("\n=== VERIFICACIÓN DE MODELOS ===")
    
    try:
        from core.models import Cliente, Proyecto, Factura, Gasto, User
        
        # Verificar que se pueden hacer consultas básicas
        total_clientes = Cliente.objects.count()
        total_proyectos = Proyecto.objects.count()
        total_facturas = Factura.objects.count()
        total_gastos = Gasto.objects.count()
        total_usuarios = User.objects.count()
        
        print(f"✓ Clientes: {total_clientes}")
        print(f"✓ Proyectos: {total_proyectos}")
        print(f"✓ Facturas: {total_facturas}")
        print(f"✓ Gastos: {total_gastos}")
        print(f"✓ Usuarios: {total_usuarios}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verificando modelos: {e}")
        return False

def verificar_urls():
    """Verifica que las URLs estén funcionando correctamente"""
    print("\n=== VERIFICACIÓN DE URLs ===")
    
    try:
        from django.urls import reverse
        from django.test import Client
        
        client = Client()
        
        # Verificar URLs principales
        urls_a_verificar = [
            'dashboard',
            'clientes_list',
            'proyectos_list',
            'facturas_list',
            'gastos_list',
        ]
        
        for url_name in urls_a_verificar:
            try:
                url = reverse(url_name)
                print(f"✓ {url_name}: {url}")
            except Exception as e:
                print(f"✗ {url_name}: Error - {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verificando URLs: {e}")
        return False

def verificar_archivos_estaticos():
    """Verifica que los archivos estáticos estén disponibles"""
    print("\n=== VERIFICACIÓN DE ARCHIVOS ESTÁTICOS ===")
    
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        
        # Verificar archivos CSS
        css_files = [
            'css/global-styles.css',
            'css/neostructure-theme.css',
            'css/neostructure-enhanced.css'
        ]
        
        for css_file in css_files:
            if find(css_file):
                print(f"✓ {css_file} encontrado")
            else:
                print(f"✗ {css_file} no encontrado")
        
        # Verificar archivos JavaScript
        js_files = [
            'js/global-functions.js',
            'js/dashboard-charts.js'
        ]
        
        for js_file in js_files:
            if find(js_file):
                print(f"✓ {js_file} encontrado")
            else:
                print(f"✗ {js_file} no encontrado")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verificando archivos estáticos: {e}")
        return False

def verificar_cache():
    """Verifica que el sistema de cache esté funcionando"""
    print("\n=== VERIFICACIÓN DE CACHE ===")
    
    try:
        from django.core.cache import cache
        
        # Probar operaciones básicas de cache
        test_key = 'test_diagnostico'
        test_value = 'valor_prueba'
        
        # Escribir en cache
        cache.set(test_key, test_value, 60)
        print("✓ Escritura en cache exitosa")
        
        # Leer del cache
        cached_value = cache.get(test_key)
        if cached_value == test_value:
            print("✓ Lectura del cache exitosa")
        else:
            print("✗ Error en lectura del cache")
        
        # Limpiar cache de prueba
        cache.delete(test_key)
        print("✓ Limpieza de cache exitosa")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verificando cache: {e}")
        return False

def verificar_servidor():
    """Verifica el estado del servidor"""
    print("\n=== VERIFICACIÓN DEL SERVIDOR ===")
    
    try:
        import socket
        
        # Verificar si el puerto 8000 está en uso
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8000))
        sock.close()
        
        if result == 0:
            print("✓ Puerto 8000 está en uso (servidor activo)")
        else:
            print("⚠ Puerto 8000 no está en uso (servidor inactivo)")
        
        return True
        
    except Exception as e:
        print(f"✗ Error verificando servidor: {e}")
        return False

def generar_reporte():
    """Genera un reporte completo del diagnóstico"""
    print("\n" + "="*60)
    print("REPORTE DE DIAGNÓSTICO DEL SISTEMA")
    print("="*60)
    
    # Ejecutar todas las verificaciones
    verificaciones = [
        ("Dependencias", verificar_dependencias),
        ("Configuración", verificar_configuracion),
        ("Modelos", verificar_modelos),
        ("URLs", verificar_urls),
        ("Archivos Estáticos", verificar_archivos_estaticos),
        ("Cache", verificar_cache),
        ("Servidor", verificar_servidor),
    ]
    
    resultados = []
    for nombre, funcion in verificaciones:
        try:
            resultado = funcion()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"✗ Error en verificación {nombre}: {e}")
            resultados.append((nombre, False))
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DEL DIAGNÓSTICO")
    print("="*60)
    
    total_verificaciones = len(resultados)
    verificaciones_exitosas = sum(1 for _, resultado in resultados if resultado)
    
    print(f"Total de verificaciones: {total_verificaciones}")
    print(f"Verificaciones exitosas: {verificaciones_exitosas}")
    print(f"Verificaciones fallidas: {total_verificaciones - verificaciones_exitosas}")
    
    if verificaciones_exitosas == total_verificaciones:
        print("\n🎉 ¡SISTEMA FUNCIONANDO PERFECTAMENTE!")
    elif verificaciones_exitosas > total_verificaciones // 2:
        print("\n⚠️ SISTEMA FUNCIONANDO CON ALGUNOS PROBLEMAS")
        print("Revisa los errores anteriores para más detalles")
    else:
        print("\n❌ SISTEMA CON PROBLEMAS CRÍTICOS")
        print("Se requiere atención inmediata")
    
    # Recomendaciones
    print("\n" + "="*60)
    print("RECOMENDACIONES")
    print("="*60)
    
    if not any("Gunicorn" in str(resultado) for _, resultado in resultados):
        print("• Instalar Gunicorn para producción: pip install gunicorn")
    
    if not any("django-redis" in str(resultado) for _, resultado in resultados):
        print("• Instalar django-redis para cache avanzado: pip install django-redis")
    
    print("• Verificar logs del servidor para errores específicos")
    print("• Revisar la consola del navegador para errores JavaScript")
    print("• Verificar que todos los archivos estáticos estén en su lugar")
    
    return resultados

def main():
    """Función principal"""
    print("DIAGNÓSTICO DEL SISTEMA DE CONSTRUCCIÓN")
    print("="*60)
    
    # Configurar Django
    if not configurar_django():
        print("No se puede continuar sin Django configurado")
        return
    
    # Generar reporte completo
    resultados = generar_reporte()
    
    print("\n" + "="*60)
    print("DIAGNÓSTICO COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    main()
