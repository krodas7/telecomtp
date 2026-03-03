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

def descargar_imagen(url, max_size=(800, 800), quality=60):
    try:
        response = requests.get(url)
        img = PilImage.open(BytesIO(response.content))
        img = ImageOps.exif_transpose(img)  # Corrige rotación

        # Convertir a RGB por si tiene canal alfa (PNG)
        img = img.convert("RGB")

        # Redimensionar proporcionalmente
        img.thumbnail(max_size)

        # Recomprimir a JPEG con calidad reducida
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        buffer.seek(0)

        # Devolver objeto PIL listo para ImageReader
        return PilImage.open(buffer)
    except Exception as e:
        print(f"Error al descargar imagen {url}: {e}")
        return None

def insertar_imagen(canvas_obj, img, x, y, width=None, height=None):
    if img:
        img_reader = ImageReader(img)
        canvas_obj.drawImage(img_reader, x, y, width=width, height=height)

  
def _get_templates_base_dir():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(base_dir, "reportes_templates", "ran_setar")


def generar_pdf_nokia(document_id, salida_pdf='reporte_nokia.pdf', data=None):
    if data is None:
        db = init_firestore()
        doc = db.collection("InstalacionesRanSetar").document(document_id).get()
        
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
            insertar_imagen(c, descargar_imagen(fotos.get("TorreCompleta")), 50, 240, 150, 173)
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
            insertar_imagen(c, descargar_imagen(fotos.get("Gabinete")), 40, 410, 122, 93)
            insertar_imagen(c, descargar_imagen(fotos.get("FijacionGabinete")), 230, 410, 122, 93)
            insertar_imagen(c, descargar_imagen(fotos.get("Tarjeta")), 440, 410, 122, 93)
            insertar_imagen(c, descargar_imagen(fotos.get("Reservas")), 40, 245, 122, 93)
            insertar_imagen(c, descargar_imagen(fotos.get("RecorridoCables")), 230, 245, 122, 93)
            
            
        
        elif pagina == 6:
        #encabezado 
            c.setFont("Helvetica", 8)
            c.drawString(355, 708, f"{datos.get('latitud', '')}")
            c.drawString(495, 708, f"{datos.get('longitud', '')}")
            c.drawString(105, 700, f"{datos.get('tipoSitio', '')}")
            c.drawString(487, 700, f"{datos.get('siteModel', '')}")
            fotos = datos.get("fotos", {})
        
            insertar_imagen(c, descargar_imagen(fotos.get("TierraOvp")), 245, 501, 122, 100)
            insertar_imagen(c, descargar_imagen(fotos.get("Ovp")), 450, 501, 122, 100) 
           
        elif pagina == 7:
            #encabezado 
            c.setFont("Helvetica", 8)
            c.drawString(352, 731, f"{datos.get('latitud', '')}")
            c.drawString(485, 731, f"{datos.get('longitud', '')}")
            c.drawString(98, 723, f"{datos.get('tipoSitio', '')}")
            c.drawString(468, 723, f"{datos.get('siteModel', '')}")
                                                
            fotos = datos.get("fotos", {})
        
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaEnergia1")), 465, 578, 80, 50)
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaEnergia2")), 465, 524, 80, 50)
            insertar_imagen(c, descargar_imagen(fotos.get("Braker")), 57, 415, 74, 50)
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaBreaker")), 57, 360, 85, 50)
        
        elif pagina == 8:
            #encabezado 
            c.setFont("Helvetica", 8)
            c.drawString(352, 716, f"{datos.get('latitud', '')}")
            c.drawString(485, 716, f"{datos.get('longitud', '')}")
            c.drawString(98, 708, f"{datos.get('tipoSitio', '')}")
            c.drawString(468, 708, f"{datos.get('siteModel', '')}")
            fotos = datos.get("fotos", {})
        
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaFOODF")), 38, 530, 122, 93)
            insertar_imagen(c, descargar_imagen(fotos.get("EtiquetaFOSFD10")), 230, 530, 122, 93)
            
            #inferior 
            insertar_imagen(c, descargar_imagen(fotos.get("ClampsVertical")), 40, 66, 106, 50)
            insertar_imagen(c, descargar_imagen(fotos.get("ClampsHorizontal")), 40, 15, 105, 50)
            insertar_imagen(c, descargar_imagen(fotos.get("EscalerillaClamps")), 235, 19, 122, 93)
            insertar_imagen(c, descargar_imagen(fotos.get("ColoresTierra")), 413, 18, 80, 93)
            insertar_imagen(c, descargar_imagen(fotos.get("ColresFPFH")), 520, 66, 55, 45) 
            insertar_imagen(c, descargar_imagen(fotos.get("ColoresFibras")), 520, 17, 58, 45) 
        
        elif pagina == 9:
        #encabezado 
          c.setFont("Helvetica", 8)
          c.drawString(352, 708, f"{datos.get('latitud', '')}")
          c.drawString(488, 708, f"{datos.get('longitud', '')}")
          c.drawString(105, 700, f"{datos.get('tipoSitio', '')}")
          c.drawString(470, 700, f"{datos.get('siteModel', '')}")
          
          fotos = datos.get("fotos", {})

    # Fila superior
          insertar_imagen(c, descargar_imagen(fotos.get("FijacionS1")),         24, 511, 70, 98)
          insertar_imagen(c, descargar_imagen(fotos.get("Fijacion2S1")),         128, 563, 40, 47)
          insertar_imagen(c, descargar_imagen(fotos.get("BrujulaS1")),         128, 511, 40, 47)

          insertar_imagen(c, descargar_imagen(fotos.get("Fijacion2S1")),      253, 511, 95, 100)
          insertar_imagen(c, descargar_imagen(fotos.get("FijacionFPFH")),     465, 511, 95, 100)

    # Fila del medio
          insertar_imagen(c, descargar_imagen(fotos.get("ConexionesFPFH")), 47, 350, 95, 100)
          insertar_imagen(c, descargar_imagen(fotos.get("TierraFPFH")),    253, 350, 95, 100)
          insertar_imagen(c, descargar_imagen(fotos.get("ConexionesAntenaS1")),    465, 350, 95, 100)
        
        # Fila del medio
          insertar_imagen(c, descargar_imagen(fotos.get("InclinometroS1")), 85, 239, 40, 47)
          insertar_imagen(c, descargar_imagen(fotos.get("Distanciometro")), 85, 185, 40, 47)
        
        elif pagina == 10:
          #encabezado 
          c.setFont("Helvetica", 8)
          c.drawString(352, 729, f"{datos.get('latitud', '')}")
          c.drawString(488, 729, f"{datos.get('longitud', '')}")
          c.drawString(105, 721, f"{datos.get('tipoSitio', '')}")
          c.drawString(470, 721, f"{datos.get('siteModel', '')}")
          
          fotos = datos.get("fotos", {})

    # Fila superior
          insertar_imagen(c, descargar_imagen(fotos.get("FijacionS2")),         14, 541, 70, 98)
          insertar_imagen(c, descargar_imagen(fotos.get("Fijacion2S2")),      120, 593, 40, 47)
          insertar_imagen(c, descargar_imagen(fotos.get("BrujulaS2")),     120, 541, 40, 47)

          insertar_imagen(c, descargar_imagen(fotos.get("Fijacion2S1")),      253, 541, 95, 100)
          insertar_imagen(c, descargar_imagen(fotos.get("ConexionesAntenaS2")),     465, 541, 95, 100)
    # Fila del medio
          insertar_imagen(c, descargar_imagen(fotos.get("TierraS2")), 54, 378, 90, 95)
          insertar_imagen(c, descargar_imagen(fotos.get("InclinometroS2")),    280, 428, 40, 47)
          insertar_imagen(c, descargar_imagen(fotos.get("Distanciometro")),    280, 377, 40, 47)

        #Tercera Fila
          insertar_imagen(c, descargar_imagen(fotos.get("FijacionS3")),         18, 191, 70, 98)
          insertar_imagen(c, descargar_imagen(fotos.get("Fijacion2S3")),      130, 243, 40, 47)
          insertar_imagen(c, descargar_imagen(fotos.get("BrujulaS3")),     130, 191, 40, 47)

          insertar_imagen(c, descargar_imagen(fotos.get("Fijacion2S3")),      253, 191, 95, 100)
          insertar_imagen(c, descargar_imagen(fotos.get("ConexionesAntenaS3")),     465, 191, 95, 100)

          #Ultima Linea
          insertar_imagen(c, descargar_imagen(fotos.get("TierraS3")), 54, 27, 90, 95)
          insertar_imagen(c, descargar_imagen(fotos.get("InclinometroS2")),    280, 78, 40, 47)
          insertar_imagen(c, descargar_imagen(fotos.get("Distanciometro")),    280, 27, 40, 47)
        
        elif pagina == 11:  
          #encabezado 
          c.setFont("Helvetica", 8)
          c.drawString(355, 710, f"{datos.get('latitud', '')}")
          c.drawString(490, 710, f"{datos.get('longitud', '')}")
          c.drawString(107, 703, f"{datos.get('tipoSitio', '')}")
          c.drawString(470, 703, f"{datos.get('siteModel', '')}")
          
          fotos = datos.get("fotos", {})
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
          altura = datos.get("alturaAntenas", "")
          c.drawString(420, 485, altura)
          c.drawString(420, 465, altura)
          c.drawString(420, 444, altura)

          c.drawString(570, 485, datos.get("azimuthS1", ""))
          c.drawString(570, 465, datos.get("azimuthS2", ""))
          c.drawString(570, 444, datos.get("azimuthS3", ""))
        
        if pagina == 14:  
            c.setFont("Helvetica", 8)
            c.drawString(75, 665, datos.get("fecha", ""))
            c.drawString(313, 665, datos.get("region", ""))
            c.drawString(313, 635, datos.get("nombre", ""))
            c.drawString(560, 635, "NOKIA")  # o datos_site.get("vendor", "NOKIA")

          # Tabla de equipos instalados
            c.setFont("Helvetica", 6)
            y_start = 500
            row_height = 19

            x_desc = 45
            x_modelo = 230
            x_codigo = 380
            x_serial = 499

            fila = 0

            # Sector1, Sector2, Sector3
            for i in range(1, 4):
                sector = datos.get(f"sector{i}", {})
                if sector:
                    y = y_start - fila * row_height
                    c.drawString(x_desc, y, sector.get("descripcion", ""))
                    c.drawString(x_modelo, y, sector.get("modelo", ""))
                    c.drawString(x_codigo, y, sector.get("modelo", ""))
                    c.drawString(x_serial, y, sector.get("serial", ""))
                    fila += 1

            # SFPs
            for s in ["sfpS11", "sfpS12", "sfpS21", "sfpS22", "sfpS31", "sfpS32"]:
                sfp = datos.get(s, {})
                if sfp:
                    y = y_start - fila * row_height
                    c.drawString(x_desc, y, sfp.get("descripcion", ""))
                    c.drawString(x_modelo, y, sfp.get("modelo", ""))
                    c.drawString(x_codigo, y, sfp.get("modelo", ""))
                    c.drawString(x_serial, y, sfp.get("serial", ""))
                    fila += 1

            # FPFH adicional
            fpfh = datos.get("FPFH", {})
            if fpfh:
                y = y_start - fila * row_height
                c.drawString(x_desc, y, fpfh.get("descripcion", "FPFH"))
                c.drawString(x_modelo, y, fpfh.get("modelo", "FPFH"))
                c.drawString(x_codigo, y, fpfh.get("modelo", "FPFH"))
                c.drawString(x_serial, y, fpfh.get("serial", ""))
        
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
