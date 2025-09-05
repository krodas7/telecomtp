from django import forms
from django.core.exceptions import ValidationError
from .models import Anticipo, Cliente, Proyecto, ArchivoProyecto, Colaborador, Factura, Gasto, Pago, CategoriaGasto, Presupuesto, PartidaPresupuesto, VariacionPresupuesto, CategoriaInventario, ItemInventario, AsignacionInventario, CarpetaProyecto
from .constants import ICONOS_CARPETAS
from decimal import Decimal


class AnticipoForm(forms.ModelForm):
    """Formulario para crear y editar anticipos"""
    
    class Meta:
        model = Anticipo
        fields = [
            'numero_anticipo', 'cliente', 'proyecto', 'tipo', 'estado',
            'monto', 'fecha_recepcion', 'fecha_vencimiento',
            'metodo_pago', 'referencia_pago', 'banco_origen',
            'descripcion', 'observaciones'
        ]
        widgets = {
            'numero_anticipo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ANT-2024-001'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select',
                'id': 'cliente-select'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select',
                'id': 'proyecto-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'fecha_recepcion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'referencia_pago': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de referencia, cheque, etc.'
            }),
            'banco_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Banco de origen del pago'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Descripción detallada del anticipo'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '2',
                'placeholder': 'Observaciones adicionales'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar proyectos por cliente seleccionado
        if self.instance.pk and self.instance.cliente:
            self.fields['proyecto'].queryset = Proyecto.objects.filter(cliente=self.instance.cliente)
        else:
            # Para nuevos anticipos, mostrar todos los proyectos activos
            # El filtro dinámico se manejará en el frontend
            self.fields['proyecto'].queryset = Proyecto.objects.filter(activo=True)
        
        # Hacer algunos campos requeridos
        self.fields['numero_anticipo'].required = True
        self.fields['cliente'].required = True
        self.fields['proyecto'].required = True
        self.fields['monto'].required = True
        self.fields['fecha_recepcion'].required = True
    
    def clean_monto(self):
        """Validar que el monto sea positivo"""
        monto = self.cleaned_data.get('monto')
        if monto and monto <= 0:
            raise ValidationError('El monto debe ser mayor a cero')
        return monto
    
    def clean_fecha_vencimiento(self):
        """Validar que la fecha de vencimiento sea posterior a la recepción"""
        fecha_recepcion = self.cleaned_data.get('fecha_recepcion')
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        
        if fecha_recepcion and fecha_vencimiento and fecha_vencimiento <= fecha_recepcion:
            raise ValidationError('La fecha de vencimiento debe ser posterior a la fecha de recepción')
        
        return fecha_vencimiento
    
    def clean(self):
        """Validaciones generales del formulario"""
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        proyecto = cleaned_data.get('proyecto')
        
        # Verificar que el proyecto pertenezca al cliente
        if cliente and proyecto and proyecto.cliente != cliente:
            raise ValidationError('El proyecto seleccionado no pertenece al cliente especificado')
        
        return cleaned_data


