#!/usr/bin/env python3
"""
Test sin decorador para verificar si el problema es el decorador
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
from datetime import date
from django.shortcuts import redirect

def gasto_aprobar_simple(request, gasto_id):
    """Función simple sin decorador"""
    try:
        gasto = Gasto.objects.get(id=gasto_id)
        
        if gasto.aprobado:
            print("   Gasto ya está aprobado")
        else:
            gasto.aprobado = True
            gasto.aprobado_por = request.user
            gasto.save()
            print("   Gasto aprobado")
        
        return redirect('gastos_list')
        
    except Gasto.DoesNotExist:
        print("   Gasto no encontrado")
        return redirect('gastos_list')
    except Exception as e:
        print(f"   Error: {e}")
        return redirect('gastos_list')

def test_sin_decorador():
    """Test sin decorador"""
    print("🔧 TEST SIN DECORADOR")
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
            descripcion='Test sin decorador',
            monto=20.00,
            fecha_gasto=date.today(),
            aprobado=False
        )
        
        print(f"✅ Gasto creado: {gasto.id}")
        print(f"   Estado inicial: {gasto.aprobado}")
        
        # Crear request factory
        factory = RequestFactory()
        request = factory.get(f'/gastos/aprobar/{gasto.id}/')
        request.user = admin_user
        
        # Probar función simple
        print("   Llamando gasto_aprobar_simple...")
        response = gasto_aprobar_simple(request, gasto.id)
        
        print(f"   Tipo de respuesta: {type(response)}")
        print(f"   Status code: {response.status_code}")
        print(f"   URL: {response.url if hasattr(response, 'url') else 'No URL'}")
        
        # Verificar que se aprobó
        gasto.refresh_from_db()
        print(f"   Estado después: {gasto.aprobado}")
        
        # Limpiar
        gasto.delete()
        
        if response.status_code == 302:
            print("✅ Redirect funciona correctamente")
            return True
        else:
            print("❌ Redirect no funciona")
            return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sin_decorador()
    sys.exit(0 if success else 1)
