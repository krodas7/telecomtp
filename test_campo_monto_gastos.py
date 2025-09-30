#!/usr/bin/env python3
"""
Script para probar que el campo de monto funcione libremente
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import CategoriaGasto, Proyecto, Cliente, Gasto
from core.forms_simple import GastoForm
from datetime import date

def probar_montos_diferentes():
    """Probar diferentes tipos de montos"""
    print("💰 PROBANDO CAMPO DE MONTO LIBRE")
    print("=" * 60)
    
    # Obtener datos necesarios
    cliente = Cliente.objects.first()
    proyecto = Proyecto.objects.first()
    categoria = CategoriaGasto.objects.first()
    
    if not all([cliente, proyecto, categoria]):
        print("❌ Faltan datos necesarios (cliente, proyecto, categoría)")
        return False
    
    # Diferentes tipos de montos a probar
    montos_prueba = [
        ("100", "Monto entero simple"),
        ("1500.50", "Monto con decimales"),
        ("0.01", "Monto mínimo"),
        ("999999.99", "Monto máximo"),
        ("25000", "Monto grande sin decimales"),
        ("1234.56", "Monto con decimales"),
        ("0", "Cero"),
        ("1.1", "Un decimal"),
        ("100.00", "Dos decimales"),
    ]
    
    print("🧪 PROBANDO DIFERENTES MONTOS:")
    
    for monto_str, descripcion in montos_prueba:
        try:
            # Crear datos del formulario
            gasto_data = {
                'proyecto': proyecto.id,
                'categoria': categoria.id,
                'descripcion': f'Gasto de prueba: {descripcion}',
                'monto': monto_str,
                'fecha_gasto': date.today(),
                'aprobado': False,
                'observaciones': f'Prueba con monto: {monto_str}'
            }
            
            # Crear formulario
            form = GastoForm(data=gasto_data)
            
            if form.is_valid():
                gasto = form.save()
                print(f"  ✅ {monto_str} - {descripcion}: VÁLIDO (ID: {gasto.id})")
                
                # Verificar que se guardó correctamente
                gasto_bd = Gasto.objects.get(id=gasto.id)
                monto_guardado = float(gasto_bd.monto)
                monto_esperado = float(monto_str)
                
                if abs(monto_guardado - monto_esperado) < 0.01:
                    print(f"    ✅ Monto guardado correctamente: Q{monto_guardado}")
                else:
                    print(f"    ❌ Error: Esperado Q{monto_esperado}, Guardado Q{monto_guardado}")
                    return False
            else:
                print(f"  ❌ {monto_str} - {descripcion}: INVÁLIDO")
                for field, errors in form.errors.items():
                    print(f"    - {field}: {errors}")
                return False
                
        except Exception as e:
            print(f"  ❌ {monto_str} - {descripcion}: ERROR - {e}")
            return False
    
    return True

def probar_montos_invalidos():
    """Probar montos que deberían ser inválidos"""
    print("\n🚫 PROBANDO MONTOS INVÁLIDOS:")
    
    # Obtener datos necesarios
    cliente = Cliente.objects.first()
    proyecto = Proyecto.objects.first()
    categoria = CategoriaGasto.objects.first()
    
    montos_invalidos = [
        ("-100", "Monto negativo"),
        ("1000000", "Monto excesivo"),
        ("abc", "Texto no numérico"),
        ("12.345", "Demasiados decimales"),
        ("", "Monto vacío"),
        ("12.34.56", "Múltiples puntos"),
    ]
    
    for monto_str, descripcion in montos_invalidos:
        try:
            gasto_data = {
                'proyecto': proyecto.id,
                'categoria': categoria.id,
                'descripcion': f'Gasto inválido: {descripcion}',
                'monto': monto_str,
                'fecha_gasto': date.today(),
                'aprobado': False,
            }
            
            form = GastoForm(data=gasto_data)
            
            if not form.is_valid():
                print(f"  ✅ {monto_str} - {descripcion}: CORRECTAMENTE RECHAZADO")
            else:
                print(f"  ❌ {monto_str} - {descripcion}: DEBERÍA SER INVÁLIDO")
                return False
                
        except Exception as e:
            print(f"  ✅ {monto_str} - {descripcion}: CORRECTAMENTE RECHAZADO ({e})")
    
    return True

def probar_formulario_web():
    """Probar el formulario en la web"""
    print("\n🌐 PROBANDO FORMULARIO WEB:")
    
    client = Client()
    admin_user = User.objects.filter(is_superuser=True).first()
    client.force_login(admin_user)
    
    try:
        response = client.get('/gastos/crear/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar que el campo de monto esté presente
            if 'id_monto' in content:
                print("  ✅ Campo de monto presente en el formulario")
            else:
                print("  ❌ Campo de monto no encontrado")
                return False
            
            # Verificar que no tenga restricciones restrictivas
            if 'min=' in content and 'id_monto' in content:
                print("  ⚠️  Campo de monto tiene restricción 'min'")
            else:
                print("  ✅ Campo de monto sin restricciones restrictivas")
            
            # Verificar que tenga placeholder
            if 'placeholder="0.00"' in content:
                print("  ✅ Campo de monto tiene placeholder apropiado")
            else:
                print("  ❌ Campo de monto sin placeholder")
            
            return True
        else:
            print(f"  ❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def mostrar_instrucciones_monto():
    """Mostrar instrucciones para el campo de monto"""
    print("\n📖 INSTRUCCIONES PARA EL CAMPO DE MONTO:")
    print("=" * 60)
    
    instrucciones = [
        "💰 FORMATOS VÁLIDOS:",
        "  • Números enteros: 100, 1500, 25000",
        "  • Números con decimales: 100.50, 1234.56",
        "  • Un solo punto decimal: 100.5 (se formatea a 100.50)",
        "  • Cero: 0 o 0.00",
        "",
        "🚫 FORMATOS INVÁLIDOS:",
        "  • Números negativos: -100",
        "  • Texto: abc, xyz",
        "  • Múltiples puntos: 12.34.56",
        "  • Más de 2 decimales: 12.345",
        "  • Montos excesivos: > Q999,999.99",
        "",
        "✨ CARACTERÍSTICAS:",
        "  • Formateo automático a 2 decimales",
        "  • Validación en tiempo real",
        "  • Sin restricciones de entrada",
        "  • Validación del servidor",
        "  • Rango: Q0.00 - Q999,999.99"
    ]
    
    for instruccion in instrucciones:
        print(instruccion)

def main():
    """Función principal"""
    print("💰 PRUEBA DEL CAMPO DE MONTO LIBRE")
    print("=" * 70)
    
    try:
        # Probar montos válidos
        montos_validos_ok = probar_montos_diferentes()
        
        # Probar montos inválidos
        montos_invalidos_ok = probar_montos_invalidos()
        
        # Probar formulario web
        web_ok = probar_formulario_web()
        
        # Mostrar instrucciones
        mostrar_instrucciones_monto()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if montos_validos_ok and montos_invalidos_ok and web_ok:
            print("🎉 ¡CAMPO DE MONTO FUNCIONANDO PERFECTAMENTE!")
            print("✅ Acepta cualquier monto válido")
            print("✅ Rechaza montos inválidos correctamente")
            print("✅ Formulario web funcionando")
            print("✅ Sin restricciones restrictivas")
            print("✅ Validación completa del lado del servidor")
            
            print(f"\n🌐 PARA PROBAR:")
            print("  1. Ve a: http://localhost:8000/gastos/crear/")
            print("  2. En el campo 'Monto del Gasto' puedes escribir:")
            print("     - 100 (se formatea a 100.00)")
            print("     - 1500.50 (se mantiene igual)")
            print("     - 0.01 (monto mínimo)")
            print("     - 999999.99 (monto máximo)")
            print("  3. El sistema validará automáticamente el formato")
        else:
            print("❌ HAY PROBLEMAS CON EL CAMPO DE MONTO")
            if not montos_validos_ok:
                print("  - Problemas con montos válidos")
            if not montos_invalidos_ok:
                print("  - Problemas con validación de montos inválidos")
            if not web_ok:
                print("  - Problemas con el formulario web")
        
        return montos_validos_ok and montos_invalidos_ok and web_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
