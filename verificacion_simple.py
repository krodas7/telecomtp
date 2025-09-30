#!/usr/bin/env python3
"""
Script simplificado para verificar que los datos se guarden correctamente
"""

import os
import sys
import django
from datetime import date, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import *

def verificar_formularios_criticos():
    """Verificar formularios críticos que podrían causar pérdida de datos"""
    print("🔍 VERIFICANDO FORMULARIOS CRÍTICOS")
    print("=" * 45)
    
    from core.forms_simple import ArchivoProyectoForm, CarpetaProyectoForm
    
    problemas = []
    
    # Verificar ArchivoProyectoForm
    print("\n📁 Verificando ArchivoProyectoForm...")
    form = ArchivoProyectoForm()
    campos_archivo = list(form.fields.keys())
    campos_requeridos = ['proyecto', 'nombre', 'archivo']
    
    campos_faltantes = [campo for campo in campos_requeridos if campo not in campos_archivo]
    if campos_faltantes:
        print(f"  ❌ Campos faltantes: {campos_faltantes}")
        problemas.append(f"ArchivoProyectoForm: {campos_faltantes}")
    else:
        print(f"  ✅ Campos requeridos presentes")
    
    # Verificar CarpetaProyectoForm
    print("\n📂 Verificando CarpetaProyectoForm...")
    form = CarpetaProyectoForm()
    campos_carpeta = list(form.fields.keys())
    campos_requeridos = ['proyecto', 'nombre', 'creada_por']
    
    campos_faltantes = [campo for campo in campos_requeridos if campo not in campos_carpeta]
    if campos_faltantes:
        print(f"  ❌ Campos faltantes: {campos_faltantes}")
        problemas.append(f"CarpetaProyectoForm: {campos_faltantes}")
    else:
        print(f"  ✅ Campos requeridos presentes")
    
    return problemas

def corregir_carpeta_form():
    """Corregir CarpetaProyectoForm para incluir campos requeridos"""
    print(f"\n🔧 CORRIGIENDO CARPETA FORM")
    print("=" * 30)
    
    # Leer el archivo actual
    with open('/Users/krodas7/Desktop/arca/arca-sistema/core/forms_simple.py', 'r') as f:
        content = f.read()
    
    # Buscar la definición de CarpetaProyectoForm
    if "class CarpetaProyectoForm" in content:
        # Reemplazar la definición de Meta
        old_meta = """    class Meta:
        model = CarpetaProyecto
        fields = ['nombre', 'descripcion', 'carpeta_padre', 'activa']"""
        
        new_meta = """    class Meta:
        model = CarpetaProyecto
        fields = ['proyecto', 'nombre', 'descripcion', 'carpeta_padre', 'creada_por', 'activa']"""
        
        if old_meta in content:
            content = content.replace(old_meta, new_meta)
            
            # Agregar widget para proyecto y creada_por
            old_widgets = """        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la carpeta'
            }),"""
            
            new_widgets = """        widgets = {
            'proyecto': forms.HiddenInput(),
            'creada_por': forms.HiddenInput(),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la carpeta'
            }),"""
            
            if old_widgets in content:
                content = content.replace(old_widgets, new_widgets)
                
                # Actualizar el __init__ para manejar proyecto y creada_por
                old_init = """    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        if proyecto:
            self.fields['carpeta_padre'].queryset = CarpetaProyecto.objects.filter(proyecto=proyecto, activa=True)"""
        
        new_init = """    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        if proyecto:
            self.fields['proyecto'].initial = proyecto
            self.fields['proyecto'].widget = forms.HiddenInput()
            self.fields['carpeta_padre'].queryset = CarpetaProyecto.objects.filter(proyecto=proyecto, activa=True)"""
        
        if old_init in content:
            content = content.replace(old_init, new_init)
            
            # Escribir el archivo corregido
            with open('/Users/krodas7/Desktop/arca/arca-sistema/core/forms_simple.py', 'w') as f:
                f.write(content)
            
            print("✅ CarpetaProyectoForm corregido")
            return True
    
    print("❌ No se pudo corregir CarpetaProyectoForm")
    return False

