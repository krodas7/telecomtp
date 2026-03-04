import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from firebase_config import init_firestore
from exportar_reportes import generar_pdf_routers_tigo
from login_gui import LoginGUI

class ExportadorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Exportador de Reportes Routers Nokia - Tigo")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Paleta de colores profesional azul
        self.colors = {
            'primary': '#0052CC',          # Azul principaL
            'primary_dark': '#003D99',     # Azul oscuro
            'primary_light': '#4C9AFF',    # Azul claro
            'secondary': '#0065FF',        # Azul secundario
            'accent': '#00C7E6',           # Azul acento/cyan
            'background': '#F4F6F9',       # Gris azulado claro
            'surface': '#FFFFFF',          # Blanco
            'surface_dark': '#E9EEF5',     # Gris claro
            'text': '#172B4D',             # Texto oscuro
            'text_secondary': '#5E6C84',   # Texto secundario
            'success': '#00875A',          # Verde
            'warning': '#FF8B00',          # Naranja
            'error': '#DE350B',            # Rojo
            'border': '#DFE1E6',           # Borde
        }
        
        # Configurar fondo principal
        self.root.configure(bg=self.colors['background'])
        
        # Variables
        self.reportes = []
        self.reporte_seleccionado = None
        
        # Configurar estilos personalizados
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar reportes al inicio
        self.root.after(100, self.cargar_reportes)
    
    def configurar_estilos(self):
        """Configurar estilos personalizados profesionales"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar colores del Treeview
        style.configure("Treeview",
            background=self.colors['surface'],
            foreground=self.colors['text'],
            rowheight=35,
            fieldbackground=self.colors['surface'],
            borderwidth=0,
            font=('Segoe UI', 10)
        )
        
        style.configure("Treeview.Heading",
            background=self.colors['primary'],
            foreground='white',
            relief='flat',
            font=('Segoe UI', 10, 'bold')
        )
        
        style.map('Treeview.Heading',
            background=[('active', self.colors['primary_dark'])]
        )
        
        style.map('Treeview',
            background=[('selected', self.colors['primary_light'])],
            foreground=[('selected', 'white')]
        )
        
        # Estilo para botones primarios
        style.configure("Primary.TButton",
            background=self.colors['primary'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 10)
        )
        
        style.map("Primary.TButton",
            background=[('active', self.colors['primary_dark']), 
                       ('disabled', self.colors['border'])],
            foreground=[('disabled', self.colors['text_secondary'])]
        )
        
        # Estilo para botones secundarios
        style.configure("Secondary.TButton",
            background=self.colors['surface'],
            foreground=self.colors['primary'],
            borderwidth=1,
            focuscolor='none',
            font=('Segoe UI', 10, 'bold'),
            padding=(20, 10)
        )
        
        style.map("Secondary.TButton",
            background=[('active', self.colors['surface_dark'])],
            foreground=[('active', self.colors['primary_dark'])]
        )
        
        # Estilo para LabelFrame
        style.configure("TLabelframe",
            background=self.colors['surface'],
            borderwidth=1,
            relief='solid',
            bordercolor=self.colors['border']
        )
        
        style.configure("TLabelframe.Label",
            background=self.colors['surface'],
            foreground=self.colors['text'],
            font=('Segoe UI', 10, 'bold')
        )
        
        # Estilo para Frame
        style.configure("TFrame",
            background=self.colors['background']
        )
        
        # Estilo para Progressbar
        style.configure("TProgressbar",
            background=self.colors['primary'],
            troughcolor=self.colors['surface_dark'],
            borderwidth=0,
            thickness=6
        )
    
    def crear_interfaz(self):
        # Frame principal con fondo
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # ===== HEADER PROFESIONAL =====
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=100)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        header_frame.grid_propagate(False)
        
        # Contenedor del header
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título principal
        titulo_label = tk.Label(
            header_content,
            text="Exportador de Reportes",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        titulo_label.pack()
        
        # Subtítulo
        subtitulo_label = tk.Label(
            header_content,
            text="Routers Nokia - Tigo",
            font=('Segoe UI', 12),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        subtitulo_label.pack()
        
        # ===== CONTENEDOR PRINCIPAL =====
        content_frame = tk.Frame(main_frame, bg=self.colors['background'])
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20)
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # ===== FRAME DE LISTA DE REPORTES =====
        list_container = tk.Frame(content_frame, bg=self.colors['surface'], relief='flat', bd=0)
        list_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(1, weight=1)
        
        # Header de la tabla
        table_header = tk.Frame(list_container, bg=self.colors['surface'], height=50)
        table_header.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=15, pady=(15, 10))
        
        header_title = tk.Label(
            table_header,
            text="📋 Reportes Disponibles",
            font=('Segoe UI', 14, 'bold'),
            bg=self.colors['surface'],
            fg=self.colors['text']
        )
        header_title.pack(side=tk.LEFT)
        
        # Badge con contador
        self.count_badge = tk.Label(
            table_header,
            text="0",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['primary'],
            fg='white',
            padx=10,
            pady=3,
            relief='flat'
        )
        self.count_badge.pack(side=tk.LEFT, padx=10)
        
        # Tabla de reportes con borde sutil
        table_frame = tk.Frame(list_container, bg=self.colors['border'], bd=1)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=(0, 15))
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        columns = ('nombre', 'id_sitio', 'reporte', 'fecha')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Definir encabezados con iconos
        self.tree.heading('nombre', text='🏢 Nombre del Sitio')
        self.tree.heading('id_sitio', text='🆔 ID Sitio')
        self.tree.heading('reporte', text='📊 Reporte')
        self.tree.heading('fecha', text='📅 Fecha')
        
        # Definir anchos de columna
        self.tree.column('nombre', width=350, anchor='w')
        self.tree.column('id_sitio', width=150, anchor='center')
        self.tree.column('reporte', width=150, anchor='center')
        self.tree.column('fecha', width=150, anchor='center')
        
        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Bind para selección
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        
        # ===== FRAME DE INFORMACIÓN DEL REPORTE =====
        info_container = tk.Frame(content_frame, bg=self.colors['surface'], relief='flat', bd=0)
        info_container.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        info_header = tk.Label(
            info_container,
            text="ℹ️ Información del Reporte",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            anchor='w'
        )
        info_header.grid(row=0, column=0, sticky=(tk.W), padx=15, pady=(15, 10))
        
        # Frame con borde para la información
        info_content = tk.Frame(info_container, bg=self.colors['surface_dark'], relief='flat', bd=0)
        info_content.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=15, pady=(0, 15))
        
        self.info_label = tk.Label(
            info_content,
            text="Selecciona un reporte de la lista para ver sus detalles",
            font=('Segoe UI', 10),
            bg=self.colors['surface_dark'],
            fg=self.colors['text_secondary'],
            anchor='w',
            justify='left',
            padx=15,
            pady=15
        )
        self.info_label.pack(fill=tk.BOTH, expand=True)
        
        # ===== FRAME DE BOTONES =====
        button_container = tk.Frame(content_frame, bg=self.colors['background'])
        button_container.grid(row=2, column=0, pady=(0, 15))
        
        self.btn_actualizar = ttk.Button(
            button_container,
            text="🔄  Actualizar Lista",
            command=self.cargar_reportes,
            style="Secondary.TButton"
        )
        self.btn_actualizar.grid(row=0, column=0, padx=8)
        
        self.btn_exportar = ttk.Button(
            button_container,
            text="📄  Exportar a PDF",
            command=self.exportar_pdf,
            state=tk.DISABLED,
            style="Primary.TButton"
        )
        self.btn_exportar.grid(row=0, column=1, padx=8)
        
        # ===== BARRA DE PROGRESO =====
        progress_container = tk.Frame(content_frame, bg=self.colors['surface'], relief='flat', bd=0)
        progress_container.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.progress = ttk.Progressbar(progress_container, mode='indeterminate')
        self.progress.pack(fill=tk.X, padx=15, pady=10)
        
        # ===== ÁREA DE LOG/CONSOLA =====
        log_container = tk.Frame(content_frame, bg=self.colors['surface'], relief='flat', bd=0)
        log_container.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        log_container.columnconfigure(0, weight=1)
        log_container.rowconfigure(1, weight=1)
        
        log_header = tk.Label(
            log_container,
            text="📝 Registro de Actividad",
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors['surface'],
            fg=self.colors['text'],
            anchor='w'
        )
        log_header.grid(row=0, column=0, sticky=(tk.W), padx=15, pady=(15, 10))
        
        # Frame con borde para el log
        log_content = tk.Frame(log_container, bg=self.colors['border'], bd=1)
        log_content.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=15, pady=(0, 15))
        log_content.columnconfigure(0, weight=1)
        log_content.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_content,
            height=8,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=('Consolas', 9),
            relief='flat',
            padx=10,
            pady=10
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar tags de colores para el log
        self.log_text.tag_config('success', foreground=self.colors['success'])
        self.log_text.tag_config('error', foreground=self.colors['error'])
        self.log_text.tag_config('warning', foreground=self.colors['warning'])
        self.log_text.tag_config('info', foreground=self.colors['primary'])
        
        main_frame.rowconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=3)
        content_frame.rowconfigure(4, weight=1)
    
    def log(self, mensaje, tipo='info'):
        """Agregar mensaje al log con colores"""
        self.log_text.config(state=tk.NORMAL)
        
        # Determinar tag basado en el contenido
        if '✅' in mensaje or 'éxito' in mensaje.lower() or 'completada' in mensaje.lower():
            tag = 'success'
        elif '❌' in mensaje or 'error' in mensaje.lower():
            tag = 'error'
        elif '⚠️' in mensaje or 'advertencia' in mensaje.lower():
            tag = 'warning'
        else:
            tag = 'info'
        
        self.log_text.insert(tk.END, mensaje + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()
    
    def cargar_reportes(self):
        """Cargar reportes desde Firebase"""
        self.log("🔄 Conectando a Firebase...")
        self.progress.start()
        self.btn_actualizar.config(state=tk.DISABLED)
        self.btn_exportar.config(state=tk.DISABLED)
        
        # Ejecutar en thread para no bloquear UI
        thread = threading.Thread(target=self._cargar_reportes_thread)
        thread.daemon = True
        thread.start()
    
    def _cargar_reportes_thread(self):
        """Thread para cargar reportes"""
        try:
            self.root.after(0, lambda: self.log("🔗 Inicializando conexión a Firebase..."))
            
            # Verificar que el archivo de credenciales existe
            import os
            if not os.path.exists('firebase-credentials.json'):
                raise FileNotFoundError("No se encontró el archivo 'firebase-credentials.json'")
            
            self.root.after(0, lambda: self.log("📄 Archivo de credenciales encontrado"))
            
            # Verificar credenciales antes de inicializar
            cred_file = 'firebase-credentials.json'
            if os.path.exists(cred_file):
                import json
                try:
                    with open(cred_file, 'r') as f:
                        cred_data = json.load(f)
                        project_id = cred_data.get('project_id', 'N/A')
                        client_email = cred_data.get('client_email', 'N/A')
                        self.root.after(0, lambda p=project_id: self.log(f"🔍 Proyecto Firebase: {p}"))
                        self.root.after(0, lambda e=client_email: self.log(f"🔍 Email servicio: {e[:50]}..."))
                except Exception as cred_error:
                    self.root.after(0, lambda msg=str(cred_error): self.log(f"⚠️ Error leyendo credenciales: {msg}"))
            
            db = init_firestore()
            self.root.after(0, lambda: self.log("✅ Conexión a Firebase establecida"))
            
            # Verificar que el cliente de Firestore funciona
            try:
                self.root.after(0, lambda: self.log("🔍 Probando acceso a Firestore..."))
                test_collection = db.collection("instalacionesRoutersTigo")
                self.root.after(0, lambda: self.log("✅ Colección 'instalacionesRoutersTigo' accesible"))
            except Exception as test_error:
                error_type = type(test_error).__name__
                error_msg = str(test_error)
                self.root.after(0, lambda t=error_type, m=error_msg: self.log(f"❌ Error accediendo colección ({t}): {m}"))
                raise
            
            coleccion = db.collection("instalacionesRoutersTigo")
            
            # Intentar obtener documentos con logging detallado
            docs_list = []
            import time
            start_time = time.time()
            
            self.root.after(0, lambda: self.log("📊 Iniciando consulta stream()..."))
            self.root.after(0, lambda: self.log(f"⏱️ Timestamp inicio: {start_time}"))
            
            # Usar el mismo método simple que funciona en exportar_pdf_simple.py
            self.root.after(0, lambda: self.log("📊 Obteniendo documentos..."))
            
            try:
                # Método simple: convertir stream a lista directamente (como funciona en exportar_reportes.py)
                self.root.after(0, lambda: self.log("🔍 Consultando Firebase..."))
                # Usar el mismo patrón que funciona en exportar_reportes.py listar_reportes_disponibles()
                docs_stream = coleccion.stream()
                
                doc_count = 0
                for doc in docs_stream:
                    docs_list.append(doc)
                    doc_count += 1
                    
                    # Log cada 10 documentos
                    if doc_count % 10 == 0:
                        self.root.after(0, lambda c=doc_count: self.log(f"📄 {c} documentos obtenidos..."))
                    
                    # Timeout de seguridad
                    if time.time() - start_time > 30:
                        self.root.after(0, lambda: self.log("⏰ Timeout alcanzado, continuando con documentos obtenidos..."))
                        break
                
                elapsed_total = time.time() - start_time
                self.root.after(0, lambda c=len(docs_list), t=elapsed_total: self.log(f"✅ {c} documentos obtenidos en {t:.2f}s"))
                        
            except Exception as stream_error:
                stream_msg = str(stream_error)
                stream_type = type(stream_error).__name__
                self.root.after(0, lambda msg=stream_msg, t=stream_type: self.log(f"⚠️ Error obteniendo documentos ({t}): {msg}"))
                
                # Método alternativo: Intentar con limit()
                try:
                    self.root.after(0, lambda: self.log("🔄 Intentando método alternativo con limit(10)..."))
                    docs_limited = coleccion.limit(10).stream()
                    for doc in docs_limited:
                        docs_list.append(doc)
                        self.root.after(0, lambda d_id=doc.id: self.log(f"📄 Documento (limitado): {d_id}"))
                except Exception as limit_error:
                    limit_msg = str(limit_error)
                    self.root.after(0, lambda msg=limit_msg: self.log(f"⚠️ Error con método alternativo: {msg}"))
            
            total_docs = len(docs_list)
            self.root.after(0, lambda: self.log(f"📋 Total de documentos encontrados: {total_docs}"))
            
            if total_docs == 0:
                self.root.after(0, lambda: self.log("⚠️ DIAGNÓSTICO: No se encontraron documentos"))
                self.root.after(0, lambda: self.log("🔍 Verificaciones:"))
                self.root.after(0, lambda: self.log("   1. ¿La colección 'instalacionesRoutersTigo' existe?"))
                self.root.after(0, lambda: self.log("   2. ¿Las credenciales tienen permisos para leer?"))
                self.root.after(0, lambda: self.log("   3. ¿Hay documentos en la colección?"))
                self.root.after(0, lambda: self.log("   4. ¿Las reglas de seguridad permiten lectura?"))
            
            if total_docs == 0:
                self.root.after(0, lambda: self.log("⚠️ No se encontraron documentos en la colección"))
                # Limpiar lista existente
                self.reportes = []
                self.root.after(0, self._actualizar_lista)
                return
            
            # Limpiar lista de reportes antes de cargar nuevos
            self.reportes = []
            contador = 0
            
            # Procesar documentos con timeout
            start_process = time.time()
            process_timeout = 60  # 60 segundos para procesar
            
            for i, doc in enumerate(docs_list):
                # Verificar timeout de procesamiento
                if time.time() - start_process > process_timeout:
                    self.root.after(0, lambda: self.log(f"⏰ Timeout de procesamiento alcanzado ({process_timeout}s)"))
                    break
                
                try:
                    datos = doc.to_dict()
                    
                    # Diagnóstico del primer documento
                    if contador == 0:
                        campos = list(datos.keys())[:10]
                        self.root.after(0, lambda c=campos: self.log(f"🔍 Primer documento - Campos: {', '.join(c)}"))
                    
                    # Intentar diferentes nombres de campos
                    nombre_sitio = (datos.get('nombreSitio') or datos.get('nombre') or 
                                   datos.get('sitio') or datos.get('nombreDelSitio') or 'Sin nombre')
                    sitio_id = (datos.get('ID') or datos.get('id') or 
                               datos.get('idSitio') or datos.get('sitioId') or 'N/A')
                    reporte = (datos.get('reporte') or datos.get('tipoReporte') or 
                              datos.get('tipo') or 'N/A')
                    fecha = (datos.get('fecha') or datos.get('fechaCreacion') or 
                            datos.get('createdAt') or 'N/A')
                    
                    self.reportes.append({
                        'id': doc.id,
                        'nombreSitio': str(nombre_sitio),
                        'ID': str(sitio_id),
                        'reporte': str(reporte),
                        'fecha': str(fecha)
                    })
                    contador += 1
                    
                    # Log cada 5 documentos
                    if contador % 5 == 0:
                        self.root.after(0, lambda c=contador, t=total_docs: self.log(f"📄 Procesados {c}/{t} documentos..."))
                        
                except Exception as doc_error:
                    error_msg = str(doc_error)
                    doc_id = doc.id
                    self.root.after(0, lambda msg=error_msg, d_id=doc_id: self.log(f"⚠️ Error procesando documento {d_id}: {msg}"))
                    continue
            
            self.root.after(0, lambda: self.log(f"✅ Procesamiento completado: {contador} documentos procesados exitosamente"))
            
            # Actualizar UI en el thread principal
            self.root.after(0, self._actualizar_lista)
            
        except FileNotFoundError as e:
            err_msg = str(e)
            self.root.after(0, lambda msg=err_msg: self.log(f"❌ Archivo no encontrado: {msg}"))
            self.root.after(0, lambda msg=err_msg: messagebox.showerror("Error de Configuración", 
                f"Archivo de credenciales no encontrado:\n{msg}\n\nAsegúrate de que 'firebase-credentials.json' esté en la carpeta del proyecto."))
        except Exception as e:
            error_msg = str(e)
            error_type = type(e).__name__
            self.root.after(0, lambda msg=error_msg: self.log(f"❌ Error al cargar reportes: {msg}"))
            self.root.after(0, lambda t=error_type: self.log(f"🔍 Tipo de error: {t}"))
            
            # Manejo específico para errores de autenticación
            if "invalid_grant" in error_msg or "JWT" in error_msg or "Token" in error_msg:
                self.root.after(0, lambda: self.log("🔑 PROBLEMA DE AUTENTICACIÓN DETECTADO"))
                self.root.after(0, lambda: self.log("💡 SOLUCIÓN: Regenera las credenciales de Firebase"))
                self.root.after(0, lambda: self.log("📋 Pasos:"))
                self.root.after(0, lambda: self.log("   1. Ve a Firebase Console"))
                self.root.after(0, lambda: self.log("   2. Configuración → Cuentas de servicio"))
                self.root.after(0, lambda: self.log("   3. Generar nueva clave privada"))
                self.root.after(0, lambda: self.log("   4. Reemplazar firebase-credentials.json"))
                
                self.root.after(0, lambda: messagebox.showerror(
                    "🔑 Error de Autenticación", 
                    "Las credenciales de Firebase han expirado.\n\n" +
                    "SOLUCIÓN:\n" +
                    "1. Ve a Firebase Console\n" +
                    "2. Configuración → Cuentas de servicio\n" +
                    "3. Generar nueva clave privada\n" +
                    "4. Reemplazar firebase-credentials.json\n\n" +
                    "Luego reinicia la aplicación."
                ))
            else:
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", f"No se pudieron cargar los reportes:\n{msg}"))
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.btn_actualizar.config(state=tk.NORMAL))
    
    def _actualizar_lista(self):
        """Actualizar la lista en el Treeview"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Agregar reportes
        for reporte in self.reportes:
            self.tree.insert('', tk.END, values=(
                reporte['nombreSitio'],
                reporte['ID'],
                reporte['reporte'],
                reporte['fecha']
            ), tags=(reporte['id'],))
        
        # Actualizar contador
        self.count_badge.config(text=str(len(self.reportes)))
        
        self.log(f"✅ Se cargaron {len(self.reportes)} reportes exitosamente")
    
    def on_select(self, event):
        """Evento cuando se selecciona un reporte"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            doc_id = item['tags'][0]
            
            # Buscar el reporte completo
            for reporte in self.reportes:
                if reporte['id'] == doc_id:
                    self.reporte_seleccionado = reporte
                    break
            
            # Actualizar información con formato mejorado
            info = f"🏢 Sitio: {self.reporte_seleccionado['nombreSitio']}\n"
            info += f"🆔 ID: {self.reporte_seleccionado['ID']}  |  "
            info += f"📊 Reporte: {self.reporte_seleccionado['reporte']}  |  "
            info += f"📅 Fecha: {self.reporte_seleccionado['fecha']}\n"
            info += f"🔑 Document ID: {self.reporte_seleccionado['id']}"
            
            self.info_label.config(text=info, fg=self.colors['text'])
            self.btn_exportar.config(state=tk.NORMAL)
            self.log(f"📋 Reporte seleccionado: {self.reporte_seleccionado['nombreSitio']}")
    
    def exportar_pdf(self):
        """Exportar el reporte seleccionado a PDF"""
        if not self.reporte_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un reporte primero")
            return
        
        # Sugerir nombre de archivo
        nombre_sugerido = f"reporte_{self.reporte_seleccionado['nombreSitio'].replace(' ', '_')}_{self.reporte_seleccionado['id'][:8]}.pdf"
        
        # Diálogo para guardar archivo
        archivo_salida = filedialog.asksaveasfilename(
            title="Guardar PDF como",
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")],
            initialfile=nombre_sugerido
        )
        
        if not archivo_salida:
            self.log("⚠️ Exportación cancelada por el usuario")
            return
        
        self.log(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        self.log(f"📤 Iniciando exportación a PDF...")
        self.log(f"🏢 Sitio: {self.reporte_seleccionado['nombreSitio']}")
        self.log(f"📄 Archivo destino: {os.path.basename(archivo_salida)}")
        self.progress.start()
        self.btn_exportar.config(state=tk.DISABLED)
        self.btn_actualizar.config(state=tk.DISABLED)
        
        # Exportar en thread
        thread = threading.Thread(
            target=self._exportar_pdf_thread,
            args=(self.reporte_seleccionado['id'], archivo_salida)
        )
        thread.daemon = True
        thread.start()
    
    def _exportar_pdf_thread(self, doc_id, archivo_salida):
        """Thread para exportar PDF"""
        try:
            # Cambiar al directorio de plantillas
            dir_actual = os.getcwd()
            script_dir = os.path.dirname(os.path.abspath(__file__))
            plantillas_dir = os.path.join(script_dir, 'plantillas')
            
            if os.path.exists(plantillas_dir):
                os.chdir(plantillas_dir)
            
            # Redirigir prints al log
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                # Generar PDF usando la ruta exacta proporcionada por el usuario
                generar_pdf_routers_tigo(doc_id, archivo_salida)
            
            # Volver al directorio original
            os.chdir(dir_actual)
            
            # Capturar output
            output = f.getvalue()
            for line in output.split('\n'):
                if line.strip():
                    self.root.after(0, lambda l=line: self.log(l))
            
            self.root.after(0, lambda: self.log(f"✅ ¡Exportación completada exitosamente!"))
            self.root.after(0, lambda: self.log(f"📂 Ubicación: {archivo_salida}"))
            self.root.after(0, lambda: self.log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"))
            self.root.after(0, lambda: messagebox.showinfo(
                "✅ Exportación Exitosa", 
                f"El PDF se ha exportado correctamente.\n\n📂 Ubicación:\n{archivo_salida}"
            ))
            
        except Exception as e:
            os.chdir(dir_actual)
            self.root.after(0, lambda: self.log(f"❌ Error durante la exportación: {str(e)}"))
            self.root.after(0, lambda: self.log(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"))
            self.root.after(0, lambda: messagebox.showerror(
                "❌ Error de Exportación", 
                f"Ocurrió un error al exportar el PDF:\n\n{str(e)}"
            ))
        
        finally:
            self.root.after(0, self.progress.stop)
            self.root.after(0, lambda: self.btn_exportar.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_actualizar.config(state=tk.NORMAL))

def main():
    # Verificar autenticación primero
    login_root = tk.Tk()
    
    login_app = LoginGUI(login_root)
    login_root.mainloop()
    
    # Verificar si el usuario se autenticó
    if not login_app.user_token:
        messagebox.showinfo("Sesión Requerida", "Debes iniciar sesión para usar la aplicación")
        return
    
    # Cerrar ventana de login
    login_root.destroy()
    
    # Abrir aplicación principal
    root = tk.Tk()
    app = ExportadorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

