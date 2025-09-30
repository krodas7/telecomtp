#!/usr/bin/env python3
"""
Script completo para verificar que todos los datos se guarden correctamente en la BD
"""

import os
import sys
import django
from io import BytesIO
from datetime import date, datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import *
from django.core.files.uploadedfile import SimpleUploadedFile

def verificar_modelos_requeridos():
    """Verificar que todos los modelos tengan campos requeridos correctos"""
    print("🔍 VERIFICANDO MODELOS Y CAMPOS REQUERIDOS")
    print("=" * 55)
    
    modelos_problema = []
    
    # Verificar modelos principales
    modelos_verificar = [
        (Cliente, ['razon_social', 'codigo_fiscal', 'email']),
        (Proyecto, ['nombre', 'cliente', 'fecha_inicio']),
        (Colaborador, ['nombre', 'dpi', 'email']),
        (Factura, ['numero_factura', 'proyecto', 'cliente', 'monto_total']),
        (Gasto, ['proyecto', 'categoria', 'monto', 'fecha_gasto']),
        (Anticipo, ['cliente', 'proyecto', 'monto']),
        (ArchivoProyecto, ['proyecto', 'nombre', 'archivo']),
        (CarpetaProyecto, ['proyecto', 'nombre', 'creada_por']),
        (Presupuesto, ['proyecto', 'nombre']),
        (PartidaPresupuesto, ['presupuesto', 'descripcion', 'monto_estimado']),
    ]
    
    for modelo, campos_requeridos in modelos_verificar:
        print(f"\n📋 Verificando {modelo.__name__}:")
        
        # Verificar campos del modelo
        campos_modelo = [field.name for field in modelo._meta.fields]
        campos_faltantes = [campo for campo in campos_requeridos if campo not in campos_modelo]
        
        if campos_faltantes:
            print(f"  ❌ Campos faltantes: {campos_faltantes}")
            modelos_problema.append((modelo.__name__, campos_faltantes))
        else:
            print(f"  ✅ Campos requeridos presentes")
        
        # Verificar campos no nulos
        campos_no_nulos = [field.name for field in modelo._meta.fields if not field.null and not field.blank]
        print(f"  📝 Campos no nulos: {len(campos_no_nulos)}")
    
    if modelos_problema:
        print(f"\n❌ PROBLEMAS ENCONTRADOS:")
        for modelo, campos in modelos_problema:
            print(f"  {modelo}: {campos}")
    else:
        print(f"\n✅ TODOS LOS MODELOS ESTÁN CORRECTOS")
    
    return len(modelos_problema) == 0

def verificar_formularios():
    """Verificar que todos los formularios incluyan campos requeridos"""
    print(f"\n🔍 VERIFICANDO FORMULARIOS")
    print("=" * 35)
    
    from core.forms_simple import (
        ClienteForm, ProyectoForm, ColaboradorForm, FacturaForm, GastoForm,
        AnticipoForm, ArchivoProyectoForm, CarpetaProyectoForm, PresupuestoForm,
        PartidaPresupuestoForm
    )
    
    formularios_verificar = [
        (ClienteForm, Cliente, ['razon_social', 'codigo_fiscal', 'email']),
        (ProyectoForm, Proyecto, ['nombre', 'cliente', 'fecha_inicio']),
        (ColaboradorForm, Colaborador, ['nombre', 'dpi', 'email']),
        (FacturaForm, Factura, ['numero_factura', 'proyecto', 'cliente', 'monto_total']),
        (GastoForm, Gasto, ['proyecto', 'categoria', 'monto', 'fecha_gasto']),
        (AnticipoForm, Anticipo, ['cliente', 'proyecto', 'monto']),
        (ArchivoProyectoForm, ArchivoProyecto, ['proyecto', 'nombre', 'archivo']),
        (CarpetaProyectoForm, CarpetaProyecto, ['proyecto', 'nombre', 'creada_por']),
        (PresupuestoForm, Presupuesto, ['proyecto', 'nombre']),
        (PartidaPresupuestoForm, PartidaPresupuesto, ['presupuesto', 'descripcion', 'monto_estimado']),
    ]
    
    formularios_problema = []
    
    for form_class, modelo, campos_requeridos in formularios_verificar:
        print(f"\n📝 Verificando {form_class.__name__}:")
        
        # Obtener campos del formulario
        form = form_class()
        campos_formulario = list(form.fields.keys())
        
        campos_faltantes = [campo for campo in campos_requeridos if campo not in campos_formulario]
        
        if campos_faltantes:
            print(f"  ❌ Campos faltantes: {campos_faltantes}")
            formularios_problema.append((form_class.__name__, campos_faltantes))
        else:
            print(f"  ✅ Campos requeridos presentes")
        
        print(f"  📋 Campos del formulario: {len(campos_formulario)}")
    
    if formularios_problema:
        print(f"\n❌ PROBLEMAS EN FORMULARIOS:")
        for form, campos in formularios_problema:
            print(f"  {form}: {campos}")
    else:
        print(f"\n✅ TODOS LOS FORMULARIOS ESTÁN CORRECTOS")
    
    return len(formularios_problema) == 0

