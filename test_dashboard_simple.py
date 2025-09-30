#!/usr/bin/env python3
"""
Script simple para probar el dashboard
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, Cliente, Factura, Gasto, Anticipo
from django.contrib.auth.models import User
from decimal import Decimal

def test_dashboard_data():
    print("🧪 Probando datos del dashboard...")
    
    try:
        # Verificar datos básicos
        total_clientes = Cliente.objects.filter(activo=True).count()
        total_proyectos = Proyecto.objects.filter(activo=True).count()
        
        print(f"📊 Clientes activos: {total_clientes}")
        print(f"📊 Proyectos activos: {total_proyectos}")
        
        # Probar cálculos de facturas
        total_facturado = Factura.objects.aggregate(total=Sum('monto_total'))['total'] or Decimal('0.00')
        print(f"📊 Total facturado: Q{total_facturado}")
        
        # Probar cálculos de gastos
        gastos_raw = Gasto.objects.filter(aprobado=True).aggregate(total=Sum('monto'))['total'] or 0
        gastos_decimal = Decimal(str(gastos_raw))
        print(f"📊 Gastos aprobados: Q{gastos_decimal}")
        
        # Probar operación que causaba error
        rentabilidad = total_facturado - gastos_decimal
        print(f"📊 Rentabilidad: Q{rentabilidad}")
        
        print("✅ Todos los cálculos funcionan correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dashboard_data()
