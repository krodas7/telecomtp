"""
Formularios simplificados del Telecom Technology
Solo los formularios esenciales que funcionan correctamente
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *
from .models import Subproyecto  # Importar explícitamente para usar en formularios


class ClienteForm(forms.ModelForm):
    """Formulario para clientes"""
    
    class Meta:
        model = Cliente
        fields = [
            'razon_social', 'codigo_fiscal', 'email', 'telefono', 
            'direccion', 'activo'
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón social del cliente'
            }),
            'codigo_fiscal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código fiscal o NIT'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+502 1234-5678'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class ProyectoForm(forms.ModelForm):
    """Formulario para proyectos"""
    
    class Meta:
        model = Proyecto
        fields = [
            'nombre', 'descripcion', 'cliente', 
            'fecha_inicio', 'estado', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del proyecto'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class ColaboradorForm(forms.ModelForm):
    """Formulario para colaboradores"""
    
    class Meta:
        model = Colaborador
        fields = [
            'nombre', 'dpi', 'direccion', 'telefono', 'email', 
            'salario', 'fecha_contratacion', 'fecha_vencimiento_contrato',
            'aplica_bono_general', 'aplica_bono_produccion', 'aplica_retenciones', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'dpi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '1234567890101'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+502 1234-5678'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'salario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_contratacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_vencimiento_contrato': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'aplica_bono_general': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aplica_bono_produccion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aplica_retenciones': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class FacturaForm(forms.ModelForm):
    """Formulario para facturas"""
    
    # Opciones para el porcentaje de ITBMS
    PORCENTAJE_ITBMS_CHOICES = [
        ('0.00', 'Sin impuesto'),
        ('3.50', 'ITBMS 3.5%'),
        ('7.00', 'ITBMS 7%'),
    ]
    
    porcentaje_itbms = forms.ChoiceField(
        choices=PORCENTAJE_ITBMS_CHOICES,
        initial='7.00',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'onchange': 'calcularFactura()'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer valor por defecto para estado
        if not self.instance.pk:  # Solo para nuevas instancias
            self.fields['estado'].initial = 'emitida'
        
        # Hacer el campo subproyecto opcional
        self.fields['subproyecto'].required = False
        self.fields['subproyecto'].empty_label = "Seleccionar subproyecto (opcional)"
        
        # Hacer que porcentaje_itbms no sea obligatorio (siempre tiene valor por defecto)
        self.fields['porcentaje_itbms'].required = False
        # Establecer valor inicial del porcentaje_itbms si es una edición
        if self.instance.pk and self.instance.porcentaje_itbms:
            self.fields['porcentaje_itbms'].initial = str(self.instance.porcentaje_itbms)
        
        # Hacer que monto_total no sea obligatorio (se calcula automáticamente)
        self.fields['monto_total'].required = False
        
        # Inicialmente, el queryset de proyectos está vacío - se llenará dinámicamente con JavaScript
        # cuando se seleccione un cliente
        if not self.instance.pk:
            # Para nuevas facturas, empezar con queryset vacío
            self.fields['proyecto'].queryset = Proyecto.objects.none()
            self.fields['proyecto'].empty_label = "Primero seleccione un cliente"
        else:
            # Para ediciones, mostrar solo proyectos del cliente de la factura
            if self.instance.cliente:
                self.fields['proyecto'].queryset = Proyecto.objects.filter(
                    cliente=self.instance.cliente,
                    activo=True
                ).order_by('nombre')
        
        # Filtrar subproyectos según el proyecto seleccionado
        if self.instance.pk and self.instance.proyecto:
            self.fields['subproyecto'].queryset = Subproyecto.objects.filter(
                proyecto=self.instance.proyecto,
                activo=True
            ).order_by('nombre')
        else:
            self.fields['subproyecto'].queryset = Subproyecto.objects.none()
    
    class Meta:
        model = Factura
        fields = [
            'numero_factura', 'proyecto', 'subproyecto', 'cliente', 'tipo', 'estado',
            'fecha_emision', 'fecha_vencimiento', 'monto_subtotal',
            'porcentaje_itbms', 'monto_iva', 'monto_total', 'descripcion_servicios',
            'porcentaje_avance', 'metodo_pago', 'referencia_pago',
            'banco_origen', 'observaciones', 'comprobante'
        ]
        widgets = {
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'F001-2025'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_proyecto',
                'onchange': 'actualizarSubproyectosFactura()'
            }),
            'subproyecto': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_subproyecto_factura'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }, format='%Y-%m-%d'),
            'monto_subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'Ingrese el subtotal',
                'oninput': 'calcularFactura()'
            }),
            'monto_iva': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'monto_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'readonly': 'readonly',
                'style': 'background-color: #f8f9fa;'
            }),
            'descripcion_servicios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de los servicios facturados'
            }),
            'porcentaje_avance': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de referencia'
            }),
            'banco_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Banco de origen'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }


class GastoForm(forms.ModelForm):
    """Formulario para gastos"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer fecha por defecto SOLO si es un nuevo registro (sin pk)
        # Si es edición (con pk), mantener la fecha existente del gasto
        if not self.instance.pk:
            from datetime import date
            self.fields['fecha_gasto'].initial = date.today()
        
        # Hacer el campo subproyecto opcional
        self.fields['subproyecto'].required = False
        self.fields['subproyecto'].empty_label = "Seleccionar subproyecto (opcional)"
        
        # Filtrar subproyectos según el proyecto seleccionado
        if self.instance.pk and self.instance.proyecto:
            self.fields['subproyecto'].queryset = Subproyecto.objects.filter(
                proyecto=self.instance.proyecto,
                activo=True
            ).order_by('nombre')
        else:
            self.fields['subproyecto'].queryset = Subproyecto.objects.none()
    
    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto is not None:
            # Convertir a string para validar formato
            monto_str = str(monto)
            try:
                # Validar que sea un número válido
                monto_float = float(monto_str)
                if monto_float < 0:
                    raise forms.ValidationError('El monto no puede ser negativo.')
                if monto_float > 999999.99:
                    raise forms.ValidationError('El monto no puede exceder Q999,999.99.')
                
                # Validar que no tenga más de 2 decimales
                if '.' in monto_str:
                    decimal_part = monto_str.split('.')[1]
                    if len(decimal_part) > 2:
                        raise forms.ValidationError('El monto no puede tener más de 2 decimales.')
                
                return monto_float
            except ValueError:
                raise forms.ValidationError('Ingrese un monto válido.')
        return monto
    
    class Meta:
        model = Gasto
        fields = [
            'proyecto', 'subproyecto', 'categoria', 'descripcion', 'monto', 
            'fecha_gasto', 'aprobado', 
            'observaciones', 'comprobante'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'subproyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del gasto'
            }),
            'monto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'pattern': '[0-9]+(\.[0-9]{1,2})?'
            }),
            'fecha_gasto': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'aprobado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control form-textarea',
                'rows': 4,
                'placeholder': 'Observaciones adicionales (opcional)'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }


