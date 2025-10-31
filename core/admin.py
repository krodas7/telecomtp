from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Rol, PerfilUsuario, Cliente, Colaborador, Proyecto,
    Factura, Pago, CategoriaGasto, Gasto, GastoFijoMensual,
    LogActividad, ArchivoAdjunto, Anticipo, AplicacionAnticipo,
    ArchivoProyecto, CarpetaProyecto, ConfiguracionSistema,
    Cotizacion, ItemCotizacion
)


class PerfilUsuarioInline(admin.StackedInline):
    model = PerfilUsuario
    can_delete = False
    verbose_name_plural = 'Perfil de Usuario'


class UserAdmin(UserAdmin):
    inlines = (PerfilUsuarioInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'creado_en']
    search_fields = ['nombre']
    list_filter = ['creado_en']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['razon_social', 'codigo_fiscal', 'email', 'telefono', 'activo', 'creado_en']
    list_filter = ['activo', 'creado_en']
    search_fields = ['razon_social', 'codigo_fiscal', 'email']
    list_editable = ['activo']


@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'dpi', 'email', 'salario', 'fecha_contratacion', 'activo']
    list_filter = ['activo', 'fecha_contratacion']
    search_fields = ['nombre', 'dpi', 'email']
    list_editable = ['activo']


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'estado', 'fecha_inicio', 'activo']
    list_filter = ['estado', 'activo', 'fecha_inicio', 'cliente']
    search_fields = ['nombre', 'cliente__razon_social']
    list_editable = ['estado', 'activo']
    date_hierarchy = 'fecha_inicio'


