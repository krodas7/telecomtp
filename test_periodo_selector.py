#!/usr/bin/env python3
"""
Script de prueba para el selector de período del dashboard
"""

import os
import sys
import django
from pathlib import Path

# Configurar Django
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import RequestFactory
from core.views import dashboard

def test_periodo_selector():
    """Probar el selector de período"""
    print("🧪 Probando selector de período del dashboard...")
    
    # Crear request factory
    factory = RequestFactory()
    
    # Probar diferentes períodos
    periodos = ['6', '3', '1']
    
    for periodo in periodos:
        print(f"\n📊 Probando período: {periodo}")
        
        # Crear request con parámetro de período
        request = factory.get(f'/dashboard/?periodo={periodo}')
        
        # Simular usuario autenticado (necesario para el decorator @login_required)
        from django.contrib.auth.models import User
        user = User.objects.first()
        if user:
            request.user = user
            
            try:
                # Llamar a la vista
                response = dashboard(request)
                
                if response.status_code == 200:
                    print(f"   ✅ Período {periodo}: OK")
                    
                    # Verificar que el contexto tenga el período correcto
                    if hasattr(response, 'context_data'):
                        periodo_actual = response.context_data.get('periodo_actual')
                        meses_grafico = response.context_data.get('meses_grafico')
                        ingresos = response.context_data.get('ingresos_mensuales')
                        gastos = response.context_data.get('gastos_mensuales')
                        
                        print(f"      📅 Período actual: {periodo_actual}")
                        print(f"      📊 Meses gráfico: {meses_grafico}")
                        print(f"      💰 Ingresos: {len(ingresos)} elementos")
                        print(f"      💸 Gastos: {len(gastos)} elementos")
                        
                        # Verificar que los datos coincidan con el período
                        if periodo == '1' and len(meses_grafico) == 1:
                            print(f"      ✅ Mes actual: 1 mes mostrado")
                        elif periodo == '3' and len(meses_grafico) == 3:
                            print(f"      ✅ 3 meses: 3 meses mostrados")
                        elif periodo == '6' and len(meses_grafico) == 6:
                            print(f"      ✅ 6 meses: 6 meses mostrados")
                        else:
                            print(f"      ⚠️ Datos no coinciden con período esperado")
                    else:
                        print(f"      ⚠️ No se pudo acceder al contexto")
                        
                else:
                    print(f"   ❌ Período {periodo}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Período {periodo}: Excepción - {str(e)}")
        else:
            print(f"   ⚠️ No hay usuarios en la base de datos")
    
    print("\n🎯 Prueba completada!")

if __name__ == '__main__':
    test_periodo_selector()
