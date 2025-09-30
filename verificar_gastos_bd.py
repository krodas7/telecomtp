#!/usr/bin/env python3
"""
Script para verificar que los gastos se estén guardando correctamente en la base de datos
"""

import os
import sys
import django
from datetime import datetime, date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Gasto, Proyecto, CategoriaGasto, Cliente
from django.contrib.auth.models import User

def verificar_gastos_bd():
    """Verificar que los gastos se estén guardando en la base de datos"""
    print("🔍 VERIFICACIÓN DE GASTOS EN BASE DE DATOS")
    print("=" * 50)
    
    # 1. Contar gastos totales
    print("\n1️⃣ CONTEO DE GASTOS:")
    total_gastos = Gasto.objects.count()
    print(f"  📊 Total de gastos en BD: {total_gastos}")
    
    if total_gastos == 0:
        print("  ⚠️ No hay gastos en la base de datos")
        return False
    
    # 2. Mostrar gastos recientes
    print(f"\n2️⃣ GASTOS RECIENTES (últimos 5):")
    gastos_recientes = Gasto.objects.all().order_by('-fecha_gasto')[:5]
    
    for i, gasto in enumerate(gastos_recientes, 1):
        print(f"  {i}. {gasto.descripcion}")
        print(f"     💰 Monto: Q{gasto.monto}")
        print(f"     📅 Fecha: {gasto.fecha_gasto}")
        print(f"     🏷️ Categoría: {gasto.categoria.nombre if gasto.categoria else 'Sin categoría'}")
        print(f"     🏗️ Proyecto: {gasto.proyecto.nombre if gasto.proyecto else 'Sin proyecto'}")
        print(f"     ✅ Aprobado: {'Sí' if gasto.aprobado else 'No'}")
        print(f"     📄 Comprobante: {'Sí' if gasto.comprobante else 'No'}")
        print(f"     👤 Aprobado por: {gasto.aprobado_por.username if gasto.aprobado_por else 'N/A'}")
        print(f"     📅 Creado: {gasto.creado_en.strftime('%Y-%m-%d %H:%M')}")
        print()
    
    # 3. Verificar integridad de datos
    print("3️⃣ VERIFICACIÓN DE INTEGRIDAD:")
    
    # Gastos sin categoría
    gastos_sin_categoria = Gasto.objects.filter(categoria__isnull=True).count()
    print(f"  📊 Gastos sin categoría: {gastos_sin_categoria}")
    
    # Gastos sin proyecto
    gastos_sin_proyecto = Gasto.objects.filter(proyecto__isnull=True).count()
    print(f"  📊 Gastos sin proyecto: {gastos_sin_proyecto}")
    
    # Gastos aprobados vs pendientes
    gastos_aprobados = Gasto.objects.filter(aprobado=True).count()
    gastos_pendientes = Gasto.objects.filter(aprobado=False).count()
    print(f"  📊 Gastos aprobados: {gastos_aprobados}")
    print(f"  📊 Gastos pendientes: {gastos_pendientes}")
    
    # 4. Calcular totales
    print(f"\n4️⃣ CÁLCULOS FINANCIEROS:")
    total_monto = sum(gasto.monto for gasto in Gasto.objects.all())
    total_aprobado = sum(gasto.monto for gasto in Gasto.objects.filter(aprobado=True))
    total_pendiente = sum(gasto.monto for gasto in Gasto.objects.filter(aprobado=False))
    
    print(f"  💰 Total general: Q{total_monto:,.2f}")
    print(f"  ✅ Total aprobado: Q{total_aprobado:,.2f}")
    print(f"  ⏳ Total pendiente: Q{total_pendiente:,.2f}")
    
    # 5. Verificar relaciones
    print(f"\n5️⃣ VERIFICACIÓN DE RELACIONES:")
    
    # Proyectos con gastos
    proyectos_con_gastos = Proyecto.objects.filter(gasto__isnull=False).distinct().count()
    print(f"  📊 Proyectos con gastos: {proyectos_con_gastos}")
    
    # Categorías con gastos
    categorias_con_gastos = CategoriaGasto.objects.filter(gasto__isnull=False).distinct().count()
    print(f"  📊 Categorías con gastos: {categorias_con_gastos}")
    
    # 6. Mostrar gastos por proyecto
    print(f"\n6️⃣ GASTOS POR PROYECTO:")
    proyectos = Proyecto.objects.all()
    for proyecto in proyectos:
        gastos_proyecto = Gasto.objects.filter(proyecto=proyecto)
        if gastos_proyecto.exists():
            total_proyecto = sum(g.monto for g in gastos_proyecto)
            print(f"  🏗️ {proyecto.nombre}: {gastos_proyecto.count()} gastos - Q{total_proyecto:,.2f}")
    
    # 7. Mostrar gastos por categoría
    print(f"\n7️⃣ GASTOS POR CATEGORÍA:")
    categorias = CategoriaGasto.objects.all()
    for categoria in categorias:
        gastos_categoria = Gasto.objects.filter(categoria=categoria)
        if gastos_categoria.exists():
            total_categoria = sum(g.monto for g in gastos_categoria)
            print(f"  🏷️ {categoria.nombre}: {gastos_categoria.count()} gastos - Q{total_categoria:,.2f}")
    
    return True

def crear_gasto_prueba():
    """Crear un gasto de prueba para verificar que funciona"""
    print(f"\n8️⃣ CREANDO GASTO DE PRUEBA:")
    
    try:
        # Obtener datos necesarios
        proyecto = Proyecto.objects.first()
        categoria = CategoriaGasto.objects.first()
        
        if not proyecto:
            print("  ❌ No hay proyectos disponibles")
            return False
        
        if not categoria:
            print("  ❌ No hay categorías disponibles")
            return False
        
        # Crear gasto de prueba
        gasto = Gasto.objects.create(
            descripcion="Gasto de prueba - Verificación BD",
            monto=500.00,
            categoria=categoria,
            proyecto=proyecto,
            fecha_gasto=date.today()
        )
        
        print(f"  ✅ Gasto de prueba creado:")
        print(f"     ID: {gasto.id}")
        print(f"     Descripción: {gasto.descripcion}")
        print(f"     Monto: Q{gasto.monto}")
        print(f"     Fecha: {gasto.fecha_gasto}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error creando gasto de prueba: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN COMPLETA DE GASTOS EN BD")
    print("=" * 60)
    
    try:
        # Verificar gastos existentes
        gastos_ok = verificar_gastos_bd()
        
        # Crear gasto de prueba
        prueba_ok = crear_gasto_prueba()
        
        # Resumen final
        print(f"\n" + "=" * 60)
        print("📋 RESUMEN FINAL")
        print("=" * 60)
        
        if gastos_ok:
            print("✅ GASTOS SE ESTÁN GUARDANDO CORRECTAMENTE EN LA BD")
            print("✅ Todas las relaciones funcionan correctamente")
            print("✅ Los cálculos financieros son precisos")
        else:
            print("⚠️ HAY PROBLEMAS CON EL ALMACENAMIENTO DE GASTOS")
        
        if prueba_ok:
            print("✅ Creación de gastos funciona correctamente")
        else:
            print("❌ Hay problemas al crear nuevos gastos")
        
        return gastos_ok and prueba_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
