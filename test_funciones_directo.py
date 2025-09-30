#!/usr/bin/env python3
"""
Test directo de las funciones de aprobar
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from core.models import CategoriaGasto, Proyecto, Gasto
from core.views import gasto_aprobar, gasto_desaprobar
from datetime import date

def test_funciones_directas():
    """Test directo de las funciones"""
    print("🔧 TEST DIRECTO DE FUNCIONES")
    print("=" * 50)
    
    try:
        # Crear gasto de prueba
        proyecto = Proyecto.objects.first()
        categoria = CategoriaGasto.objects.first()
        admin_user = User.objects.filter(is_superuser=True).first()
        
        if not proyecto or not categoria or not admin_user:
            print("❌ No hay datos necesarios")
            return False
        
        gasto = Gasto.objects.create(
            proyecto=proyecto,
            categoria=categoria,
            descripcion='Test directo',
            monto=25.00,
            fecha_gasto=date.today(),
            aprobado=False
        )
        
        print(f"✅ Gasto creado: {gasto.id}")
        print(f"   Estado inicial: {gasto.aprobado}")
        
        # Crear request factory
        factory = RequestFactory()
        request = factory.get(f'/gastos/aprobar/{gasto.id}/')
        request.user = admin_user
        
        # Probar función directamente
        print("   Probando función gasto_aprobar...")
        response = gasto_aprobar(request, gasto.id)
        print(f"   Respuesta: {response.status_code}")
        
        # Verificar que se aprobó
        gasto.refresh_from_db()
        print(f"   Estado después: {gasto.aprobado}")
        
        if gasto.aprobado:
            print("✅ Función de aprobar funciona correctamente")
        else:
            print("❌ Función de aprobar no funciona")
            return False
        
        # Probar desaprobar
        request2 = factory.get(f'/gastos/desaprobar/{gasto.id}/')
        request2.user = admin_user
        
        print("   Probando función gasto_desaprobar...")
        response2 = gasto_desaprobar(request2, gasto.id)
        print(f"   Respuesta: {response2.status_code}")
        
        # Verificar que se desaprobó
        gasto.refresh_from_db()
        print(f"   Estado después: {gasto.aprobado}")
        
        if not gasto.aprobado:
            print("✅ Función de desaprobar funciona correctamente")
        else:
            print("❌ Función de desaprobar no funciona")
            return False
        
        # Limpiar
        gasto.delete()
        print("✅ Test directo completado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_funciones_directas()
    sys.exit(0 if success else 1)
