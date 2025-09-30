#!/usr/bin/env python3
"""
Script para probar la eliminación de archivos
"""

import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, ArchivoProyecto, CarpetaProyecto
from django.contrib.auth.models import User

def test_eliminar_archivo():
    print("🧪 Probando eliminación de archivos...")
    
    # Obtener un archivo para eliminar
    archivo = ArchivoProyecto.objects.filter(activo=True).first()
    if not archivo:
        print("❌ No hay archivos para eliminar")
        return
    
    print(f"📄 Archivo a eliminar: {archivo.nombre}")
    print(f"📄 ID: {archivo.id}")
    print(f"📄 Proyecto: {archivo.proyecto.nombre}")
    
    # Simular petición POST
    url = f"http://localhost:8000/archivos/{archivo.id}/eliminar/"
    
    data = {
        'confirmacion': 'ELIMINAR',
        'csrfmiddlewaretoken': 'test'  # Esto no funcionará sin sesión real
    }
    
    try:
        # Primero hacer GET para obtener la página
        response = requests.get(url, timeout=10)
        print(f"✅ GET exitoso: {response.status_code}")
        
        # Buscar el token CSRF en el HTML
        import re
        csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
        if csrf_match:
            csrf_token = csrf_match.group(1)
            print(f"✅ Token CSRF encontrado: {csrf_token[:20]}...")
            
            # Ahora hacer POST con el token real
            data['csrfmiddlewaretoken'] = csrf_token
            
            # Crear sesión para mantener cookies
            session = requests.Session()
            session.get(url)  # Obtener cookies
            
            response = session.post(url, data=data, timeout=10)
            print(f"✅ POST exitoso: {response.status_code}")
            
            if response.status_code == 302:
                print("✅ Redirección exitosa (archivo eliminado)")
            else:
                print(f"❌ Error en POST: {response.status_code}")
                print(f"Respuesta: {response.text[:200]}")
        else:
            print("❌ No se encontró token CSRF")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_eliminar_archivo()