class AplicacionAnticipoForm(forms.Form):
    """Formulario para aplicar anticipos a facturas"""
    
    factura = forms.ModelChoiceField(
        queryset=None,
        empty_label="Seleccionar factura...",
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'factura-select'
        })
    )
    
    monto_aplicar = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'placeholder': '0.00'
        })
    )
    
    def __init__(self, anticipo=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if anticipo:
            # Filtrar facturas disponibles para este anticipo
            self.fields['factura'].queryset = anticipo.proyecto.facturas.filter(
                estado__in=['emitida', 'enviada']
            ).exclude(
                id__in=anticipo.aplicaciones.values_list('factura_id', flat=True)
            )
            
            # Establecer monto máximo disponible
            self.fields['monto_aplicar'].max_value = anticipo.monto_disponible
            self.fields['monto_aplicar'].widget.attrs['max'] = str(anticipo.monto_disponible)
    
    def clean_monto_aplicar(self):
        """Validar que el monto a aplicar no exceda el disponible"""
        monto = self.cleaned_data.get('monto_aplicar')
        anticipo = getattr(self, 'anticipo', None)
        
        if anticipo and monto and monto > anticipo.monto_disponible:
            raise ValidationError(f'El monto no puede exceder Q{anticipo.monto_disponible} disponible')
        
        return monto


class ArchivoProyectoForm(forms.ModelForm):
    """Formulario para subir archivos de proyectos"""
    
    class Meta:
        model = ArchivoProyecto
        fields = ['nombre', 'archivo', 'tipo', 'descripcion', 'carpeta']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre descriptivo del archivo'
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.txt,.dwg,.dxf,.jpg,.jpeg,.png,.gif,.bmp,.webp'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'carpeta': forms.Select(attrs={
                'class': 'form-control'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del archivo (opcional)'
            })
        }
    
    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        super().__init__(*args, **kwargs)
        
        if proyecto:
            # Filtrar carpetas solo del proyecto actual
            self.fields['carpeta'].queryset = CarpetaProyecto.objects.filter(
                proyecto=proyecto, 
                activa=True
            ).order_by('nombre')
            
            # Agregar opción para "Sin carpeta"
            self.fields['carpeta'].empty_label = "Sin carpeta (carpeta raíz)"
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar tamaño del archivo (máximo 50MB)
            if archivo.size > 50 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede ser mayor a 50MB')
            
            # Validar extensión
            extensiones_permitidas = [
                'pdf', 'doc', 'docx', 'txt', 'rtf',  # Documentos
                'dwg', 'dxf',  # Planos CAD
                'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'  # Imágenes
            ]
            extension = archivo.name.split('.')[-1].lower()
            if extension not in extensiones_permitidas:
                raise forms.ValidationError(
                    f'Extensión no permitida. Solo se permiten: {", ".join(extensiones_permitidas)}'
                )
        
        return archivo


class CarpetaProyectoForm(forms.ModelForm):
    """Formulario para crear y editar carpetas de proyectos"""
    
    class Meta:
        model = CarpetaProyecto
        fields = ['nombre', 'descripcion', 'color', 'icono', 'carpeta_padre']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la carpeta'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción de la carpeta (opcional)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'title': 'Selecciona un color para la carpeta'
            }),
            'icono': forms.Select(attrs={
                'class': 'form-control'
            }, choices=ICONOS_CARPETAS),
            'carpeta_padre': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        proyecto = kwargs.pop('proyecto', None)
        carpeta_actual = kwargs.pop('carpeta_actual', None)
        super().__init__(*args, **kwargs)
        
        if proyecto:
            # Filtrar carpetas solo del proyecto actual
            queryset = CarpetaProyecto.objects.filter(proyecto=proyecto, activa=True)
            
            # Si estamos editando una carpeta, excluirla y sus subcarpetas para evitar referencias circulares
            if carpeta_actual:
                queryset = queryset.exclude(id=carpeta_actual.id)
                # También excluir subcarpetas para evitar referencias circulares
                subcarpetas_ids = self._get_subcarpetas_ids(carpeta_actual)
                queryset = queryset.exclude(id__in=subcarpetas_ids)
            
            self.fields['carpeta_padre'].queryset = queryset.order_by('nombre')
            self.fields['carpeta_padre'].empty_label = "Carpeta raíz (sin carpeta padre)"
    
    def _get_subcarpetas_ids(self, carpeta):
        """Obtener IDs de todas las subcarpetas de una carpeta"""
        ids = []
        for subcarpeta in carpeta.subcarpetas.filter(activa=True):
            ids.append(subcarpeta.id)
            ids.extend(self._get_subcarpetas_ids(subcarpeta))
        return ids
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        proyecto = self.instance.proyecto if self.instance.pk else None
        carpeta_padre = self.cleaned_data.get('carpeta_padre')
        
        if proyecto:
            # Verificar que no exista otra carpeta con el mismo nombre en el mismo nivel
            queryset = CarpetaProyecto.objects.filter(
                proyecto=proyecto,
                carpeta_padre=carpeta_padre,
                activa=True
            )
            
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            
            if queryset.filter(nombre=nombre).exists():
                if carpeta_padre:
                    raise forms.ValidationError(
                        f'Ya existe una carpeta llamada "{nombre}" en "{carpeta_padre.nombre}"'
                    )
                else:
                    raise forms.ValidationError(
                        f'Ya existe una carpeta raíz llamada "{nombre}"'
                    )
        
        return nombre


class ClienteForm(forms.ModelForm):
    """Formulario para crear y editar clientes"""
    
    class Meta:
        model = Cliente
        fields = [
            'razon_social', 'codigo_fiscal', 'email', 'telefono', 
            'direccion', 'activo'
        ]
        widgets = {
            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón Social o Nombre'
            }),
            'codigo_fiscal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NIT, DPI, etc.'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

        }


