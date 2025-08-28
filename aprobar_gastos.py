#!/usr/bin/env python
"""
Script para aprobar gastos pendientes
Sistema ARCA Construcción
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Gasto
from django.contrib.auth.models import User

def aprobar_gastos_pendientes():
    """Aprobar todos los gastos pendientes"""
    print("🚀 Aprobando gastos pendientes...")
    print("=" * 50)
    
    # Obtener usuario admin (o crear uno si no existe)
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser('admin', 'admin@arca.com', 'admin123')
            print("✅ Usuario admin creado")
    except:
        admin_user = User.objects.first()
    
    # Obtener gastos pendientes
    gastos_pendientes = Gasto.objects.filter(aprobado=False)
    
    if not gastos_pendientes.exists():
        print("✅ No hay gastos pendientes para aprobar")
        return
    
    print(f"📋 Encontrados {gastos_pendientes.count()} gastos pendientes:")
    
    # Aprobar cada gasto
    for gasto in gastos_pendientes:
        print(f"   • {gasto.descripcion} - Q{gasto.monto}")
        gasto.aprobado = True
        gasto.aprobado_por = admin_user
        gasto.save()
        print(f"     ✅ APROBADO")
    
    print("=" * 50)
    print("📊 RESUMEN:")
    print(f"   • Gastos aprobados: {Gasto.objects.filter(aprobado=True).count()}")
    print(f"   • Gastos pendientes: {Gasto.objects.filter(aprobado=False).count()}")
    print(f"   • Total gastos: {Gasto.objects.count()}")
    print("=" * 50)
    print("✅ ¡Gastos aprobados exitosamente!")
    print("🌐 Ahora deberían aparecer en el módulo de gastos y en la rentabilidad")

if __name__ == '__main__':
    aprobar_gastos_pendientes()
