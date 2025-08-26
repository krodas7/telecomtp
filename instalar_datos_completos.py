#!/usr/bin/env python
"""
Script de instalación completa de datos para el Sistema de Construcción
Ejecuta todos los generadores en secuencia para una instalación completa
"""

import os
import sys
import subprocess
import time

def ejecutar_script(script_path, descripcion):
    """Ejecuta un script de Python y muestra el progreso"""
    print(f"\n{'='*70}")
    print(f"EJECUTANDO: {descripcion}")
    print(f"Script: {script_path}")
    print(f"{'='*70}")
    
    try:
        # Ejecutar el script
        resultado = subprocess.run([sys.executable, script_path], 
                                 capture_output=True, text=True, check=True)
        
        print("Script ejecutado exitosamente")
        if resultado.stdout:
            print("Salida del script:")
            print(resultado.stdout)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {script_path}: {e}")
        if e.stdout:
            print("Salida estándar:")
            print(e.stdout)
        if e.stderr:
            print("Error estándar:")
            print(e.stderr)
        return False
    except FileNotFoundError:
        print(f"No se encontró el script: {script_path}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def verificar_dependencias():
    """Verifica que las dependencias estén instaladas"""
    print("Verificando dependencias...")
    
    try:
        import django
        print("Django instalado")
    except ImportError:
        print("Django no está instalado")
        return False
    
    try:
        import numpy
        print("NumPy instalado")
    except ImportError:
        print("NumPy no está instalado")
        return False
    
    try:
        import pandas
        print("Pandas instalado")
    except ImportError:
        print("Pandas no está instalado")
        return False
    
    try:
        import sklearn
        print("Scikit-learn instalado")
    except ImportError:
        print("Scikit-learn no está instalado")
        return False
    
    return True

def main():
    """Función principal de instalación"""
    print("INSTALADOR COMPLETO DE DATOS - SISTEMA DE CONSTRUCCION")
    print("=" * 70)
    print("Este script instalará:")
    print("Datos masivos del sistema (clientes, proyectos, facturas, etc.)")
    print("Datos específicos para IA y machine learning")
    print("Casos de prueba para análisis de riesgos")
    print("Datos para gráficos y reportes del dashboard")
    print("=" * 70)
    
    # Verificar que estemos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("Error: No se encontró manage.py")
        print("   Asegúrate de estar en el directorio raíz del proyecto Django")
        return
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\nFaltan dependencias. Instala las dependencias primero:")
        print("   pip install -r requirements.txt")
        return
    
    # Confirmar instalación automáticamente
    print("\nIniciando instalación automática...")
    print("Este proceso puede tomar varios minutos...")
    
    # Lista de scripts a ejecutar en orden
    scripts = [
        ('cargar_datos_masivos.py', 'Generación de datos masivos del sistema'),
        ('generar_datos_ia.py', 'Generación de datos específicos para IA')
    ]
    
    # Ejecutar scripts en secuencia
    exitos = []
    for script_path, descripcion in scripts:
        if os.path.exists(script_path):
            exito = ejecutar_script(script_path, descripcion)
            exitos.append(exito)
            
            if not exito:
                print(f"\nError en {descripcion}")
                print("   Continuando con los siguientes scripts...")
        else:
            print(f"\nScript no encontrado: {script_path}")
            print("   Saltando...")
            exitos.append(False)
    
    # Resumen final
    print(f"\n{'='*70}")
    print("RESUMEN DE INSTALACION")
    print(f"{'='*70}")
    
    total_scripts = len(scripts)
    scripts_exitosos = sum(exitos)
    
    print(f"Total de scripts: {total_scripts}")
    print(f"Scripts exitosos: {scripts_exitosos}")
    print(f"Scripts fallidos: {total_scripts - scripts_exitosos}")
    
    if scripts_exitosos == total_scripts:
        print(f"\n¡INSTALACION COMPLETADA EXITOSAMENTE!")
        print(f"{'='*70}")
        print("El sistema está listo para pruebas de rendimiento!")
        print("\nCredenciales de acceso:")
        print("   • Usuario: admin")
        print("   • Contraseña: admin123")
        print("\nPróximos pasos:")
        print("1. Iniciar el servidor: python manage.py runserver")
        print("2. Acceder al dashboard: http://127.0.0.1:8000/")
        print("3. Probar la generación de reportes IA")
        print("4. Verificar el rendimiento del sistema")
        print("5. Probar los módulos de inteligencia artificial")
        print("6. Verificar gráficos y visualizaciones del dashboard")
        
    elif scripts_exitosos > 0:
        print(f"\nINSTALACION PARCIALMENTE COMPLETADA")
        print(f"{'='*70}")
        print("Algunos scripts fallaron, pero el sistema puede funcionar")
        print("Revisa los errores anteriores para más detalles")
        
    else:
        print(f"\nINSTALACION FALLIDA")
        print(f"{'='*70}")
        print("Todos los scripts fallaron")
        print("Revisa los errores anteriores y verifica la configuración")
    
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
