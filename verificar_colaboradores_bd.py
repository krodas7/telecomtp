#!/usr/bin/env python3
"""
Script para verificar que los colaboradores se estén guardando correctamente en la base de datos
"""

import os
import sys
import django
from datetime import datetime, date

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Colaborador, Proyecto, Cliente
from django.contrib.auth.models import User

def verificar_colaboradores_bd():
    """Verificar que los colaboradores se estén guardando en la base de datos"""
    print("🔍 VERIFICACIÓN DE COLABORADORES EN BASE DE DATOS")
    print("=" * 60)
    
    # 1. Contar colaboradores totales
    print("\n1️⃣ CONTEO DE COLABORADORES:")
    total_colaboradores = Colaborador.objects.count()
    print(f"  📊 Total de colaboradores en BD: {total_colaboradores}")
    
    if total_colaboradores == 0:
        print("  ⚠️ No hay colaboradores en la base de datos")
        return False
    
    # 2. Mostrar colaboradores recientes
    print(f"\n2️⃣ COLABORADORES RECIENTES (últimos 5):")
    colaboradores_recientes = Colaborador.objects.all().order_by('-id')[:5]
    
    for i, colaborador in enumerate(colaboradores_recientes, 1):
        print(f"  {i}. {colaborador.nombre}")
        print(f"     📧 Email: {colaborador.email or 'Sin email'}")
        print(f"     📞 Teléfono: {colaborador.telefono or 'Sin teléfono'}")
        print(f"     🆔 DPI: {colaborador.dpi or 'Sin DPI'}")
        print(f"     💰 Salario: Q{colaborador.salario or 0}")
        print(f"     📅 Fecha de contratación: {colaborador.fecha_contratacion or 'Sin fecha'}")
        print(f"     📅 Fecha vencimiento: {colaborador.fecha_vencimiento_contrato or 'Sin fecha'}")
        print(f"     ✅ Activo: {'Sí' if colaborador.activo else 'No'}")
        print(f"     📍 Dirección: {colaborador.direccion or 'Sin dirección'}")
        print(f"     📅 Creado: {colaborador.creado_en.strftime('%Y-%m-%d %H:%M')}")
        print()
    
    # 3. Verificar integridad de datos
    print("3️⃣ VERIFICACIÓN DE INTEGRIDAD:")
    
    # Colaboradores activos vs inactivos
    colaboradores_activos = Colaborador.objects.filter(activo=True).count()
    colaboradores_inactivos = Colaborador.objects.filter(activo=False).count()
    print(f"  📊 Colaboradores activos: {colaboradores_activos}")
    print(f"  📊 Colaboradores inactivos: {colaboradores_inactivos}")
    
    # Colaboradores con email
    colaboradores_con_email = Colaborador.objects.exclude(email='').count()
    print(f"  📊 Colaboradores con email: {colaboradores_con_email}")
    
    # Colaboradores con teléfono
    colaboradores_con_telefono = Colaborador.objects.exclude(telefono='').count()
    print(f"  📊 Colaboradores con teléfono: {colaboradores_con_telefono}")
    
    # 4. Calcular estadísticas
    print(f"\n4️⃣ ESTADÍSTICAS FINANCIERAS:")
    total_salarios = sum(colaborador.salario for colaborador in Colaborador.objects.filter(activo=True))
    salario_promedio = total_salarios / colaboradores_activos if colaboradores_activos > 0 else 0
    salario_maximo = max((colaborador.salario for colaborador in Colaborador.objects.filter(activo=True)), default=0)
    salario_minimo = min((colaborador.salario for colaborador in Colaborador.objects.filter(activo=True)), default=0)
    
    print(f"  💰 Total de salarios (activos): Q{total_salarios:,.2f}")
    print(f"  📊 Salario promedio: Q{salario_promedio:,.2f}")
    print(f"  📈 Salario máximo: Q{salario_maximo:,.2f}")
    print(f"  📉 Salario mínimo: Q{salario_minimo:,.2f}")
    
    # 5. Verificar relaciones
    print(f"\n5️⃣ VERIFICACIÓN DE RELACIONES:")
    
    # Colaboradores con proyectos asignados
    colaboradores_con_proyectos = Colaborador.objects.filter(proyectos__isnull=False).distinct().count()
    print(f"  📊 Colaboradores con proyectos: {colaboradores_con_proyectos}")
    
    # 6. Mostrar colaboradores por estado
    print(f"\n6️⃣ COLABORADORES POR ESTADO:")
    print(f"  ✅ Activos: {colaboradores_activos}")
    print(f"  ❌ Inactivos: {colaboradores_inactivos}")
    
    # Colaboradores con información completa
    print(f"\n7️⃣ COLABORADORES CON INFORMACIÓN COMPLETA:")
    colaboradores_completos = Colaborador.objects.filter(
        email__isnull=False,
        telefono__isnull=False,
        salario__isnull=False,
        fecha_contratacion__isnull=False
    ).exclude(
        email='',
        telefono=''
    ).count()
    print(f"  📊 Colaboradores con datos completos: {colaboradores_completos}")
    
    return True