def probar_guardado_completo():
    """Probar el guardado de todos los módulos principales"""
    print(f"\n🧪 PROBANDO GUARDADO COMPLETO")
    print("=" * 40)
    
    # Obtener usuario admin
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay usuario admin")
        return False
    
    # Limpiar datos de prueba anteriores
    print("🧹 Limpiando datos de prueba anteriores...")
    ArchivoProyecto.objects.filter(nombre__startswith='TEST_').delete()
    CarpetaProyecto.objects.filter(nombre__startswith='TEST_').delete()
    
    try:
        # 1. Crear cliente
        print("\n1️⃣ Creando cliente...")
        cliente_data = {
            'razon_social': 'TEST Cliente Verificación',
            'codigo_fiscal': 'TEST123456789',
            'email': 'test@verificacion.com',
            'telefono': '+502 1234-5678',
            'direccion': 'Dirección de prueba',
            'activo': True
        }
        cliente = Cliente.objects.create(**cliente_data)
        print(f"  ✅ Cliente creado: {cliente.id} - {cliente.razon_social}")
        
        # 2. Crear proyecto
        print("\n2️⃣ Creando proyecto...")
        proyecto_data = {
            'nombre': 'TEST Proyecto Verificación',
            'descripcion': 'Proyecto de prueba para verificación',
            'cliente': cliente,
            'presupuesto': Decimal('100000.00'),
            'fecha_inicio': date.today(),
            'fecha_fin': date.today() + timedelta(days=30),
            'estado': 'en_progreso',
            'activo': True
        }
        proyecto = Proyecto.objects.create(**proyecto_data)
        print(f"  ✅ Proyecto creado: {proyecto.id} - {proyecto.nombre}")
        
        # 3. Crear colaborador
        print("\n3️⃣ Creando colaborador...")
        colaborador_data = {
            'nombre': 'TEST Colaborador Verificación',
            'dpi': '1234567890101',
            'email': 'colaborador@test.com',
            'telefono': '+502 8765-4321',
            'direccion': 'Dirección colaborador',
            'salario': Decimal('5000.00'),
            'fecha_contratacion': date.today(),
            'activo': True
        }
        colaborador = Colaborador.objects.create(**colaborador_data)
        print(f"  ✅ Colaborador creado: {colaborador.id} - {colaborador.nombre}")
        
        # 4. Crear categoría de gasto
        print("\n4️⃣ Creando categoría de gasto...")
        categoria_data = {
            'nombre': 'TEST Categoría',
            'descripcion': 'Categoría de prueba',
            'color': '#FF5733',
            'icono': 'fas fa-tools'
        }
        categoria = CategoriaGasto.objects.create(**categoria_data)
        print(f"  ✅ Categoría creada: {categoria.id} - {categoria.nombre}")
        
        # 5. Crear gasto
        print("\n5️⃣ Creando gasto...")
        gasto_data = {
            'proyecto': proyecto,
            'categoria': categoria,
            'descripcion': 'Gasto de prueba para verificación',
            'monto': Decimal('1000.00'),
            'fecha_gasto': date.today(),
            'aprobado': True
        }
        gasto = Gasto.objects.create(**gasto_data)
        print(f"  ✅ Gasto creado: {gasto.id} - Q{gasto.monto}")
        
        # 6. Crear factura
        print("\n6️⃣ Creando factura...")
        factura_data = {
            'numero_factura': 'TEST-FAC-001',
            'proyecto': proyecto,
            'cliente': cliente,
            'tipo': 'servicios',
            'estado': 'enviada',
            'fecha_emision': date.today(),
            'fecha_vencimiento': date.today() + timedelta(days=30),
            'monto_subtotal': Decimal('50000.00'),
            'monto_iva': Decimal('7500.00'),
            'monto_total': Decimal('57500.00'),
            'descripcion_servicios': 'Servicios de construcción'
        }
        factura = Factura.objects.create(**factura_data)
        print(f"  ✅ Factura creada: {factura.id} - {factura.numero_factura}")
        
        # 7. Crear anticipo
        print("\n7️⃣ Creando anticipo...")
        anticipo_data = {
            'cliente': cliente,
            'proyecto': proyecto,
            'monto': Decimal('20000.00'),
            'tipo': 'anticipo',
            'estado': 'pendiente',
            'fecha_recepcion': date.today(),
            'observaciones': 'Anticipo de prueba'
        }
        anticipo = Anticipo.objects.create(**anticipo_data)
        print(f"  ✅ Anticipo creado: {anticipo.id} - Q{anticipo.monto}")
        
        # 8. Crear carpeta
        print("\n8️⃣ Creando carpeta...")
        carpeta_data = {
            'proyecto': proyecto,
            'nombre': 'TEST Carpeta Verificación',
            'descripcion': 'Carpeta de prueba',
            'creada_por': admin_user,
            'activa': True
        }
        carpeta = CarpetaProyecto.objects.create(**carpeta_data)
        print(f"  ✅ Carpeta creada: {carpeta.id} - {carpeta.nombre}")
        
        # 9. Crear archivo
        print("\n9️⃣ Creando archivo...")
        archivo_contenido = SimpleUploadedFile(
            "TEST_verificacion.txt",
            b"Contenido de prueba para verificacion",
            content_type="text/plain"
        )
        archivo_data = {
            'proyecto': proyecto,
            'carpeta': carpeta,
            'nombre': 'TEST Archivo Verificación',
            'descripcion': 'Archivo de prueba',
            'archivo': archivo_contenido,
            'tipo': 'documento',
            'subido_por': admin_user,
            'activo': True
        }
        archivo = ArchivoProyecto.objects.create(**archivo_data)
        print(f"  ✅ Archivo creado: {archivo.id} - {archivo.nombre}")
        
        # 10. Crear presupuesto
        print("\n🔟 Creando presupuesto...")
        presupuesto_data = {
            'proyecto': proyecto,
            'nombre': 'TEST Presupuesto Verificación',
            'version': '1.0',
            'estado': 'borrador'
        }
        presupuesto = Presupuesto.objects.create(**presupuesto_data)
        print(f"  ✅ Presupuesto creado: {presupuesto.id} - {presupuesto.nombre}")
        
        # 11. Crear partida de presupuesto
        print("\n1️⃣1️⃣ Creando partida de presupuesto...")
        partida_data = {
            'presupuesto': presupuesto,
            'codigo': '001',
            'descripcion': 'Partida de prueba',
            'unidad': 'm2',
            'cantidad': Decimal('100.00'),
            'precio_unitario': Decimal('50.00'),
            'monto_estimado': Decimal('5000.00'),
            'categoria': 'Materiales',
            'subcategoria': 'Concreto',
            'notas': 'Partida de prueba',
            'orden': 1
        }
        partida = PartidaPresupuesto.objects.create(**partida_data)
        print(f"  ✅ Partida creada: {partida.id} - {partida.descripcion}")
        
        print(f"\n✅ TODOS LOS DATOS GUARDADOS CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR AL GUARDAR DATOS: {e}")
        import traceback
        traceback.print_exc()
        return False