@admin.register(Anticipo)
class AnticipoAdmin(admin.ModelAdmin):
    list_display = ['numero_anticipo', 'cliente', 'proyecto', 'monto', 'monto_aplicado', 'monto_disponible', 'estado', 'fecha_recepcion', 'tipo']
    list_filter = ['estado', 'tipo', 'metodo_pago', 'fecha_recepcion', 'cliente', 'proyecto']
    search_fields = ['numero_anticipo', 'cliente__nombre', 'proyecto__nombre', 'descripcion']
    readonly_fields = ['monto_disponible', 'porcentaje_aplicado', 'dias_vencimiento', 'fecha_creacion', 'fecha_modificacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_anticipo', 'cliente', 'proyecto', 'tipo', 'estado')
        }),
        ('Montos', {
            'fields': ('monto', 'monto_aplicado', 'monto_disponible', 'porcentaje_aplicado')
        }),
        ('Fechas', {
            'fields': ('fecha_recepcion', 'fecha_vencimiento', 'fecha_aplicacion', 'dias_vencimiento')
        }),
        ('Información de Pago', {
            'fields': ('metodo_pago', 'referencia_pago', 'banco_origen')
        }),
        ('Detalles', {
            'fields': ('descripcion', 'observaciones')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'modificado_por', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nuevo anticipo
            obj.creado_por = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(AplicacionAnticipo)
class AplicacionAnticipoAdmin(admin.ModelAdmin):
    list_display = ['anticipo', 'factura', 'monto_aplicado', 'fecha_aplicacion', 'aplicado_por']
    list_filter = ['fecha_aplicacion', 'anticipo__cliente', 'factura__proyecto']
    search_fields = ['anticipo__numero_anticipo', 'factura__numero_factura']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Aplicación', {
            'fields': ('anticipo', 'factura', 'monto_aplicado')
        }),
        ('Fechas', {
            'fields': ('fecha_aplicacion', 'fecha_creacion')
        }),
        ('Usuario', {
            'fields': ('aplicado_por',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nueva aplicación
            obj.aplicado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_factura', 'cliente', 'proyecto', 'monto_total', 'monto_pendiente', 'estado', 'fecha_emision', 'fecha_vencimiento']
    list_filter = ['estado', 'tipo', 'fecha_emision', 'fecha_vencimiento', 'cliente', 'proyecto']
    search_fields = ['numero_factura', 'cliente__nombre', 'proyecto__nombre', 'descripcion_servicios']
    readonly_fields = ['monto_pendiente', 'porcentaje_pagado', 'dias_vencimiento', 'fecha_creacion', 'fecha_modificacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_factura', 'proyecto', 'cliente', 'tipo', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_vencimiento', 'fecha_pago', 'dias_vencimiento')
        }),
        ('Montos', {
            'fields': ('monto_subtotal', 'monto_iva', 'monto_total', 'monto_pagado', 'monto_anticipos', 'monto_pendiente', 'porcentaje_pagado')
        }),
        ('Detalles', {
            'fields': ('descripcion_servicios', 'porcentaje_avance')
        }),
        ('Pago', {
            'fields': ('metodo_pago', 'referencia_pago', 'banco_origen')
        }),
        ('Adicionales', {
            'fields': ('observaciones', 'archivos_adjuntos')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'modificado_por', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Nueva factura
            obj.creado_por = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'factura', 'monto', 'metodo_pago', 'estado', 'fecha_pago']
    list_filter = ['estado', 'metodo_pago', 'fecha_pago']
    search_fields = ['factura__numero_factura']
    list_editable = ['estado']


@admin.register(CategoriaGasto)
class CategoriaGastoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'creado_en']
    search_fields = ['nombre']


@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ['descripcion', 'proyecto', 'categoria', 'monto', 'fecha_gasto', 'aprobado']
    list_filter = ['aprobado', 'categoria', 'fecha_gasto', 'proyecto']
    search_fields = ['descripcion', 'proyecto__nombre']
    list_editable = ['aprobado']
    date_hierarchy = 'fecha_gasto'


@admin.register(GastoFijoMensual)
class GastoFijoMensualAdmin(admin.ModelAdmin):
    list_display = ['concepto', 'monto', 'activo', 'creado_en']
    list_filter = ['activo', 'creado_en']
    list_editable = ['activo', 'monto']


@admin.register(LogActividad)
class LogActividadAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'accion', 'modulo', 'fecha_actividad', 'ip_address']
    list_filter = ['accion', 'modulo', 'fecha_actividad', 'usuario']
    search_fields = ['usuario__username', 'accion', 'modulo']
    date_hierarchy = 'fecha_actividad'
    readonly_fields = ['fecha_actividad', 'ip_address', 'user_agent']


@admin.register(ArchivoAdjunto)
class ArchivoAdjuntoAdmin(admin.ModelAdmin):
    list_display = ['nombre_archivo', 'tipo', 'registro_id', 'uploaded_by', 'creado_en']
    list_filter = ['tipo', 'creado_en', 'uploaded_by']
    search_fields = ['nombre_archivo', 'tipo']
    readonly_fields = ['tamano', 'tipo_mime', 'creado_en']


@admin.register(ArchivoProyecto)
class ArchivoProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'proyecto', 'tipo', 'subido_por', 'fecha_subida', 'activo']
    list_filter = ['tipo', 'activo', 'fecha_subida', 'proyecto']
    search_fields = ['nombre', 'descripcion', 'proyecto__nombre']
    readonly_fields = ['fecha_subida', 'subido_por']
    list_per_page = 25
    
    fieldsets = (
        ('Información del Archivo', {
            'fields': ('proyecto', 'nombre', 'archivo', 'tipo', 'descripcion')
        }),
        ('Metadatos', {
            'fields': ('subido_por', 'fecha_subida', 'activo'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo archivo
            obj.subido_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(CarpetaProyecto)
class CarpetaProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'proyecto', 'carpeta_padre', 'color', 'icono', 'creada_por', 'fecha_creacion', 'activa']
    list_filter = ['activa', 'fecha_creacion', 'proyecto', 'carpeta_padre']
    search_fields = ['nombre', 'descripcion', 'proyecto__nombre']
    readonly_fields = ['fecha_creacion', 'creada_por']
    list_per_page = 25
    
    fieldsets = (
        ('Información de la Carpeta', {
            'fields': ('proyecto', 'nombre', 'descripcion', 'carpeta_padre')
        }),
        ('Personalización', {
            'fields': ('color', 'icono')
        }),
        ('Metadatos', {
            'fields': ('creada_por', 'fecha_creacion', 'activa'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'moneda', 'zona_horaria', 'idioma', 'ultima_actualizacion']
    readonly_fields = ['ultima_actualizacion']
    
    fieldsets = (
        ('Información de la Empresa', {
            'fields': ('nombre_empresa', 'moneda')
        }),
        ('Configuración Regional', {
            'fields': ('zona_horaria', 'idioma')
        }),
        ('Configuración del Sistema', {
            'fields': ('max_usuarios_simultaneos', 'tiempo_sesion')
        }),
        ('Configuraciones Avanzadas', {
            'fields': ('respaldo_automatico', 'notificaciones_email')
        }),
        ('Configuración de Email', {
            'fields': ('email_host', 'email_port', 'email_username', 'email_password', 'email_use_tls'),
            'classes': ('collapse',)
        }),
        ('Metadatos', {
            'fields': ('ultima_actualizacion', 'actualizado_por'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir una configuración
        return not ConfiguracionSistema.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # No permitir eliminar la configuración
        return False
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva carpeta
            obj.creada_por = request.user
        super().save_model(request, obj, form, change)


class ItemCotizacionInline(admin.TabularInline):
    """Inline para items de cotización"""
    model = ItemCotizacion
    extra = 1
    fields = ['descripcion', 'cantidad', 'precio_unitario', 'precio_costo', 'total', 'orden']
    readonly_fields = ['total']
    ordering = ['orden']


@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ['numero_cotizacion', 'titulo', 'cliente', 'proyecto', 'monto_total', 'estado', 'fecha_emision']
    list_filter = ['estado', 'tipo_cotizacion', 'fecha_emision', 'fecha_vencimiento']
    search_fields = ['numero_cotizacion', 'titulo', 'cliente__razon_social', 'proyecto__nombre']
    readonly_fields = ['monto_iva', 'monto_total', 'fecha_creacion', 'fecha_modificacion', 'creado_por', 'modificado_por']
    date_hierarchy = 'fecha_emision'
    inlines = [ItemCotizacionInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_cotizacion', 'titulo', 'proyecto', 'cliente', 'tipo_cotizacion', 'estado')
        }),
        ('Descripción', {
            'fields': ('descripcion',)
        }),
        ('Montos', {
            'fields': ('monto_subtotal', 'monto_iva', 'monto_total')
        }),
        ('Fechas', {
            'fields': ('fecha_emision', 'fecha_vencimiento', 'fecha_aceptacion', 'validez_dias')
        }),
        ('Condiciones', {
            'fields': ('condiciones_pago', 'terminos_condiciones')
        }),
        ('Archivos y Notas', {
            'fields': ('archivo_cotizacion', 'observaciones', 'notas_cliente')
        }),
        ('Auditoría', {
            'fields': ('creado_por', 'fecha_creacion', 'modificado_por', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        obj.modificado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(ItemCotizacion)
class ItemCotizacionAdmin(admin.ModelAdmin):
    list_display = ['cotizacion', 'descripcion', 'cantidad', 'precio_unitario', 'total', 'orden']
    list_filter = ['cotizacion__estado', 'cotizacion__proyecto']
    search_fields = ['descripcion', 'cotizacion__numero_cotizacion']
    readonly_fields = ['total', 'creado_en', 'modificado_en']
    list_per_page = 25