class CategoriaGastoForm(forms.ModelForm):
    """Formulario para categorías de gasto"""
    
    class Meta:
        model = CategoriaGasto
        fields = ['nombre', 'descripcion', 'color', 'icono']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la categoría'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color'
            }),
            'icono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-tools'
            })
        }


class ArchivoProyectoForm(forms.ModelForm):
    """Formulario para archivos de proyecto"""
    
    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        if self.proyecto:
            # Filtrar carpetas del proyecto
            self.fields['carpeta'].queryset = CarpetaProyecto.objects.filter(
                proyecto=self.proyecto, 
                activa=True
            )
            self.fields['carpeta'].required = False
    
    def clean_archivo(self):
        """Validar el archivo subido"""
        import logging
        logger = logging.getLogger(__name__)
        
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Extensiones permitidas (COMPLETA)
            extensiones_permitidas = [
                # Documentos
                '.pdf', '.doc', '.docx', '.odt', '.txt', '.rtf',
                # Excel
                '.xls', '.xlsx', '.xlsm', '.xlsb', '.csv',
                # Imágenes
                '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg',
                # Comprimidos
                '.zip', '.rar', '.7z', '.tar', '.gz',
                # CAD
                '.dwg', '.dxf', '.dwf',
                # Otros
                '.ppt', '.pptx', '.xml', '.json'
            ]
            
            # Obtener la extensión del archivo
            nombre_archivo = archivo.name.lower()
            logger.info(f"📎 Archivo recibido: {nombre_archivo}")
            logger.info(f"📎 Tamaño: {archivo.size} bytes")
            
            extension_valida = any(nombre_archivo.endswith(ext) for ext in extensiones_permitidas)
            
            if not extension_valida:
                logger.error(f"❌ Extensión no válida para: {nombre_archivo}")
                raise forms.ValidationError(
                    f'Tipo de archivo no permitido: "{nombre_archivo}". Extensiones permitidas: {", ".join(extensiones_permitidas)}'
                )
            
            logger.info(f"✅ Extensión válida para: {nombre_archivo}")
            
            # Validar tamaño del archivo (máximo 100MB)
            if archivo.size > 100 * 1024 * 1024:  # 100MB
                raise forms.ValidationError('El archivo es demasiado grande. Tamaño máximo: 100MB')
            
            logger.info(f"✅ Tamaño válido: {archivo.size} bytes")
        
        return archivo
    
    class Meta:
        model = ArchivoProyecto
        fields = ['nombre', 'descripcion', 'archivo', 'carpeta', 'tipo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del archivo (opcional, se usa el nombre del archivo si está vacío)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del archivo (opcional)'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.xls,.xlsx,.xlsm,.xlsb,.csv,.jpg,.jpeg,.png,.gif,.zip,.rar'
            }),
            'carpeta': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class CarpetaProyectoForm(forms.ModelForm):
    """Formulario para carpetas de proyecto"""
    
    def __init__(self, *args, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        
        self.proyecto = kwargs.pop('proyecto', None)
        logger.info(f"🔍 CarpetaProyectoForm.__init__ - Proyecto recibido: {self.proyecto}")
        
        super().__init__(*args, **kwargs)
        
        logger.info(f"🔍 Fields disponibles: {list(self.fields.keys())}")
        
        if self.proyecto:
            # Filtrar carpetas padre del mismo proyecto
            self.fields['carpeta_padre'].queryset = CarpetaProyecto.objects.filter(
                proyecto=self.proyecto, 
                activa=True
            )
            self.fields['carpeta_padre'].required = False
            logger.info(f"✅ Carpeta padre configurada para proyecto {self.proyecto.id}")
    
    class Meta:
        model = CarpetaProyecto
        fields = ['nombre', 'descripcion', 'carpeta_padre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la carpeta'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la carpeta'
            }),
            'carpeta_padre': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class UsuarioForm(UserCreationForm):
    """Formulario para crear usuarios"""
    
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contraseña'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Confirmar contraseña'
            })
        }


