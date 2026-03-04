"""
Script simple para exportar un PDF de un reporte específico
Uso: python exportar_pdf_simple.py [DOC_ID]
O ejecutar directamente y pedir el ID
"""

import sys
import os
from exportar_reportes import generar_pdf_routers_tigo

def exportar_por_id(doc_id=None, nombre_salida=None):
    """Exportar PDF por ID de documento"""
    
    # Si no se proporciona ID, pedirlo
    if not doc_id:
        print("\n" + "="*60)
        print("📄 EXPORTADOR SIMPLE DE REPORTES")
        print("="*60 + "\n")
        doc_id = input("Ingresa el ID del documento a exportar: ").strip()
        
        if not doc_id:
            print("❌ Error: Debes proporcionar un ID de documento")
            return
    
    # Generar nombre de archivo si no se proporciona
    if not nombre_salida:
        nombre_salida = f"reporte_{doc_id[:20]}.pdf"
    
    print(f"\n📝 Exportando documento: {doc_id}")
    print(f"📄 Archivo de salida: {nombre_salida}")
    print("⏳ Generando PDF...\n")
    
    # Obtener directorio raíz del script (donde está firebase-credentials.json)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    dir_actual = os.getcwd()
    
    # Cambiar al directorio raíz para que encuentre las credenciales
    os.chdir(script_dir)
    
    # Cambiar al directorio de plantillas si existe
    plantillas_dir = os.path.join(script_dir, 'plantillas')
    
    if os.path.exists(plantillas_dir):
        os.chdir(plantillas_dir)
        archivo_completo = os.path.join('..', nombre_salida)
    else:
        archivo_completo = os.path.join(script_dir, nombre_salida)
    
    try:
        # Cambiar temporalmente al directorio raíz para cargar credenciales
        os.chdir(script_dir)
        
        # Generar PDF
        generar_pdf_routers_tigo(doc_id, archivo_completo)
        
        print(f"\n✅ ¡PDF generado exitosamente!")
        print(f"📂 Ubicación: {os.path.abspath(archivo_completo)}\n")
        
    except Exception as e:
        print(f"\n❌ Error al generar PDF: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Volver al directorio original
        os.chdir(dir_actual)

if __name__ == "__main__":
    # Si se pasa ID como argumento
    if len(sys.argv) > 1:
        doc_id = sys.argv[1]
        nombre_salida = sys.argv[2] if len(sys.argv) > 2 else None
        exportar_por_id(doc_id, nombre_salida)
    else:
        # Modo interactivo
        exportar_por_id()
