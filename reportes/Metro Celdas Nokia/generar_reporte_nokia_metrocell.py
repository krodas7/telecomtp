from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PIL import Image as PilImage
from PIL import ImageOps
import requests
from io import BytesIO
import os
from firebase_config import init_firestore
import uuid 
from datetime import datetime
from reportlab.lib.utils import ImageReader

def descargar_imagen(url, max_size=(800, 800), quality=60, max_retries=3):
    """
    Descarga una imagen desde una URL y la procesa.
    Maneja imágenes truncadas o corruptas con reintentos.
    """
    if not url:
        return None
    
    for intento in range(max_retries):
        try:
            # Descargar con timeout y verificar status
            # Usar stream=False para asegurar descarga completa
            response = requests.get(url, timeout=30, stream=False)
            response.raise_for_status()  # Lanza excepción si hay error HTTP
            
            # Verificar que el Content-Length coincide con lo descargado
            content = response.content
            expected_length = response.headers.get('Content-Length')
            
            if expected_length:
                expected_length = int(expected_length)
                if len(content) < expected_length:
                    # Descarga incompleta
                    if intento < max_retries - 1:
                        continue  # Reintentar
                    print(f"⚠️  Advertencia: Imagen descargada incompleta ({len(content)}/{expected_length} bytes)")
            
            # Verificar que hay contenido
            if not content or len(content) < 100:  # Mínimo razonable para una imagen
                raise ValueError("Imagen demasiado pequeña o vacía")
            
            # Intentar abrir la imagen
            img = None
            try:
                # Configurar PIL para ser más permisivo con imágenes truncadas
                # Esto permite procesar imágenes que están ligeramente truncadas pero aún utilizables
                from PIL import ImageFile
                ImageFile.LOAD_TRUNCATED_IMAGES = True  # Permite cargar imágenes truncadas
                
                img = PilImage.open(BytesIO(content))
                # Intentar cargar completamente
                try:
                    img.load()
                except Exception as load_error:
                    # Si el error es de truncamiento, la imagen puede ser aún utilizable
                    if "truncated" in str(load_error).lower():
                        # Intentar reabrir y procesar de todas formas
                        # Muchas imágenes truncadas aún pueden ser procesadas
                        img = PilImage.open(BytesIO(content))
                        # Continuar con el procesamiento aunque esté truncada
                        # No mostrar error si la imagen se puede abrir
                    else:
                        # Otro error al cargar, reintentar
                        if intento < max_retries - 1:
                            continue
                        raise load_error
            except Exception as img_error:
                # Error al abrir la imagen
                if "truncated" in str(img_error).lower():
                    # Intentar abrir de todas formas con LOAD_TRUNCATED_IMAGES
                    try:
                        from PIL import ImageFile
                        ImageFile.LOAD_TRUNCATED_IMAGES = True
                        img = PilImage.open(BytesIO(content))
                    except:
                        if intento < max_retries - 1:
                            continue
                        # Si es el último intento y aún falla, omitir esta imagen
                        return None
                else:
                    if intento < max_retries - 1:
                        continue
                    raise img_error
            
            if img is None:
                if intento < max_retries - 1:
                    continue
                return None
            
            # Corregir rotación EXIF
            try:
                img = ImageOps.exif_transpose(img)
            except:
                pass  # Si falla, continuar sin corrección EXIF

            # Convertir a RGB por si tiene canal alfa (PNG)
            img = img.convert("RGB")

            # Redimensionar proporcionalmente
            try:
                # Intentar con Resampling (PIL 10.0+)
                img.thumbnail(max_size, PilImage.Resampling.LANCZOS)
            except AttributeError:
                # Fallback para versiones anteriores
                img.thumbnail(max_size, PilImage.LANCZOS)

            # Recomprimir a JPEG con calidad reducida
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True)
            buffer.seek(0)

            # Devolver objeto PIL listo para ImageReader
            return PilImage.open(buffer)
            
        except requests.exceptions.RequestException as e:
            if intento < max_retries - 1:
                continue
            print(f"Error al descargar imagen {url[:50]}...: {e}")
            return None
        except Exception as e:
            if intento < max_retries - 1:
                continue
            # Solo mostrar error si es el último intento
            error_msg = str(e)
            if "truncated" not in error_msg.lower():
                print(f"Error al procesar imagen {url[:50]}...: {e}")
            return None
    
    return None

def insertar_imagen(canvas_obj, img, x, y, width=None, height=None):
    if img:
        img_reader = ImageReader(img)
        canvas_obj.drawImage(img_reader, x, y, width=width, height=height)

  
def _get_templates_base_dir():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "reportes_templates", "metro_celdas")


