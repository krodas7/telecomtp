#!/usr/bin/env python3
"""
Script para agregar días trabajados a trabajadores diarios existentes
"""

import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, TrabajadorDiario, RegistroTrabajo
from django.contrib.auth.models import User

def agregar_dias_trabajados():
    print("🔧 AGREGANDO DÍAS TRABAJADOS A TRABAJADORES DIARIOS")
    print("=" * 60)
    
    try:
        # Obtener el primer proyecto
        proyecto = Proyecto.objects.first()
        if not proyecto:
            print("❌ No hay proyectos en la base de datos")
            return
        
        print(f"📋 Proyecto: {proyecto.nombre}")
        
        # Obtener trabajadores diarios del proyecto
        trabajadores = TrabajadorDiario.objects.filter(proyecto=proyecto, activo=True)
        print(f"👥 Trabajadores activos: {trabajadores.count()}")
        
        if not trabajadores.exists():
            print("❌ No hay trabajadores diarios activos")
            return
        
        # Obtener usuario admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No hay usuario admin")
            return
        
        # Agregar días trabajados a cada trabajador
        for trabajador in trabajadores:
            print(f"\n👤 Trabajador: {trabajador.nombre}")
            
            # Verificar si ya tiene registros
            registros_existentes = trabajador.registros_trabajo.count()
            print(f"   Registros existentes: {registros_existentes}")
            
            if registros_existentes == 0:
                # Crear un registro de trabajo con días aleatorios
                dias_trabajados = 15  # Días de ejemplo
                fecha_inicio = date.today() - timedelta(days=30)
                fecha_fin = date.today() - timedelta(days=1)
                
                registro = RegistroTrabajo.objects.create(
                    trabajador=trabajador,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    dias_trabajados=dias_trabajados,
                    observaciones=f"Registro automático de {dias_trabajados} días trabajados",
                    registrado_por=admin_user
                )
                
                print(f"   ✅ Creado registro: {dias_trabajados} días trabajados")
                print(f"   📅 Período: {fecha_inicio} a {fecha_fin}")
            else:
                print(f"   ⚠️  Ya tiene {registros_existentes} registros")
        
        # Mostrar resumen final
        print("\n📊 RESUMEN FINAL:")
        print("-" * 40)
        total_general = 0
        
        for trabajador in trabajadores:
            dias_trabajados = sum(registro.dias_trabajados for registro in trabajador.registros_trabajo.all())
            total_trabajador = float(trabajador.pago_diario) * dias_trabajados
            total_general += total_trabajador
            
            print(f"  {trabajador.nombre}: {dias_trabajados} días = Q{total_trabajador:.2f}")
        
        print(f"\n💰 TOTAL GENERAL: Q{total_general:.2f}")
        print("\n✅ DÍAS TRABAJADOS AGREGADOS CORRECTAMENTE")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    agregar_dias_trabajados()
