"""
Script para descargar todas las imágenes de un reporte de Ericsson desde Firebase.
Descarga las imágenes en una carpeta organizada por secciones.
"""

import os
import requests
from firebase_config import init_firestore


def descargar_imagen(url, ruta_destino):
    """
    Descarga una imagen desde una URL y la guarda en la ruta especificada.
    
    Args:
        url: URL de la imagen
        ruta_destino: Ruta completa donde guardar la imagen
    
    Returns:
        True si la descarga fue exitosa, False en caso contrario
    """
    if not url or not url.startswith("http"):
        return False
    
    try:
        response = requests.get(url, timeout=(10, 30), stream=True)
        if response.ok:
            # Verificar que sea una imagen
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                return False
            
            # Crear directorio si no existe
            directorio = os.path.dirname(ruta_destino)
            if directorio:
                os.makedirs(directorio, exist_ok=True)
            
            # Descargar imagen
            with open(ruta_destino, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return True
        else:
            return False
    
    except requests.exceptions.Timeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        return False


def obtener_antenas(sitio_torre, cantidad_antenas):
    """Obtiene las antenas del sitio con compatibilidad hacia atrás."""
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
    """Obtiene las ODUs del sitio con compatibilidad hacia atrás."""
    odus = []
    
    # Intentar leer estructura nueva primero (campos numerados)
    for i in range(1, cantidad_odus + 1):
        # Buscar con mayúscula (estructura nueva)
        conexion = sitio_torre.get(f"ConexionOdu{i}", "").strip()
        # Si no existe con mayúscula, intentar minúscula (solo para i=1, compatibilidad)
        if not conexion and i == 1:
            conexion = sitio_torre.get("conexionOdu", "").strip()
        
        etiqueta = sitio_torre.get(f"etiquetaRadio{i}", "").strip()
        if not etiqueta and i == 1:
            etiqueta = sitio_torre.get("etiquetaRadio", "").strip()
        
        serie = sitio_torre.get(f"serieOdu{i}", "").strip()
        if not serie and i == 1:
            serie = sitio_torre.get("serieOdu", "").strip()
        
        aterrizaje = sitio_torre.get(f"aterrizajeOdu{i}", "").strip()
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
        serie_antigua = sitio_torre.get("serieOdu1", "").strip()
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


def descargar_imagenes_reporte(document_id, carpeta_salida=None):
    """
    Descarga todas las imágenes de un reporte desde Firebase.
    
    Args:
        document_id: ID del documento en Firestore
        carpeta_salida: Carpeta donde guardar las imágenes (default: imagenes_{document_id})
    """
    if not carpeta_salida:
        carpeta_salida = f"imagenes_{document_id}"
    
    print(f"🔄 Iniciando descarga de imágenes para documento: {document_id}")
    print(f"📁 Las imágenes se guardarán en: {carpeta_salida}/\n")
    
    # Conectar a Firebase
    db = init_firestore()
    doc_ref = db.collection("reportesEnlacesEricssonTigo").document(document_id)
    doc = doc_ref.get()
    
    if not doc.exists:
        print(f"⚠️ Documento {document_id} no encontrado.")
        return
    
    datos = doc.to_dict()
    datos_generales = datos.get("DatosGenerales", {})
    sitio_a = datos_generales.get("SitioA", "SiteA")
    sitio_b = datos_generales.get("SitioB", "SiteB")
    
    # Leer cantidades
    cantidad_antenas = datos.get("cantidadAntenas", 1)
    cantidad_odus = datos.get("cantidadOdus", 1)
    cantidad_antenas = max(1, min(4, cantidad_antenas))
    cantidad_odus = max(1, min(8, cantidad_odus))
    
    print(f"📊 Configuración: {cantidad_antenas} antena(s), {cantidad_odus} ODU(s)\n")
    
    contador_imagenes = 0
    contador_exitosas = 0
    
    # ===== SECCIÓN: GENERALES =====
    print("📸 Descargando imágenes Generales...")
    generales = datos.get("Generales", {})
    campos_generales = ["Caratula", "PathCalculator", "Profile"]
    
    for campo in campos_generales:
        url = generales.get(campo, "").strip()
        if url.startswith("http"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "Generales", f"{campo}.jpg")
            if descargar_imagen(url, ruta):
                contador_exitosas += 1
                print(f"  ✅ {campo}")
            else:
                print(f"  ❌ {campo}")
    
    # ===== SECCIÓN: SITE A CAPTURAS =====
    print("\n📸 Descargando imágenes SiteACapturas...")
    site_a_capturas = datos.get("SiteACapturas", {})
    campos_capturas_a = [
        "configFrec1", "configFrec2", "configFrec3",
        "mediciones", "discriminacion1", "discriminacion2",
        "inventario", "performance", "licencia"
    ]
    
    for campo in campos_capturas_a:
        url = site_a_capturas.get(campo, "").strip()
        if url.startswith("http"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteACapturas", f"{campo}.jpg")
            if descargar_imagen(url, ruta):
                contador_exitosas += 1
                print(f"  ✅ {campo}")
            else:
                print(f"  ❌ {campo}")
    
    # ===== SECCIÓN: SITE B CAPTURAS =====
    print("\n📸 Descargando imágenes SiteBCapturas...")
    site_b_capturas = datos.get("SiteBCapturas", {})
    campos_capturas_b = [
        "configFrec1", "configFrec2", "configFrec3",
        "mediciones", "discriminacion1", "discriminacion2",
        "inventario", "performance", "licencia",
        "berTest", "pruebaRFC"
    ]
    
    for campo in campos_capturas_b:
        url = site_b_capturas.get(campo, "").strip()
        if url.startswith("http"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBCapturas", f"{campo}.jpg")
            if descargar_imagen(url, ruta):
                contador_exitosas += 1
                print(f"  ✅ {campo}")
            else:
                print(f"  ❌ {campo}")
    
    # ===== SECCIÓN: SITE A TORRE =====
    print("\n📸 Descargando imágenes SiteATorre...")
    site_a_torre = datos.get("SiteATorre", {})
    
    # Campos comunes
    campos_comunes_torre = [
        "lineaVista", "etiquetadoAntena", "etiquetaCableCoax",
        "groundingKit", "barraTierraGroundingKit", "aterrizajeOduPlatina",
        "verticeAntenaTorre", "sitioGeneral"
    ]
    
    for campo in campos_comunes_torre:
        url = site_a_torre.get(campo, "").strip()
        if url.startswith("http"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteATorre", f"{campo}.jpg")
            if descargar_imagen(url, ruta):
                contador_exitosas += 1
                print(f"  ✅ {campo}")
    
    # Antenas dinámicas
    antenas = obtener_antenas(site_a_torre, cantidad_antenas)
    for antena in antenas:
        num = antena["numero"]
        if antena.get("fijacionAntena"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteATorre", f"fijacionAntena{num}.jpg")
            if descargar_imagen(antena["fijacionAntena"], ruta):
                contador_exitosas += 1
                print(f"  ✅ fijacionAntena{num}")
        
        if antena.get("SerieAntena"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteATorre", f"SerieAntena{num}.jpg")
            if descargar_imagen(antena["SerieAntena"], ruta):
                contador_exitosas += 1
                print(f"  ✅ SerieAntena{num}")
    
    # ODUs dinámicas
    odus = obtener_odus(site_a_torre, cantidad_odus)
    for odu in odus:
        num = odu["numero"]
        if odu.get("ConexionOdu"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteATorre", f"ConexionOdu{num}.jpg")
            if descargar_imagen(odu["ConexionOdu"], ruta):
                contador_exitosas += 1
                print(f"  ✅ ConexionOdu{num}")
        
        if odu.get("etiquetaRadio"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteATorre", f"etiquetaRadio{num}.jpg")
            if descargar_imagen(odu["etiquetaRadio"], ruta):
                contador_exitosas += 1
                print(f"  ✅ etiquetaRadio{num}")
        
        if odu.get("serieOdu"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteATorre", f"serieOdu{num}.jpg")
            if descargar_imagen(odu["serieOdu"], ruta):
                contador_exitosas += 1
                print(f"  ✅ serieOdu{num}")
        
        if odu.get("aterrizajeOdu"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteATorre", f"aterrizajeOdu{num}.jpg")
            if descargar_imagen(odu["aterrizajeOdu"], ruta):
                contador_exitosas += 1
                print(f"  ✅ aterrizajeOdu{num}")
    
    # ===== SECCIÓN: SITE A PISO =====
    print("\n📸 Descargando imágenes SiteAPiso...")
    site_a_piso = datos.get("SiteAPiso", {})
    campos_piso_a = [
        "pasamuros", "idu", "etiquetaIdu", "serieMagazine",
        "etiquetaCableAlimentacion", "panelBreakers", "fibra1", "fibra2",
        "aterrizajeIdu", "arrestores", "gabineteAbierto", "shelter"
    ]
    
    for campo in campos_piso_a:
        url = site_a_piso.get(campo, "").strip()
        if url.startswith("http"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteAPiso", f"{campo}.jpg")
            if descargar_imagen(url, ruta):
                contador_exitosas += 1
                print(f"  ✅ {campo}")
    
    # ===== SECCIÓN: SITE B TORRE =====
    print("\n📸 Descargando imágenes SiteBTorre...")
    site_b_torre = datos.get("SiteBTorre", {})
    
    # Campos comunes
    for campo in campos_comunes_torre:
        url = site_b_torre.get(campo, "").strip()
        if url.startswith("http"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBTorre", f"{campo}.jpg")
            if descargar_imagen(url, ruta):
                contador_exitosas += 1
                print(f"  ✅ {campo}")
    
    # Antenas dinámicas
    antenas = obtener_antenas(site_b_torre, cantidad_antenas)
    for antena in antenas:
        num = antena["numero"]
        if antena.get("fijacionAntena"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBTorre", f"fijacionAntena{num}.jpg")
            if descargar_imagen(antena["fijacionAntena"], ruta):
                contador_exitosas += 1
                print(f"  ✅ fijacionAntena{num}")
        
        if antena.get("SerieAntena"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBTorre", f"SerieAntena{num}.jpg")
            if descargar_imagen(antena["SerieAntena"], ruta):
                contador_exitosas += 1
                print(f"  ✅ SerieAntena{num}")
    
    # ODUs dinámicas
    odus = obtener_odus(site_b_torre, cantidad_odus)
    for odu in odus:
        num = odu["numero"]
        if odu.get("ConexionOdu"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBTorre", f"ConexionOdu{num}.jpg")
            if descargar_imagen(odu["ConexionOdu"], ruta):
                contador_exitosas += 1
                print(f"  ✅ ConexionOdu{num}")
        
        if odu.get("etiquetaRadio"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBTorre", f"etiquetaRadio{num}.jpg")
            if descargar_imagen(odu["etiquetaRadio"], ruta):
                contador_exitosas += 1
                print(f"  ✅ etiquetaRadio{num}")
        
        if odu.get("serieOdu"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBTorre", f"serieOdu{num}.jpg")
            if descargar_imagen(odu["serieOdu"], ruta):
                contador_exitosas += 1
                print(f"  ✅ serieOdu{num}")
        
        if odu.get("aterrizajeOdu"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBTorre", f"aterrizajeOdu{num}.jpg")
            if descargar_imagen(odu["aterrizajeOdu"], ruta):
                contador_exitosas += 1
                print(f"  ✅ aterrizajeOdu{num}")
    
    # ===== SECCIÓN: SITE B PISO =====
    print("\n📸 Descargando imágenes SiteBPiso...")
    site_b_piso = datos.get("SiteBPiso", {})
    
    for campo in campos_piso_a:
        url = site_b_piso.get(campo, "").strip()
        if url.startswith("http"):
            contador_imagenes += 1
            ruta = os.path.join(carpeta_salida, "SiteBPiso", f"{campo}.jpg")
            if descargar_imagen(url, ruta):
                contador_exitosas += 1
                print(f"  ✅ {campo}")
    
    # ===== RESUMEN =====
    print("\n" + "="*50)
    print(f"✅ Descarga completada!")
    print(f"📊 Total de imágenes encontradas: {contador_imagenes}")
    print(f"✅ Imágenes descargadas exitosamente: {contador_exitosas}")
    print(f"❌ Imágenes fallidas: {contador_imagenes - contador_exitosas}")
    print(f"📁 Imágenes guardadas en: {carpeta_salida}/")
    print("="*50)


if __name__ == "__main__":
    # Configurar IDs de documentos a descargar
    # Cambia este ID por el documento que quieras descargar
    documento_ids = [
        "dfYPsmdPSD6I7BGRMK7U"  # Cambia este ID según necesites
    ]
    
    for doc_id in documento_ids:
        descargar_imagenes_reporte(doc_id)
        print()  # Línea en blanco entre documentos