class RolForm(forms.ModelForm):
    """Formulario para roles"""
    
    class Meta:
        model = Rol
        fields = ['nombre', 'descripcion', 'modulos_activos']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del rol'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del rol'
            }),
            'modulos_activos': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            })
        }


class PerfilUsuarioForm(forms.ModelForm):
    """Formulario para perfil de usuario"""
    
    class Meta:
        model = PerfilUsuario
        fields = ['rol', 'telefono', 'direccion', 'activo']
        widgets = {
            'rol': forms.Select(attrs={
                'class': 'form-select'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+502 1234-5678'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class AnticipoForm(forms.ModelForm):
    """Formulario para anticipos"""
    
    class Meta:
        model = Anticipo
        fields = [
            'cliente', 'proyecto', 'numero_anticipo', 'monto', 'tipo', 
            'metodo_pago', 'referencia_pago', 'banco_origen',
            'fecha_recepcion', 'descripcion', 'observaciones'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'numero_anticipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ANT-2025-001'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de cheque, transferencia, etc.'
            }),
            'banco_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Banco de origen del pago'
            }),
            'fecha_recepcion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción detallada del anticipo'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            })
        }


class PagoForm(forms.ModelForm):
    """Formulario para pagos"""
    
    class Meta:
        model = Pago
        fields = [
            'factura', 'monto', 'fecha_pago', 'metodo_pago', 
            'estado', 'comprobante_pago'
        ]
        widgets = {
            'factura': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_pago': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'comprobante_pago': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            })
        }


