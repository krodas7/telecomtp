#!/usr/bin/env python3
"""
Script para probar que el formulario de gastos funcione completamente
con todos los campos incluidos
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
from datetime import date, timedelta

def probar_formulario_completo():
    """Probar que el formulario tenga todos los campos necesarios"""
    print("🔧 PROBANDO FORMULARIO COMPLETO DE GASTOS")
    print("=" * 60)
    
    # Verificar que el formulario tenga todos los campos
    form = GastoForm()
    campos_esperados = [
        'proyecto', 'categoria', 'descripcion', 'monto', 
        'fecha_gasto', 'fecha_vencimiento', 'aprobado', 
        'observaciones', 'comprobante'
    ]
    
    campos_presentes = list(form.fields.keys())
    
    print("📋 VERIFICANDO CAMPOS DEL FORMULARIO:")
    for campo in campos_esperados:
        if campo in campos_presentes:
            print(f"  ✅ {campo}: Presente")
        else:
            print(f"  ❌ {campo}: FALTANTE")
    
    # Verificar que el modelo tenga todos los campos
    print("\n🗄️ VERIFICANDO CAMPOS DEL MODELO:")
    campos_modelo = [field.name for field in Gasto._meta.fields]
    
    for campo in campos_esperados:
        if campo in campos_modelo:
            print(f"  ✅ {campo}: Presente en modelo")
        else:
            print(f"  ❌ {campo}: FALTANTE en modelo")
    
    return len([c for c in campos_esperados if c in campos_presentes]) == len(campos_esperados)

def probar_creacion_gasto():
    """Probar la creación de un gasto con todos los campos"""
    print("\n💾 PROBANDO CREACIÓN DE GASTO")
    print("=" * 60)
    
    try:
        # Obtener datos necesarios
        cliente = Cliente.objects.first()
        if not cliente:
            print("❌ No hay clientes en la base de datos")
            return False
        
        proyecto = Proyecto.objects.first()
        if not proyecto:
            print("❌ No hay proyectos en la base de datos")
            return False
        
        categoria = CategoriaGasto.objects.first()
        if not categoria:
            print("❌ No hay categorías de gasto en la base de datos")
            return False
        
        # Crear gasto con todos los campos
        gasto_data = {
            'proyecto': proyecto.id,
            'categoria': categoria.id,
            'descripcion': 'Gasto de prueba con todos los campos',
            'monto': 1500.50,
            'fecha_gasto': date.today(),
            'fecha_vencimiento': date.today() + timedelta(days=30),
            'aprobado': True,
            'observaciones': 'Esta es una observación de prueba para verificar que el campo funciona correctamente.',
            'comprobante': None  # No subimos archivo en la prueba
        }
        
        form = GastoForm(data=gasto_data)
        
        if form.is_valid():
            gasto = form.save()
            print(f"✅ Gasto creado exitosamente: {gasto.id}")
            print(f"  📝 Descripción: {gasto.descripcion}")
            print(f"  💰 Monto: Q{gasto.monto}")
            print(f"  📅 Fecha gasto: {gasto.fecha_gasto}")
            print(f"  📅 Fecha vencimiento: {gasto.fecha_vencimiento}")
            print(f"  ✅ Aprobado: {gasto.aprobado}")
            print(f"  📝 Observaciones: {gasto.observaciones}")
            print(f"  📁 Comprobante: {gasto.comprobante}")
            
            # Verificar que se guardó en la base de datos
            gasto_bd = Gasto.objects.get(id=gasto.id)
            if gasto_bd.observaciones == gasto_data['observaciones']:
                print("✅ Observaciones guardadas correctamente en BD")
            else:
                print("❌ Error: Observaciones no se guardaron en BD")
                return False
            
            if gasto_bd.fecha_vencimiento == gasto_data['fecha_vencimiento']:
                print("✅ Fecha de vencimiento guardada correctamente en BD")
            else:
                print("❌ Error: Fecha de vencimiento no se guardó en BD")
                return False
            
            if gasto_bd.aprobado == gasto_data['aprobado']:
                print("✅ Estado de aprobación guardado correctamente en BD")
            else:
                print("❌ Error: Estado de aprobación no se guardó en BD")
                return False
            
            return True
        else:
            print("❌ Formulario inválido:")
            for field, errors in form.errors.items():
                print(f"  - {field}: {errors}")
            return False
            
    except Exception as e:
        print(f"❌ Error creando gasto: {e}")
        return False

def probar_formulario_web():
    """Probar el formulario en la web"""
    print("\n🌐 PROBANDO FORMULARIO EN LA WEB")
    print("=" * 60)
    
    client = Client()
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Autenticar
    client.force_login(admin_user)
    print(f"✅ Usuario autenticado: {admin_user.username}")
    
    try:
        # Acceder al formulario
        response = client.get('/gastos/crear/')
        
        if response.status_code == 200:
            content = response.content.decode()
            
            # Verificar que todos los campos estén presentes en el HTML
            campos_html = [
                'id_observaciones',
                'id_fecha_vencimiento', 
                'id_aprobado',
                'id_comprobante'
            ]
            
            campos_encontrados = 0
            print("🔍 VERIFICANDO CAMPOS EN HTML:")
            for campo in campos_html:
                if campo in content:
                    campos_encontrados += 1
                    print(f"  ✅ {campo}: Presente en HTML")
                else:
                    print(f"  ❌ {campo}: Faltante en HTML")
            
            # Verificar que no hay errores de template
            if 'TemplateDoesNotExist' in content or 'TemplateSyntaxError' in content:
                print("❌ Error de template detectado")
                return False
            
            if campos_encontrados == len(campos_html):
                print("✅ Todos los campos presentes en el formulario web")
                return True
            else:
                print("❌ Faltan campos en el formulario web")
                return False
        else:
            print(f"❌ Error accediendo al formulario: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verificar_integridad_datos():
    """Verificar que no se pierdan datos al guardar"""
    print("\n🔒 VERIFICANDO INTEGRIDAD DE DATOS")
    print("=" * 60)
    
    try:
        # Obtener el último gasto creado
        ultimo_gasto = Gasto.objects.last()
        if not ultimo_gasto:
            print("❌ No hay gastos en la base de datos")
            return False
        
        print(f"📊 Verificando gasto ID: {ultimo_gasto.id}")
        
        # Verificar que todos los campos críticos tengan valores
        campos_criticos = {
            'proyecto': ultimo_gasto.proyecto,
            'categoria': ultimo_gasto.categoria,
            'descripcion': ultimo_gasto.descripcion,
            'monto': ultimo_gasto.monto,
            'fecha_gasto': ultimo_gasto.fecha_gasto,
            'aprobado': ultimo_gasto.aprobado,
            'creado_en': ultimo_gasto.creado_en
        }
        
        campos_ok = 0
        for campo, valor in campos_criticos.items():
            if valor is not None and valor != '':
                campos_ok += 1
                print(f"  ✅ {campo}: {valor}")
            else:
                print(f"  ❌ {campo}: Valor vacío o nulo")
        
        # Verificar campos opcionales
        campos_opcionales = {
            'fecha_vencimiento': ultimo_gasto.fecha_vencimiento,
            'observaciones': ultimo_gasto.observaciones,
            'comprobante': ultimo_gasto.comprobante
        }
        
        print("\n📝 Campos opcionales:")
        for campo, valor in campos_opcionales.items():
            if valor is not None and valor != '':
                print(f"  ✅ {campo}: {valor}")
            else:
                print(f"  ⚪ {campo}: Vacío (opcional)")
        
        if campos_ok == len(campos_criticos):
            print("✅ Integridad de datos verificada")
            return True
        else:
            print("❌ Problemas de integridad de datos")
            return False
            
    except Exception as e:
        print(f"❌ Error verificando integridad: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 PRUEBA COMPLETA DEL FORMULARIO DE GASTOS")
    print("=" * 70)
    
    try:
        # Probar formulario completo
        formulario_ok = probar_formulario_completo()
        
        # Probar creación de gasto
        creacion_ok = probar_creacion_gasto()
        
        # Probar formulario web
        web_ok = probar_formulario_web()
        
        # Verificar integridad
        integridad_ok = verificar_integridad_datos()
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        if formulario_ok and creacion_ok and web_ok and integridad_ok:
            print("🎉 ¡FORMULARIO DE GASTOS FUNCIONANDO AL 100%!")
            print("✅ Todos los campos presentes y funcionando")
            print("✅ Creación de gastos exitosa")
            print("✅ Formulario web funcionando")
            print("✅ Integridad de datos verificada")
            print("✅ NO HAY RIESGO DE PÉRDIDA DE DATOS")
            
            print(f"\n🌐 PARA PROBAR:")
            print("  1. Ve a: http://localhost:8000/gastos/crear/")
            print("  2. Llena todos los campos incluyendo observaciones")
            print("  3. Marca/desmarca la casilla de aprobado")
            print("  4. Guarda el gasto y verifica que se guarde correctamente")
        else:
            print("❌ HAY PROBLEMAS CON EL FORMULARIO")
            if not formulario_ok:
                print("  - Problemas con campos del formulario")
            if not creacion_ok:
                print("  - Problemas creando gastos")
            if not web_ok:
                print("  - Problemas con el formulario web")
            if not integridad_ok:
                print("  - Problemas de integridad de datos")
        
        return formulario_ok and creacion_ok and web_ok and integridad_ok
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
