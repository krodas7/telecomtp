
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from firebase_config import init_firestore
import os
import textwrap
import requests
import uuid
import time

# Debug: guardar copias de imágenes descargadas para verificación visual
DEBUG_SAVE_IMAGES = True

def insertar_imagen_remota(canvas_obj, url, x, y, width, height, nombre_campo="imagen", debug_dir=None):
    """
    Descarga una imagen remota y la inserta en el canvas del PDF.
    Usa nombres únicos y fuerza la recarga para evitar caché.
    """
    if not url or not url.startswith("http"):
        return
    
    # Generar nombre único con timestamp y campo
    nombre_temp = f"temp_{nombre_campo}_{uuid.uuid4().hex}_{int(time.time()*1000)}.jpg"
    
    try:
        # Descargar imagen con headers para evitar caché
        headers = {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        response = requests.get(url, timeout=15, headers=headers)
        
        if response.ok:
            # Guardar temporalmente
            with open(nombre_temp, "wb") as f:
                f.write(response.content)
            
            # Forzar flush del sistema de archivos
            os.sync() if hasattr(os, 'sync') else None
            
            # Esperar un poco para asegurar que el archivo esté listo
            time.sleep(0.05)
            
            # Guardar copia de depuración si aplica
            try:
                if DEBUG_SAVE_IMAGES and debug_dir:
                    os.makedirs(debug_dir, exist_ok=True)
                    copia_path = os.path.join(debug_dir, f"{nombre_campo}.jpg")
                    # Evitar sobrescribir: agregar sufijo incremental
                    idx = 1
                    base, ext = os.path.splitext(copia_path)
                    while os.path.exists(copia_path):
                        copia_path = f"{base}_{idx}{ext}"
                        idx += 1
                    with open(copia_path, "wb") as fc:
                        fc.write(response.content)
            except Exception as dbg_err:
                print(f"   ⚠️  Debug save fallo para {nombre_campo}: {dbg_err}")

            # Crear ImageReader directamente desde el archivo
            # No reutilizar objetos ImageReader para evitar caché
            img = ImageReader(nombre_temp)
            canvas_obj.drawImage(img, x, y, width=width, height=height, mask='auto')
            
            # Limpiar inmediatamente después de insertar
            try:
                img = None  # Liberar referencia
                if os.path.exists(nombre_temp):
                    os.remove(nombre_temp)
            except Exception as cleanup_error:
                print(f"   ⚠️  Error al limpiar {nombre_temp}: {cleanup_error}")
        else:
            print(f"   ⚠️  HTTP {response.status_code} para {nombre_campo}")
            
    except Exception as e:
        print(f"   ❌ Error en {nombre_campo}: {e}")
        # Limpiar archivo temporal en caso de error
        if os.path.exists(nombre_temp):
            try:
                os.remove(nombre_temp)
            except:
                pass

def _get_templates_base_dir():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "reportes_templates", "routers_nokia")


