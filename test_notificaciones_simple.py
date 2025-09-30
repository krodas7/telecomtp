#!/usr/bin/env python3
"""
Script para mostrar las notificaciones mejoradas de anticipos
"""

def mostrar_notificaciones_mejoradas():
    """Mostrar las notificaciones mejoradas de anticipos"""
    print("🔔 NOTIFICACIONES MEJORADAS DE ANTICIPOS")
    print("=" * 60)
    
    # Datos de ejemplo
    cliente = "Constructora Maya S.A."
    proyecto = "Torre Residencial Vista Hermosa"
    monto = 150000.00
    monto_aplicar = 75000.00
    
    print(f"📊 Datos de ejemplo:")
    print(f"  Cliente: {cliente}")
    print(f"  Proyecto: {proyecto}")
    print(f"  Monto: Q{monto:,.2f}")
    print(f"  Monto a aplicar: Q{monto_aplicar:,.2f}")
    
    print(f"\n🔔 NOTIFICACIONES MEJORADAS:")
    print("=" * 40)
    
    # Notificación de creación
    print("1️⃣ CREACIÓN DE ANTICIPO:")
    notificacion_creacion = (
        f'✅ <strong>Anticipo creado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{monto:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{proyecto}</strong><br>'
        f'👤 Cliente: <strong>{cliente}</strong>'
    )
    print(notificacion_creacion)
    
    # Notificación de aplicación al proyecto
    print(f"\n2️⃣ APLICACIÓN AL PROYECTO:")
    notificacion_aplicacion = (
        f'✅ <strong>Anticipo aplicado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{monto_aplicar:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{proyecto}</strong><br>'
        f'👤 Cliente: <strong>{cliente}</strong>'
    )
    print(notificacion_aplicacion)
    
    # Notificación de aplicación a factura
    print(f"\n3️⃣ APLICACIÓN A FACTURA:")
    notificacion_factura = (
        f'✅ <strong>Anticipo aplicado a factura</strong><br>'
        f'💰 Monto: <strong>Q{monto_aplicar:,.2f}</strong><br>'
        f'📄 Factura: <strong>FAC-2024-001</strong><br>'
        f'🏗️ Proyecto: <strong>{proyecto}</strong>'
    )
    print(notificacion_factura)
    
    # Notificación de actualización
    print(f"\n4️⃣ ACTUALIZACIÓN DE ANTICIPO:")
    notificacion_actualizacion = (
        f'✅ <strong>Anticipo actualizado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{monto:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{proyecto}</strong><br>'
        f'👤 Cliente: <strong>{cliente}</strong>'
    )
    print(notificacion_actualizacion)
    
    # Notificación de eliminación
    print(f"\n5️⃣ ELIMINACIÓN DE ANTICIPO:")
    notificacion_eliminacion = (
        f'🗑️ <strong>Anticipo eliminado exitosamente</strong><br>'
        f'💰 Monto: <strong>Q{monto:,.2f}</strong><br>'
        f'🏗️ Proyecto: <strong>{proyecto}</strong><br>'
        f'👤 Cliente: <strong>{cliente}</strong>'
    )
    print(notificacion_eliminacion)
    
    print(f"\n" + "=" * 60)
    print("✅ NOTIFICACIONES MEJORADAS IMPLEMENTADAS")
    print("=" * 60)
    print("🎯 MEJORAS IMPLEMENTADAS:")
    print("  ✅ Emojis para mejor visualización")
    print("  ✅ Información detallada (monto, proyecto, cliente)")
    print("  ✅ Formato HTML para mejor presentación")
    print("  ✅ Formato de moneda con separadores de miles")
    print("  ✅ Información contextual relevante")
    print("  ✅ Notificaciones más informativas y atractivas")
    
    print(f"\n🌐 Para probar en el navegador:")
    print("  1. Ve a: http://localhost:8000/")
    print("  2. Inicia sesión con: admin / admin123")
    print("  3. Ve a Anticipos")
    print("  4. Crea, edita o aplica un anticipo")
    print("  5. Observa las notificaciones mejoradas")
    
    print(f"\n💡 COMPARACIÓN:")
    print("  ❌ ANTES: 'Anticipo aplicado exitosamente al proyecto Torre Residencial Vista Hermosa'")
    print("  ✅ AHORA: Notificación con emojis, formato HTML y información detallada")

if __name__ == "__main__":
    mostrar_notificaciones_mejoradas()
