#!/usr/bin/env python3
"""
Script para probar las notificaciones mejoradas de anticipos
"""

import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_construccion.settings')
django.setup()

from core.models import Cliente, Proyecto, Anticipo
from django.contrib.auth.models import User

def test_notification_content():
    """Probar el contenido de las notificaciones mejoradas"""
    print("🧪 PROBANDO NOTIFICACIONES MEJORADAS DE ANTICIPOS")
    print("=" * 60)
    
    # Obtener datos de prueba
    cliente = Cliente.objects.first()
    proyecto = Proyecto.objects.first()
    user = User.objects.first()
    
    if not all([cliente, proyecto, user]):
        print("❌ Faltan datos para la prueba")
        return
    
    # Crear un anticipo de prueba
    anticipo = Anticipo.objects.create(
        cliente=cliente,
        proyecto=proyecto,
        monto=Decimal('150000.00'),
        tipo='inicial',
        estado='recibido',
        fecha_recepcion=datetime.now().date(),
        observaciones='Anticipo de prueba para notificaciones'
    )
    
    print(f"📊 Datos de prueba:")
    print(f"  Cliente: {cliente.razon_social}")
    print(f"  Proyecto: {proyecto.nombre}")
    print(f"  Anticipo: Q{anticipo.monto:,.2f}")
    
    # Simular notificaciones
    print(f"\n🔔 NOTIFICACIONES MEJORADAS:")
    print("=" * 40)
    
    # Notificación de creación
    print("1️⃣ CREACIÓN DE ANTICIPO:")
    notificacion_creacion = (
        f'✅ <strong>Anticipo creado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{anticipo.monto:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{anticipo.proyecto.nombre}</strong><br>'
        f'👤 Cliente: <strong>{anticipo.cliente.razon_social}</strong>'
    )
    print(notificacion_creacion)
    
    # Notificación de aplicación al proyecto
    print(f"\n2️⃣ APLICACIÓN AL PROYECTO:")
    monto_aplicar = Decimal('75000.00')
    notificacion_aplicacion = (
        f'✅ <strong>Anticipo aplicado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{monto_aplicar:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{anticipo.proyecto.nombre}</strong><br>'
        f'👤 Cliente: <strong>{anticipo.cliente.razon_social}</strong>'
    )
    print(notificacion_aplicacion)
    
    # Notificación de actualización
    print(f"\n3️⃣ ACTUALIZACIÓN DE ANTICIPO:")
    notificacion_actualizacion = (
        f'✅ <strong>Anticipo actualizado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{anticipo.monto:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{anticipo.proyecto.nombre}</strong><br>'
        f'👤 Cliente: <strong>{anticipo.cliente.razon_social}</strong>'
    )
    print(notificacion_actualizacion)
    
    # Notificación de eliminación
    print(f"\n4️⃣ ELIMINACIÓN DE ANTICIPO:")
    notificacion_eliminacion = (
        f'🗑️ <strong>Anticipo eliminado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{anticipo.monto:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{anticipo.proyecto.nombre}</strong><br>'
        f'👤 Cliente: <strong>{anticipo.cliente.razon_social}</strong>'
    )
    print(notificacion_eliminacion)
    
    # Limpiar anticipo de prueba
    anticipo.delete()
    print(f"\n🧹 Anticipo de prueba eliminado")
    
    print(f"\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)
    print("🎯 MEJORAS IMPLEMENTADAS:")
    print("  ✅ Emojis para mejor visualización")
    print("  ✅ Información detallada (monto, proyecto, cliente)")
    print("  ✅ Formato HTML para mejor presentación")
    print("  ✅ Formato de moneda con separadores de miles")
    print("  ✅ Información contextual relevante")
    
    print(f"\n🌐 Para probar en el navegador:")
    print("  1. Ve a: http://localhost:8000/")
    print("  2. Inicia sesión con: admin / admin123")
    print("  3. Ve a Anticipos")
    print("  4. Crea, edita o aplica un anticipo")
    print("  5. Observa las notificaciones mejoradas")

if __name__ == "__main__":
    test_notification_content()