class EventoCalendarioForm(forms.ModelForm):
    """Formulario para eventos del calendario"""
    
    class Meta:
        model = EventoCalendario
        fields = [
            'titulo', 'descripcion', 'fecha_inicio', 'fecha_fin',
            'hora_inicio', 'hora_fin', 'tipo', 'color', 'todo_el_dia',
            'proyecto', 'factura'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del evento'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del evento'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'hora_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'color': forms.Select(attrs={
                'class': 'form-select'
            }),
            'todo_el_dia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'factura': forms.Select(attrs={
                'class': 'form-select'
            })
        }


# FORMULARIO PresupuestoForm ELIMINADO - YA NO SE USA


# FORMULARIO PartidaPresupuestoForm ELIMINADO - YA NO SE USA


class CategoriaInventarioForm(forms.ModelForm):
    """Formulario para categorías de inventario"""
    
    class Meta:
        model = CategoriaInventario
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la categoría'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción de la categoría'
            })
        }


class ItemInventarioForm(forms.ModelForm):
    """Formulario para items de inventario"""
    
    class Meta:
        model = ItemInventario
        fields = [
            'categoria', 'nombre', 'descripcion', 'codigo', 
            'unidad_medida', 'precio_unitario', 'stock_actual', 'stock_minimo', 
            'proveedor', 'fecha_ultima_compra', 'activo'
        ]
        widgets = {
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del item'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Descripción del item'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código del item'
            }),
            'unidad_medida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Unidad de medida'
            }),
            'precio_unitario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'stock_minimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'proveedor': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Proveedor'
            }),
            'fecha_ultima_compra': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class AsignacionInventarioForm(forms.ModelForm):
    """Formulario para asignaciones de inventario"""
    
    class Meta:
        model = AsignacionInventario
        fields = [
            'proyecto', 'item', 'cantidad_asignada', 'fecha_devolucion', 
            'estado', 'notas'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'item': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cantidad_asignada': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'fecha_devolucion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Notas de la asignación'
            })
        }


class TrabajadorDiarioForm(forms.ModelForm):
    """Formulario para trabajadores diarios"""
    
    class Meta:
        model = TrabajadorDiario
        fields = [
            'planilla', 'nombre', 'pago_diario', 'activo'
        ]
        widgets = {
            'planilla': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del trabajador'
            }),
            'pago_diario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.planilla = kwargs.pop('planilla', None)
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        
        # Cargar planillas del proyecto
        if proyecto:
            self.fields['planilla'].queryset = PlanillaTrabajadoresDiarios.objects.filter(proyecto=proyecto)
            self.fields['planilla'].empty_label = "Selecciona una planilla"
        
        # Si se pasa una planilla específica, seleccionarla y ocultarla del formulario
        if self.planilla:
            self.fields['planilla'].initial = self.planilla.id
            self.fields['planilla'].widget = forms.HiddenInput()
            self.fields['planilla'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        # Si se pasó una planilla específica, asegurarse de que esté en cleaned_data
        if self.planilla:
            cleaned_data['planilla'] = self.planilla
        return cleaned_data


class RegistroTrabajoForm(forms.ModelForm):
    """Formulario para registros de trabajo"""
    
    class Meta:
        model = RegistroTrabajo
        fields = [
            'trabajador', 'fecha_inicio', 'fecha_fin', 'dias_trabajados', 
            'observaciones'
        ]
        widgets = {
            'trabajador': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'dias_trabajados': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones del período de trabajo'
            })
        }


