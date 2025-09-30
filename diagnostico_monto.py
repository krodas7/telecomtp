#!/usr/bin/env python3
"""
Script de diagnóstico para el campo de monto
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.forms_simple import GastoForm
from core.models import Proyecto, CategoriaGasto
from datetime import date

def diagnosticar_monto():
    """Diagnosticar el problema con el campo de monto"""
    print("🔍 DIAGNÓSTICO DEL CAMPO DE MONTO")
    print("=" * 50)
    
    # Obtener datos necesarios
    proyecto = Proyecto.objects.first()
    categoria = CategoriaGasto.objects.first()
    
    if not proyecto or not categoria:
        print("❌ Faltan datos necesarios")
        return
    
    # Probar diferentes valores de monto
    valores_prueba = [
        "0.01",
        "0.1", 
        "1.0",
        "1.00",
        "10.00",
        "100.00",
        "0",
        "1",
        "10"
    ]
    
    for valor in valores_prueba:
        print(f"\n🧪 Probando valor: '{valor}'")
        
        # Crear datos del formulario
        gasto_data = {
            'proyecto': proyecto.id,
            'categoria': categoria.id,
            'descripcion': f'Prueba con {valor}',
            'monto': valor,
            'fecha_gasto': date.today(),
            'aprobado': False,
        }
        
        # Crear formulario
        form = GastoForm(data=gasto_data)
        
        print(f"  📝 Datos: {gasto_data}")
        print(f"  ✅ Válido: {form.is_valid()}")
        
        if not form.is_valid():
            print(f"  ❌ Errores: {form.errors}")
        else:
            print(f"  ✅ Sin errores")
            
        # Probar el método clean_monto directamente
        try:
            form.cleaned_data = {'monto': valor}
            monto_limpio = form.clean_monto()
            print(f"  🔧 clean_monto(): {monto_limpio}")
        except Exception as e:
            print(f"  ❌ Error en clean_monto(): {e}")

def diagnosticar_modelo():
    """Diagnosticar el modelo de Gasto"""
    print("\n🗄️ DIAGNÓSTICO DEL MODELO")
    print("=" * 50)
    
    from core.models import Gasto
    
    # Verificar la definición del campo
    campo_monto = Gasto._meta.get_field('monto')
    print(f"📊 Campo monto:")
    print(f"  - Tipo: {type(campo_monto)}")
    print(f"  - max_digits: {campo_monto.max_digits}")
    print(f"  - decimal_places: {campo_monto.decimal_places}")
    
    # Probar crear un gasto directamente
    try:
        proyecto = Proyecto.objects.first()
        categoria = CategoriaGasto.objects.first()
        
        gasto = Gasto(
            proyecto=proyecto,
            categoria=categoria,
            descripcion="Prueba directa",
            monto=0.01,
            fecha_gasto=date.today()
        )
        gasto.full_clean()
        print("  ✅ Modelo acepta 0.01 directamente")
    except Exception as e:
        print(f"  ❌ Error en modelo: {e}")

if __name__ == "__main__":
    diagnosticar_monto()
    diagnosticar_modelo()