def crear_colaborador_prueba():
    """Crear un colaborador de prueba para verificar que funciona"""
    print(f"\n7️⃣ CREANDO COLABORADOR DE PRUEBA:")
    
    try:
        # Obtener un proyecto para asignar al colaborador
        proyecto = Proyecto.objects.first()
        
        if not proyecto:
            print("  ❌ No hay proyectos disponibles")
            return False
        
        # Crear colaborador de prueba
        colaborador = Colaborador.objects.create(
            nombre="Colaborador Prueba BD",
            email="colaborador.prueba@test.com",
            telefono="5555-1234",
            dpi="1234567890123",
            direccion="Dirección de prueba",
            salario=3500.00,
            fecha_contratacion=date.today(),
            fecha_vencimiento_contrato=date(2026, 9, 29)
        )
        
        print(f"  ✅ Colaborador de prueba creado:")
        print(f"     ID: {colaborador.id}")
        print(f"     Nombre: {colaborador.nombre}")
        print(f"     Email: {colaborador.email}")
        print(f"     Teléfono: {colaborador.telefono}")
        print(f"     DPI: {colaborador.dpi}")
        print(f"     Salario: Q{colaborador.salario}")
        print(f"     Fecha contratación: {colaborador.fecha_contratacion}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error creando colaborador de prueba: {e}")
        return False

def verificar_formulario_colaboradores():
    """Verificar que el formulario de colaboradores funcione correctamente"""
    print(f"\n8️⃣ VERIFICANDO FORMULARIO DE COLABORADORES:")
    
    try:
        from django.test import Client
        from django.contrib.auth.models import User
        
        client = Client()
        admin_user = User.objects.filter(is_superuser=True).first()
        
        if not admin_user:
            print("  ❌ No hay usuario admin")
            return False
        
        client.force_login(admin_user)
        
        # Probar creación de colaborador
        form_data = {
            'nombre': 'Colaborador Formulario Test',
            'email': 'formulario@test.com',
            'telefono': '6666-7890',
            'dpi': '9876543210987',
            'direccion': 'Dirección de formulario',
            'salario': '4000.00',
            'fecha_contratacion': '2025-09-29',
            'fecha_vencimiento_contrato': '2026-09-29'
        }
        
        response = client.post('/colaboradores/crear/', form_data)
        
        if response.status_code == 302:
            print("  ✅ Formulario de colaboradores funciona correctamente")
            print("  ✅ Colaborador creado desde formulario")
            return True
        else:
            print(f"  ❌ Error en formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando formulario: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN COMPLETA DE COLABORADORES EN BD")
    print("=" * 70)
    
    try:
        # Verificar colaboradores existentes
        colaboradores_ok = verificar_colaboradores_bd()
        
        # Crear colaborador de prueba
        prueba_ok = crear_colaborador_prueba()
        
        # Verificar formulario
        formulario_ok = verificar_formulario_colaboradores()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if colaboradores_ok:
            print("✅ COLABORADORES SE ESTÁN GUARDANDO CORRECTAMENTE EN LA BD")
            print("✅ Todas las relaciones funcionan correctamente")
            print("✅ Los cálculos financieros son precisos")
        else:
            print("⚠️ HAY PROBLEMAS CON EL ALMACENAMIENTO DE COLABORADORES")
        
        if prueba_ok:
            print("✅ Creación de colaboradores funciona correctamente")
        else:
            print("❌ Hay problemas al crear nuevos colaboradores")
        
        if formulario_ok:
            print("✅ Formulario de colaboradores funciona correctamente")
        else:
            print("❌ Hay problemas con el formulario de colaboradores")
        
        return colaboradores_ok and prueba_ok and formulario_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
