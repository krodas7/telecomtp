# 📊 Exportador de Reportes Routers Nokia

Sistema automatizado para exportar reportes de instalación de routers Nokia desde Firebase a documentos PDF profesionales con interfaz gráfica.

## 📋 Descripción

Este proyecto genera reportes PDF de instalaciones de routers Nokia Tigo, tomando los datos almacenados en Firebase Firestore y aplicándolos sobre plantillas prediseñadas. El sistema descarga automáticamente las fotografías desde Firebase Storage y las integra en el documento final.

## ✨ Características

- 🖥️ **Interfaz Gráfica (GUI)**: Aplicación de escritorio fácil de usar
- 🔥 **Conexión con Firebase**: Sincronización automática con Firestore
- 📄 **Generación de PDF**: Reportes profesionales de 5 páginas
- 🖼️ **Gestión de imágenes**: Descarga automática de fotografías desde Firebase Storage
- 💾 **Guardar personalizado**: Elige dónde y con qué nombre guardar el PDF
- 📊 **Plantillas personalizadas**: Diseño específico para routers Nokia
- ✅ **Encoding UTF-8**: Soporte completo para caracteres especiales
- 📦 **Ejecutable Windows**: Distribuible sin necesidad de instalar Python

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- Acceso a un proyecto de Firebase con Firestore
- Archivo de credenciales de Firebase

### 1. Clonar o descargar el proyecto

```bash
cd C:\xampp\htdocs\router-nokia
```

### 2. Instalar dependencias

```bash
pip install firebase-admin reportlab requests
```

### 3. Configurar Firebase

#### a) Obtener credenciales de Firebase

