# ReporteEricsson - Generador de Reportes PDF desde Firebase

## 📋 Descripción

**ReporteEricsson** es un programa Python que genera reportes PDF exportando datos desde Firebase Firestore. El sistema genera reportes técnicos completos para enlaces Ericsson Tigo, incluyendo información de sitios, configuraciones, mediciones, inventarios y fotografías.

## 🏗️ Arquitectura del Proyecto

### Estructura de Directorios

```
ReporteEricsson/
├── main.py                          # Punto de entrada principal
├── generar_reporte_ericsson.py      # Lógica de generación de PDF
├── firebase_config.py               # Configuración de Firebase/Firestore
├── export.py                        # Utilidad para exportar documentos a JSON
├── firebase-key.json                # Credenciales de Firebase (NO COMMITEAR)
├── plantillas/                      # Plantillas de imágenes (r1.jpg - r34.jpg)
│   └── r*.jpg
├── r*.jpg                           # Imágenes de plantilla (34 páginas)
└── tigo new.xlsx                    # Archivo Excel de referencia
```

## 🔧 Dependencias

### Librerías Python Requeridas

```txt
firebase-admin          # SDK de Firebase para Python
reportlab              # Generación de PDFs
Pillow (PIL)           # Procesamiento de imágenes
requests               # Descarga de imágenes remotas
google-cloud-firestore # Cliente de Firestore
```

### Instalación

```bash
pip install firebase-admin reportlab Pillow requests google-cloud-firestore
```

O crear un archivo `requirements.txt`:

```txt
firebase-admin>=6.0.0
reportlab>=3.6.0
Pillow>=9.0.0
requests>=2.28.0
google-cloud-firestore>=2.10.0
```

## 📦 Componentes Principales

### 1. `main.py`
Punto de entrada del programa. Define los IDs de documentos a procesar y genera los PDFs correspondientes.

**Uso:**
```python
documento_ids = ["0OOFHWP2w3aCwGggN5ww"]
for doc_id in documento_ids:
    generar_pdf_ericsson(doc_id, f"reporte_ericsson_{doc_id}.pdf")
```

### 2. `firebase_config.py`
Módulo de configuración de Firebase. Inicializa la conexión con Firestore usando las credenciales del archivo `firebase-key.json`.

**Funciones:**
- `init_firestore()`: Inicializa y retorna el cliente de Firestore

### 3. `generar_reporte_ericsson.py`
Módulo principal que contiene la lógica de generación del PDF.

**Funciones principales:**
- `generar_pdf_ericsson(document_id, salida_pdf)`: Genera el PDF completo
- `insertar_imagen_remota(canvas_obj, url, x, y, width, height, nombre_temp)`: Descarga e inserta imágenes desde URLs

**Estructura del PDF generado:**
- **34 páginas** en total
- Páginas 1-4: Datos generales, carátula, path calculator, profile
- Páginas 5-10: Configuraciones de frecuencias (Site A y Site B)
- Páginas 11-12: Mediciones (Site A y Site B)
- Páginas 13-16: Discriminaciones (Site A y Site B)
- Páginas 17-18: Inventarios (Site A y Site B)
- Páginas 19-20: Performance (Site A y Site B)
- Páginas 21-22: Licencias (Site A y Site B)
- Páginas 23-24: BER Test y Prueba RFC
- Páginas 25-29: Fotografías Site A (Torre y Piso)
- Páginas 30-34: Fotografías Site B (Torre y Piso)

### 4. `export.py`
Utilidad para exportar documentos de Firestore a JSON. Útil para debugging y análisis de datos.

## 🔥 Estructura de Datos en Firestore

El programa espera documentos en la colección `reportesEnlacesEricssonTigo` con la siguiente estructura:

### Campos en la Raíz del Documento

```json
{
  "DatosGenerales": {
    "SitioA": "string",
    "SitioB": "string"
  },
  "cantidadAntenas": 2,  // ⭐ NUEVO: Cantidad de antenas (1-4)
  "cantidadOdus": 4,     // ⭐ NUEVO: Cantidad de ODUs (1-8)
  "Generales": {
    "Caratula": "URL",
    "PathCalculator": "URL",
    "Profile": "URL"
  },
  "SiteACapturas": {
    "configFrec1": "URL",
    "configFrec2": "URL",
    "configFrec3": "URL",
    "mediciones": "URL",
    "discriminacion1": "URL",
    "discriminacion2": "URL",
    "inventario": "URL",
    "performance": "URL",
    "licencia": "URL"
  },
  "SiteBCapturas": {
    "configFrec1": "URL",
    "configFrec2": "URL",
    "configFrec3": "URL",
    "mediciones": "URL",
    "discriminacion1": "URL",
    "discriminacion2": "URL",
    "inventario": "URL",
    "performance": "URL",
    "licencia": "URL",
    "berTest": "URL",
    "pruebaRFC": "URL"
  },
```