def generar_pdf_nokia_metrocell(document_id, salida_pdf='reporte_nokia_metrocell.pdf', data=None):
    if data is None:
        db = init_firestore()
        doc = db.collection("InstalacionesNokiaMetroCeldas").document(document_id).get()
        
        if not doc.exists:
            print("Documento no encontrado.")
            return

        datos = doc.to_dict()
    else:
        datos = data

    c = canvas.Canvas(salida_pdf, pagesize=letter)
    ancho, alto = letter

    templates_dir = _get_templates_base_dir()

    for pagina in range(1, 17):
        # Saltar página 10 - no existe plantilla ni datos
        if pagina == 10:
            continue
            
        plantilla_path = os.path.join(templates_dir, f"Nokia{pagina}.jpg")
        if os.path.exists(plantilla_path):
            c.drawImage(plantilla_path, 0, 0, width=ancho, height=alto)
        else:
            print(f"Plantilla {plantilla_path} no encontrada.")

        #Ejemplo: Insertar texto y fotos en distintas páginas
        
        if pagina == 2:
            c.setFont("Helvetica", 11)
            c.drawString(125, 660, f"{datos.get('nombre', '')}")
            c.drawString(380, 610, f"{datos.get('region', '')}")
            c.drawString(380, 585, f"{datos.get('latitud', '')}")
            c.drawString(380, 573, f"{datos.get('longitud', '')}")
            c.drawString(127, 530, f"{datos.get('tipoSitio', '')}")
            c.drawString(127, 510, f"Tipo de Torre: {datos.get('tipoTorre', '')}")
            c.drawString(127, 465, f"{datos.get('vendor', '')}")
            c.drawString(445, 465, f"{datos.get('fecha', '')}") 
            fotos = datos.get("fotos", {})
            # TorreCompleta → PosteCompleto
            insertar_imagen(c, descargar_imagen(fotos.get("PosteCompleto")), 50, 240, 150, 173)
            # Mapa → Mapa (igual)
            insertar_imagen(c, descargar_imagen(fotos.get("Mapa")), 325, 240, 125, 173)
        
        elif pagina == 3:
             
             c.setFont("Helvetica-Bold", 10)

    # Vendor (izquierda)
             c.drawString(550, 675, f"{datos.get('vendor')}")

    # Region (debajo del vendor)
             #c.drawString(180, 690, f" {datos.get('region', '')}")

    # Nombre (derecha superior)
             c.drawString(295, 675, f"{datos.get('nombre', '')}")

    # Fecha (debajo del nombre)
             c.drawString(75, 690, f"{datos.get('fecha', '')}")
        
        elif pagina == 4:
             
             c.setFont("Helvetica-Bold", 10)

    # Vendor (izquierda)
             c.drawString(557, 675, f"{datos.get('vendor')}")

    # Region (debajo del vendor)
             #c.drawString(190, 690, f" {datos.get('region', '')}")

    # Nombre (derecha superior)
             c.drawString(300, 675, f"{datos.get('nombre', '')}")

    # Fecha (debajo del nombre)
             c.drawString(75, 690, f"{datos.get('fecha', '')}")
        
        elif pagina == 5:
            #encabezado 
            c.setFont("Helvetica", 8)
            c.drawString(350, 708, f"{datos.get('latitud', '')}")
            c.drawString(480, 708, f"{datos.get('longitud', '')}")
            c.drawString(99, 700, f"{datos.get('tipoSitio', '')}")
            c.drawString(460, 700, f"{datos.get('siteModel', '')}")

            c.drawString(140, 684, f"{datos.get('fecha', '')}")
            c.drawString(140, 668, f"{datos.get('nombre', '')}")
            c.drawString(140, 643, f"{datos.get('vendor', '')}")
            c.drawString(140, 635, f"{datos.get('region', '')}")
            fotos = datos.get("fotos", {})
            # Gabinete → GabineteAbierto
            insertar_imagen(c, descargar_imagen(fotos.get("GabineteAbierto")), 40, 410, 122, 93)
            # FijacionGabinete → GabineteCerrado
            insertar_imagen(c, descargar_imagen(fotos.get("GabineteCerrado")), 230, 410, 122, 93)
            # Tarjeta → SitioGeneral
            insertar_imagen(c, descargar_imagen(fotos.get("SitioGeneral")), 440, 410, 122, 93)
            # Reservas → OrganizadoCablesInterno
            insertar_imagen(c, descargar_imagen(fotos.get("OrganizadoCablesInterno")), 40, 245, 122, 93)
            # RecorridoCables → RecorridoCables (igual)
            insertar_imagen(c, descargar_imagen(fotos.get("RecorridoCables")), 230, 245, 122, 93)
            
            
        
        elif pagina == 6:
        #encabezado 
            c.setFont("Helvetica", 8)
            c.drawString(359, 712, f"{datos.get('latitud', '')}")
            c.drawString(499, 712, f"{datos.get('longitud', '')}")
            c.drawString(109, 704, f"{datos.get('tipoSitio', '')}")
            c.drawString(491, 704, f"{datos.get('siteModel', '')}")
            fotos = datos.get("fotos", {})
        
            # TierraOvp → AntenaPoste
            insertar_imagen(c, descargar_imagen(fotos.get("AntenaPoste")), 245, 501, 122, 100)
            # Ovp → AntenaZoom
            insertar_imagen(c, descargar_imagen(fotos.get("AntenaZoom")), 450, 501, 122, 100) 
           
        elif pagina == 7:
            #encabezado 
            c.setFont("Helvetica", 8)
            c.drawString(357, 730, f"{datos.get('latitud', '')}")
            c.drawString(490, 730, f"{datos.get('longitud', '')}")
            c.drawString(103, 722, f"{datos.get('tipoSitio', '')}")
            c.drawString(473, 722, f"{datos.get('siteModel', '')}")
                                                
            fotos = datos.get("fotos", {})
        
            # EtiquetaEnergia1 → JumpersConexion1
            insertar_imagen(c, descargar_imagen(fotos.get("JumpersConexion1")), 465, 573, 80, 50)
            # EtiquetaEnergia2 → JumpersConexion2
            insertar_imagen(c, descargar_imagen(fotos.get("JumpersConexion2")), 465, 519, 80, 50)
            # Braker → ConexionAC
            insertar_imagen(c, descargar_imagen(fotos.get("ConexionAC")), 57, 405, 74, 50)
            # EtiquetaBreaker → GeneralAC
            insertar_imagen(c, descargar_imagen(fotos.get("GeneralAC")), 57, 350, 85, 50)

            insertar_imagen(c, descargar_imagen(fotos.get("jumpers")), 245, 350, 122, 100)
        
        elif pagina == 8:
            #encabezado 
            c.setFont("Helvetica", 8)
            c.drawString(355, 724, f"{datos.get('latitud', '')}")
            c.drawString(488, 724, f"{datos.get('longitud', '')}")
            c.drawString(101, 716, f"{datos.get('tipoSitio', '')}")
            c.drawString(471, 716, f"{datos.get('siteModel', '')}")
            fotos = datos.get("fotos", {})
        
            # EtiquetaFOODF → Bateria
            insertar_imagen(c, descargar_imagen(fotos.get("Bateria")), 38, 195, 122, 93)
            
            # FijacionS1 → EtiquetaFODF (mantener coordenadas originales)
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaFODF")), 38, 530, 122, 93)
            # Fijacion2S1 → EtiquetaFO2 (mantener coordenadas originales)
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaFO2")), 230, 530, 122, 93)
         

            #inferior 
           
            # ClampsHorizontal → COM
            insertar_imagen(c, descargar_imagen(fotos.get("COM")), 40, 19, 122, 93)
            # EscalerillaClamps → DistribuidorDC
            insertar_imagen(c, descargar_imagen(fotos.get("DistribuidorDC")), 235, 19, 122, 93)
            # ColoresTierra → EtiquetaEnergia
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaEnergia")), 413, 18, 80, 93)
            # ColresFPFH → Braker
            insertar_imagen(c, descargar_imagen(fotos.get("Braker")), 520, 66, 55, 45) 
            # ColoresFibras → EtiquetaBreaker
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaBreaker")), 520, 17, 58, 45) 
        
        elif pagina == 9:
        #encabezado 
          c.setFont("Helvetica", 8)
          c.drawString(350, 721, f"{datos.get('latitud', '')}")
          c.drawString(486, 721, f"{datos.get('longitud', '')}")
          c.drawString(103, 713, f"{datos.get('tipoSitio', '')}")
          c.drawString(468, 713, f"{datos.get('siteModel', '')}")
          
          fotos = datos.get("fotos", {})

    # Fila superior - Mapeo de fotos (eliminadas secciones Sector 1, 2, 3)
          # EtiquetaFOSFD10 → Radio5G
          insertar_imagen(c, descargar_imagen(fotos.get("Radio5G")), 38, 530, 122, 93)
          # ClampsVertical → RadioLTE
          insertar_imagen(c, descargar_imagen(fotos.get("RadioLTE")), 240, 530, 122, 93)
          # FijacionFPFH → TierraFisica (mantener coordenadas originales)
          insertar_imagen(c, descargar_imagen(fotos.get("TierraFisica")), 465, 530, 95, 100)
          # Ovp → AntenaZoom
          insertar_imagen(c, descargar_imagen(fotos.get("AntenaZoom")), 38, 365, 122, 93) 
    # Fila del medio - Eliminadas fotos de Sector 1 (ConexionesFPFH, TierraFPFH, ConexionesAntenaS1, InclinometroS1, Distanciometro)
          # Espacios vacíos - estas fotos no existen en MetroCell
        
        elif pagina == 11:  
          #encabezado 
          c.setFont("Helvetica", 8)
          c.drawString(355, 710, f"{datos.get('latitud', '')}")
          c.drawString(490, 710, f"{datos.get('longitud', '')}")
          c.drawString(107, 703, f"{datos.get('tipoSitio', '')}")
          c.drawString(470, 703, f"{datos.get('siteModel', '')}")
          
          fotos = datos.get("fotos", {})
          # SitioLimpio → SitioLimpio (igual)
          insertar_imagen(c, descargar_imagen(fotos.get("SitioLimpio")), 64, 516, 70, 95)

        
        elif pagina == 12: 
        
          c.setFont("Helvetica", 8)
          c.drawString(80, 665, datos.get("fecha", ""))
          c.drawString(300, 665, datos.get("region", ""))
          c.drawString(300, 637, datos.get("nombre", ""))
          c.drawString(550, 637, "NOKIA")  # o datos_site.get("vendor", "NOKIA")
        
        elif pagina == 13:  
          c.setFont("Helvetica", 8)
          c.drawString(75, 685, datos.get("fecha", ""))
          c.drawString(310, 685, datos.get("region", ""))
          c.drawString(310, 655, datos.get("nombre", ""))
          c.drawString(560, 655, "NOKIA")  # o datos_site.get("vendor", "NOKIA")
          # alturaAntenas → alturaAntena (singular)
          altura = datos.get("alturaAntena", "")
          c.drawString(420, 485, altura)
          # Eliminados azimuthS1, azimuthS2, azimuthS3
        
        if pagina == 14:  
            c.setFont("Helvetica", 8)
            c.drawString(75, 665, datos.get("fecha", ""))
            c.drawString(313, 665, datos.get("region", ""))
            c.drawString(313, 635, datos.get("nombre", ""))
            c.drawString(560, 635, "NOKIA")  # o datos_site.get("vendor", "NOKIA")

          # Tabla de equipos instalados - Cambiados de 10 a 6 equipos
            c.setFont("Helvetica", 6)
            y_start = 500
            row_height = 19

            x_desc = 45
            x_modelo = 230
            x_codigo = 380
            x_serial = 499

            fila = 0

            # Equipos MetroCell: Antena, Radio5g, Radio4g, FPFH, COM, BATERIA
            equipos_metrocell = ["Antena", "Radio5g", "Radio4g", "FPFH", "COM", "BATERIA"]
            
            for equipo in equipos_metrocell:
                equipo_data = datos.get(equipo, {})
                if equipo_data:
                    y = y_start - fila * row_height
                    c.drawString(x_desc, y, equipo_data.get("descripcion", ""))
                    c.drawString(x_modelo, y, equipo_data.get("modelo", ""))
                    c.drawString(x_codigo, y, equipo_data.get("modelo", ""))
                    c.drawString(x_serial, y, equipo_data.get("serial", ""))
                    fila += 1
        
        elif pagina == 15:
            c.setFont("Helvetica", 8)
            c.drawString(80, 723, datos.get("fecha", ""))
            c.drawString(216, 724, "NOKIA")  # o datos_site.get("vendor", "NOKIA")
            c.drawString(315, 710, datos.get("nombre", ""))
            c.drawString(80, 678, datos.get("latitud", ""))
            c.drawString(315, 678, datos.get("longitud", ""))
            c.drawString(470, 678, datos.get("equipmentType", ""))
            c.drawString(115, 660, datos.get("tipoSitio", ""))
            c.drawString(315, 660, datos.get("tipoTorre", ""))
        
        
        elif pagina == 16:
        # Insertar los datos en la página 16 
        
         c.setFont("Helvetica", 11)
         c.drawString(300, 330, "Humberto Gonzalez")
         c.drawString(300, 305, f"{datos.get('vendor', '')}")
         c.drawString(300, 280, f"{datetime.today().strftime('%Y-%m-%d')}")   
         
         datos_site = datos.get("datos", {})

         c.setFont("Helvetica", 8)
         c.drawString(80, 665, datos.get("fecha", ""))
         c.drawString(200, 665, datos.get("region", ""))
         c.drawString(350, 638, datos.get("nombre", ""))
         c.drawString(550, 638, "NOKIA")  # o datos_site.get("vendor", "NOKIA")
         

        # Puedes seguir añadiendo lógicas similares para las otras páginas (sector2, sector3, SFPs, energía, etc.)

        c.showPage()

    c.save()
    print(f"PDF generado: {salida_pdf}")