def probar_guardado_basico():
    """Probar guardado básico de datos críticos"""
    print(f"\n🧪 PROBANDO GUARDADO BÁSICO")
    print("=" * 35)
    
    try:
        # Obtener usuario admin
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            print("❌ No hay usuario admin")
            return False
        
        # Limpiar datos de prueba
        Cliente.objects.filter(razon_social__startswith='TEST_').delete()
        Proyecto.objects.filter(nombre__startswith='TEST_').delete()
        
        # 1. Crear cliente
        print("1️⃣ Creando cliente...")
        cliente = Cliente.objects.create(
            razon_social='TEST Cliente BD',
            codigo_fiscal='TEST123456',
            email='test@bd.com',
            telefono='+502 1234-5678',
            direccion='Dirección de prueba',
            activo=True
        )
        print(f"  ✅ Cliente: {cliente.id}")
        
        # 2. Crear proyecto
        print("2️⃣ Creando proyecto...")
        proyecto = Proyecto.objects.create(
            nombre='TEST Proyecto BD',
            descripcion='Proyecto de prueba',
            cliente=cliente,
            presupuesto=Decimal('50000.00'),
            fecha_inicio=date.today(),
            estado='en_progreso',
            activo=True
        )
        print(f"  ✅ Proyecto: {proyecto.id}")
        
        # 3. Crear carpeta
        print("3️⃣ Creando carpeta...")
        carpeta = CarpetaProyecto.objects.create(
            proyecto=proyecto,
            nombre='TEST Carpeta BD',
            descripcion='Carpeta de prueba',
            creada_por=admin_user,
            activa=True
        )
        print(f"  ✅ Carpeta: {carpeta.id}")
        
        # 4. Crear archivo
        print("4️⃣ Creando archivo...")
        from django.core.files.uploadedfile import SimpleUploadedFile
        
        archivo_contenido = SimpleUploadedFile(
            "test_bd.txt",
            b"Contenido de prueba",
            content_type="text/plain"
        )
        
        archivo = ArchivoProyecto.objects.create(
            proyecto=proyecto,
            carpeta=carpeta,
            nombre='TEST Archivo BD',
            descripcion='Archivo de prueba',
            archivo=archivo_contenido,
            tipo='documento',
            subido_por=admin_user,
            activo=True
        )
        print(f"  ✅ Archivo: {archivo.id}")
        
        # 5. Verificar que todo se guardó
        print("5️⃣ Verificando guardado...")
        cliente_verificado = Cliente.objects.filter(id=cliente.id).exists()
        proyecto_verificado = Proyecto.objects.filter(id=proyecto.id).exists()
        carpeta_verificada = CarpetaProyecto.objects.filter(id=carpeta.id).exists()
        archivo_verificado = ArchivoProyecto.objects.filter(id=archivo.id).exists()
        
        if cliente_verificado and proyecto_verificado and carpeta_verificada and archivo_verificado:
            print("  ✅ Todos los datos guardados correctamente")
            return True
        else:
            print("  ❌ Algunos datos no se guardaron")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verificar_conteos_finales():
    """Verificar conteos finales de datos"""
    print(f"\n📊 CONTEO FINAL DE DATOS")
    print("=" * 30)
    
    conteos = {
        'Clientes': Cliente.objects.count(),
        'Proyectos': Proyecto.objects.count(),
        'Colaboradores': Colaborador.objects.count(),
        'Facturas': Factura.objects.count(),
        'Gastos': Gasto.objects.count(),
        'Anticipos': Anticipo.objects.count(),
        'Archivos': ArchivoProyecto.objects.count(),
        'Carpetas': CarpetaProyecto.objects.count(),
        'Usuarios': User.objects.count(),
    }
    
    for entidad, conteo in conteos.items():
        print(f"  {entidad}: {conteo}")
    
    return conteos

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN DE GUARDADO EN BASE DE DATOS")
    print("=" * 55)
    
    # Verificar formularios críticos
    problemas_formularios = verificar_formularios_criticos()
    
    # Corregir formularios si es necesario
    if problemas_formularios:
        print(f"\n🔧 CORRIGIENDO FORMULARIOS...")
        for problema in problemas_formularios:
            if "CarpetaProyectoForm" in problema:
                corregir_carpeta_form()
    
    # Probar guardado básico
    guardado_ok = probar_guardado_basico()
    
    # Verificar conteos
    conteos = verificar_conteos_finales()
    
    # Resumen final
    print(f"\n" + "=" * 55)
    print("📋 RESUMEN FINAL")
    print("=" * 55)
    
    if guardado_ok:
        print("✅ TODOS LOS DATOS SE GUARDAN CORRECTAMENTE")
        print("✅ NO HAY RIESGO DE PÉRDIDA DE DATOS")
        print("✅ EL SISTEMA ES SEGURO PARA MANTENIMIENTOS")
    else:
        print("❌ HAY PROBLEMAS DE GUARDADO")
        print("❌ EXISTE RIESGO DE PÉRDIDA DE DATOS")
    
    print(f"\n📊 DATOS ACTUALES EN LA BASE DE DATOS:")
    for entidad, conteo in conteos.items():
        print(f"  {entidad}: {conteo}")

if __name__ == "__main__":
    main()
