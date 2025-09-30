#!/usr/bin/env python3
"""
Test simple para verificar la funcionalidad de aprobar gastos
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import CategoriaGasto, Proyecto, Cliente, Gasto
from datetime import date

def test_aprobar_gasto():
    """Test simple para aprobar gasto"""
    print("🔧 TEST SIMPLE DE APROBAR GASTO")
    print("=" * 50)
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        # Crear gasto de prueba
        proyecto = Proyecto.objects.first()
        categoria = CategoriaGasto.objects.first()
        
        if not proyecto or not categoria:
            print("❌ No hay proyecto o categoría disponible")
            return False
        
        gasto = Gasto.objects.create(
            proyecto=proyecto,
            categoria=categoria,
            descripcion='Test de aprobación',
            monto=50.00,
            fecha_gasto=date.today(),
            aprobado=False
        )
        
        print(f"✅ Gasto creado: {gasto.id}")
        print(f"   Estado inicial: {gasto.aprobado}")
        
        # Probar aprobar
        response = client.get(f'/gastos/aprobar/{gasto.id}/')
        print(f"   Respuesta aprobar: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Redirect correcto")
            # Verificar que se aprobó
            gasto.refresh_from_db()
            print(f"   Estado después: {gasto.aprobado}")
            if gasto.aprobado:
                print("✅ Gasto aprobado correctamente")
            else:
                print("❌ Gasto no se aprobó")
                return False
        else:
            print(f"❌ Error en redirect: {response.status_code}")
            print(f"   Contenido: {response.content.decode()[:200]}")
            return False
        
        # Probar desaprobar
        response = client.get(f'/gastos/desaprobar/{gasto.id}/')
        print(f"   Respuesta desaprobar: {response.status_code}")
        
        if response.status_code == 302:
            print("✅ Redirect correcto")
            # Verificar que se desaprobó
            gasto.refresh_from_db()
            print(f"   Estado después: {gasto.aprobado}")
            if not gasto.aprobado:
                print("✅ Gasto desaprobado correctamente")
            else:
                print("❌ Gasto no se desaprobó")
                return False
        else:
            print(f"❌ Error en redirect: {response.status_code}")
            return False
        
        # Limpiar
        gasto.delete()
        print("✅ Test completado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_aprobar_gasto()
    sys.exit(0 if success else 1)
