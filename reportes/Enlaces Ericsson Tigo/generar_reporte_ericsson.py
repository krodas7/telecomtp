
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from firebase_config import init_firestore
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
import os
from PIL import Image as PilImage
from PIL import ImageOps
import requests
from io import BytesIO



def _get_templates_base_dir():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "reportes_templates", "enlaces_ericsson")


def buscar_plantilla(nombre_archivo):
    """
    Busca una plantilla en múltiples ubicaciones posibles.
    
    Args:
        nombre_archivo: Nombre del archivo de plantilla (ej: "r1.jpg")
    
    Returns:
        Ruta completa del archivo si se encuentra, None si no existe
    """
    templates_dir = _get_templates_base_dir()
    # Lista de ubicaciones posibles
    ubicaciones = [
        nombre_archivo,  # Directorio actual
        os.path.join("plantillas", nombre_archivo),  # Subdirectorio plantillas
        os.path.join("ReporteEricsson", nombre_archivo),  # Si se ejecuta desde raíz
        os.path.join("ReporteEricsson", "plantillas", nombre_archivo),  # Combinación
        os.path.join(templates_dir, nombre_archivo),  # Nuevo directorio centralizado
    ]
    
    for ruta in ubicaciones:
        if os.path.exists(ruta):
            return ruta
    
    return ""


def comprimir_plantilla(ruta_original):
    """
    Comprime una plantilla local y retorna la ruta del archivo comprimido.
    
    Args:
        ruta_original: Ruta del archivo de plantilla original
    
    Returns:
        Ruta del archivo comprimido temporal, o None si falla
    """
    if not ruta_original or not os.path.exists(ruta_original):
        return None
    
    try:
        # Crear nombre para archivo comprimido temporal
        nombre_base = os.path.basename(ruta_original)
        nombre_comprimido = f"temp_compressed_{nombre_base}"
        
        # Abrir imagen con PIL
        img = PilImage.open(ruta_original)
        
        # Convertir a RGB si es necesario (para JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            # Crear fondo blanco para imágenes con transparencia
            fondo = PilImage.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            fondo.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = fondo
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Calcular dimensiones máximas (1024px manteniendo proporción)
        max_dimension = 1024
        if img.width > max_dimension or img.height > max_dimension:
            ratio = min(max_dimension / img.width, max_dimension / img.height)
            new_width = int(img.width * ratio)
            new_height = int(img.height * ratio)
            img = img.resize((new_width, new_height), PilImage.Resampling.LANCZOS)
        
        # Guardar con compresión JPEG (calidad 50 - balance entre calidad y tamaño)
        img.save(nombre_comprimido, 'JPEG', quality=50, optimize=True)
        
        return nombre_comprimido
    
    except Exception as e:
        print(f"⚠️ Error al comprimir plantilla {ruta_original}: {e}")
        return None


def insertar_plantilla_comprimida(canvas_obj, ruta_imagen, ancho, alto):
    """
    Inserta una plantilla comprimida en el PDF.
    
    Args:
        canvas_obj: Objeto canvas de ReportLab
        ruta_imagen: Ruta de la plantilla original
        ancho: Ancho de la página
        alto: Alto de la página
    """
    if not ruta_imagen:
        return
    
    ruta_comprimida = comprimir_plantilla(ruta_imagen)
    if ruta_comprimida:
        try:
            canvas_obj.drawImage(ImageReader(ruta_comprimida), 0, 0, width=ancho, height=alto)
        finally:
            # Limpiar archivo temporal comprimido
            if os.path.exists(ruta_comprimida):
                try:
                    os.remove(ruta_comprimida)
                except:
                    pass
    else:
        # Si falla la compresión, usar original
        canvas_obj.drawImage(ImageReader(ruta_imagen), 0, 0, width=ancho, height=alto)


