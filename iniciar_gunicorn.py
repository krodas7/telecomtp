#!/usr/bin/env python
"""
Script para iniciar Gunicorn con la configuración correcta
"""

import os
import sys
import subprocess
import signal
import time

def iniciar_gunicorn():
    """Inicia Gunicorn con la configuración del proyecto"""
    print("🚀 Iniciando Gunicorn para el Sistema de Construcción...")
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("❌ Error: No se encontró manage.py")
        print("   Asegúrate de estar en el directorio raíz del proyecto Django")
        return False
    
    # Verificar que Gunicorn esté instalado
    try:
        import gunicorn
        print(f"✅ Gunicorn {gunicorn.__version__} instalado")
    except ImportError:
        print("❌ Gunicorn no está instalado")
        print("   Instala con: pip install gunicorn")
        return False
    
    # Comando para iniciar Gunicorn
    comando = [
        'gunicorn',
        '--config', 'gunicorn.conf.py',
        '--bind', '127.0.0.1:8000',
        '--workers', '3',
        '--timeout', '30',
        '--preload',
        'sistema_construccion.wsgi:application'
    ]
    
    print(f"📋 Comando: {' '.join(comando)}")
    print("⏳ Iniciando servidor...")
    
    try:
        # Iniciar Gunicorn
        proceso = subprocess.Popen(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"✅ Gunicorn iniciado con PID: {proceso.pid}")
        print("🌐 Servidor disponible en: http://127.0.0.1:8000")
        print("📝 Presiona Ctrl+C para detener el servidor")
        
        # Esperar a que el proceso termine
        try:
            stdout, stderr = proceso.communicate()
            if proceso.returncode == 0:
                print("✅ Gunicorn terminó correctamente")
            else:
                print(f"❌ Gunicorn terminó con código: {proceso.returncode}")
                if stderr:
                    print(f"Error: {stderr}")
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo Gunicorn...")
            proceso.terminate()
            proceso.wait()
            print("✅ Gunicorn detenido")
        
        return True
        
    except Exception as e:
        print(f"❌ Error iniciando Gunicorn: {e}")
        return False

def verificar_gunicorn():
    """Verifica que Gunicorn esté funcionando correctamente"""
    print("\n🔍 Verificando estado de Gunicorn...")
    
    try:
        import requests
        response = requests.get('http://127.0.0.1:8000/', timeout=5)
        if response.status_code == 200:
            print("✅ Gunicorn responde correctamente")
            return True
        else:
            print(f"⚠️ Gunicorn responde con código: {response.status_code}")
            return False
    except ImportError:
        print("⚠️ requests no está instalado, no se puede verificar")
        return True
    except Exception as e:
        print(f"❌ Error verificando Gunicorn: {e}")
        return False

def main():
    """Función principal"""
    print("=" * 60)
    print("SISTEMA DE CONSTRUCCIÓN - INICIADOR DE GUNICORN")
    print("=" * 60)
    
    # Iniciar Gunicorn
    if iniciar_gunicorn():
        print("\n🎉 Gunicorn iniciado exitosamente!")
        
        # Verificar funcionamiento
        verificar_gunicorn()
        
        print("\n" + "=" * 60)
        print("INFORMACIÓN DEL SERVIDOR")
        print("=" * 60)
        print("• URL: http://127.0.0.1:8000")
        print("• Workers: 3")
        print("• Timeout: 30 segundos")
        print("• Configuración: gunicorn.conf.py")
        print("• Logs: Consola")
        print("\nPara detener: Ctrl+C")
        print("Para reiniciar: python iniciar_gunicorn.py")
        
    else:
        print("\n❌ No se pudo iniciar Gunicorn")
        print("Revisa los errores anteriores")

if __name__ == "__main__":
    main()
