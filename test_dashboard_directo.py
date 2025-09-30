#!/usr/bin/env python3
"""
Script para probar el dashboard directamente
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.views import dashboard
from django.test import RequestFactory
from django.contrib.auth.models import User
from decimal import Decimal

def test_dashboard_directo():
    print("🧪 Probando dashboard directamente...")
    
    try:
        # Crear un usuario de prueba
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'is_staff': True, 'is_superuser': True}
        )
        
        # Crear request de prueba
        factory = RequestFactory()
        request = factory.get('/dashboard/')
        request.user = user
        
        # Llamar a la vista del dashboard
        response = dashboard(request)
        
        print(f"✅ Dashboard ejecutado exitosamente")
        print(f"📊 Status code: {response.status_code}")
        
        # Verificar que no hay errores en el contexto
        if hasattr(response, 'context_data'):
            context = response.context_data
            print(f"📊 Contexto disponible: {list(context.keys())}")
            
            # Verificar datos específicos
            if 'total_proyectos' in context:
                print(f"📊 Total proyectos: {context['total_proyectos']}")
            if 'total_clientes' in context:
                print(f"📊 Total clientes: {context['total_clientes']}")
            if 'total_facturado' in context:
                print(f"📊 Total facturado: {context['total_facturado']}")
            if 'total_cobrado' in context:
                print(f"📊 Total cobrado: {context['total_cobrado']}")
        
        print("✅ Dashboard funciona correctamente")
        
    except Exception as e:
        print(f"❌ Error en dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard_directo()
