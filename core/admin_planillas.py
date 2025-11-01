from django.contrib import admin
from .models import ConfiguracionPlanilla, PlanillaLiquidada


@admin.register(ConfiguracionPlanilla)
class ConfiguracionPlanillaAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'total_retenciones_porcentaje', 'aplicar_retenciones', 'aplicar_bonos']
    list_filter = ['aplicar_retenciones', 'aplicar_bonos']
    search_fields = ['proyecto__nombre']
    readonly_fields = ['total_retenciones_porcentaje', 'creado_en', 'modificado_en']


@admin.register(PlanillaLiquidada)
class PlanillaLiquidadaAdmin(admin.ModelAdmin):
    list_display = ['proyecto', 'mes', 'año', 'quincena', 'total_planilla', 'cantidad_personal', 'liquidada_por']
    list_filter = ['año', 'mes', 'quincena']
    search_fields = ['proyecto__nombre']
    readonly_fields = ['fecha_liquidacion']