class AnticipoTrabajadorDiarioForm(forms.ModelForm):
    """Formulario para anticipos de trabajadores diarios"""
    
    def __init__(self, *args, **kwargs):
        proyecto_id = kwargs.pop('proyecto_id', None)
        trabajador_id = kwargs.pop('trabajador_id', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar trabajadores por proyecto
        if proyecto_id:
            self.fields['trabajador'].queryset = TrabajadorDiario.objects.filter(
                proyecto_id=proyecto_id,
                activo=True
            ).order_by('nombre')
        
        # Preseleccionar trabajador si se pasa trabajador_id
        if trabajador_id and not self.instance.pk:
            try:
                trabajador = TrabajadorDiario.objects.get(id=trabajador_id)
                self.fields['trabajador'].initial = trabajador
            except TrabajadorDiario.DoesNotExist:
                pass
    
    class Meta:
        model = AnticipoTrabajadorDiario
        fields = [
            'trabajador', 'monto', 'fecha_anticipo', 'observaciones'
        ]
        widgets = {
            'trabajador': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'fecha_anticipo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones del anticipo'
            })
        }


class PlanillaTrabajadoresDiariosForm(forms.ModelForm):
    """Formulario para crear/editar planillas de trabajadores diarios"""
    
    class Meta:
        model = PlanillaTrabajadoresDiarios
        fields = [
            'nombre', 'descripcion', 'observaciones'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Planilla Semana 1, Planilla Enero 2025'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la planilla'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            })
        }
    
    def __init__(self, *args, **kwargs):
        self.proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class IngresoProyectoForm(forms.ModelForm):
    """Formulario para registrar ingresos por proyecto"""
    
    class Meta:
        model = IngresoProyecto
        fields = [
            'proyecto', 'factura', 'tipo_ingreso', 'numero_documento', 'descripcion',
            'monto_subtotal', 'monto_iva', 'monto_total', 'fecha_emision', 'fecha_registro',
            'fecha_pago', 'porcentaje_pagado', 'observaciones'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'factura': forms.Select(attrs={
                'class': 'form-control'
            }),
            'tipo_ingreso': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: FAC-001-2025',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del ingreso',
                'required': True
            }),
            'monto_subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '$0.00'
            }),
            'monto_iva': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '$0.00'
            }),
            'monto_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '$0.00',
                'readonly': True
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'fecha_registro': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_pago': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'porcentaje_pagado': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar proyectos activos
        self.fields['proyecto'].queryset = Proyecto.objects.filter(activo=True).order_by('nombre')
        
        # Filtrar facturas activas
        self.fields['factura'].queryset = Factura.objects.filter(
            estado__in=['emitida', 'enviada', 'pagada']
        ).order_by('-fecha_emision')
        
        # Establecer fecha de registro por defecto
        if not self.instance.pk:
            self.fields['fecha_registro'].initial = timezone.now().date()
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Validar que el monto total sea positivo
        monto_total = cleaned_data.get('monto_total')
        if monto_total and monto_total <= 0:
            raise forms.ValidationError('El monto total debe ser mayor a 0.')
        
        # Validar porcentaje pagado
        porcentaje_pagado = cleaned_data.get('porcentaje_pagado')
        if porcentaje_pagado and (porcentaje_pagado < 0 or porcentaje_pagado > 100):
            raise forms.ValidationError('El porcentaje pagado debe estar entre 0 y 100.')
        
        return cleaned_data