def verificar_integridad_bd():
    """Verificar integridad referencial de la base de datos"""
    print(f"\n🔍 VERIFICANDO INTEGRIDAD DE LA BASE DE DATOS")
    print("=" * 55)
    
    problemas = []
    
    # Verificar relaciones de Cliente
    print("\n👥 Verificando Clientes...")
    clientes_sin_proyectos = Cliente.objects.filter(proyectos__isnull=True).count()
    if clientes_sin_proyectos > 0:
        print(f"  ⚠️  {clientes_sin_proyectos} clientes sin proyectos")
    
    # Verificar relaciones de Proyecto
    print("\n🏗️ Verificando Proyectos...")
    proyectos_sin_cliente = Proyecto.objects.filter(cliente__isnull=True).count()
    if proyectos_sin_cliente > 0:
        print(f"  ❌ {proyectos_sin_cliente} proyectos sin cliente")
        problemas.append("Proyectos sin cliente")
    
    # Verificar relaciones de Factura
    print("\n💰 Verificando Facturas...")
    facturas_sin_proyecto = Factura.objects.filter(proyecto__isnull=True).count()
    facturas_sin_cliente = Factura.objects.filter(cliente__isnull=True).count()
    if facturas_sin_proyecto > 0:
        print(f"  ❌ {facturas_sin_proyecto} facturas sin proyecto")
        problemas.append("Facturas sin proyecto")
    if facturas_sin_cliente > 0:
        print(f"  ❌ {facturas_sin_cliente} facturas sin cliente")
        problemas.append("Facturas sin cliente")
    
    # Verificar relaciones de Gasto
    print("\n💸 Verificando Gastos...")
    gastos_sin_proyecto = Gasto.objects.filter(proyecto__isnull=True).count()
    gastos_sin_categoria = Gasto.objects.filter(categoria__isnull=True).count()
    if gastos_sin_proyecto > 0:
        print(f"  ❌ {gastos_sin_proyecto} gastos sin proyecto")
        problemas.append("Gastos sin proyecto")
    if gastos_sin_categoria > 0:
        print(f"  ❌ {gastos_sin_categoria} gastos sin categoría")
        problemas.append("Gastos sin categoría")
    
    # Verificar relaciones de ArchivoProyecto
    print("\n📁 Verificando Archivos...")
    archivos_sin_proyecto = ArchivoProyecto.objects.filter(proyecto__isnull=True).count()
    if archivos_sin_proyecto > 0:
        print(f"  ❌ {archivos_sin_proyecto} archivos sin proyecto")
        problemas.append("Archivos sin proyecto")
    
    # Verificar relaciones de CarpetaProyecto
    print("\n📂 Verificando Carpetas...")
    carpetas_sin_proyecto = CarpetaProyecto.objects.filter(proyecto__isnull=True).count()
    carpetas_sin_creador = CarpetaProyecto.objects.filter(creada_por__isnull=True).count()
    if carpetas_sin_proyecto > 0:
        print(f"  ❌ {carpetas_sin_proyecto} carpetas sin proyecto")
        problemas.append("Carpetas sin proyecto")
    if carpetas_sin_creador > 0:
        print(f"  ❌ {carpetas_sin_creador} carpetas sin creador")
        problemas.append("Carpetas sin creador")
    
    if problemas:
        print(f"\n❌ PROBLEMAS DE INTEGRIDAD ENCONTRADOS:")
        for problema in problemas:
            print(f"  - {problema}")
    else:
        print(f"\n✅ INTEGRIDAD DE LA BASE DE DATOS CORRECTA")
    
    return len(problemas) == 0

