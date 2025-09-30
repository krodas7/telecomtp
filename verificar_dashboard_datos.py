#!/usr/bin/env python3
"""
Script para verificar y corregir los datos del dashboard
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Cliente, Proyecto, Colaborador, Anticipo, Factura, Gasto
from django.db.models import Sum, Count
from decimal import Decimal

def verificar_datos():
    """Verificar los datos actuales en la base de datos"""
    print("🔍 VERIFICANDO DATOS DEL DASHBOARD")
    print("=" * 50)
    
    # Verificar clientes
    total_clientes = Cliente.objects.filter(activo=True).count()
    print(f"👥 Clientes activos: {total_clientes}")
    
    # Verificar proyectos
    total_proyectos = Proyecto.objects.filter(activo=True).count()
    print(f"🏗️ Proyectos activos: {total_proyectos}")
    
    # Verificar facturas
    total_facturado = Factura.objects.aggregate(total=Sum('monto_total'))['total'] or 0
    print(f"💰 Total facturado: Q{total_facturado:,.2f}")
    
    # Verificar anticipos
    total_anticipos = Anticipo.objects.count()
    anticipos_aplicados = Anticipo.objects.filter(aplicado_al_proyecto=True).count()
    monto_anticipos_aplicados = Anticipo.objects.filter(aplicado_al_proyecto=True).aggregate(total=Sum('monto_aplicado_proyecto'))['total'] or 0
    print(f"💳 Total anticipos: {total_anticipos}")
    print(f"✅ Anticipos aplicados al proyecto: {anticipos_aplicados}")
    print(f"💰 Monto anticipos aplicados: Q{monto_anticipos_aplicados:,.2f}")
    
    # Verificar gastos
    total_gastos = Gasto.objects.filter(aprobado=True).aggregate(total=Sum('monto'))['total'] or 0
    print(f"💸 Total gastos aprobados: Q{total_gastos:,.2f}")
    
    print(f"\n📊 RESUMEN:")
    print(f"  Clientes: {total_clientes}")
    print(f"  Proyectos: {total_proyectos}")
    print(f"  Facturado: Q{total_facturado:,.2f}")
    print(f"  Anticipos aplicados: Q{monto_anticipos_aplicados:,.2f}")
    print(f"  Total cobrado: Q{total_facturado + monto_anticipos_aplicados:,.2f}")
    
    return {
        'clientes': total_clientes,
        'proyectos': total_proyectos,
        'facturado': total_facturado,
        'anticipos_aplicados': monto_anticipos_aplicados,
        'total_cobrado': total_facturado + monto_anticipos_aplicados
    }

def corregir_anticipos():
    """Aplicar algunos anticipos al proyecto para mostrar datos en el dashboard"""
    print(f"\n🔧 CORRIGIENDO ANTICIPOS")
    print("=" * 30)
    
    # Obtener anticipos que no están aplicados
    anticipos_pendientes = Anticipo.objects.filter(aplicado_al_proyecto=False)[:3]
    
    if not anticipos_pendientes.exists():
        print("❌ No hay anticipos pendientes para aplicar")
        return
    
    for anticipo in anticipos_pendientes:
        try:
            # Aplicar el 50% del anticipo al proyecto
            monto_aplicar = anticipo.monto * Decimal('0.5')
            anticipo.aplicar_al_proyecto(monto_aplicar)
            print(f"✅ Aplicado Q{monto_aplicar:,.2f} del anticipo {anticipo.numero_anticipo}")
        except Exception as e:
            print(f"❌ Error aplicando anticipo {anticipo.numero_anticipo}: {e}")

def crear_facturas_ejemplo():
    """Crear algunas facturas de ejemplo para mostrar datos"""
    print(f"\n📄 CREANDO FACTURAS DE EJEMPLO")
    print("=" * 35)
    
    # Obtener un proyecto
    proyecto = Proyecto.objects.filter(activo=True).first()
    if not proyecto:
        print("❌ No hay proyectos disponibles")
        return
    
    # Crear facturas de ejemplo
    from datetime import date
    facturas_data = [
        {
            'proyecto': proyecto,
            'cliente': proyecto.cliente,
            'numero_factura': 'FAC-2024-001',
            'monto_total': Decimal('50000.00'),
            'fecha_emision': date(2024, 1, 15),
            'fecha_vencimiento': date(2024, 2, 15),
            'estado': 'pagada'
        },
        {
            'proyecto': proyecto,
            'cliente': proyecto.cliente,
            'numero_factura': 'FAC-2024-002',
            'monto_total': Decimal('75000.00'),
            'fecha_emision': date(2024, 1, 20),
            'fecha_vencimiento': date(2024, 2, 20),
            'estado': 'enviada'
        }
    ]
    
    for factura_data in facturas_data:
        factura, created = Factura.objects.get_or_create(
            numero_factura=factura_data['numero_factura'],
            defaults=factura_data
        )
        if created:
            print(f"✅ Factura creada: {factura.numero_factura} - Q{factura.monto_total:,.2f}")
        else:
            print(f"⚠️ Factura ya existe: {factura.numero_factura}")

def main():
    """Función principal"""
    print("🚀 VERIFICACIÓN Y CORRECCIÓN DEL DASHBOARD")
    print("=" * 50)
    
    # Verificar datos actuales
    datos_antes = verificar_datos()
    
    # Corregir anticipos
    corregir_anticipos()
    
    # Crear facturas de ejemplo
    crear_facturas_ejemplo()
    
    # Verificar datos después de las correcciones
    print(f"\n🔍 VERIFICACIÓN DESPUÉS DE CORRECCIONES")
    print("=" * 45)
    datos_despues = verificar_datos()
    
    # Mostrar diferencias
    print(f"\n📈 CAMBIOS REALIZADOS:")
    print(f"  Clientes: {datos_antes['clientes']} → {datos_despues['clientes']}")
    print(f"  Proyectos: {datos_antes['proyectos']} → {datos_despues['proyectos']}")
    print(f"  Facturado: Q{datos_antes['facturado']:,.2f} → Q{datos_despues['facturado']:,.2f}")
    print(f"  Anticipos aplicados: Q{datos_antes['anticipos_aplicados']:,.2f} → Q{datos_despues['anticipos_aplicados']:,.2f}")
    print(f"  Total cobrado: Q{datos_antes['total_cobrado']:,.2f} → Q{datos_despues['total_cobrado']:,.2f}")
    
    print(f"\n✅ VERIFICACIÓN COMPLETADA")
    print("🌐 Recarga el dashboard en el navegador para ver los cambios")

if __name__ == "__main__":
    main()
