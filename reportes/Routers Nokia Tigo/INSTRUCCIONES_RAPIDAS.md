# 🚀 Instrucciones Rápidas - Exportador de Reportes

## ⚡ Inicio Rápido

### Opción A: Ejecutar con Python (Interfaz Gráfica)

```bash
python exportador_gui.py
```

### Opción B: Ejecutar con Python (Consola)

```bash
python exportar_reportes.py
```

### Opción C: Usar el Ejecutable Windows

1. Doble clic en `ExportadorRoutersNokia.exe`
2. Espera unos segundos a que cargue
3. Selecciona el reporte
4. Click en "Exportar PDF"
5. ¡Listo!

---

## 📋 Uso de la Interfaz Gráfica

### Paso 1: Iniciar
- Ejecuta `python exportador_gui.py`
- La aplicación se conectará automáticamente a Firebase

### Paso 2: Seleccionar Reporte
- Verás una tabla con todos los reportes disponibles
- Haz clic en el reporte que deseas exportar
- La información del reporte aparecerá abajo

### Paso 3: Exportar
- Click en el botón **"📄 Exportar PDF"**
- Elige la ubicación donde guardar el archivo
- Escribe el nombre que prefieras (o usa el sugerido)
- Click en "Guardar"

### Paso 4: Esperar
- Verás el progreso en la barra y en el log
- El proceso tarda entre 30-60 segundos
- Cuando termine verás un mensaje de éxito

---

## 🔧 Solución Rápida de Problemas

### ❌ Error: "No module named 'firebase_admin'"
```bash
pip install -r requirements.txt
```

### ❌ Error: "FileNotFoundError: firebase-credentials.json"
- Asegúrate de tener el archivo `firebase-credentials.json` en la carpeta del proyecto
- Descárgalo desde Firebase Console si no lo tienes

### ❌ Error: "No se pudieron cargar los reportes"
- Verifica tu conexión a internet
- Verifica que las credenciales de Firebase sean correctas

### ❌ Las imágenes en el PDF son todas iguales
- Este es un problema de los datos en Firebase
- Verifica que cada fotografía tenga su propia URL única en Firebase
- Revisa el proceso de carga de imágenes en tu aplicación

---

## 📦 Crear Ejecutable

### Paso 1: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 2: Ejecutar script
```bash
crear_ejecutable.bat
```

### Paso 3: Encontrar el ejecutable
```
📁 dist\ExportadorRoutersNokia.exe
```

### Paso 4: Distribuir
Copia estos archivos juntos:
- ✅ ExportadorRoutersNokia.exe
- ✅ Carpeta plantillas\
- ✅ firebase-credentials.json

---

## 📞 Ayuda Rápida

### Archivos Importantes

| Archivo | Para qué sirve |
|---------|----------------|
| `exportador_gui.py` | Interfaz gráfica principal |
| `exportar_reportes.py` | Script de consola |
| `firebase_config.py` | Configuración de Firebase |
| `firebase-credentials.json` | Credenciales de acceso |
| `plantillas/router*.jpg` | Fondos para el PDF |

### Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar GUI
python exportador_gui.py

# Ejecutar consola
python exportar_reportes.py

# Crear ejecutable
crear_ejecutable.bat

# Ver estructura del proyecto
tree /F
```

---

## ✅ Checklist antes de distribuir

- [ ] Archivo `firebase-credentials.json` está presente
- [ ] Carpeta `plantillas/` contiene las 5 imágenes
- [ ] Se probó el ejecutable en una máquina limpia
- [ ] Las credenciales de Firebase están vigentes
- [ ] Los reportes en Firebase tienen URLs de imágenes únicas

---

**¿Problemas?** Revisa el archivo `README.md` completo para más detalles.