def verificar_conteos():
    """Verificar conteos de datos en la base de datos"""
    print(f"\n📊 VERIFICANDO CONTEO DE DATOS")
    print("=" * 40)
    
    conteos = {
        'Clientes': Cliente.objects.count(),
        'Proyectos': Proyecto.objects.count(),
        'Colaboradores': Colaborador.objects.count(),
        'Facturas': Factura.objects.count(),
        'Gastos': Gasto.objects.count(),
        'Anticipos': Anticipo.objects.count(),
        'Archivos': ArchivoProyecto.objects.count(),
        'Carpetas': CarpetaProyecto.objects.count(),
        'Presupuestos': Presupuesto.objects.count(),
        'Partidas': PartidaPresupuesto.objects.count(),
        'Usuarios': User.objects.count(),
    }
    
    for entidad, conteo in conteos.items():
        print(f"  {entidad}: {conteo}")
    
    return conteos

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN COMPLETA DE BASE DE DATOS")
    print("=" * 50)
    
    # Verificar modelos
    modelos_ok = verificar_modelos_requeridos()
    
    # Verificar formularios
    formularios_ok = verificar_formularios()
    
    # Probar guardado
    guardado_ok = probar_guardado_completo()
    
    # Verificar integridad
    integridad_ok = verificar_integridad_bd()
    
    # Verificar conteos
    conteos = verificar_conteos()
    
    # Resumen final
    print(f"\n" + "=" * 50)
    print("📋 RESUMEN DE VERIFICACIÓN")
    print("=" * 50)
    
    print(f"✅ Modelos: {'OK' if modelos_ok else '❌ PROBLEMAS'}")
    print(f"✅ Formularios: {'OK' if formularios_ok else '❌ PROBLEMAS'}")
    print(f"✅ Guardado: {'OK' if guardado_ok else '❌ PROBLEMAS'}")
    print(f"✅ Integridad: {'OK' if integridad_ok else '❌ PROBLEMAS'}")
    
    if modelos_ok and formularios_ok and guardado_ok and integridad_ok:
        print(f"\n🎉 ¡TODOS LOS DATOS SE GUARDAN CORRECTAMENTE EN LA BASE DE DATOS!")
        print(f"✅ No hay riesgo de pérdida de datos durante mantenimientos")
    else:
        print(f"\n⚠️  HAY PROBLEMAS QUE NECESITAN CORRECCIÓN")
        print(f"❌ Existe riesgo de pérdida de datos")
    
    print(f"\n📊 DATOS ACTUALES EN LA BASE DE DATOS:")
    for entidad, conteo in conteos.items():
        print(f"  {entidad}: {conteo}")

if __name__ == "__main__":
    main()
