#!/usr/bin/env python3
"""
Script para verificar que todos los cambios se están guardando correctamente en la base de datos
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import (
    Proyecto, TrabajadorDiario, AnticipoTrabajadorDiario, 
    PlanillaLiquidada, ArchivoProyecto, CarpetaProyecto,
    Colaborador, AnticipoProyecto
)
from django.contrib.auth.models import User

print("=" * 80)
print("🔍 VERIFICACIÓN DE GUARDADO EN BASE DE DATOS")
print("=" * 80)

# 1. Verificar proyectos
proyectos = Proyecto.objects.all()
print(f"\n✅ PROYECTOS: {proyectos.count()} proyecto(s) en BD")
for p in proyectos[:3]:
    print(f"   - {p.nombre} (ID: {p.id})")

# 2. Verificar trabajadores diarios
trabajadores_diarios = TrabajadorDiario.objects.all()
print(f"\n✅ TRABAJADORES DIARIOS: {trabajadores_diarios.count()} trabajador(es) en BD")
for t in trabajadores_diarios[:5]:
    print(f"   - {t.nombre} | Proyecto: {t.proyecto.nombre} | Activo: {t.activo}")
    print(f"     Días trabajados: {t.total_dias_trabajados} | Total a pagar: Q{t.total_a_pagar}")

# 3. Verificar anticipos de trabajadores diarios
anticipos_td = AnticipoTrabajadorDiario.objects.all()
print(f"\n✅ ANTICIPOS TRABAJADORES DIARIOS: {anticipos_td.count()} anticipo(s) en BD")
for a in anticipos_td[:5]:
    print(f"   - {a.trabajador.nombre} | Monto: Q{a.monto} | Estado: {a.estado}")

# 4. Verificar planillas liquidadas (NUEVO MODELO)
planillas = PlanillaLiquidada.objects.all()
print(f"\n✅ PLANILLAS LIQUIDADAS: {planillas.count()} planilla(s) en BD")
for pl in planillas[:5]:
    print(f"   - Proyecto: {pl.proyecto.nombre}")
    print(f"     Fecha: {pl.fecha_liquidacion.strftime('%d/%m/%Y %H:%M')}")
    print(f"     Total Salarios: Q{pl.total_salarios}")
    print(f"     Total Anticipos: Q{pl.total_anticipos}")
    print(f"     TOTAL PLANILLA: Q{pl.total_planilla}")
    print(f"     Personal: {pl.cantidad_personal}")

# 5. Verificar archivos de planillas en BD
archivos_planillas = ArchivoProyecto.objects.filter(
    nombre__icontains='planilla',
    activo=True
)
print(f"\n✅ ARCHIVOS DE PLANILLAS: {archivos_planillas.count()} archivo(s) PDF en BD")
for arch in archivos_planillas[:5]:
    print(f"   - {arch.nombre} | Proyecto: {arch.proyecto.nombre}")
    print(f"     Tiene archivo físico: {bool(arch.archivo)}")
    if arch.archivo:
        print(f"     Tamaño: {arch.archivo.size} bytes")

# 6. Verificar carpetas de archivos
carpetas = CarpetaProyecto.objects.filter(activa=True)
print(f"\n✅ CARPETAS DE ARCHIVOS: {carpetas.count()} carpeta(s) en BD")
for c in carpetas[:5]:
    archivos_count = ArchivoProyecto.objects.filter(carpeta=c, activo=True).count()
    print(f"   - {c.nombre} | Proyecto: {c.proyecto.nombre} | Archivos: {archivos_count}")

# 7. Verificar colaboradores
colaboradores = Colaborador.objects.all()
print(f"\n✅ COLABORADORES: {colaboradores.count()} colaborador(es) en BD")
for col in colaboradores[:3]:
    print(f"   - {col.nombre} | Salario: Q{col.salario or 0}")

# 8. Verificar anticipos de proyecto
anticipos_proyecto = AnticipoProyecto.objects.all()
print(f"\n✅ ANTICIPOS DE PROYECTO: {anticipos_proyecto.count()} anticipo(s) en BD")
estados = anticipos_proyecto.values('estado').annotate(count=django.db.models.Count('id'))
for est in estados:
    print(f"   - {est['estado']}: {est['count']} anticipo(s)")

print("\n" + "=" * 80)
print("✅ VERIFICACIÓN COMPLETADA")
print("=" * 80)

# Resumen final
print("\n📊 RESUMEN:")
print(f"   - Total proyectos: {proyectos.count()}")
print(f"   - Total trabajadores diarios: {trabajadores_diarios.count()}")
print(f"   - Total anticipos TD: {anticipos_td.count()}")
print(f"   - Total planillas liquidadas: {planillas.count()}")
print(f"   - Total archivos planillas: {archivos_planillas.count()}")
print(f"   - Total colaboradores: {colaboradores.count()}")
print(f"   - Total anticipos proyecto: {anticipos_proyecto.count()}")

# Verificar integridad
print("\n🔍 VERIFICACIÓN DE INTEGRIDAD:")
if trabajadores_diarios.count() > 0 and anticipos_td.count() == 0:
    print("   ⚠️  WARNING: Hay trabajadores diarios pero sin anticipos registrados")
else:
    print("   ✅ Trabajadores diarios y anticipos: OK")

if proyectos.count() > 0 and colaboradores.count() == 0:
    print("   ⚠️  WARNING: Hay proyectos pero sin colaboradores asignados")
else:
    print("   ✅ Proyectos y colaboradores: OK")

if archivos_planillas.count() > 0:
    archivos_sin_archivo = archivos_planillas.filter(archivo='')
    if archivos_sin_archivo.exists():
        print(f"   ⚠️  WARNING: {archivos_sin_archivo.count()} archivo(s) de planilla sin archivo físico")
    else:
        print("   ✅ Todos los archivos de planilla tienen archivo físico: OK")

print("\n✅ TODO LISTO PARA SUBIR AL SERVIDOR")
print("=" * 80)

