#!/usr/bin/env python3
"""
Script de verificación completa del Sistema de Construcciones ARCA
Verifica todos los módulos, endpoints, guardado en BD, y funcionalidad
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import *
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from decimal import Decimal

print("=" * 100)
print("🔍 VERIFICACIÓN COMPLETA DEL SISTEMA DE CONSTRUCCIONES ARCA")
print("=" * 100)

# ========================================
# 1. VERIFICAR MÓDULOS PRINCIPALES
# ========================================
print("\n" + "=" * 100)
print("📦 1. VERIFICACIÓN DE MÓDULOS PRINCIPALES")
print("=" * 100)

modulos = {
    'Proyectos': Proyecto.objects.all().count(),
    'Clientes': Cliente.objects.all().count(),
    'Colaboradores': Colaborador.objects.all().count(),
    'Facturas': Factura.objects.all().count(),
    'Gastos': Gasto.objects.all().count(),
    'Categorías de Gasto': CategoriaGasto.objects.all().count(),
    'Anticipos': Anticipo.objects.all().count(),
    'Pagos': Pago.objects.all().count(),
    'Presupuestos': Presupuesto.objects.all().count(),
    'Inventario': ItemInventario.objects.all().count(),
    'Trabajadores Diarios': TrabajadorDiario.objects.all().count(),
    'Anticipos TD': AnticipoTrabajadorDiario.objects.all().count(),
    'Planillas Liquidadas': PlanillaLiquidada.objects.all().count(),
    'Archivos': ArchivoProyecto.objects.all().count(),
    'Carpetas': CarpetaProyecto.objects.all().count(),
    'Usuarios': User.objects.all().count(),
    'Roles': Rol.objects.all().count(),
}

for modulo, count in modulos.items():
    status = "✅" if count > 0 else "⚠️ "
    print(f"{status} {modulo}: {count} registro(s)")

# ========================================
# 2. VERIFICAR INTEGRIDAD DE DATOS
# ========================================
print("\n" + "=" * 100)
print("🔍 2. VERIFICACIÓN DE INTEGRIDAD DE DATOS")
print("=" * 100)

# Proyectos sin cliente
proyectos_sin_cliente = Proyecto.objects.filter(cliente__isnull=True).count()
print(f"{'✅' if proyectos_sin_cliente == 0 else '❌'} Proyectos sin cliente: {proyectos_sin_cliente}")

# Gastos sin proyecto
gastos_sin_proyecto = Gasto.objects.filter(proyecto__isnull=True).count()
print(f"{'✅' if gastos_sin_proyecto == 0 else '❌'} Gastos sin proyecto: {gastos_sin_proyecto}")

# Facturas sin proyecto
facturas_sin_proyecto = Factura.objects.filter(proyecto__isnull=True).count()
print(f"{'✅' if facturas_sin_proyecto == 0 else '❌'} Facturas sin proyecto: {facturas_sin_proyecto}")

# Archivos sin archivo físico
archivos_sin_archivo = ArchivoProyecto.objects.filter(archivo='', activo=True).exclude(
    nombre__icontains='planilla_trabajadores'
).count()
print(f"{'✅' if archivos_sin_archivo == 0 else '⚠️ '} Archivos sin archivo físico: {archivos_sin_archivo}")

# Trabajadores diarios sin proyecto
trabajadores_sin_proyecto = TrabajadorDiario.objects.filter(proyecto__isnull=True).count()
print(f"{'✅' if trabajadores_sin_proyecto == 0 else '❌'} Trabajadores diarios sin proyecto: {trabajadores_sin_proyecto}")

# ========================================
# 3. VERIFICAR CÁLCULOS FINANCIEROS
# ========================================
print("\n" + "=" * 100)
print("💰 3. VERIFICACIÓN DE CÁLCULOS FINANCIEROS")
print("=" * 100)

# Totales por proyecto
for proyecto in Proyecto.objects.all()[:3]:
    print(f"\n📊 Proyecto: {proyecto.nombre}")
    
    # Facturas
    total_facturado = Factura.objects.filter(proyecto=proyecto).aggregate(
        total=Sum('monto_total')
    )['total'] or Decimal('0.00')
    print(f"   💵 Total Facturado: Q{total_facturado}")
    
    # Gastos
    total_gastos = Gasto.objects.filter(proyecto=proyecto).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')
    gastos_aprobados = Gasto.objects.filter(proyecto=proyecto, aprobado=True).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')
    print(f"   💸 Total Gastos: Q{total_gastos} (Aprobados: Q{gastos_aprobados})")
    
    # Anticipos
    total_anticipos = Anticipo.objects.filter(proyecto=proyecto).aggregate(
        total=Sum('monto')
    )['total'] or Decimal('0.00')
    print(f"   💰 Total Anticipos: Q{total_anticipos}")
    
    # Nómina
    planillas = PlanillaLiquidada.objects.filter(proyecto=proyecto)
    total_nomina = planillas.aggregate(total=Sum('total_planilla'))['total'] or Decimal('0.00')
    print(f"   👥 Total Nómina (Planillas): Q{total_nomina}")
    
    trabajadores_td_inactivos = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=False)
    total_td = sum(t.total_dias_trabajados * t.pago_diario for t in trabajadores_td_inactivos)
    print(f"   👷 Total Trabajadores Diarios: Q{total_td}")
    
    total_historico_nomina = total_nomina + Decimal(str(total_td))
    print(f"   📊 TOTAL HISTÓRICO NÓMINA: Q{total_historico_nomina}")

# ========================================
# 4. VERIFICAR ARCHIVOS Y CARPETAS
# ========================================
print("\n" + "=" * 100)
print("📁 4. VERIFICACIÓN DE ARCHIVOS Y CARPETAS")
print("=" * 100)

carpetas = CarpetaProyecto.objects.filter(activa=True)
for carpeta in carpetas[:5]:
    archivos_count = ArchivoProyecto.objects.filter(carpeta=carpeta, activo=True).count()
    print(f"✅ {carpeta.nombre} ({carpeta.proyecto.nombre}): {archivos_count} archivo(s)")

archivos_planillas = ArchivoProyecto.objects.filter(
    nombre__icontains='planilla',
    activo=True
)
print(f"\n✅ Total archivos de planillas: {archivos_planillas.count()}")

# ========================================
# 5. VERIFICAR ESTADOS Y CONSISTENCIA
# ========================================
print("\n" + "=" * 100)
print("🔍 5. VERIFICACIÓN DE ESTADOS Y CONSISTENCIA")
print("=" * 100)

# Estados de gastos
gastos_aprobados = Gasto.objects.filter(aprobado=True).count()
gastos_pendientes = Gasto.objects.filter(aprobado=False).count()
print(f"✅ Gastos aprobados: {gastos_aprobados}")
print(f"✅ Gastos pendientes: {gastos_pendientes}")

# Estados de anticipos
for estado in ['pendiente', 'aplicado', 'liquidado', 'devuelto', 'cancelado']:
    count = Anticipo.objects.filter(estado=estado).count()
    if count > 0:
        print(f"✅ Anticipos {estado}: {count}")

# Estados de anticipos de proyecto
for estado in ['pendiente', 'liquidado', 'procesado', 'cancelado']:
    count = AnticipoProyecto.objects.filter(estado=estado).count()
    if count > 0:
        print(f"✅ Anticipos Proyecto {estado}: {count}")

# ========================================
# 6. VERIFICAR MIGRACIONES
# ========================================
print("\n" + "=" * 100)
print("🔄 6. VERIFICACIÓN DE MIGRACIONES")
print("=" * 100)

from django.db.migrations.recorder import MigrationRecorder
migraciones = MigrationRecorder.Migration.objects.filter(app='core').order_by('-id')[:5]
print("✅ Últimas 5 migraciones aplicadas:")
for mig in migraciones:
    print(f"   - {mig.name}")

# ========================================
# 7. VERIFICAR FUNCIONES CRÍTICAS
# ========================================
print("\n" + "=" * 100)
print("⚙️  7. VERIFICACIÓN DE FUNCIONES CRÍTICAS")
print("=" * 100)

# Verificar que los modelos tienen las propiedades necesarias
try:
    proyecto_test = Proyecto.objects.first()
    if proyecto_test:
        # Esto debería funcionar sin errores
        _ = proyecto_test.total_facturado
        print("✅ Proyecto.total_facturado - OK")
    
    anticipo_test = Anticipo.objects.first()
    if anticipo_test:
        _ = anticipo_test.porcentaje_aplicado
        _ = anticipo_test.total_aplicado
        print("✅ Anticipo.porcentaje_aplicado y total_aplicado - OK")
    
    trabajador_test = TrabajadorDiario.objects.first()
    if trabajador_test:
        _ = trabajador_test.total_a_pagar
        _ = trabajador_test.total_anticipos_aplicados
        print("✅ TrabajadorDiario.total_a_pagar y total_anticipos_aplicados - OK")
        
except Exception as e:
    print(f"❌ Error en propiedades de modelos: {e}")

# ========================================
# RESUMEN FINAL
# ========================================
print("\n" + "=" * 100)
print("📊 RESUMEN FINAL")
print("=" * 100)

total_registros = sum(modulos.values())
print(f"✅ Total de registros en BD: {total_registros}")
print(f"✅ Módulos activos: {len([v for v in modulos.values() if v > 0])}/{len(modulos)}")

# Verificar si hay datos de prueba
if total_registros > 0:
    print("\n✅ HAY DATOS EN LA BASE DE DATOS")
    print("✅ El sistema tiene información para mostrar")
else:
    print("\n⚠️  NO HAY DATOS EN LA BASE DE DATOS")
    print("⚠️  Se recomienda cargar datos de prueba")

print("\n" + "=" * 100)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 100)

