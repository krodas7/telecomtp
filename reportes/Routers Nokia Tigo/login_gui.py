import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
import json
import os
from firebase_auth_config import init_firebase_auth, create_user_with_email_password, verify_email_password, get_user_info

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Iniciar Sesión - Exportador de Reportes")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#F4F6F9')
        
        # Centrar ventana
        self.center_window()
        
        # Variables
        self.user_token = None
        self.user_info = None
        
        # Paleta de colores profesional
        self.colors = {
            'primary': '#0052CC',
            'primary_dark': '#003D99',
            'primary_light': '#4C9AFF',
            'accent': '#00C7E6',
            'background': '#F4F6F9',
            'surface': '#FFFFFF',
            'surface_dark': '#E9EEF5',
            'text': '#172B4D',
            'text_secondary': '#5E6C84',
            'success': '#00875A',
            'error': '#DE350B',
            'border': '#DFE1E6',
        }
        
        # Configurar estilos
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Verificar si ya hay un token guardado
        self.verificar_token_guardado()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        # Usar tamaño fijo conocido para evitar ventana 1x1
        desired_width = 500
        desired_height = 600
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (desired_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (desired_height // 2)
        self.root.geometry(f'{desired_width}x{desired_height}+{x}+{y}')
    
    def configurar_estilos(self):
        """Configurar estilos personalizados"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones primarios
        style.configure("Primary.TButton",
            background=self.colors['primary'],
            foreground='white',
            borderwidth=0,
            focuscolor='none',
            font=('Segoe UI', 12, 'bold'),
            padding=(20, 15)
        )
        
        style.map("Primary.TButton",
            background=[('active', self.colors['primary_dark'])],
            foreground=[('active', 'white')]
        )
        
        # Estilo para botones secundarios
        style.configure("Secondary.TButton",
            background=self.colors['surface'],
            foreground=self.colors['primary'],
            borderwidth=1,
            focuscolor='none',
            font=('Segoe UI', 10, 'bold'),
            padding=(15, 10)
        )
        
        style.map("Secondary.TButton",
            background=[('active', self.colors['surface_dark'])],
            foreground=[('active', self.colors['primary_dark'])]
        )
    
    def crear_interfaz(self):
        """Crear la interfaz de login"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['primary'], height=120)
        header_frame.pack(fill=tk.X, pady=(0, 30))
        header_frame.pack_propagate(False)
        
        # Contenido del header
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.place(relx=0.5, rely=0.5, anchor='center')
        
        # Título
        titulo = tk.Label(
            header_content,
            text="🔐 Iniciar Sesión",
            font=('Segoe UI', 24, 'bold'),
            bg=self.colors['primary'],
            fg='white'
        )
        titulo.pack()
        
        # Subtítulo
        subtitulo = tk.Label(
            header_content,
            text="Exportador de Reportes Routers Nokia",
            font=('Segoe UI', 12),
            bg=self.colors['primary'],
            fg=self.colors['accent']
        )
        subtitulo.pack()
        
        # Frame de contenido
        content_frame = tk.Frame(main_frame, bg=self.colors['surface'], relief='flat', bd=0)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Información del usuario (inicialmente oculta)
        self.user_info_frame = tk.Frame(content_frame, bg=self.colors['surface_dark'], relief='flat', bd=0)
        self.user_info_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        self.user_info_label = tk.Label(
            self.user_info_frame,
            text="",
            font=('Segoe UI', 10),
            bg=self.colors['surface_dark'],
            fg=self.colors['text'],
            justify='left',
            anchor='w'
        )
        self.user_info_label.pack(fill=tk.X, padx=15, pady=15)
        
        # Formulario de login
        self.form_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        self.form_frame.pack(fill=tk.X, pady=20)
        
        # Campo de email
        email_frame = tk.Frame(self.form_frame, bg=self.colors['surface'])
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            email_frame,
            text="📧 Email:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.email_entry = tk.Entry(
            email_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=1,
            bg=self.colors['surface_dark'],
            fg=self.colors['text']
        )
        self.email_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Campo de contraseña
        password_frame = tk.Frame(self.form_frame, bg=self.colors['surface'])
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            password_frame,
            text="🔒 Contraseña:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=1,
            bg=self.colors['surface_dark'],
            fg=self.colors['text'],
            show='*'
        )
        self.password_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Botones de autenticación
        self.auth_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        self.auth_frame.pack(fill=tk.X, pady=20)
        
        # Botón de login
        self.btn_login = ttk.Button(
            self.auth_frame,
            text="🔑 Iniciar Sesión",
            command=self.login_email_password,
            style="Primary.TButton"
        )
        self.btn_login.pack(fill=tk.X, pady=(0, 15))
        
        # Botón de registro
        self.btn_register = ttk.Button(
            self.auth_frame,
            text="📝 Crear Cuenta",
            command=self.registrar_usuario,
            style="Secondary.TButton"
        )
        self.btn_register.pack(fill=tk.X, pady=(0, 15))
        
        # Botón de continuar (inicialmente oculto)
        self.btn_continue = ttk.Button(
            self.auth_frame,
            text="✅ Continuar a la Aplicación",
            command=self.continuar_aplicacion,
            style="Primary.TButton"
        )
        
        # Botón de cerrar sesión (inicialmente oculto)
        self.btn_logout = ttk.Button(
            self.auth_frame,
            text="🚪 Cerrar Sesión",
            command=self.cerrar_sesion,
            style="Secondary.TButton"
        )
        
        # Área de estado
        self.status_frame = tk.Frame(content_frame, bg=self.colors['surface_dark'], relief='flat', bd=0)
        self.status_frame.pack(fill=tk.X, pady=(20, 0), padx=20)
        
        self.status_label = tk.Label(
            self.status_frame,
            text="Selecciona un método de autenticación",
            font=('Segoe UI', 9),
            bg=self.colors['surface_dark'],
            fg=self.colors['text_secondary'],
            justify='left',
            anchor='w'
        )
        self.status_label.pack(fill=tk.X, padx=15, pady=10)
    
    def login_email_password(self):
        """Iniciar sesión con email y contraseña"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor, completa todos los campos")
            return
        
        if "@" not in email:
            messagebox.showerror("Error", "Por favor, ingresa un email válido")
            return
        
        self.actualizar_estado("🔍 Verificando credenciales...")
        self.btn_login.config(state=tk.DISABLED)
        
        # Verificar credenciales en thread
        thread = threading.Thread(target=self._verificar_credenciales_thread, args=(email, password))
        thread.daemon = True
        thread.start()
    
    def _verificar_credenciales_thread(self, email, password):
        """Thread para verificar credenciales"""
        try:
            # Verificar email y contraseña
            user_info = verify_email_password(email, password)
            
            # Guardar información
            self.user_token = f"email:{email}"  # Token simulado
            self.user_info = user_info
            
            # Actualizar UI
            self.root.after(0, self._mostrar_usuario_autenticado)
            
        except Exception as e:
            self.root.after(0, lambda: self.actualizar_estado(f"❌ Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error de Autenticación", f"Credenciales inválidas:\n{str(e)}"))
            self.root.after(0, lambda: self.btn_login.config(state=tk.NORMAL))
    
    def registrar_usuario(self):
        """Registrar nuevo usuario"""
        self.crear_dialogo_registro()
    
    def crear_dialogo_registro(self):
        """Crear diálogo para registro de usuario"""
        # Crear ventana de registro
        self.registro_window = tk.Toplevel(self.root)
        self.registro_window.title("📝 Crear Cuenta")
        self.registro_window.geometry("450x500")
        self.registro_window.configure(bg=self.colors['background'])
        self.registro_window.resizable(False, False)
        
        # Centrar ventana
        self.registro_window.transient(self.root)
        self.registro_window.grab_set()
        
        # Contenido
        frame = tk.Frame(self.registro_window, bg=self.colors['background'])
        frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Título
        titulo = tk.Label(
            frame,
            text="📝 Crear Nueva Cuenta",
            font=('Segoe UI', 18, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        )
        titulo.pack(pady=(0, 20))
        
        # Campo de nombre
        nombre_frame = tk.Frame(frame, bg=self.colors['background'])
        nombre_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            nombre_frame,
            text="👤 Nombre completo:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.nombre_entry = tk.Entry(
            nombre_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=1,
            bg=self.colors['surface_dark'],
            fg=self.colors['text']
        )
        self.nombre_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Campo de email
        email_frame = tk.Frame(frame, bg=self.colors['background'])
        email_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            email_frame,
            text="📧 Email:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.registro_email_entry = tk.Entry(
            email_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=1,
            bg=self.colors['surface_dark'],
            fg=self.colors['text']
        )
        self.registro_email_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Campo de contraseña
        password_frame = tk.Frame(frame, bg=self.colors['background'])
        password_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            password_frame,
            text="🔒 Contraseña:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.registro_password_entry = tk.Entry(
            password_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=1,
            bg=self.colors['surface_dark'],
            fg=self.colors['text'],
            show='*'
        )
        self.registro_password_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Campo de confirmar contraseña
        confirm_frame = tk.Frame(frame, bg=self.colors['background'])
        confirm_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            confirm_frame,
            text="🔒 Confirmar contraseña:",
            font=('Segoe UI', 11, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.confirm_password_entry = tk.Entry(
            confirm_frame,
            font=('Segoe UI', 11),
            relief='flat',
            bd=1,
            bg=self.colors['surface_dark'],
            fg=self.colors['text'],
            show='*'
        )
        self.confirm_password_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)
        
        # Botones
        button_frame = tk.Frame(frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        ttk.Button(
            button_frame,
            text="📝 Crear Cuenta",
            command=self.crear_cuenta,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="❌ Cancelar",
            command=self.registro_window.destroy,
            style="Secondary.TButton"
        ).pack(side=tk.LEFT)
    
    def crear_cuenta(self):
        """Crear nueva cuenta"""
        nombre = self.nombre_entry.get().strip()
        email = self.registro_email_entry.get().strip()
        password = self.registro_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        
        # Validaciones
        if not all([nombre, email, password, confirm_password]):
            messagebox.showerror("Error", "Por favor, completa todos los campos")
            return
        
        if "@" not in email:
            messagebox.showerror("Error", "Por favor, ingresa un email válido")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        # Crear cuenta en thread
        thread = threading.Thread(target=self._crear_cuenta_thread, args=(email, password, nombre))
        thread.daemon = True
        thread.start()
    
    def _crear_cuenta_thread(self, email, password, nombre):
        """Thread para crear cuenta"""
        try:
            # Crear usuario
            user_info = create_user_with_email_password(email, password, nombre)
            
            # Guardar información
            self.user_token = f"email:{email}"  # Token simulado
            self.user_info = user_info
            
            # Actualizar UI
            self.root.after(0, self.registro_window.destroy)
            self.root.after(0, self._mostrar_usuario_autenticado)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error de Registro", f"Error creando cuenta:\n{str(e)}"))
    
    def mostrar_instrucciones_google(self):
        """Mostrar instrucciones para login con Google"""
        instrucciones = """
