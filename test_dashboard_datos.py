#!/usr/bin/env python3
"""
Script para verificar que los datos se están mostrando correctamente en el dashboard
"""

import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Cliente, Proyecto, Colaborador, Anticipo, Factura, Gasto

def verificar_datos():
    """Verificar que los datos están en la base de datos"""
    print("🔍 VERIFICANDO DATOS EN EL SISTEMA")
    print("=" * 50)
    
    # Verificar clientes
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(activo=True).count()
    print(f"📊 CLIENTES:")
    print(f"  Total: {total_clientes}")
    print(f"  Activos: {clientes_activos}")
    
    if total_clientes > 0:
        print("  ✅ Clientes encontrados:")
        for cliente in Cliente.objects.all()[:3]:
            print(f"    - {cliente.razon_social}")
    
    # Verificar proyectos
    total_proyectos = Proyecto.objects.count()
    proyectos_activos = Proyecto.objects.filter(activo=True).count()
    proyectos_en_progreso = Proyecto.objects.filter(activo=True, estado='en_progreso').count()
    print(f"\n📊 PROYECTOS:")
    print(f"  Total: {total_proyectos}")
    print(f"  Activos: {proyectos_activos}")
    print(f"  En progreso: {proyectos_en_progreso}")
    
    if total_proyectos > 0:
        print("  ✅ Proyectos encontrados:")
        for proyecto in Proyecto.objects.all()[:3]:
            print(f"    - {proyecto.nombre} (Cliente: {proyecto.cliente.razon_social})")
    
    # Verificar colaboradores
    total_colaboradores = Colaborador.objects.count()
    colaboradores_activos = Colaborador.objects.filter(activo=True).count()
    print(f"\n📊 COLABORADORES:")
    print(f"  Total: {total_colaboradores}")
    print(f"  Activos: {colaboradores_activos}")
    
    if total_colaboradores > 0:
        print("  ✅ Colaboradores encontrados:")
        for colaborador in Colaborador.objects.all()[:3]:
            print(f"    - {colaborador.nombre} (Salario: Q{colaborador.salario})")
    
    # Verificar anticipos
    total_anticipos = Anticipo.objects.count()
    anticipos_recibidos = Anticipo.objects.filter(estado='recibido').count()
    print(f"\n📊 ANTICIPOS:")
    print(f"  Total: {total_anticipos}")
    print(f"  Recibidos: {anticipos_recibidos}")
    
    if total_anticipos > 0:
        print("  ✅ Anticipos encontrados:")
        for anticipo in Anticipo.objects.all()[:3]:
            print(f"    - {anticipo.cliente.razon_social} - {anticipo.proyecto.nombre} (Q{anticipo.monto})")
    
    # Verificar facturas
    total_facturas = Factura.objects.count()
    print(f"\n📊 FACTURAS:")
    print(f"  Total: {total_facturas}")
    
    # Verificar gastos
    total_gastos = Gasto.objects.count()
    print(f"\n📊 GASTOS:")
    print(f"  Total: {total_gastos}")
    
    # Calcular totales financieros
    total_anticipos_monto = Anticipo.objects.aggregate(
        total=models.Sum('monto')
    )['total'] or Decimal('0.00')
    
    print(f"\n💰 RESUMEN FINANCIERO:")
    print(f"  Total anticipos: Q{total_anticipos_monto:,.2f}")
    
    # Verificar asignaciones de colaboradores a proyectos
    print(f"\n🔗 ASIGNACIONES:")
    for proyecto in Proyecto.objects.all()[:3]:
        colaboradores_asignados = proyecto.colaboradores.count()
        print(f"  {proyecto.nombre}: {colaboradores_asignados} colaboradores")
    
    print("\n" + "=" * 50)
    print("✅ VERIFICACIÓN COMPLETADA")
    print("=" * 50)
    
    if total_clientes > 0 and total_proyectos > 0 and total_colaboradores > 0:
        print("🎉 ¡El sistema tiene datos y debería mostrarlos en el dashboard!")
        print("\n🌐 Para ver el dashboard:")
        print("  1. Ve a: http://localhost:8000/")
        print("  2. Inicia sesión con: admin / admin123")
        print("  3. El dashboard debería mostrar todos los datos")
    else:
        print("❌ Faltan datos en el sistema")

if __name__ == "__main__":
    from django.db import models
    verificar_datos()