### Estructura Dinámica de SiteATorre y SiteBTorre

**IMPORTANTE:** Los campos de antenas y ODUs ahora son **dinámicos y numerados** según `cantidadAntenas` y `cantidadOdus`.

#### Estructura Nueva (Recomendada)

```json
  "SiteATorre": {
    // Campos comunes (sin cambios)
    "lineaVista": "URL",
    "etiquetadoAntena": "URL",
    "barraTierraGroundingKit": "URL",
    "groundingKit": "URL",
    "aterrizajeOduPlatina": "URL",
    "etiquetaCableCoax": "URL",
    "verticeAntenaTorre": "URL",
    "sitioGeneral": "URL",
    
    // Antenas dinámicas (hasta 4, según cantidadAntenas)
    "fijacionAntena1": "URL",  // ✅ CON número
    "SerieAntena1": "URL",       // ✅ CON número
    "fijacionAntena2": "URL",    // Si cantidadAntenas >= 2
    "SerieAntena2": "URL",       // Si cantidadAntenas >= 2
    // ... hasta fijacionAntena4 y SerieAntena4
    
    // ODUs dinámicas (hasta 8, según cantidadOdus)
    "ConexionOdu1": "URL",       // ✅ CON número, mayúscula
    "etiquetaRadio1": "URL",     // ✅ CON número
    "serieOdu1": "URL",          // ✅ CON número
    "aterrizajeOdu1": "URL",     // ✅ CON número
    "ConexionOdu2": "URL",       // Si cantidadOdus >= 2
    "etiquetaRadio2": "URL",     // Si cantidadOdus >= 2
    "serieOdu2": "URL",          // Si cantidadOdus >= 2
    "aterrizajeOdu2": "URL",     // Si cantidadOdus >= 2
    // ... hasta ConexionOdu8, etiquetaRadio8, serieOdu8, aterrizajeOdu8
  },
```

#### Compatibilidad con Estructura Antigua

El sistema mantiene **compatibilidad hacia atrás** con documentos antiguos que usan campos sin numeración:

```json
  "SiteATorre": {
    // Estructura antigua (aún soportada)
    "fijacionAntena": "URL",     // Se mapea a fijacionAntena1
    "SerieAntena": "URL",         // Se mapea a SerieAntena1
    "conexionOdu": "URL",         // Se mapea a ConexionOdu1 (minúscula)
    "etiquetaRadio": "URL",       // Se mapea a etiquetaRadio1
    "aterrizajeOdu": "URL",       // Se mapea a aterrizajeOdu1
    // ... otros campos comunes
  },
  "SiteAPiso": {
    "pasamuros": "URL",
    "idu": "URL",
    "etiquetaIdu": "URL",
    "serieMagazine": "URL",
    "etiquetaCableAlimentacion": "URL",
    "panelBreakers": "URL",
    "fibra1": "URL",
    "fibra2": "URL",
    "aterrizajeIdu": "URL",
    "arrestores": "URL",
    "gabineteAbierto": "URL",
    "shelter": "URL"
  },
  "SiteBTorre": { /* Similar a SiteATorre */ },
  "SiteBPiso": { /* Similar a SiteAPiso */ }
}
```

## 🚀 Uso

### Ejecución Básica

```bash
cd ReporteEricsson
python main.py
```

### Personalizar Documentos a Procesar

Editar `main.py` y modificar la lista `documento_ids`:

```python
documento_ids = [
    "ID_DOCUMENTO_1",
    "ID_DOCUMENTO_2",
    "ID_DOCUMENTO_3"
]
```

### Exportar Documento a JSON

```bash
python export.py
```

Modificar `export.py` para cambiar la colección, documento y archivo de salida.

## 📁 Archivos de Plantilla

El proyecto utiliza 34 imágenes de plantilla (r1.jpg a r34.jpg) que sirven como fondo para cada página del PDF. Estas imágenes deben estar presentes en el directorio `ReporteEricsson/` o en `plantillas/`.