def insertar_imagen_remota(canvas_obj, url, x, y, width=None, height=None, nombre_temp="temp_img.jpg"):
    """
    Descarga e inserta una imagen remota en el PDF.
    
    Args:
        canvas_obj: Objeto canvas de ReportLab
        url: URL de la imagen a descargar
        x, y: Posición en el PDF
        width, height: Dimensiones de la imagen
        nombre_temp: Nombre temporal del archivo
    """
    if not url or not url.startswith("http"):
        return
    
    try:
        # Agregar timeout para evitar que se cuelgue (10 segundos de conexión, 30 segundos total)
        response = requests.get(url, timeout=(10, 30), stream=True)
        
        if response.ok:
            # Verificar que sea una imagen válida
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                print(f"⚠️ URL no es una imagen: {url} (Content-Type: {content_type})")
                return
            
            # Descargar contenido en chunks para manejar archivos grandes
            with open(nombre_temp, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            # Verificar que el archivo se descargó correctamente
            if os.path.exists(nombre_temp) and os.path.getsize(nombre_temp) > 0:
                # Comprimir y optimizar la imagen antes de insertarla
                nombre_comprimido = nombre_temp.replace(".jpg", "_compressed.jpg")
                try:
                    # Abrir imagen con PIL
                    img = PilImage.open(nombre_temp)
                    
                    # Convertir a RGB si es necesario (para JPEG)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        # Crear fondo blanco para imágenes con transparencia
                        fondo = PilImage.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        fondo.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                        img = fondo
                    elif img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Calcular dimensiones máximas (1024px manteniendo proporción)
                    max_dimension = 1024
                    if img.width > max_dimension or img.height > max_dimension:
                        ratio = min(max_dimension / img.width, max_dimension / img.height)
                        new_width = int(img.width * ratio)
                        new_height = int(img.height * ratio)
                        img = img.resize((new_width, new_height), PilImage.Resampling.LANCZOS)
                    
                    # Guardar con compresión JPEG (calidad 50 - balance entre calidad y tamaño)
                    img.save(nombre_comprimido, 'JPEG', quality=50, optimize=True)
                    
                    # Eliminar imagen original
                    os.remove(nombre_temp)
                    
                    # Usar la imagen comprimida
                    canvas_obj.drawImage(ImageReader(nombre_comprimido), x, y, width=width, height=height)
                    os.remove(nombre_comprimido)
                    
                except Exception as e:
                    # Si falla la compresión, intentar con la imagen original
                    print(f"⚠️ Error al comprimir imagen, usando original: {url} - {e}")
                    try:
                        canvas_obj.drawImage(ImageReader(nombre_temp), x, y, width=width, height=height)
                    except:
                        pass
                    finally:
                        if os.path.exists(nombre_temp):
                            os.remove(nombre_temp)
                        if os.path.exists(nombre_comprimido):
                            try:
                                os.remove(nombre_comprimido)
                            except:
                                pass
            else:
                print(f"⚠️ Imagen descargada está vacía: {url}")
        else:
            print(f"⚠️ Error HTTP {response.status_code} al descargar: {url}")
    
    except requests.exceptions.Timeout:
        print(f"⏱️ Timeout al descargar imagen (demasiado lenta): {url}")
    except requests.exceptions.ConnectionError:
        print(f"🔌 Error de conexión al descargar: {url}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al descargar imagen: {url} - {e}")
    except KeyboardInterrupt:
        print(f"⚠️ Descarga interrumpida por el usuario: {url}")
        # Limpiar archivo temporal si existe
        if os.path.exists(nombre_temp):
            try:
                os.remove(nombre_temp)
            except:
                pass
        raise  # Re-lanzar para que el usuario sepa que fue interrumpido
    except Exception as e:
        print(f"❌ Error inesperado al insertar imagen remota: {url} - {type(e).__name__}: {e}")
        # Limpiar archivo temporal si existe
        if os.path.exists(nombre_temp):
            try:
                os.remove(nombre_temp)
            except:
                pass


def obtener_antenas(sitio_torre, cantidad_antenas):
    """
    Obtiene las antenas del sitio con compatibilidad hacia atrás.
    Busca primero campos numerados (estructura nueva), luego campos antiguos.
    
    Args:
        sitio_torre: Diccionario con datos de SiteATorre o SiteBTorre
        cantidad_antenas: Cantidad de antenas esperadas (1-4)
    
    Returns:
        Lista de diccionarios con datos de antenas: [{"numero": 1, "fijacionAntena": url, "SerieAntena": url}, ...]
    """
    antenas = []
    
    # Intentar leer estructura nueva primero (campos numerados)
    for i in range(1, cantidad_antenas + 1):
        fijacion = sitio_torre.get(f"fijacionAntena{i}", "").strip()
        serie = sitio_torre.get(f"SerieAntena{i}", "").strip()
        
        if fijacion or serie:
            antenas.append({
                "numero": i,
                "fijacionAntena": fijacion,
                "SerieAntena": serie
            })
    
    # Si no hay antenas numeradas, intentar estructura antigua (compatibilidad)
    if not antenas:
        fijacion_antigua = sitio_torre.get("fijacionAntena", "").strip()
        serie_antigua = sitio_torre.get("SerieAntena", "").strip()
        
        if fijacion_antigua or serie_antigua:
            antenas.append({
                "numero": 1,
                "fijacionAntena": fijacion_antigua,
                "SerieAntena": serie_antigua
            })
    
    return antenas


def obtener_odus(sitio_torre, cantidad_odus):
    """
    Obtiene las ODUs del sitio con compatibilidad hacia atrás.
    Busca primero campos numerados (estructura nueva), luego campos antiguos.
    
    Args:
        sitio_torre: Diccionario con datos de SiteATorre o SiteBTorre
        cantidad_odus: Cantidad de ODUs esperadas (1-8)
    
    Returns:
        Lista de diccionarios con datos de ODUs: [{"numero": 1, "ConexionOdu": url, "etiquetaRadio": url, "serieOdu": url, "aterrizajeOdu": url}, ...]
    """
    odus = []
    
    # Intentar leer estructura nueva primero (campos numerados)
    for i in range(1, cantidad_odus + 1):
        # Buscar con mayúscula (estructura nueva)
        conexion = sitio_torre.get(f"ConexionOdu{i}", "").strip()
        # Si no existe con mayúscula, intentar minúscula (solo para i=1, compatibilidad)
        if not conexion and i == 1:
            conexion = sitio_torre.get("conexionOdu", "").strip()
        
        etiqueta = sitio_torre.get(f"etiquetaRadio{i}", "").strip()
        # Si no existe numerado, intentar sin número (solo para i=1, compatibilidad)
        if not etiqueta and i == 1:
            etiqueta = sitio_torre.get("etiquetaRadio", "").strip()
        
        serie = sitio_torre.get(f"serieOdu{i}", "").strip()
        # serieOdu1 ya existía, pero verificar si hay serieOdu sin número (compatibilidad)
        if not serie and i == 1:
            serie = sitio_torre.get("serieOdu", "").strip()
        
        aterrizaje = sitio_torre.get(f"aterrizajeOdu{i}", "").strip()
        # Si no existe numerado, intentar sin número (solo para i=1, compatibilidad)
        if not aterrizaje and i == 1:
            aterrizaje = sitio_torre.get("aterrizajeOdu", "").strip()
        
        if conexion or etiqueta or serie or aterrizaje:
            odus.append({
                "numero": i,
                "ConexionOdu": conexion,
                "etiquetaRadio": etiqueta,
                "serieOdu": serie,
                "aterrizajeOdu": aterrizaje
            })
    
    # Si no hay ODUs numeradas, intentar estructura antigua completa (compatibilidad)
    if not odus:
        conexion_antigua = sitio_torre.get("conexionOdu", "").strip()
        etiqueta_antigua = sitio_torre.get("etiquetaRadio", "").strip()
        serie_antigua = sitio_torre.get("serieOdu1", "").strip()  # serieOdu1 ya tenía número
        if not serie_antigua:
            serie_antigua = sitio_torre.get("serieOdu", "").strip()
        aterrizaje_antigua = sitio_torre.get("aterrizajeOdu", "").strip()
        
        if conexion_antigua or etiqueta_antigua or serie_antigua or aterrizaje_antigua:
            odus.append({
                "numero": 1,
                "ConexionOdu": conexion_antigua,
                "etiquetaRadio": etiqueta_antigua,
                "serieOdu": serie_antigua,
                "aterrizajeOdu": aterrizaje_antigua
            })
    
    return odus


def generar_pdf_ericsson(document_id, salida_pdf, data=None):
    doc_label = document_id or "sin_id"
    print(f"🔄 Iniciando generación de PDF para documento: {doc_label}")
    print("⏳ Esto puede tardar varios minutos si hay muchas imágenes que descargar...")
    print("   (Puedes presionar Ctrl+C para cancelar si es necesario)\n")

    if data is None:
        db = init_firestore()
        doc_ref = db.collection("reportesEnlacesEricssonTigo").document(document_id)
        doc = doc_ref.get()

        if not doc.exists:
            print(f"⚠️ Documento {document_id} no encontrado.")
            return

        datos = doc.to_dict()
    else:
        datos = data
    datos_generales = datos.get("DatosGenerales", {})
    generales = datos.get("Generales", {})
    
    # Leer cantidades de antenas y ODUs (nuevos campos, default: 1 para compatibilidad)
    cantidad_antenas = datos.get("cantidadAntenas", 1)
    cantidad_odus = datos.get("cantidadOdus", 1)
    
    # Validar rangos
    cantidad_antenas = max(1, min(4, cantidad_antenas))  # Entre 1 y 4
    cantidad_odus = max(1, min(8, cantidad_odus))  # Entre 1 y 8
    
    print(f"📊 Configuración detectada: {cantidad_antenas} antena(s), {cantidad_odus} ODU(s)")

    c = canvas.Canvas(salida_pdf, pagesize=letter)
    ancho, alto = letter

    # Página 1
    ruta_imagen = buscar_plantilla("r1.jpg")
    if ruta_imagen:
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r1.jpg no encontrada en ninguna ubicación")

    c.setFont("Helvetica", 10)
    c.drawString(9.51 * cm, 24.46 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(9.51 * cm, 24.13 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(6.62 * cm, 4.29 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

    url_caratula = generales.get("Caratula", "")
    insertar_imagen_remota(
        c,
        url_caratula,
        x=2.69 * cm,
        y=6.48 * cm,
        width=14 * cm,
        height=16 * cm,
        nombre_temp="caratula_temp.jpg"
    )

    c.showPage()

    # Página 2
    ruta_imagen = buscar_plantilla("r2.jpg")
    if ruta_imagen:
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r2.jpg no encontrada en ninguna ubicación")

    c.setFont("Helvetica", 10)
    c.drawString(9.51 * cm, 24.46 * cm, datos_generales.get("SitioA", ""))
    c.drawString(9.51 * cm, 24.13 * cm, datos_generales.get("SitioB", ""))
    c.showPage()

    # Página 3
    ruta_imagen = buscar_plantilla("r3.jpg")
    if ruta_imagen:
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r3.jpg no encontrada en ninguna ubicación")

    c.setFont("Helvetica", 10)
    c.drawString(3.47 * cm, 24.18 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

    url_path = generales.get("PathCalculator", "")
    insertar_imagen_remota(
        c,
        url_path,
        x=2.69 * cm,
        y=6.48 * cm,
        width=14 * cm,
        height=16 * cm,
        nombre_temp="path_temp.jpg"
    )

    c.showPage()

    # Página 4
    ruta_imagen = buscar_plantilla("r4.jpg")
    if ruta_imagen:
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r4.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(3.14 * cm, 23.12 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')


    url_profile = generales.get("Profile", "")
    insertar_imagen_remota(
        c,
        url_profile,
        x=2.59 * cm,
        y=6.22 * cm,
        width=14 * cm,
        height=14 * cm,
        nombre_temp="profile_temp.jpg"
    )

    c.showPage()  
    
    #PAGINA 5 
    ruta_imagen = buscar_plantilla("r5.jpg")
    if ruta_imagen:
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r5.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10) 
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.52 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_conf1 = site_a.get("configFrec1", "")
    

# Establece solo el ancho
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_conf1,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="conf1_temp.jpg"
) 

    c.showPage()  
    #PAGINA 6 
    ruta_imagen = buscar_plantilla("r6.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r6.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.52 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_conf2 = site_a.get("configFrec2", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16

    insertar_imagen_remota(
    c,
    url_conf2,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="conf2_temp.jpg"
)


    c.showPage()  
    #PAGINA 7  
    ruta_imagen = buscar_plantilla("r7.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r7.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.52 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_conf3 = site_a.get("configFrec3", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_conf3,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="conf3_temp.jpg"
)

    c.showPage()  
    #PAGINA 8  
    ruta_imagen = buscar_plantilla("r8.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r6.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.52 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_conf1b = site_b.get("configFrec1", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_conf1b,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="conf1b_temp.jpg"
)

    c.showPage()  
    #PAGINA 9 
    ruta_imagen = buscar_plantilla("r9.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r6.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.52 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_conf2b = site_b.get("configFrec2", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_conf2b,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="conf2b_temp.jpg"
)


    c.showPage()  
    #PAGINA 10  
    ruta_imagen = buscar_plantilla("r10.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r6.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.52 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_conf3b = site_b.get("configFrec3", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  # 7.875 cm

    insertar_imagen_remota(
    c,
    url_conf3b,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="conf3b_temp.jpg"
)


    c.showPage()  
    #PAGINA 11  
    ruta_imagen = buscar_plantilla("r11.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r11.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_meda = site_a.get("mediciones", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  # 7.875 cm

    insertar_imagen_remota(
    c,
    url_meda,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="meda_temp.jpg"
)

    c.showPage() 
    #PAGINA 12 
    ruta_imagen = buscar_plantilla("r12.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r12.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_medb = site_b.get("mediciones", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_medb,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="medb_temp.jpg"
)

    c.showPage()
    #PAGINA 13 
    ruta_imagen = buscar_plantilla("r13.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r13.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_dis1 = site_a.get("discriminacion1", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  # 7.875 cm

    insertar_imagen_remota(
    c,
    url_dis1,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="dis1_temp.jpg"
)

    c.showPage()

    #PAGINA 14 
    ruta_imagen = buscar_plantilla("r14.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r14.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_dis2 = site_a.get("discriminacion2", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  # 7.875 cm

    insertar_imagen_remota(
    c,
    url_dis2,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="dis2_temp.jpg"
)

    c.showPage()
    #PAGINA 15  
    ruta_imagen = buscar_plantilla("r15.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r15.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_dis1 = site_b.get("discriminacion1", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  # Calcula alto para mantener 16:9

    insertar_imagen_remota(
    c,
    url_dis1,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="dis1_temp.jpg"
)

    c.showPage()
    #PAGINA 16 
    ruta_imagen = buscar_plantilla("r16.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r16.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteACapturas", {})
    url_dis2 = site_b.get("discriminacion2", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_dis2,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="dis2_temp.jpg"
)

    c.showPage()
    #PAGINA 17  
    ruta_imagen = buscar_plantilla("r17.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r17.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_inv1 = site_b.get("inventario", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  # 7.875 cm

    insertar_imagen_remota(
    c,
    url_inv1,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="inv1_temp.jpg"
)

    c.showPage()
    #PAGINA 18  
    ruta_imagen = buscar_plantilla("r18.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r18.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_inv2 = site_b.get("inventario", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_inv2,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="inv2_temp.jpg"
)

    c.showPage()
    
    #PAGINA 19  
    ruta_imagen = buscar_plantilla("r19.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r19.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_perf1 = site_a.get("performance", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_perf1,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="perf1_temp.jpg"
)

    c.showPage()
    #PAGINA 20  
    ruta_imagen = buscar_plantilla("r20.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r20.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_perf2 = site_b.get("performance", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_perf2,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="perf2_temp.jpg"
)

    c.showPage()
    #PAGINA 21 
    ruta_imagen = buscar_plantilla("r21.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r21.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_a = datos.get("SiteACapturas", {})
    url_licen1 = site_a.get("licencia", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_licen1,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="licen1_temp.jpg"
)

    c.showPage()
    #PAGINA 22 
    ruta_imagen = buscar_plantilla("r22.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r22.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(2.96 * cm, 22.60 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(3.14 * cm, 23.99 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_licen2 = site_b.get("licencia", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_licen2,
    x=2.36 * cm,
    y=6.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="licen2_temp.jpg"
)

    c.showPage()
    #PAGINA 23 
    ruta_imagen = buscar_plantilla("r23.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r23.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(3.14 * cm, 10.35 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_bertest = site_b.get("berTest", "")
    

# Insertar imagen remota
    ancho_img = 17 * cm
    alto_img = (ancho_img * 9) / 16  

    insertar_imagen_remota(
    c,
    url_bertest,
    x=2.36 * cm,
    y=10.22 * cm,
    width=ancho_img,
    height=alto_img,
    nombre_temp="berTest_temp.jpg"
)
 
    c.showPage()
    #PAGINA 24  
    ruta_imagen = buscar_plantilla("r24.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r24.jpg no encontrada en ninguna ubicación") 
        
    c.setFont("Helvetica", 10)
    c.drawString(3.14 * cm, 24.25 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}')

   # Extraer la URL desde SiteACapturas
    site_b = datos.get("SiteBCapturas", {})
    url_rfc = site_b.get("pruebaRFC", "")
    

# Insertar imagen remota
    insertar_imagen_remota(
    c,
    url_rfc,
    x=2.59 * cm,
    y=6.22 * cm,
    width=14 * cm,
    height=14 * cm,
    nombre_temp="rfc_temp.jpg"
    
)

    c.showPage()
   #########REPORTRIA IMAGENES SITIO A !#######
    
    #PAGINA 25 

    doc_ref = db.collection("reportesEnlacesEricssonTigo").document(document_id)

    doc = doc_ref.get()
    data = doc.to_dict()
    
    ruta_imagen = buscar_plantilla("r25.jpg")
    if ruta_imagen:
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r25.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteATorre del documento Firestore
    site_a_torre = datos.get("SiteATorre", {})

    # Campos comunes (sin cambios)
    campos_comunes = [
        ("lineaVista", 1.83, 16.77),
        ("etiquetadoAntena", 10.91, 16.77),
    ]
    
    for campo, x, y in campos_comunes:
        url = site_a_torre.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
    
    # Obtener antenas dinámicamente
    antenas = obtener_antenas(site_a_torre, cantidad_antenas)
    
    # Obtener ODUs dinámicamente
    odus = obtener_odus(site_a_torre, cantidad_odus)
    
    # Posiciones para antenas y ODUs (distribución en la página)
    # Primera fila: etiquetaRadio1 (si existe) y fijacionAntena1
    # Segunda fila: SerieAntena1 y serieOdu1
    # Si hay más, se distribuyen en las posiciones disponibles
    
    # Renderizar primera ODU (etiquetaRadio1) - posición 1.83, 10.67
    if len(odus) > 0 and odus[0].get("etiquetaRadio"):
        insertar_imagen_remota(
            c,
            odus[0]["etiquetaRadio"],
            x=1.83 * cm,
            y=10.67 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="etiquetaRadio1.jpg"
        )
    
    # Renderizar primera antena (fijacionAntena1) - posición 10.91, 10.67
    if len(antenas) > 0 and antenas[0].get("fijacionAntena"):
        insertar_imagen_remota(
            c,
            antenas[0]["fijacionAntena"],
            x=10.91 * cm,
            y=10.67 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="fijacionAntena1.jpg"
        )
    
    # Renderizar primera antena (SerieAntena1) - posición 1.83, 4.54
    if len(antenas) > 0 and antenas[0].get("SerieAntena"):
        insertar_imagen_remota(
            c,
            antenas[0]["SerieAntena"],
            x=1.83 * cm,
            y=4.54 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="SerieAntena1.jpg"
        )
    
    # Renderizar primera ODU (serieOdu1) - posición 10.91, 4.54
    if len(odus) > 0 and odus[0].get("serieOdu"):
        insertar_imagen_remota(
            c,
            odus[0]["serieOdu"],
            x=10.91 * cm,
            y=4.54 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="serieOdu1.jpg"
        )

    c.showPage()

    #PAGINA 26 
    ruta_imagen = buscar_plantilla("r26.jpg")
    if ruta_imagen:
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r26.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteATorre del documento Firestore
    site_a_torre = datos.get("SiteATorre", {})

    # Campos comunes (sin cambios)
    campos_comunes = [
        ("barraTierraGroundingKit", 10.91, 16.77),
        ("groundingKit", 1.83, 10.67),
        ("aterrizajeOduPlatina", 10.91, 10.67),
        ("etiquetaCableCoax", 1.83, 4.54),
    ]
    
    for campo, x, y in campos_comunes:
        url = site_a_torre.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
    
    # Obtener ODUs dinámicamente
    odus = obtener_odus(site_a_torre, cantidad_odus)
    
    # Renderizar primera ODU (ConexionOdu1) - posición 1.83, 16.77
    if len(odus) > 0 and odus[0].get("ConexionOdu"):
        insertar_imagen_remota(
            c,
            odus[0]["ConexionOdu"],
            x=1.83 * cm,
            y=16.77 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="ConexionOdu1.jpg"
        )
    
    # Renderizar segunda ODU (serieOdu2) - posición 10.91, 4.54
    if len(odus) > 1 and odus[1].get("serieOdu"):
        insertar_imagen_remota(
            c,
            odus[1]["serieOdu"],
            x=10.91 * cm,
            y=4.54 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="serieOdu2.jpg"
        )

    c.showPage()

    #PAGINA 27 
    ruta_imagen = buscar_plantilla("r27.jpg")
    if ruta_imagen:
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r27.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteATorre del documento Firestore
    site_a_piso = datos.get("SiteAPiso", {})

# Definir campos de imagen y posiciones (x, y)
    imagenes = [
        ("pasamuros", 1.83, 16.77),
        ("idu", 10.91, 16.77),
        ("etiquetaIdu", 1.83, 10.67),
        ("serieMagazine", 10.91, 10.67),
        ("etiquetaIdu", 1.83, 4.54),
        ("etiquetaCableAlimentacion", 10.91, 4.54),
    ]

# Descargar e insertar cada imagen
    for campo, x, y in imagenes:
        url = site_a_piso.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
        else:
            print(f" No se encontró URL válida para {campo}")

    c.showPage()

    #PAGINA 28 
    ruta_imagen = buscar_plantilla("r28.jpg")
    if os.path.exists(ruta_imagen):
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r28.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteATorre del documento Firestore
    site_a_piso = datos.get("SiteAPiso", {})

# Definir campos de imagen y posiciones (x, y)
    imagenes = [
        ("panelBreakers", 1.83, 16.77),
        ("fibra1", 10.91, 16.77),
        ("fibra2", 1.83, 10.67),
        ("aterrizajeIdu", 10.91, 10.67),
        ("aterrizajeIdu", 1.83, 4.54),
        ("arrestores", 10.91, 4.54),
    ]

# Descargar e insertar cada imagen
    for campo, x, y in imagenes:
        url = site_a_piso.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
        else:
            print(f"⚠️ No se encontró URL válida para {campo}")

    c.showPage()

    #PAGINA 29 
    ruta_imagen = buscar_plantilla("r29.jpg")
    if ruta_imagen:
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r29.jpg no encontrada en ninguna ubicación")

    # Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioA", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

    # Acceder a ambos subdocumentos
    site_a_torre = datos.get("SiteATorre", {}) 
    site_a_piso = datos.get("SiteAPiso", {})

    # Lista de imágenes con origen específico
    imagenes = [
        ("verticeAntenaTorre", "torre", 1.83, 16.77),
        ("gabineteAbierto", "piso", 10.91, 16.77),
        ("sitioGeneral", "torre", 1.83, 10.67),
        ("shelter", "piso", 10.91, 10.67),
        ("", "piso", 1.83, 4.54),
        ("", "piso", 10.91, 4.54),
    ]

    # Insertar imágenes desde el origen correcto
    for campo, origen, x, y in imagenes:
        if not campo:
            continue  # Saltar campos vacíos

        if origen == "torre":
            url = site_a_torre.get(campo, "").strip()
        elif origen == "piso":
            url = site_a_piso.get(campo, "").strip()
        else:
            url = ""

        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
        else:
            print(f"⚠️ No se encontró URL válida para {campo} ({origen})")

    c.showPage()
    
    #########REPORTRIA IMAGENES SITIO B !#######
    #PAGINA 30  
    doc_ref = db.collection("reportesEnlacesEricssonTigo").document(document_id)

    doc = doc_ref.get()
    data = doc.to_dict()
   
    ruta_imagen = buscar_plantilla("r30.jpg")
    if ruta_imagen:
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r30.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteBTorre del documento Firestore
    site_b_torre = datos.get("SiteBTorre", {})

    # Campos comunes (sin cambios)
    campos_comunes = [
        ("lineaVista", 1.83, 16.77),
        ("etiquetadoAntena", 10.91, 16.77),
    ]
    
    for campo, x, y in campos_comunes:
        url = site_b_torre.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
    
    # Obtener antenas dinámicamente
    antenas = obtener_antenas(site_b_torre, cantidad_antenas)
    
    # Obtener ODUs dinámicamente
    odus = obtener_odus(site_b_torre, cantidad_odus)
    
    # Renderizar primera ODU (etiquetaRadio1) - posición 1.83, 10.67
    if len(odus) > 0 and odus[0].get("etiquetaRadio"):
        insertar_imagen_remota(
            c,
            odus[0]["etiquetaRadio"],
            x=1.83 * cm,
            y=10.67 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="etiquetaRadio1.jpg"
        )
    
    # Renderizar primera antena (fijacionAntena1) - posición 10.91, 10.67
    if len(antenas) > 0 and antenas[0].get("fijacionAntena"):
        insertar_imagen_remota(
            c,
            antenas[0]["fijacionAntena"],
            x=10.91 * cm,
            y=10.67 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="fijacionAntena1.jpg"
        )
    
    # Renderizar primera antena (SerieAntena1) - posición 1.83, 4.54
    if len(antenas) > 0 and antenas[0].get("SerieAntena"):
        insertar_imagen_remota(
            c,
            antenas[0]["SerieAntena"],
            x=1.83 * cm,
            y=4.54 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="SerieAntena1.jpg"
        )
    
    # Renderizar primera ODU (serieOdu1) - posición 10.91, 4.54
    if len(odus) > 0 and odus[0].get("serieOdu"):
        insertar_imagen_remota(
            c,
            odus[0]["serieOdu"],
            x=10.91 * cm,
            y=4.54 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="serieOdu1.jpg"
        )

    c.showPage()
    #PAGINA 31
    doc_ref = db.collection("reportesEnlacesEricssonTigo").document(document_id)

    doc = doc_ref.get()
    data = doc.to_dict()
   
    ruta_imagen = buscar_plantilla("r31.jpg")
    if ruta_imagen:
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print("⚠️ Imagen r31.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteBTorre del documento Firestore
    site_b_torre = datos.get("SiteBTorre", {})

    # Campos comunes (sin cambios)
    campos_comunes = [
        ("barraTierraGroundingKit", 10.91, 16.77),
        ("groundingKit", 1.83, 10.67),
        ("aterrizajeOduPlatina", 10.91, 10.67),
        ("etiquetaCableCoax", 1.83, 4.54),
    ]
    
    for campo, x, y in campos_comunes:
        url = site_b_torre.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
    
    # Obtener ODUs dinámicamente
    odus = obtener_odus(site_b_torre, cantidad_odus)
    
    # Renderizar primera ODU (ConexionOdu1) - posición 1.83, 16.77
    if len(odus) > 0 and odus[0].get("ConexionOdu"):
        insertar_imagen_remota(
            c,
            odus[0]["ConexionOdu"],
            x=1.83 * cm,
            y=16.77 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="ConexionOdu1.jpg"
        )
    
    # Renderizar segunda ODU (serieOdu2) - posición 10.91, 4.54
    if len(odus) > 1 and odus[1].get("serieOdu"):
        insertar_imagen_remota(
            c,
            odus[1]["serieOdu"],
            x=10.91 * cm,
            y=4.54 * cm,
            width=8.5 * cm,
            height=5 * cm,
            nombre_temp="serieOdu2.jpg"
        )

    c.showPage()
    #PAGINA 32
    doc_ref = db.collection("reportesEnlacesEricssonTigo").document(document_id)

    doc = doc_ref.get()
    data = doc.to_dict()
   
    ruta_imagen = buscar_plantilla("r32.jpg")
    if os.path.exists(ruta_imagen):
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r32.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteATorre del documento Firestore
    site_b_piso = datos.get("SiteBPiso", {})

# Definir campos de imagen y posiciones (x, y)
    imagenes = [
        ("pasamuros", 1.83, 16.77),
        ("idu", 10.91, 16.77),
        ("etiquetaIdu", 1.83, 10.67),
        ("serieMagazine", 10.91, 10.67),
        ("etiquetaIdu", 1.83, 4.54),
        ("etiquetaCableAlimentacion", 10.91, 4.54),
    ]


# Descargar e insertar cada imagen
    for campo, x, y in imagenes:
        url = site_b_piso.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
        else:
            print(f"⚠️ No se encontró URL válida para {campo}")

    c.showPage()
    #PAGINA 33
    doc_ref = db.collection("reportesEnlacesEricssonTigo").document(document_id)

    doc = doc_ref.get()
    data = doc.to_dict()
   
    ruta_imagen = buscar_plantilla("r33.jpg")
    if os.path.exists(ruta_imagen):
       insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r33.jpg no encontrada en ninguna ubicación")

# Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

# Acceder al subdocumento SiteATorre del documento Firestore
    site_b_piso = datos.get("SiteBPiso", {})

# Definir campos de imagen y posiciones (x, y)
    imagenes = [
        ("panelBreakers", 1.83, 16.77),
        ("fibra1", 10.91, 16.77),
        ("fibra2", 1.83, 10.67),
        ("aterrizajeIdu", 10.91, 10.67),
        ("aterrizajeIdu", 1.83, 4.54),
        ("arrestores", 10.91, 4.54),
    ]


# Descargar e insertar cada imagen
    for campo, x, y in imagenes:
        url = site_b_piso.get(campo, "").strip()
        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
        else:
            print(f"⚠️ No se encontró URL válida para {campo}")

    c.showPage()
    #PAGINA 34
    ruta_imagen = buscar_plantilla("r34.jpg")
    if os.path.exists(ruta_imagen):
        insertar_plantilla_comprimida(c, ruta_imagen, ancho, alto)
    else:
        print(" Imagen r34.jpg no encontrada en ninguna ubicación")

    # Textos en encabezado
    c.setFont("Helvetica", 10)
    c.drawString(10.75 * cm, 22.44 * cm, datos_generales.get("SitioB", "S"))
    c.drawString(10.75 * cm, 23.44 * cm, f'{datos_generales.get("SitioA", "")} - {datos_generales.get("SitioB", "")}') 

    # Acceder a ambos subdocumentos
    site_b_torre = datos.get("SiteATorre", {}) 
    site_b_piso = datos.get("SiteAPiso", {})

    # Lista de imágenes con origen específico
    imagenes = [
        ("verticeAntenaTorre", "torre", 1.83, 16.77),
        ("gabineteAbierto", "piso", 10.91, 16.77),
        ("sitioGeneral", "torre", 1.83, 10.67),
        ("shelter", "piso", 10.91, 10.67),
        ("", "piso", 1.83, 4.54),
        ("", "piso", 10.91, 4.54),
    ]

    # Insertar imágenes desde el origen correcto
    for campo, origen, x, y in imagenes:
        if not campo:
            continue  # Saltar campos vacíos

        if origen == "torre":
            url = site_b_torre.get(campo, "").strip()
        elif origen == "piso":
            url = site_b_piso.get(campo, "").strip()
        else:
            url = ""

        if url.startswith("http"):
            insertar_imagen_remota(
                c,
                url,
                x=x * cm,
                y=y * cm,
                width=8.5 * cm,
                height=5 * cm,
                nombre_temp=f"{campo}.jpg"
            )
        else:
            print(f"⚠️ No se encontró URL válida para {campo} ({origen})")

    c.showPage()
    

    # Finalizar PDF
    c.save()
    print(f"✅ PDF generado exitosamente: {salida_pdf}")