class CotizacionForm(forms.ModelForm):
    """Formulario para cotizaciones"""
    
    class Meta:
        model = Cotizacion
        fields = [
            'proyecto', 'cliente', 'numero_cotizacion', 'titulo', 'descripcion',
            'tipo_cotizacion', 'estado', 'monto_subtotal', 'monto_iva', 'monto_total',
            'fecha_emision', 'fecha_vencimiento', 'condiciones_pago', 'validez_dias',
            'terminos_condiciones'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'numero_cotizacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Se generará automáticamente',
                'readonly': True,
                'style': 'background-color: #f8f9fa;'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título de la cotización',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada de los servicios',
                'required': False
            }),
            'tipo_cotizacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto_subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'oninput': 'calcularCotizacion()'
            }),
            'monto_iva': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'readonly': True,
                'style': 'background-color: #f8f9fa;'
            }),
            'monto_total': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'readonly': True,
                'style': 'background-color: #f8f9fa;'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': False
            }),
            'validez_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '30',
                'required': False
            }),
            'condiciones_pago': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: 50% al inicio, 50% al finalizar',
                'required': False
            }),
            'terminos_condiciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Términos y condiciones generales',
                'required': False
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El número de cotización se genera automáticamente
        self.fields['numero_cotizacion'].required = False
        # La fecha de vencimiento no es obligatoria
        self.fields['fecha_vencimiento'].required = False
        # Campos que ya no están en el template
        self.fields['descripcion'].required = False
        self.fields['validez_dias'].required = False
        self.fields['condiciones_pago'].required = False
        self.fields['terminos_condiciones'].required = False
        # Estado por defecto enviada y ocultar el campo
        self.fields['estado'].widget = forms.HiddenInput()
        if not self.instance.pk:
            self.fields['estado'].initial = 'enviada'
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_emision = cleaned_data.get('fecha_emision')
        fecha_vencimiento = cleaned_data.get('fecha_vencimiento')
        
        if fecha_emision and fecha_vencimiento:
            if fecha_vencimiento <= fecha_emision:
                raise forms.ValidationError('La fecha de vencimiento debe ser posterior a la fecha de emisión.')
        
        return cleaned_data


class ConfiguracionPlanillaForm(forms.ModelForm):
    """Formulario para configurar retenciones y bonos de planilla"""
    
    class Meta:
        model = ConfiguracionPlanilla
        fields = [
            'retencion_seguro_social', 'retencion_seguro_educativo',
            'bono_general', 'bono_produccion',
            'aplicar_retenciones', 'aplicar_bonos'
        ]
        widgets = {
            'retencion_seguro_social': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'retencion_seguro_educativo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'bono_general': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'bono_produccion': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '0.00'
            }),
            'aplicar_retenciones': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aplicar_bonos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class CajaMenudaForm(forms.ModelForm):
    """Formulario para Caja Menuda"""
    
    class Meta:
        model = CajaMenuda
        fields = ['folio', 'fecha', 'descripcion', 'monto', 'proyecto']
        widgets = {
            'folio': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CM-001'
            }),
            'fecha': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del movimiento...'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class ServicioTorreroForm(forms.ModelForm):
    """Formulario para crear/editar servicios de torreros"""
    class Meta:
        model = ServicioTorrero
        fields = [
            'cliente', 'proyecto', 'descripcion', 'cantidad_torreros',
            'periodo', 'dias_solicitados', 'fecha_inicio', 'fecha_fin_estimada',
            'tarifa_por_dia', 'estado', 'observaciones'
        ]
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe el servicio solicitado...'
            }),
            'cantidad_torreros': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1'
            }),
            'periodo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'dias_solicitados': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'step': '0.5',
                'placeholder': 'Ej: 5'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'tarifa_por_dia': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar clientes activos
        self.fields['cliente'].queryset = Cliente.objects.filter(activo=True).order_by('razon_social')
        
        # Filtrar proyectos activos
        self.fields['proyecto'].queryset = Proyecto.objects.filter(activo=True).order_by('nombre')
        
        # Establecer valores por defecto si es nuevo servicio
        if not self.instance.pk:
            self.fields['estado'].initial = 'activo'
            self.fields['periodo'].initial = 'dias'
            self.fields['cantidad_torreros'].initial = 1


