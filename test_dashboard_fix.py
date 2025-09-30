#!/usr/bin/env python3
"""
Script para probar que el dashboard funcione correctamente
"""

import os
import django
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, Cliente, Factura, Gasto, Anticipo
from django.contrib.auth.models import User

def test_dashboard():
    print("🧪 Probando dashboard...")
    
    # Verificar datos en la base de datos
    total_clientes = Cliente.objects.filter(activo=True).count()
    total_proyectos = Proyecto.objects.filter(activo=True).count()
    total_facturas = Factura.objects.count()
    total_gastos = Gasto.objects.count()
    total_anticipos = Anticipo.objects.count()
    
    print(f"📊 Datos en BD:")
    print(f"  - Clientes activos: {total_clientes}")
    print(f"  - Proyectos activos: {total_proyectos}")
    print(f"  - Facturas: {total_facturas}")
    print(f"  - Gastos: {total_gastos}")
    print(f"  - Anticipos: {total_anticipos}")
    
    # Probar acceso al dashboard
    try:
        response = requests.get('http://localhost:8000/dashboard/', timeout=10)
        print(f"✅ Dashboard accesible: {response.status_code}")
        
        if response.status_code == 200:
            # Verificar que no contenga el mensaje de error
            if "contexto de emergencia" in response.text:
                print("❌ Dashboard usando contexto de emergencia")
            else:
                print("✅ Dashboard usando datos reales")
                
            # Verificar que contenga datos
            if "PROYECTOS ACTIVOS" in response.text and "0" in response.text:
                print("⚠️ Dashboard muestra 0 proyectos (posible problema de datos)")
            else:
                print("✅ Dashboard muestra datos")
        else:
            print(f"❌ Error en dashboard: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_dashboard()
