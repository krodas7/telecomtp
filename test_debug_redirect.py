#!/usr/bin/env python3
"""
Test para debuggear el problema del redirect
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
from core.views import gasto_aprobar
from datetime import date

def test_debug_redirect():
    """Test para debuggear redirect"""
    print("🔧 DEBUG REDIRECT")
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
            descripcion='Test debug',
            monto=15.00,
            fecha_gasto=date.today(),
            aprobado=False
        )
        
        print(f"✅ Gasto creado: {gasto.id}")
        print(f"   Estado inicial: {gasto.aprobado}")
        
        # Crear request factory
        factory = RequestFactory()
        request = factory.get(f'/gastos/aprobar/{gasto.id}/')
        request.user = admin_user
        
        print(f"   Request method: {request.method}")
        print(f"   Request path: {request.path}")
        print(f"   Request user: {request.user}")
        
        # Probar función directamente
        print("   Llamando gasto_aprobar...")
        response = gasto_aprobar(request, gasto.id)
        
        print(f"   Tipo de respuesta: {type(response)}")
        print(f"   Status code: {response.status_code}")
        print(f"   URL: {response.url if hasattr(response, 'url') else 'No URL'}")
        
        # Verificar que se aprobó
        gasto.refresh_from_db()
        print(f"   Estado después: {gasto.aprobado}")
        
        # Limpiar
        gasto.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_debug_redirect()
    sys.exit(0 if success else 1)
