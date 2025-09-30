#!/usr/bin/env python3
"""
Script para verificar que todos los módulos del menú estén funcionando
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

def probar_todos_los_modulos():
    """Probar que todos los módulos del menú estén funcionando"""
    print("🔍 VERIFICANDO TODOS LOS MÓDULOS DEL MENÚ")
    print("=" * 45)
    
    # Crear cliente de prueba
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    # Lista de módulos a probar
    modulos = [
        ("Dashboard", "/dashboard/", "dashboard"),
        ("Proyectos", "/proyectos/", "proyectos_list"),
        ("Clientes", "/clientes/", "clientes_list"),
        ("Facturas", "/facturas/", "facturas_list"),
        ("Colaboradores", "/colaboradores/", "colaboradores_list"),
        ("Gastos", "/gastos/", "gastos_list"),
        ("Inventario", "/inventario/", "inventario_list"),
        ("Presupuestos", "/presupuestos/", "presupuestos_list"),
        ("Usuarios", "/usuarios/", "usuarios_lista"),
        ("Archivos", "/archivos/", "archivos_list"),
        ("Anticipos", "/anticipos/", "anticipos_list"),
        ("Pagos", "/pagos/", "pagos_list"),
        ("Rentabilidad", "/rentabilidad/", "rentabilidad"),
        ("Sistema", "/sistema/", "sistema"),
    ]
    
    resultados = []
    
    for nombre, url, url_name in modulos:
        print(f"\n🔍 Probando {nombre}...")
        try:
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {nombre} funciona correctamente")
                resultados.append((nombre, True, "OK"))
            elif response.status_code == 302:
                print(f"  ⚠️ {nombre} redirige (posible login requerido)")
                resultados.append((nombre, True, "REDIRECT"))
            else:
                print(f"  ❌ {nombre} error: {response.status_code}")
                resultados.append((nombre, False, f"ERROR {response.status_code}"))
        except Exception as e:
            print(f"  ❌ {nombre} excepción: {e}")
            resultados.append((nombre, False, f"EXCEPTION: {e}"))
    
    return resultados

def main():
    """Función principal"""
    print("🎯 VERIFICACIÓN COMPLETA DEL MENÚ")
    print("=" * 45)
    
    # Probar todos los módulos
    resultados = probar_todos_los_modulos()
    
    # Resumen final
    print(f"\n" + "=" * 45)
    print("📋 RESUMEN DE MÓDULOS")
    print("=" * 45)
    
    funcionando = 0
    con_problemas = 0
    
    for nombre, ok, detalle in resultados:
        if ok:
            print(f"✅ {nombre}: {detalle}")
            funcionando += 1
        else:
            print(f"❌ {nombre}: {detalle}")
            con_problemas += 1
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"  ✅ Funcionando: {funcionando}")
    print(f"  ❌ Con problemas: {con_problemas}")
    print(f"  📈 Total: {len(resultados)}")
    
    if con_problemas == 0:
        print(f"\n🎉 ¡TODOS LOS MÓDULOS FUNCIONAN PERFECTAMENTE!")
    else:
        print(f"\n⚠️ {con_problemas} módulos necesitan atención")

if __name__ == "__main__":
    main()