def generar_pdf_routers_tigo(doc_id, salida_pdf, data=None, templates_dir=None, debug_save_images=None):
    global DEBUG_SAVE_IMAGES
    if data is None:
        db = init_firestore()
        doc_ref = db.collection("instalacionesRoutersTigo").document(doc_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            print(f" Documento {doc_id} no encontrado.")
            return

        datos = doc.to_dict()
    else:
        datos = data
    c = canvas.Canvas(salida_pdf, pagesize=letter)
    width, height = letter

    templates_dir = templates_dir or _get_templates_base_dir()
    original_debug_setting = DEBUG_SAVE_IMAGES
    if debug_save_images is not None:
        DEBUG_SAVE_IMAGES = debug_save_images

    # Carpeta de depuración por documento
    debug_dir = None
    if DEBUG_SAVE_IMAGES:
        try:
            base_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
            debug_dir = os.path.join(base_dir, f"imagenes_debug_{doc_id}")
        except Exception:
            debug_dir = os.path.join(os.getcwd(), f"imagenes_debug_{doc_id}")

    # Página 1 - router1
    fondo = os.path.join(templates_dir, "router1.jpg")
    if os.path.exists(fondo):
        c.drawImage(ImageReader(fondo), 0, 0, width=width, height=height)
    else:
        print(" Imagen router1.jpg no encontrada")

    c.setFont("Helvetica", 8)
    c.drawString(5.4 * cm, 24.07 * cm, datos.get("autor", ""))
    c.drawString(16.72 * cm, 24.07 * cm, datos.get("fecha", ""))
    c.drawString(16.72 * cm, 23.29 * cm, datos.get("reporte", ""))
    c.drawString(5.4 * cm, 23.29 * cm, datos.get("contratista", ""))
    c.drawString(5.4 * cm, 22.38 * cm, datos.get("nombreSitio", ""))
    c.drawString(15.3 * cm, 24.75 * cm, datos.get("coordenadas", ""))
    c.drawString(5.4 * cm, 21.47 * cm, datos.get("ID", ""))
    #c.drawString(16.72 * cm, 21.47 * cm, datos.get("MDIUtilizado", ""))
    c.drawString(16.72 * cm, 22.38 * cm, datos.get("latitud", ""))
    c.drawString(18.72 * cm, 22.38 * cm, datos.get("longitud", ""))
    c.drawString(5.4 * cm, 20.63 * cm, datos.get("ubicacionEquipo", ""))
    c.drawString(16.72 * cm, 20.63 * cm, datos.get("protocolo", ""))
    c.drawString(16.72 * cm, 19.78 * cm, datos.get("Coordinador", ""))
    
    #split MDI
    # Texto a imprimir
    texto_mdi = datos.get("MDIUtilizado", "")
    lineas = textwrap.wrap(texto_mdi, width=30)  # Ajusta width según el espacio disponible

   # Establecer fuente más pequeña
    c.setFont("Helvetica", 7)

   # Imprimir hasta 2 líneas
    if len(lineas) > 0:
     c.drawString(16.72 * cm, 21.47 * cm, lineas[0])
    if len(lineas) > 1:
     c.drawString(16.72 * cm, 21.1 * cm, lineas[1])  # un poco más abajo (ajusta si hace falta)

    fuenteA = datos.get("condicionesElectricas", {}).get("fuenteA", {})
    c.drawString(5.4 * cm, 19.78 * cm, fuenteA.get("identificacionEquipo", ""))

    fotos = datos.get("fotografias", {})

    def _foto_from_aliases(fotos_dict, aliases):
        for k in aliases:
            v = fotos_dict.get(k)
            if v:
                return v
        return ""

    # Orden solicitado para página 1 (6 imágenes):
    # 1: gabineteGeneral, 2: ubicacion, 3: serie
    # 4: etiquetaRouterNuevo, 5: etiquetaFibra1, 6: etiquetaFibra2
    page1_slots = [
        ("gabineteGeneral", ["gabineteGeneral"], 2.0, 14.1),
        ("ubicacion", ["ubicacion"], 8.4, 14.1),
        ("serie", ["serie"], 14.8, 14.1),
        ("etiquetaRouterNuevo", ["etiquetaRouterNuevo"], 2.0, 7.7),
        ("etiquetaFibra1", ["etiquetaFibra1", "etiqueteFibra1"], 8.4, 7.7),
        ("etiquetaFibra2", ["etiquetaFibra2", "etiqeutaFibra2"], 14.8, 7.7),
    ]
    print("📄 Página 1 - Descargando imágenes...")
    for nombre_campo, alias_list, x, y in page1_slots:
        url = _foto_from_aliases(fotos, alias_list)
        if url and url.startswith("http"):
            suf = url.split("/")[-1][:24]
            print(f"   ⬇️  {nombre_campo} -> {suf}... ", end="", flush=True)
            insertar_imagen_remota(c, url, x * cm, y * cm, 4.5 * cm, 4.5 * cm, nombre_campo, debug_dir)
            print("✓")
    c.showPage()

    # Página 2 - router2
    ruta_imagen = os.path.join(templates_dir, "router2.jpg")
    if os.path.exists(ruta_imagen):
        c.drawImage(ImageReader(ruta_imagen), 0, 0, width=width, height=height)

    # Orden solicitado para página 2 (8 imágenes):
    # 7: etiquetaEnergia, 8: breaker, 9: etiquetaDCDU
    # 10: conexionTierraSwitch, 11: etiquetaTierra, 12: conexionTierraPlatina
    # 13: etiquetaODFConectante, 14: etiquetaSwitchConectante
    page2_slots = [
        ("etiquetaEnergia", ["etiquetaEnergia"], 2.0, 21.3),
        ("breaker", ["breaker"], 8.4, 21.3),
        ("etiquetaDCDU", ["etiquetaDCDU"], 14.8, 21.3),
        ("conexionTierraSwitch", ["conexionTierraSwitch"], 2.0, 14.9),
        ("etiquetaTierra", ["etiquetaTierra"], 8.4, 14.9),
        ("conexionTierraPlatina", ["conexionTierraPlatina"], 14.8, 14.9),
        ("etiquetaODFConectante", ["etiquetaODFConectante", "etiquetaODFSitioConectante"], 2.0, 8.5),
        ("etiquetaSwitchConectante", ["etiquetaSwitchConectante", "etiquetaSwitchSitioConectante"], 8.4, 8.5),
    ]
    print("📄 Página 2 - Descargando imágenes...")
    for nombre_campo, alias_list, x, y in page2_slots:
        url = _foto_from_aliases(fotos, alias_list)
        if url and url.startswith("http"):
            suf = url.split("/")[-1][:24]
            print(f"   ⬇️  {nombre_campo} -> {suf}... ", end="", flush=True)
            insertar_imagen_remota(c, url, x * cm, y * cm, 4.5 * cm, 4.5 * cm, nombre_campo, debug_dir)
            print("✓")
    c.showPage()

    # Página 3 - router3
    fondo_r3 = os.path.join(templates_dir, "router3.jpg")
    if os.path.exists(fondo_r3):
        c.drawImage(ImageReader(fondo_r3), 0, 0, width=width, height=height)

    c.setFont("Helvetica", 8)
    fuenteB = datos.get("condicionesElectricas", {}).get("fuenteB", {})
    x_coords = [5.7 * cm, 9 * cm, 12.5 * cm, 16 * cm]
    y_filaA = 19.5 * cm
    y_filaB = 18 * cm
    filaA = [
        str(fuenteA.get("calibreCable", "")),
        fuenteA.get("capacidadBreaker", ""),
        fuenteA.get("identificacionEquipo", ""),
        fuenteA.get("identificacionRectificador", ""),
    ]
    filaB = [
        str(fuenteB.get("calibreCable", "")),
        fuenteB.get("capacidadBreaker", ""),
        fuenteB.get("identificacionEquipo", ""),
        fuenteB.get("identificacionRectificador", ""),
    ]
    for i, valor in enumerate(filaA):
        c.drawString(x_coords[i], y_filaA, valor)
    for i, valor in enumerate(filaB):
        c.drawString(x_coords[i], y_filaB, valor)
    c.showPage()

    # Página 4 - router4
    fondo_r4 = os.path.join(templates_dir, "router4.jpg")
    if os.path.exists(fondo_r4):
        c.drawImage(ImageReader(fondo_r4), 0, 0, width=width, height=height)

    c.setFont("Helvetica", 7)
    inventario = datos.get("inventario", [])
    x_cols = [2.7 * cm, 8 * cm, 12.6 * cm, 17.3 * cm]
    y_start = 21.7 * cm
    row_height = 0.60 * cm
    for i, item in enumerate(inventario[:23]):
        y = y_start - (i * row_height)
        fila = [
            str(item.get("descripcion", "")),
            str(item.get("noParte", "")),
            str(item.get("noSerie", "")),
            str(item.get("posicion", "")),
        ]
        for j, valor in enumerate(fila):
            c.drawString(x_cols[j], y, valor)
    c.showPage()

    # Página 5 - router5
    fondo_r5 = os.path.join(templates_dir, "router5.jpg")
    if os.path.exists(fondo_r5):
        c.drawImage(ImageReader(fondo_r5), 0, 0, width=width, height=height)

    c.setFont("Helvetica", 7)
    fibra = datos.get("posicionFO", [])
    # 5 columnas: desde - puertoDesde - hacia - puertoHacia - servicio
    x_cols = [1.9 * cm, 6.3 * cm, 8.7 * cm, 13.1 * cm, 15.5 * cm]
    y_inicio = 22.2 * cm
    salto_fila = 0.60 * cm
    for i, item in enumerate(fibra[:20]):
        y = y_inicio - i * salto_fila
        fila = [
            item.get("desde", ""),
            item.get("puertoDesde", ""),
            item.get("hacia", ""),
            item.get("puertoHacia", ""),
            item.get("servicio", ""),
        ]
        for j, valor in enumerate(fila):
            c.drawString(x_cols[j], y, str(valor))
    c.showPage()

    c.save()
    print(f"✅ PDF generado correctamente: {salida_pdf}")
    if debug_save_images is not None:
        DEBUG_SAVE_IMAGES = original_debug_setting

def listar_reportes_disponibles():
    """Lista todos los reportes disponibles en Firebase"""
    db = init_firestore()
    coleccion = db.collection("instalacionesRoutersTigo")
    docs = coleccion.stream()
    
    reportes = []
    for doc in docs:
        datos = doc.to_dict()
        reportes.append({
            'id': doc.id,
            'nombreSitio': datos.get('nombreSitio', 'Sin nombre'),
            'reporte': datos.get('reporte', 'N/A'),
            'fecha': datos.get('fecha', 'N/A'),
            'ID': datos.get('ID', 'N/A')
        })
    
    return reportes

def menu_interactivo():
    """Menú interactivo para seleccionar y exportar reportes"""
    # Configurar encoding UTF-8 para Windows
    import sys
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    
    print("\n" + "="*60)
    print("📊 EXPORTADOR DE REPORTES ROUTERS TIGO")
    print("="*60 + "\n")
    
    print("🔄 Conectando a Firebase y cargando reportes...")
    
    try:
        reportes = listar_reportes_disponibles()
        
        if not reportes:
            print("\n⚠️  No se encontraron reportes en Firebase.")
            return
        
        print(f"\n✅ Se encontraron {len(reportes)} reportes disponibles:\n")
        
        # Mostrar lista de reportes
        for i, reporte in enumerate(reportes, 1):
            print(f"{i}. 📍 {reporte['nombreSitio']}")
            print(f"   ID Sitio: {reporte['ID']}")
            print(f"   Reporte: {reporte['reporte']}")
            print(f"   Fecha: {reporte['fecha']}")
            print(f"   Doc ID: {reporte['id']}")
            print()
        
        # Selección del reporte
        while True:
            try:
                seleccion = input(f"Selecciona el número del reporte a exportar (1-{len(reportes)}) o 'q' para salir: ").strip()
                
                if seleccion.lower() == 'q':
                    print("\n👋 Saliendo...")
                    return
                
                num = int(seleccion)
                if 1 <= num <= len(reportes):
                    reporte_seleccionado = reportes[num - 1]
                    break
                else:
                    print(f"❌ Por favor ingresa un número entre 1 y {len(reportes)}")
            except ValueError:
                print("❌ Por favor ingresa un número válido")
        
        # Generar nombre del archivo de salida
        nombre_sitio_limpio = reporte_seleccionado['nombreSitio'].replace(' ', '_').replace('/', '_')
        nombre_salida = f"reporte_{nombre_sitio_limpio}_{reporte_seleccionado['id'][:8]}.pdf"
        
        print(f"\n📝 Generando PDF para: {reporte_seleccionado['nombreSitio']}")
        print(f"📄 Archivo de salida: {nombre_salida}")
        print("⏳ Por favor espera...\n")
        
        # Generar el PDF usando plantillas centralizadas
        dir_actual = os.getcwd()
        templates_dir = _get_templates_base_dir()
        salida_path = os.path.join(dir_actual, nombre_salida)
        generar_pdf_routers_tigo(
            reporte_seleccionado['id'],
            salida_path,
            templates_dir=templates_dir
        )
        
        print(f"\n🎉 ¡Exportación completada! El archivo se guardó como: {nombre_salida}\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    menu_interactivo()