🔑 INSTRUCCIONES PARA GOOGLE:

1. Se abrió una ventana del navegador
2. Inicia sesión con tu cuenta de Google
3. Copia el token de autenticación
4. Pégalo en el campo de abajo
5. Haz clic en "Verificar Token"

Token de autenticación:
        """
        
        # Crear ventana de instrucciones
        self.instrucciones_window = tk.Toplevel(self.root)
        self.instrucciones_window.title("Instrucciones de Autenticación")
        self.instrucciones_window.geometry("500x400")
        self.instrucciones_window.configure(bg=self.colors['background'])
        self.instrucciones_window.resizable(False, False)
        
        # Centrar ventana
        self.instrucciones_window.transient(self.root)
        self.instrucciones_window.grab_set()
        
        # Contenido
        frame = tk.Frame(self.instrucciones_window, bg=self.colors['background'])
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instrucciones
        instrucciones_label = tk.Label(
            frame,
            text=instrucciones,
            font=('Segoe UI', 10),
            bg=self.colors['background'],
            fg=self.colors['text'],
            justify='left',
            anchor='w'
        )
        instrucciones_label.pack(fill=tk.X, pady=(0, 20))
        
        # Campo de token
        token_frame = tk.Frame(frame, bg=self.colors['background'])
        token_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            token_frame,
            text="Token:",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['background'],
            fg=self.colors['text']
        ).pack(anchor='w')
        
        self.token_entry = tk.Entry(
            token_frame,
            font=('Consolas', 9),
            width=60,
            relief='flat',
            bd=1
        )
        self.token_entry.pack(fill=tk.X, pady=(5, 0))
        
        # Botones
        button_frame = tk.Frame(frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X)
        
        ttk.Button(
            button_frame,
            text="🔍 Verificar Token",
            command=self.verificar_token_google,
            style="Primary.TButton"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame,
            text="❌ Cancelar",
            command=self.instrucciones_window.destroy,
            style="Secondary.TButton"
        ).pack(side=tk.LEFT)
    
    def verificar_token_google(self):
        """Verificar token de Google"""
        token = self.token_entry.get().strip()
        
        if not token:
            messagebox.showerror("Error", "Por favor, ingresa un token válido")
            return
        
        self.actualizar_estado("🔍 Verificando token...")
        
        # Verificar token en thread
        thread = threading.Thread(target=self._verificar_token_thread, args=(token,))
        thread.daemon = True
        thread.start()
    
    def _verificar_token_thread(self, token):
        """Thread para verificar token"""
        try:
            # Inicializar Firebase Auth
            auth = init_firebase_auth()
            
            # Verificar token
            decoded_token = verify_user_token(token)
            user_info = get_user_info(decoded_token['uid'])
            
            # Guardar información
            self.user_token = token
            self.user_info = user_info
            
            # Actualizar UI
            self.root.after(0, self._mostrar_usuario_autenticado)
            
        except Exception as e:
            self.root.after(0, lambda: self.actualizar_estado(f"❌ Error: {str(e)}"))
            self.root.after(0, lambda: messagebox.showerror("Error de Autenticación", f"Token inválido:\n{str(e)}"))
    
    def _mostrar_usuario_autenticado(self):
        """Mostrar información del usuario autenticado"""
        # Cerrar ventana de instrucciones solo si existe (flujo Google)
        try:
            if hasattr(self, 'instrucciones_window') and self.instrucciones_window and self.instrucciones_window.winfo_exists():
                self.instrucciones_window.destroy()
        except Exception:
            pass
        
        # Mostrar información del usuario
        user_text = f"👤 Usuario: {self.user_info['email']}\n"
        user_text += f"🆔 UID: {self.user_info['uid']}\n"
        user_text += f"✅ Email verificado: {'Sí' if self.user_info['email_verified'] else 'No'}"
        
        self.user_info_label.config(text=user_text)
        self.user_info_frame.pack(fill=tk.X, pady=(0, 20), padx=20)
        
        # Mostrar botones de continuar y cerrar sesión
        self.btn_continue.pack(fill=tk.X, pady=(0, 10))
        self.btn_logout.pack(fill=tk.X, pady=(0, 10))
        
        # Ocultar formulario de login
        self.form_frame.pack_forget()
        self.btn_login.pack_forget()
        self.btn_register.pack_forget()
        
        self.actualizar_estado("✅ Autenticación exitosa")
    
    def crear_dialogo_email(self):
        """Crear diálogo para login con email"""
        # Implementar login con email/password
        messagebox.showinfo("Próximamente", "Login con email estará disponible en la próxima versión")
    
    def crear_dialogo_registro(self):
        """Crear diálogo para registro"""
        # Implementar registro de usuario
        messagebox.showinfo("Próximamente", "Registro de usuario estará disponible en la próxima versión")
    
    def continuar_aplicacion(self):
        """Continuar a la aplicación principal"""
        # Guardar token para uso posterior
        self.guardar_token()
        
        # Cerrar ventana de login
        self.root.quit()
    
    def cerrar_sesion(self):
        """Cerrar sesión"""
        self.user_token = None
        self.user_info = None
        
        # Ocultar información del usuario
        self.user_info_frame.pack_forget()
        self.btn_continue.pack_forget()
        self.btn_logout.pack_forget()
        
        # Mostrar formulario de login
        self.form_frame.pack(fill=tk.X, pady=20)
        self.btn_login.pack(fill=tk.X, pady=(0, 15))
        self.btn_register.pack(fill=tk.X, pady=(0, 15))
        
        self.actualizar_estado("Sesión cerrada")
    
    def guardar_token(self):
        """Guardar token para uso posterior"""
        if self.user_token:
            try:
                with open('user_token.json', 'w') as f:
                    json.dump({
                        'token': self.user_token,
                        'user_info': self.user_info
                    }, f)
            except Exception as e:
                print(f"Error guardando token: {e}")
    
    def verificar_token_guardado(self):
        """Verificar si hay un token guardado"""
        try:
            if os.path.exists('user_token.json'):
                with open('user_token.json', 'r') as f:
                    data = json.load(f)
                    self.user_token = data.get('token')
                    self.user_info = data.get('user_info')
                    
                    if self.user_token and self.user_info:
                        self._mostrar_usuario_autenticado()
        except Exception as e:
            print(f"Error cargando token guardado: {e}")
    
    def actualizar_estado(self, mensaje):
        """Actualizar mensaje de estado"""
        self.status_label.config(text=mensaje)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = LoginGUI(root)
    root.mainloop()
    
    # Retornar información del usuario si se autenticó
    return app.user_token, app.user_info

if __name__ == "__main__":
    main()
