#!/usr/bin/env python3
"""
Script para probar la generación de PDF de trabajadores diarios
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Proyecto, TrabajadorDiario, RegistroTrabajo
from django.contrib.auth.models import User
from django.utils import timezone

def test_pdf_trabajadores():
    print("🧪 PROBANDO GENERACIÓN DE PDF DE TRABAJADORES DIARIOS")
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
        
        # Mostrar información de cada trabajador
        print("\n📊 INFORMACIÓN DE TRABAJADORES:")
        print("-" * 60)
        total_general = 0
        
        for i, trabajador in enumerate(trabajadores, 1):
            # Calcular días trabajados
            dias_trabajados = sum(registro.dias_trabajados for registro in trabajador.registros_trabajo.all())
            total_trabajador = float(trabajador.pago_diario) * dias_trabajados
            total_general += total_trabajador
            
            print(f"  {i}. {trabajador.nombre}")
            print(f"     Pago diario: Q{trabajador.pago_diario}")
            print(f"     Días trabajados: {dias_trabajados}")
            print(f"     Total a pagar: Q{total_trabajador:.2f}")
            print(f"     Registros: {trabajador.registros_trabajo.count()}")
            print()
        
        print(f"💰 TOTAL GENERAL: Q{total_general:.2f}")
        
        # Probar la URL del PDF
        print("\n🔗 PROBANDO URL DEL PDF:")
        from django.test import Client
        from django.contrib.auth.models import User
        
        # Crear cliente de prueba
        client = Client()
        
        # Obtener usuario admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No hay usuario admin")
            return
        
        # Hacer login
        client.force_login(admin_user)
        
        # Probar la URL del PDF
        url = f'/proyectos/{proyecto.id}/trabajadores-diarios/pdf/'
        print(f"   URL: {url}")
        
        response = client.get(url)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ PDF generado correctamente")
            print(f"   Tamaño: {len(response.content)} bytes")
            
            # Verificar que es un PDF
            if response.get('Content-Type') == 'application/pdf':
                print("   ✅ Content-Type correcto (PDF)")
            else:
                print(f"   ⚠️  Content-Type: {response.get('Content-Type')}")
        else:
            print("   ❌ Error al generar PDF")
            print(f"   Respuesta: {response.content.decode()[:200]}...")
        
        print("\n✅ PRUEBA COMPLETADA")
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_pdf_trabajadores()