**Nota:** Las imágenes también están duplicadas en el directorio raíz y en `plantillas/`. Se recomienda mantener una única ubicación para evitar confusión.

## 🔐 Seguridad

⚠️ **IMPORTANTE:** El archivo `firebase-key.json` contiene credenciales sensibles. 

- **NO** debe ser commiteado a repositorios públicos
- **NO** debe ser compartido
- Debe estar en `.gitignore`

## 🐛 Troubleshooting

### Error: "Documento no encontrado"
- Verificar que el ID del documento existe en Firestore
- Verificar que la colección es `reportesEnlacesEricssonTigo`
- Verificar conexión a Firebase

### Error: "Imagen rX.jpg no encontrada"
- Verificar que todas las imágenes de plantilla (r1.jpg - r34.jpg) están presentes
- Verificar la ruta de trabajo del script

### Error: "Error al insertar imagen remota"
- Verificar conectividad a internet
- Verificar que las URLs en Firestore son válidas y accesibles
- Algunas URLs pueden requerir autenticación

### Error de Firebase
- Verificar que `firebase-key.json` existe y es válido
- Verificar permisos de la cuenta de servicio en Firebase Console

## 📝 Notas de Desarrollo

- El código utiliza coordenadas en centímetros para posicionar elementos
- Las imágenes remotas se descargan temporalmente y se eliminan después de insertarse
- El formato de página es `letter` (8.5 x 11 pulgadas)
- Las imágenes se escalan manteniendo proporción 16:9 cuando aplica

## 🔄 Cambios Recientes en la Estructura de Datos

### Soporte para Múltiples Antenas y ODUs

El sistema ahora soporta **estructura dinámica** para antenas y ODUs:

- **Antenas:** Hasta 4 antenas por sitio (configurable con `cantidadAntenas`)
- **ODUs:** Hasta 8 ODUs por sitio (configurable con `cantidadOdus`)
- **Campos numerados:** Los campos ahora incluyen números (ej: `fijacionAntena1`, `ConexionOdu1`)
- **Compatibilidad hacia atrás:** El sistema detecta automáticamente documentos antiguos y los mapea a la nueva estructura

### Funciones Auxiliares

El código incluye funciones para manejar la nueva estructura:

- `obtener_antenas(sitio_torre, cantidad_antenas)`: Obtiene antenas con compatibilidad hacia atrás
- `obtener_odus(sitio_torre, cantidad_odus)`: Obtiene ODUs con compatibilidad hacia atrás

Estas funciones buscan primero campos numerados (estructura nueva) y luego campos antiguos si no encuentran los nuevos.

### Mapeo de Campos Antiguos a Nuevos

| Campo Antiguo | Campo Nuevo |
|---------------|-------------|
| `fijacionAntena` | `fijacionAntena1` |
| `SerieAntena` | `SerieAntena1` |
| `conexionOdu` | `ConexionOdu1` (mayúscula) |
| `etiquetaRadio` | `etiquetaRadio1` |
| `aterrizajeOdu` | `aterrizajeOdu1` |
| `serieOdu1` | Se mantiene igual |

## 🔄 Flujo de Trabajo

1. **Preparación:**
   - Asegurar que `firebase-key.json` está presente
   - Verificar que todas las plantillas (r1.jpg - r34.jpg) están disponibles

2. **Configuración:**
   - Editar `main.py` con los IDs de documentos a procesar

3. **Ejecución:**
   - Ejecutar `python main.py`

4. **Resultado:**
   - Se generan archivos PDF con el formato `reporte_ericsson_{document_id}.pdf`

## 📊 Colección de Firestore

- **Colección:** `reportesEnlacesEricssonTigo`
- **Tipo:** Documentos individuales identificados por ID

## 🛠️ Mejoras Futuras Sugeridas

- [ ] Refactorizar código repetitivo en bucles
- [ ] Agregar manejo de errores más robusto
- [ ] Implementar logging estructurado
- [ ] Agregar validación de datos antes de generar PDF
- [ ] Crear archivo `requirements.txt`
- [ ] Agregar tests unitarios
- [ ] Optimizar descarga de imágenes (cache, paralelización)
- [ ] Agregar soporte para múltiples formatos de salida
- [ ] Crear CLI con argumentos de línea de comandos

## 📄 Licencia

Este proyecto es de uso interno para generación de reportes técnicos de Ericsson Tigo.

---

**Última actualización:** 2025
**Versión:** 1.0