class RegistroDiasTrabajarForm(forms.ModelForm):
    """Formulario para registrar días trabajados"""
    # Campo para seleccionar múltiples torreros (no es parte del modelo, se maneja separadamente)
    torreros = forms.ModelMultipleChoiceField(
        queryset=Torrero.objects.filter(activo=True),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        help_text="Selecciona los torreros que trabajaron en estos días"
    )
    
    class Meta:
        model = RegistroDiasTrabajados
        fields = [
            'fecha_registro', 'dias_trabajados', 'torreros_presentes',
            'descripcion', 'observaciones'
        ]
        widgets = {
            'fecha_registro': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'dias_trabajados': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'step': '0.5',
                'value': '1'
            }),
            'torreros_presentes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'value': '1',
                'readonly': 'readonly'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe el trabajo realizado...'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        servicio = kwargs.pop('servicio', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar torreros activos
        self.fields['torreros'].queryset = Torrero.objects.filter(activo=True).order_by('nombre')
        
        # Si hay un servicio, establecer fecha por defecto
        if servicio and not self.instance.pk:
            self.fields['fecha_registro'].initial = timezone.now().date()
        
        # Para edición, obtener torreros ya asignados al servicio
        if servicio and self.instance.pk:
            asignaciones = AsignacionTorrero.objects.filter(
                servicio=servicio,
                activo=True
            ).select_related('torrero')
            self.fields['torreros'].initial = [a.torrero.id for a in asignaciones]


class PagoServicioTorreroForm(forms.ModelForm):
    """Formulario para registrar pagos de servicios de torreros"""
    class Meta:
        model = PagoServicioTorrero
        fields = [
            'fecha_pago', 'monto', 'metodo_pago', 'numero_referencia',
            'comprobante', 'concepto', 'observaciones'
        ]
        widgets = {
            'fecha_pago': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'numero_referencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de referencia, cheque o transacción'
            }),
            'comprobante': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'concepto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Concepto del pago'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }


class TorreroForm(forms.ModelForm):
    """Formulario para crear/editar torreros"""
    class Meta:
        model = Torrero
        fields = [
            'nombre', 'cedula', 'telefono', 'email', 'direccion',
            'fecha_ingreso', 'especialidad', 'tarifa_diaria', 'foto',
            'activo', 'observaciones'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del torrero'
            }),
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cédula o documento de identidad'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección de residencia'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'especialidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Soldadura, Electricidad, etc.'
            }),
            'tarifa_diaria': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales (opcional)'
            })
        }


class SubproyectoForm(forms.ModelForm):
    """Formulario para subproyectos"""
    
    class Meta:
        model = Subproyecto
        fields = [
            'nombre', 'codigo', 'descripcion', 'cotizacion',
            'fecha_inicio', 'fecha_fin_estimada', 'estado', 
            'porcentaje_avance'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del subproyecto'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único (ej: PROJ-001-SUB-001)'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del subproyecto'
            }),
            'cotizacion': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin_estimada': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'porcentaje_avance': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '100',
                'step': '0.01'
            })
        }
    
    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        
        # Filtrar cotizaciones solo del proyecto actual
        # Mostrar TODAS las cotizaciones del proyecto sin restricción de estado
        if proyecto:
            self.fields['cotizacion'].queryset = Cotizacion.objects.filter(
                proyecto=proyecto
            ).order_by('-fecha_creacion')
        else:
            # Si no hay proyecto, mostrar todas las cotizaciones disponibles
            self.fields['cotizacion'].queryset = Cotizacion.objects.all().order_by('-fecha_creacion')
        
        # Hacer el campo opcional
        self.fields['cotizacion'].required = False
        self.fields['cotizacion'].empty_label = "Seleccionar cotización (opcional)"