1. Ve a [Firebase Console](https://console.firebase.google.com/)
2. Selecciona tu proyecto
3. Click en ⚙️ → **Configuración del proyecto**
4. Ve a la pestaña **Cuentas de servicio**
5. Click en **Generar nueva clave privada**
6. Descarga el archivo JSON

#### b) Configurar credenciales

1. Guarda el archivo JSON descargado en la carpeta del proyecto
2. Renómbralo como `firebase-credentials.json`
3. Si usas otro nombre, edita `firebase_config.py` línea 18:

```python
cred = credentials.Certificate('tu-nombre-de-archivo.json')
```

## 📁 Estructura del Proyecto

```
router-nokia/
│
├── exportar_reportes.py          # Script principal
├── firebase_config.py             # Configuración de Firebase
├── firebase-credentials.json      # Credenciales (no subir a Git)
│
├── plantillas/                    # Plantillas de fondo para PDF
│   ├── router1.jpg               # Página 1
│   ├── router2.jpg               # Página 2
│   ├── router3.JPG               # Página 3
│   ├── router4.jpg               # Página 4
│   └── router5.jpg               # Página 5
│
├── reporte_*.pdf                  # PDFs generados
└── README.md                      # Este archivo
```

## 🎯 Uso

### Opción 1: Interfaz Gráfica (Recomendado)

Ejecuta la aplicación con interfaz gráfica:

```bash
python exportador_gui.py
```

**Interfaz incluye:**
- 📋 Lista de todos los reportes disponibles en Firebase
- 🔍 Información detallada del reporte seleccionado
- 💾 Diálogo para elegir dónde guardar el PDF
- 📊 Barra de progreso y log de estado en tiempo real
- 🔄 Botón para actualizar la lista de reportes

**Flujo de trabajo:**
1. La aplicación se conecta automáticamente a Firebase
2. Muestra todos los reportes en una tabla
3. Haz clic en el reporte que deseas exportar
4. Click en "📄 Exportar PDF"
5. Elige dónde guardar el archivo y con qué nombre
6. ¡Listo! El PDF se genera automáticamente

### Opción 2: Línea de Comandos

Ejecuta el script de consola:

```bash
python exportar_reportes.py
```

**Flujo de trabajo:**
1. El sistema se conecta a Firebase y lista todos los reportes
2. Muestra información de cada reporte
3. Selecciona el reporte escribiendo el número correspondiente
4. El PDF se genera automáticamente

### Ejemplo de ejecución

```
============================================================
📊 EXPORTADOR DE REPORTES ROUTERS TIGO
============================================================

🔄 Conectando a Firebase y cargando reportes...

✅ Se encontraron 3 reportes disponibles:

1. 📍 Gatuncillo
   ID Sitio: 403004
   Reporte: Final
   Fecha: 2025-04-21
   Doc ID: 123r91j9d

2. 📍 Las Perlas
   ID Sitio: 403005
   Reporte: Inicial
   Fecha: 2025-04-22
   Doc ID: 456abc789

Selecciona el número del reporte a exportar (1-2) o 'q' para salir: 1

📝 Generando PDF para: Gatuncillo
📄 Archivo de salida: reporte_Gatuncillo_123r91j9.pdf
⏳ Por favor espera...

✅ PDF generado correctamente: reporte_Gatuncillo_123r91j9.pdf

🎉 ¡Exportación completada!
```

## 📄 Estructura del PDF Generado

El PDF generado contiene **5 páginas**:

### Página 1 - Información General
- Datos del autor y contratista
- Fecha y número de reporte
- Ubicación y coordenadas GPS
- ID del sitio
- MDI utilizado
- Protocolo y coordinador
- 6 fotografías: breaker, conexiones a tierra, etiquetas

### Página 2 - Documentación Visual
- 8 fotografías adicionales:
  - Etiquetas de fibra
  - ODF sitio conectante
  - Router nuevo
  - Switch sitio conectante
  - Gabinete general
  - Serie y ubicación

### Página 3 - Condiciones Eléctricas
- Fuente A:
  - Calibre de cable
  - Capacidad del breaker
  - Identificación del equipo
  - Identificación del rectificador
- Fuente B: (mismos campos)

### Página 4 - Inventario
- Tabla con hasta 23 equipos:
  - Descripción
  - Número de parte
  - Número de serie
  - Posición

### Página 5 - Posiciones de Fibra Óptica
- Tabla con hasta 20 registros:
  - Descripción
  - Puerto de origen
  - Destino (hacia)
  - Puerto
  - Servicio

## 🔧 Configuración Avanzada

### Modificar la colección de Firebase

Por defecto, el sistema consulta la colección `instalacionesRoutersTigo`. Para cambiarla, edita las líneas correspondientes en `exportar_reportes.py`:

```python
coleccion = db.collection("tu-coleccion")
```

### Ajustar posiciones en el PDF

Las coordenadas de texto e imágenes se definen en centímetros. Por ejemplo:

```python
c.drawString(5.4 * cm, 24.07 * cm, datos.get("autor", ""))
```

Para ajustar, modifica los valores numéricos según necesites.

## 🔒 Seguridad

⚠️ **IMPORTANTE**: 

- **NUNCA** subas el archivo `firebase-credentials.json` a repositorios públicos
- Agrega `firebase-credentials.json` a tu `.gitignore`:

```gitignore
# Credenciales de Firebase
firebase-credentials.json
*-firebase-adminsdk-*.json

# PDFs generados
reporte_*.pdf
```

## 🐛 Solución de Problemas

### Error: "Module 'firebase_admin' not found"
```bash
pip install firebase-admin
```

### Error: "No module named 'reportlab'"
```bash
pip install reportlab
```

### Error: "Documento no encontrado"
- Verifica que el ID del documento existe en Firebase
- Confirma que la colección sea la correcta

### Error de encoding en Windows
El script ya incluye soporte UTF-8 para Windows. Si persiste el error, ejecuta:
```bash
chcp 65001
python exportar_reportes.py
```

### Imágenes de plantilla no encontradas
Asegúrate de que las imágenes estén en la carpeta `plantillas/`:
- router1.jpg
- router2.jpg
- router3.JPG
- router4.jpg
- router5.jpg

## 📦 Crear Ejecutable de Windows

Para crear un archivo `.exe` que puedas distribuir sin necesidad de instalar Python:

### 1. Ejecutar el script de compilación

```bash
crear_ejecutable.bat
```

### 2. Resultado

El ejecutable se generará en:
```
dist\ExportadorRoutersNokia.exe
```

### 3. Distribución

Para distribuir la aplicación, necesitas copiar:
- ✅ `ExportadorRoutersNokia.exe` (el ejecutable)
- ✅ Carpeta `plantillas\` (las imágenes de fondo)
- ✅ `firebase-credentials.json` (las credenciales)

**Estructura para distribución:**
```
ExportadorRoutersNokia/
├── ExportadorRoutersNokia.exe
├── firebase-credentials.json
└── plantillas/
    ├── router1.jpg
    ├── router2.jpg
    ├── router3.JPG
    ├── router4.jpg
    └── router5.jpg
```

### Notas sobre el ejecutable

- ⚡ El ejecutable tarda unos segundos en iniciar (normal en PyInstaller)
- 💾 Tamaño aproximado: 40-60 MB
- 🖥️ Compatible con Windows 10/11
- 🔒 Requiere las credenciales de Firebase en la misma carpeta

## 📦 Dependencias

```
firebase-admin>=6.8.0
reportlab>=4.0.0
requests>=2.31.0
Pillow>=10.0.0
pyinstaller>=6.0.0
```

## 🤝 Contribuir

Si deseas mejorar este proyecto:

1. Realiza un fork del repositorio
2. Crea una rama para tu feature (`git checkout -b feature/mejora`)
3. Haz commit de tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📝 Notas

- Los PDFs se generan en el directorio raíz del proyecto
- Las imágenes temporales se eliminan automáticamente después de ser insertadas
- El sistema valida que las URLs de imágenes comiencen con "http"
- Compatible con Windows, macOS y Linux

## 📧 Contacto

Para preguntas o soporte sobre este proyecto, contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto es de uso interno para la gestión de instalaciones de routers Nokia.

---

**Desarrollado para:** Instalaciones Routers Tigo  
**Última actualización:** Octubre 2025  
**Versión:** 1.0.0