class ProyectoForm(forms.ModelForm):
    """Formulario para crear y editar proyectos"""
    
    class Meta:
        model = Proyecto
        fields = [
            'nombre', 'descripcion', 'cliente', 'presupuesto', 
            'fecha_inicio', 'fecha_fin', 'estado', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del proyecto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción detallada del proyecto'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'presupuesto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_fin': forms.DateInput(attrs={
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
    """Formulario para crear y editar colaboradores"""
    
    class Meta:
        model = Colaborador
        fields = [
            'nombre', 'dpi', 'direccion', 'telefono', 'email', 
            'salario', 'fecha_contratacion', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'dpi': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de DPI'
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Dirección completa'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Teléfono de contacto'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'salario': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'fecha_contratacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class FacturaForm(forms.ModelForm):
    """Formulario para crear y editar facturas"""
    
    class Meta:
        model = Factura
        fields = [
            'numero_factura', 'proyecto', 'cliente', 'tipo', 
            'fecha_emision', 'fecha_vencimiento', 'monto_subtotal', 
            'monto_iva', 'descripcion_servicios', 'estado'
        ]
        widgets = {
            'numero_factura': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'FAC-2024-001'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cliente': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'fecha_emision': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_vencimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'monto_subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'monto_iva': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.00',
                'placeholder': '0.00'
            }),
            'descripcion_servicios': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Descripción de los servicios facturados'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }


class GastoForm(forms.ModelForm):
    """Formulario para crear y editar gastos"""
    
    class Meta:
        model = Gasto
        fields = [
            'proyecto', 'categoria', 'descripcion', 'monto', 
            'fecha_gasto', 'aprobado'
        ]
        widgets = {
            'proyecto': forms.Select(attrs={
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
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
            }),
            'fecha_gasto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'aprobado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


class PagoForm(forms.ModelForm):
    """Formulario para crear y editar pagos"""
    
    class Meta:
        model = Pago
        fields = [
            'factura', 'monto', 'fecha_pago', 'metodo_pago', 
            'estado'
        ]
        widgets = {
            'factura': forms.Select(attrs={
                'class': 'form-select'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
                'placeholder': '0.00'
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

        }


class CategoriaGastoForm(forms.ModelForm):
    """Formulario para crear y editar categorías de gasto"""
    
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
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '#007bff',
                'type': 'text'
            }),
            'icono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fas fa-tools'
            }),
        }

class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['nombre', 'version', 'estado', 'observaciones']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PartidaPresupuestoForm(forms.ModelForm):
    class Meta:
        model = PartidaPresupuesto
        fields = ['codigo', 'descripcion', 'unidad', 'cantidad', 'precio_unitario', 'categoria', 'subcategoria', 'notas', 'orden']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'unidad': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'subcategoria': forms.TextInput(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'orden': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class VariacionPresupuestoForm(forms.ModelForm):
    class Meta:
        model = VariacionPresupuesto
        fields = ['tipo', 'monto_anterior', 'monto_nuevo', 'motivo']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'monto_anterior': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'monto_nuevo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# ===== FORMULARIOS DEL MÓDULO DE INVENTARIO =====

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
                'rows': 3,
                'placeholder': 'Descripción de la categoría'
            })
        }

class ItemInventarioForm(forms.ModelForm):
    """Formulario para items del inventario"""
    class Meta:
        model = ItemInventario
        fields = [
            'nombre', 'codigo', 'descripcion', 'categoria', 'stock_actual', 'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del item'
            }),
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Código único del item'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada del item'
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select'
            }),
            'stock_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

class AsignacionInventarioForm(forms.ModelForm):
    """Formulario para asignaciones de inventario"""
    class Meta:
        model = AsignacionInventario
        fields = ['item', 'proyecto', 'cantidad_asignada', 'estado', 'notas']
        widgets = {
            'item': forms.Select(attrs={
                'class': 'form-select'
            }),
            'proyecto': forms.Select(attrs={
                'class': 'form-select'
            }),
            'cantidad_asignada': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales sobre la asignación'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo items activos y con stock disponible
        self.fields['item'].queryset = ItemInventario.objects.filter(
            activo=True
        ).order_by('nombre')
        
        # Filtrar solo proyectos activos
        self.fields['proyecto'].queryset = Proyecto.objects.filter(
            estado__in=['activo', 'en_progreso', 'planificado']
        ).order_by('nombre')
