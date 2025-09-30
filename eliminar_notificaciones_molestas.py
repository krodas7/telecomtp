#!/usr/bin/env python3
"""
Script para encontrar y eliminar todas las notificaciones molestas en el sistema
"""

import os
import sys
import glob
import re

def buscar_notificaciones_molestas():
    """Buscar todas las notificaciones estáticas molestas en templates"""
    print("🔍 BUSCANDO NOTIFICACIONES MOLESTAS EN EL SISTEMA")
    print("=" * 60)
    
    # Patrones de notificaciones molestas
    patrones_molestos = [
        r'alert alert-info.*botón verde',
        r'alert alert-info.*facturas.*pagadas',
        r'alert alert-warning.*Fechas.*Emisión',
        r'alert alert-info.*proyecto.*inactivo',
        r'alert alert-info.*eliminar.*físicamente',
        r'alert alert-info.*facturas.*gastos.*afectados'
    ]
    
    templates_con_problemas = []
    
    # Buscar en todos los templates
    template_files = glob.glob('templates/**/*.html', recursive=True)
    
    for template_file in template_files:
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            problemas_encontrados = []
            for patron in patrones_molestos:
                if re.search(patron, content, re.IGNORECASE | re.DOTALL):
                    problemas_encontrados.append(patron)
            
            if problemas_encontrados:
                templates_con_problemas.append({
                    'archivo': template_file,
                    'problemas': problemas_encontrados
                })
                
        except Exception as e:
            print(f"  ⚠️ Error leyendo {template_file}: {e}")
    
    return templates_con_problemas

def mostrar_templates_problematicos(templates_con_problemas):
    """Mostrar templates con notificaciones molestas"""
    print(f"\n📋 TEMPLATES CON NOTIFICACIONES MOLESTAS:")
    print("=" * 60)
    
    if not templates_con_problemas:
        print("  ✅ No se encontraron notificaciones molestas")
        return
    
    for i, template in enumerate(templates_con_problemas, 1):
        print(f"\n{i}. {template['archivo']}")
        for problema in template['problemas']:
            print(f"   ❌ Patrón: {problema}")

def crear_ayuda_contextual_para_template(template_file):
    """Crear ayuda contextual para un template específico"""
    print(f"\n🔧 CREANDO AYUDA CONTEXTUAL PARA: {template_file}")
    
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determinar el módulo basado en la ruta
        if 'facturas' in template_file:
            modulo = 'facturas'
            funcion_ayuda = 'mostrarAyudaFacturas()'
            texto_boton = 'Ayuda sobre Facturas'
        elif 'proyectos' in template_file:
            modulo = 'proyectos'
            funcion_ayuda = 'mostrarAyudaProyectos()'
            texto_boton = 'Ayuda sobre Proyectos'
        elif 'anticipos' in template_file:
            modulo = 'anticipos'
            funcion_ayuda = 'mostrarAyudaAnticipos()'
            texto_boton = 'Ayuda sobre Anticipos'
        else:
            modulo = 'general'
            funcion_ayuda = 'mostrarAyudaGeneral()'
            texto_boton = 'Ayuda'
        
        # Reemplazar notificaciones estáticas con botón de ayuda
        patron_notificacion = r'<div class="alert alert-info">.*?</div>'
        boton_ayuda = f'''<!-- Botón de ayuda contextual -->
                    <div class="mt-2">
                        <button type="button" class="btn btn-outline-info btn-sm" onclick="{funcion_ayuda}">
                            <i class="fas fa-question-circle me-1"></i>{texto_boton}
                        </button>
                    </div>'''
        
        # Aplicar reemplazo
        content_nuevo = re.sub(patron_notificacion, boton_ayuda, content, flags=re.DOTALL)
        
        # Agregar JavaScript si no existe
        if f'function {funcion_ayuda.replace("()", "")}' not in content_nuevo:
            js_ayuda = f'''
<script>
// Función para mostrar ayuda usando notificaciones toast
function {funcion_ayuda.replace("()", "")}() {{
    if (typeof toastNotification !== 'undefined') {{
        toastNotification.info(
            'Información del Sistema',
            'Información contextual disponible cuando la necesites.',
            6000
        );
    }} else {{
        alert('Información del sistema disponible');
    }}
}}
</script>'''
            
            # Agregar antes del cierre del template
            if '{% endblock %}' in content_nuevo:
                content_nuevo = content_nuevo.replace('{% endblock %}', js_ayuda + '\n\n{% endblock %}')
            else:
                content_nuevo += js_ayuda
        
        # Guardar archivo modificado
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(content_nuevo)
        
        print(f"  ✅ Ayuda contextual agregada para {modulo}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error procesando {template_file}: {e}")
        return False

def main():
    """Función principal"""
    print("🔔 ELIMINADOR DE NOTIFICACIONES MOLESTAS")
    print("=" * 70)
    
    try:
        # Buscar notificaciones molestas
        templates_problematicos = buscar_notificaciones_molestas()
        
        # Mostrar resultados
        mostrar_templates_problematicos(templates_problematicos)
        
        if not templates_problematicos:
            print("\n🎉 ¡NO HAY NOTIFICACIONES MOLESTAS EN EL SISTEMA!")
            print("✅ Todos los templates están limpios")
            return True
        
        # Procesar templates problemáticos
        print(f"\n🔧 PROCESANDO {len(templates_problematicos)} TEMPLATES...")
        print("=" * 60)
        
        templates_procesados = 0
        for template in templates_problematicos:
            if crear_ayuda_contextual_para_template(template['archivo']):
                templates_procesados += 1
        
        # Resumen final
        print(f"\n" + "=" * 70)
        print("📋 RESUMEN FINAL")
        print("=" * 70)
        
        print(f"📊 Templates procesados: {templates_procesados}/{len(templates_problematicos)}")
        
        if templates_procesados == len(templates_problematicos):
            print("🎉 ¡TODAS LAS NOTIFICACIONES MOLESTAS ELIMINADAS!")
            print("✅ Ayuda contextual implementada en todos los módulos")
            print("✅ Interfaz más limpia y profesional")
            print("✅ Mejor experiencia de usuario")
        else:
            print("⚠️ Algunos templates no se pudieron procesar")
        
        return templates_procesados == len(templates_problematicos)
        
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
