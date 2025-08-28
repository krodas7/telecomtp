from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import models
from django.db.models import Sum, Count, Q, F, Avg
from django.db.models.functions import Extract
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from django.core.cache import cache
import os
import json
import logging
from .models import (
    Cliente, Proyecto, Colaborador, Factura, Pago, 
    Gasto, CategoriaGasto, GastoFijoMensual, LogActividad, Anticipo, AplicacionAnticipo, ArchivoProyecto, Presupuesto, PartidaPresupuesto, VariacionPresupuesto,
    NotificacionSistema, ConfiguracionNotificaciones, HistorialNotificaciones,
    ItemInventario, CategoriaInventario, AsignacionInventario,
    Rol, PerfilUsuario, Modulo, Permiso, RolPermiso, AnticipoProyecto,
    CarpetaProyecto
)
from .forms import (
    AnticipoForm, ArchivoProyectoForm, ClienteForm, ProyectoForm, 
    ColaboradorForm, FacturaForm, GastoForm, PagoForm, CategoriaGastoForm, PresupuestoForm, PartidaPresupuestoForm, VariacionPresupuestoForm,
    CategoriaInventarioForm, ItemInventarioForm, AsignacionInventarioForm,
    CarpetaProyectoForm
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from .services import NotificacionService, SistemaNotificacionesAutomaticas
# from .optimization import performance_monitor  # ELIMINADO
from django.conf import settings
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO

# Configurar logger
logger = logging.getLogger(__name__)

def login_view(request):
    """Vista de login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Registrar actividad
            LogActividad.objects.create(
                usuario=user,
                accion='Login',
                modulo='Sistema',
                descripcion=f'Usuario {username} inició sesión',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas')
    
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    """Vista de logout"""
    # Registrar actividad
    LogActividad.objects.create(
        usuario=request.user,
        accion='Logout',
        modulo='Sistema',
        descripcion=f'Usuario {request.user.username} cerró sesión',
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    """
    Vista del dashboard principal SUPER SIMPLE Y FUNCIONAL
    """
    try:
        # Datos básicos del sistema
        total_clientes = Cliente.objects.filter(activo=True).count()
        total_proyectos = Proyecto.objects.filter(activo=True).count()
        total_facturado = Factura.objects.aggregate(total=Sum('monto_total'))['total'] or 0
        total_cobrado = Factura.objects.filter(estado='pagada').aggregate(total=Sum('monto_total'))['total'] or 0
        
        # ============================================================================
        # DATOS DE RENTABILIDAD REAL
        # ============================================================================
        
        # Calcular rentabilidad del mes actual
        hoy = timezone.now()
        mes_actual = hoy.month
        año_actual = hoy.year
        
        # Ingresos del mes (SOLO facturas pagadas, no facturadas)
        ingresos_mes = Factura.objects.filter(
            fecha_emision__month=mes_actual,
            fecha_emision__year=año_actual,
            estado='pagada'  # Solo facturas pagadas
        ).aggregate(total=Sum('monto_total'))['total'] or Decimal('0.00')
        
        # DEBUG: Mostrar diferencia en dashboard
        total_facturado_mes = Factura.objects.filter(
            fecha_emision__month=mes_actual,
            fecha_emision__year=año_actual
        ).aggregate(total=Sum('monto_total'))['total'] or Decimal('0.00')
        
        print(f"🔍 DEBUG DASHBOARD - Mes: {mes_actual}/{año_actual}")
        print(f"🔍 DEBUG DASHBOARD - Facturado: Q{total_facturado_mes}")
        print(f"🔍 DEBUG DASHBOARD - Cobrado: Q{ingresos_mes}")
        print(f"🔍 DEBUG DASHBOARD - Pendiente: Q{total_facturado_mes - ingresos_mes}")
        
        # Gastos del mes (gastos aprobados)
        gastos_mes = Gasto.objects.filter(
            fecha_gasto__month=mes_actual,
            fecha_gasto__year=año_actual,
            aprobado=True
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
        
        # Calcular rentabilidad
        rentabilidad_mes = ingresos_mes - gastos_mes
        margen_rentabilidad = (rentabilidad_mes / ingresos_mes * 100) if ingresos_mes > 0 else Decimal('0.00')
        
        # Gastos por categoría del mes
        gastos_categoria_mes = Gasto.objects.filter(
            fecha_gasto__month=mes_actual,
            fecha_gasto__year=año_actual,
            aprobado=True
        ).values('categoria__nombre').annotate(
            total=Sum('monto')
        ).order_by('-total')[:5]
        
        # Proyectos más rentables del mes
        proyectos_rentables = []
        proyectos_activos = Proyecto.objects.filter(activo=True)
        
        for proyecto in proyectos_activos:
            ingresos_proyecto = Factura.objects.filter(
                proyecto=proyecto,
                fecha_emision__month=mes_actual,
                fecha_emision__year=año_actual,
                monto_pagado__gt=0
            ).aggregate(total=Sum('monto_pagado'))['total'] or Decimal('0.00')
            
            gastos_proyecto = Gasto.objects.filter(
                proyecto=proyecto,
                fecha_gasto__month=mes_actual,
                fecha_gasto__year=año_actual,
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            
            rentabilidad_proyecto = ingresos_proyecto - gastos_proyecto
            
            if rentabilidad_proyecto > 0:  # Solo proyectos rentables
                proyectos_rentables.append({
                    'nombre': proyecto.nombre,
                    'rentabilidad': rentabilidad_proyecto,
                    'ingresos': ingresos_proyecto,
                    'gastos': gastos_proyecto
                })
        
        # Ordenar por rentabilidad
        proyectos_rentables.sort(key=lambda x: x['rentabilidad'], reverse=True)
        proyectos_rentables = proyectos_rentables[:5]  # Top 5
        
        # Calendario con eventos básicos
        eventos_calendario = []
        
        # Eventos de facturas
        facturas = Factura.objects.filter(fecha_vencimiento__isnull=False)[:5]
        for factura in facturas:
            eventos_calendario.append({
                'id': f'factura_{factura.id}',
                'title': f'Vencimiento: {factura.numero_factura}',
                'start': factura.fecha_vencimiento.isoformat(),
                'end': factura.fecha_vencimiento.isoformat(),
                'className': 'evento-factura',
                'backgroundColor': '#dc3545',
                'borderColor': '#dc3545'
            })
        
        # Eventos de proyectos
        proyectos = Proyecto.objects.filter(fecha_inicio__isnull=False)[:5]
        for proyecto in proyectos:
            eventos_calendario.append({
                'id': f'proyecto_{proyecto.id}',
                'title': f'Inicio: {proyecto.nombre}',
                'start': proyecto.fecha_inicio.isoformat(),
                'end': proyecto.fecha_inicio.isoformat(),
                'className': 'evento-proyecto',
                'backgroundColor': '#28a745',
                'borderColor': '#28a745'
            })
        
        # Convertir a JSON para el template
        import json
        eventos_calendario_json = json.dumps(eventos_calendario, default=str)
        
        # DEBUG: Imprimir contexto
        print(f"🔍 DEBUG - Eventos calendario: {eventos_calendario}")
        print(f"🔍 DEBUG - Eventos JSON: {eventos_calendario_json}")
        
        # Datos simples para gráficos (sin cálculos complejos por ahora)
        meses_grafico = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
        
        # Convertir Decimal a float para evitar errores de tipo
        total_facturado_float = float(total_facturado) if total_facturado else 0.0
        
        ingresos_mensuales = [total_facturado_float * 0.1, total_facturado_float * 0.15, total_facturado_float * 0.2, total_facturado_float * 0.25, total_facturado_float * 0.3, total_facturado_float * 0.35]
        gastos_mensuales = [total_facturado_float * 0.05, total_facturado_float * 0.1, total_facturado_float * 0.15, total_facturado_float * 0.2, total_facturado_float * 0.25, total_facturado_float * 0.3]
        evolucion_proyectos = [1, 2, 1, 3, 2, total_proyectos]
        
        # Obtener período seleccionado (por defecto 6 meses)
        periodo = request.GET.get('periodo', '6')
        
        # Generar datos del gráfico según el período
        if periodo == '3':
            # 3 meses
            meses_grafico = ['Abr', 'May', 'Jun']
            total_facturado_float = float(total_facturado) if total_facturado else 0.0
            ingresos_mensuales = [total_facturado_float * 0.25, total_facturado_float * 0.3, total_facturado_float * 0.35]
            gastos_mensuales = [total_facturado_float * 0.2, total_facturado_float * 0.25, total_facturado_float * 0.3]
            evolucion_proyectos = [3, 2, total_proyectos]
        elif periodo == '1':
            # Mes actual
            from datetime import datetime
            mes_actual = datetime.now().strftime('%b')
            meses_grafico = [mes_actual]
            total_facturado_float = float(total_facturado) if total_facturado else 0.0
            ingresos_mensuales = [total_facturado_float * 0.35]
            gastos_mensuales = [total_facturado_float * 0.3]
            evolucion_proyectos = [total_proyectos]
        else:
            # 6 meses (por defecto)
            meses_grafico = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun']
            total_facturado_float = float(total_facturado) if total_facturado else 0.0
            ingresos_mensuales = [total_facturado_float * 0.1, total_facturado_float * 0.15, total_facturado_float * 0.2, total_facturado_float * 0.25, total_facturado_float * 0.3, total_facturado_float * 0.35]
            gastos_mensuales = [total_facturado_float * 0.05, total_facturado_float * 0.1, total_facturado_float * 0.15, total_facturado_float * 0.2, total_facturado_float * 0.25, total_facturado_float * 0.3]
            evolucion_proyectos = [1, 2, 1, 3, 2, total_proyectos]
        
        # Contexto simplificado
        context = {
            'total_clientes': total_clientes,
            'total_proyectos': total_proyectos,
            'total_facturado': total_facturado,
            'total_cobrado': total_cobrado,
            'eventos_calendario': eventos_calendario,
            'eventos_calendario_json': eventos_calendario_json,
            'evolucion_proyectos': evolucion_proyectos,
            'categorias_gastos': ['Materiales', 'Mano de Obra', 'Equipos', 'Administrativos'],
            'montos_gastos': [total_facturado_float * 0.4, total_facturado_float * 0.3, total_facturado_float * 0.2, total_facturado_float * 0.1],
            'ingresos_mensuales': ingresos_mensuales,
            'gastos_mensuales': gastos_mensuales,
            'meses_grafico': meses_grafico,
            'periodo_actual': periodo,
            # ============================================================================
            # DATOS DE RENTABILIDAD REAL PARA EL DASHBOARD
            # ============================================================================
            'ingresos_mes': ingresos_mes,
            'gastos_mes': gastos_mes,
            'rentabilidad_mes': rentabilidad_mes,
            'margen_rentabilidad': margen_rentabilidad,
            'gastos_categoria_mes': gastos_categoria_mes,
            'proyectos_rentables': proyectos_rentables,
        }
        
        # DEBUG: Imprimir contexto final
        print(f"🔍 DEBUG - Contexto final: {list(context.keys())}")
        print(f"🔍 DEBUG - Eventos JSON en contexto: {context.get('eventos_calendario_json', 'NO ENCONTRADO')}")
        
        # DEBUG: Verificar si hay algún problema con Decimal
        print(f"🔍 DEBUG - Verificando contexto completo...")
        for key, value in context.items():
            if isinstance(value, (int, float)):
                print(f"   ✅ {key}: {value} (tipo: {type(value).__name__})")
            elif isinstance(value, str):
                print(f"   ✅ {key}: {value[:50]}... (tipo: string)")
            elif isinstance(value, list):
                print(f"   ✅ {key}: {len(value)} elementos (tipo: list)")
            else:
                print(f"   ⚠️ {key}: {value} (tipo: {type(value).__name__})")
        
        return render(request, 'core/dashboard.html', context)
        
    except Exception as e:
        logger.error(f"Error en dashboard: {str(e)}")
        # Contexto de emergencia
        print(f"🔍 DEBUG - Usando contexto de emergencia")
        context = {
            'total_clientes': 0,
            'total_proyectos': 0,
            'total_facturado': 0,
            'total_cobrado': 0,
            'eventos_calendario': [],
            'eventos_calendario_json': '[]',
            'evolucion_proyectos': [],
            'categorias_gastos': [],
            'montos_gastos': [],
            'ingresos_mensuales': [],
            'gastos_mensuales': [],
            'meses_grafico': [],
        }
        
        return render(request, 'core/dashboard.html', context)


# ===== CRUD CLIENTES =====
@login_required
def clientes_list(request):
    """Lista de clientes"""
    # Obtener todos los clientes (activos e inactivos) para la lista
    clientes = Cliente.objects.all().order_by('razon_social')
    
    # Calcular estadísticas correctas
    total_clientes = Cliente.objects.count()
    clientes_activos = Cliente.objects.filter(activo=True).count()
    clientes_inactivos = Cliente.objects.filter(activo=False).count()
    
    context = {
        'clientes': clientes,
        'total_clientes': total_clientes,
        'clientes_activos': clientes_activos,
        'clientes_inactivos': clientes_inactivos,
    }
    
    return render(request, 'core/clientes/list.html', context)


@login_required
def cliente_create(request):
    """Crear cliente"""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Clientes',
                descripcion=f'Cliente creado: {cliente.razon_social}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Cliente creado exitosamente')
            return redirect('clientes_list')
    else:
        form = ClienteForm()
    
    return render(request, 'core/clientes/create.html', {'form': form})


@login_required
def cliente_edit(request, cliente_id):
    """Editar cliente"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Clientes',
                descripcion=f'Cliente editado: {cliente.razon_social}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Cliente actualizado exitosamente')
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    
    return render(request, 'core/clientes/edit.html', {'form': form, 'cliente': cliente})


@login_required
def cliente_delete(request, cliente_id):
    """Eliminar cliente (desactivar)"""
    cliente = get_object_or_404(Cliente, id=cliente_id)
    
    if request.method == 'POST':
        cliente.activo = False
        cliente.save()
        
        # Registrar actividad
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Clientes',
            descripcion=f'Cliente desactivado: {cliente.razon_social}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Cliente eliminado exitosamente')
        return redirect('clientes_list')
    
    return render(request, 'core/clientes/delete.html', {'cliente': cliente})


# ===== CRUD PROYECTOS =====
@login_required
def proyectos_list(request):
    """Lista de proyectos con paginación"""
    
    # Obtener parámetros de paginación
    per_page = int(request.GET.get('per_page', 25))
    page = request.GET.get('page', 1)
    
    # Aplicar filtros si existen
    filters = {}
    estado = request.GET.get('estado')
    cliente_id = request.GET.get('cliente')
    
    if estado:
        filters['estado'] = estado
    if cliente_id:
        filters['cliente_id'] = cliente_id
    
    # Query base optimizada
    proyectos = Proyecto.objects.filter(activo=True).select_related(
        'cliente'
    ).order_by('-creado_en')
    
    # Aplicar filtros
    for field, value in filters.items():
        if value:
            proyectos = proyectos.filter(**{field: value})
    
    # Paginar resultados
    from django.core.paginator import Paginator
    paginator = Paginator(proyectos, per_page)
    
    try:
        page_obj = paginator.page(page)
    except:
        page_obj = paginator.page(1)
    
    # Obtener opciones de filtro
    clientes = Cliente.objects.filter(activo=True).order_by('razon_social')
    estados = Proyecto.ESTADO_CHOICES
    
    # Obtener estadísticas totales (sin filtros)
    total_proyectos = Proyecto.objects.filter(activo=True).count()
    proyectos_en_progreso = Proyecto.objects.filter(activo=True, estado='en_progreso').count()
    proyectos_completados = Proyecto.objects.filter(activo=True, estado='completado').count()
    proyectos_pendientes = Proyecto.objects.filter(activo=True, estado='pendiente').count()
    proyectos_cancelados = Proyecto.objects.filter(activo=True, estado='cancelado').count()
    
    context = {
        'proyectos': page_obj,
        'clientes': clientes,
        'estados': estados,
        'total_proyectos': total_proyectos,
        'proyectos_en_progreso': proyectos_en_progreso,
        'proyectos_completados': proyectos_completados,
        'proyectos_pendientes': proyectos_pendientes,
        'proyectos_cancelados': proyectos_cancelados,
        'filtros_activos': {
            'estado': request.GET.get('estado'),
            'cliente': request.GET.get('cliente'),
        },
        'paginator': paginator,
        'page_obj': page_obj,
    }
    
    return render(request, 'core/proyectos/list.html', context)


@login_required
def proyecto_create(request):
    """Crear proyecto"""
    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            # Asegurar que el proyecto se cree como activo
            proyecto.activo = True
            proyecto.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Proyectos',
                descripcion=f'Proyecto creado: {proyecto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Proyecto creado exitosamente')
            return redirect('proyectos_list')
    else:
        form = ProyectoForm()
    
    # Obtener clientes activos para el dropdown
    clientes = Cliente.objects.filter(activo=True).order_by('razon_social')
    
    # Obtener estadísticas para el sidebar
    proyectos_activos = Proyecto.objects.filter(activo=True).count()
    presupuesto_promedio = Proyecto.objects.filter(activo=True).aggregate(
        promedio=Avg('presupuesto')
    )['promedio'] or 0.00
    
    context = {
        'form': form,
        'clientes': clientes,
        'proyectos_activos': proyectos_activos,
        'presupuesto_promedio': presupuesto_promedio
    }
    
    return render(request, 'core/proyectos/create.html', context)


@login_required
def proyecto_edit(request, proyecto_id):
    """Editar proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            proyecto = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Proyectos',
                descripcion=f'Proyecto editado: {proyecto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Proyecto actualizado exitosamente')
            return redirect('proyectos_list')
    else:
        form = ProyectoForm(instance=proyecto)
    
    # Obtener clientes activos para el dropdown
    clientes = Cliente.objects.filter(activo=True).order_by('razon_social')
    
    # Obtener estadísticas para el sidebar
    proyectos_activos = Proyecto.objects.filter(activo=True).count()
    presupuesto_promedio = Proyecto.objects.filter(activo=True).aggregate(
        promedio=Avg('presupuesto')
    )['promedio'] or 0.00
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'clientes': clientes,
        'proyectos_activos': proyectos_activos,
        'presupuesto_promedio': presupuesto_promedio
    }
    
    return render(request, 'core/proyectos/edit.html', context)


@login_required
def proyecto_delete(request, proyecto_id):
    """Eliminar proyecto (desactivar)"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        proyecto.activo = False
        proyecto.save()
        
        # Registrar actividad
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Proyectos',
            descripcion=f'Proyecto desactivado: {proyecto.nombre}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Proyecto eliminado exitosamente')
        return redirect('proyectos_list')
    
    return render(request, 'core/proyectos/delete.html', {'proyecto': proyecto})


# ===== CRUD COLABORADORES =====
@login_required
def colaboradores_list(request):
    """Lista de colaboradores"""
    # Obtener todos los colaboradores (activos e inactivos) para la lista
    colaboradores = Colaborador.objects.all().order_by('nombre')
    
    # Calcular estadísticas correctas
    total_colaboradores = Colaborador.objects.count()
    colaboradores_activos = Colaborador.objects.filter(activo=True).count()
    colaboradores_inactivos = Colaborador.objects.filter(activo=False).count()
    
    context = {
        'colaboradores': colaboradores,
        'total_colaboradores': total_colaboradores,
        'colaboradores_activos': colaboradores_activos,
        'colaboradores_inactivos': colaboradores_inactivos,
    }
    
    return render(request, 'core/colaboradores/list.html', context)


@login_required
def colaborador_detail(request, colaborador_id):
    """Detalle de colaborador"""
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    
    # Obtener proyectos del colaborador usando la relación ManyToManyField
    proyectos = colaborador.proyectos.all()
    
    context = {
        'colaborador': colaborador,
        'proyectos': proyectos
    }
    
    return render(request, 'core/colaboradores/detail.html', context)


@login_required
def asignar_colaboradores_proyecto(request, proyecto_id):
    """Asignar colaboradores a un proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        colaboradores_ids = request.POST.getlist('colaboradores')
        
        # Limpiar asignaciones existentes
        proyecto.colaboradores.clear()
        
        # Asignar nuevos colaboradores
        if colaboradores_ids:
            colaboradores = Colaborador.objects.filter(id__in=colaboradores_ids, activo=True)
            proyecto.colaboradores.add(*colaboradores)
            
            messages.success(request, f'Colaboradores asignados exitosamente al proyecto {proyecto.nombre}')
        else:
            messages.info(request, f'No se asignaron colaboradores al proyecto {proyecto.nombre}')
        
        return redirect('proyectos_list')
    
    # Obtener todos los colaboradores activos
    colaboradores_disponibles = Colaborador.objects.filter(activo=True).order_by('nombre')
    colaboradores_asignados = proyecto.colaboradores.all()
    
    context = {
        'proyecto': proyecto,
        'colaboradores_disponibles': colaboradores_disponibles,
        'colaboradores_asignados': colaboradores_asignados,
    }
    
    return render(request, 'core/proyectos/asignar_colaboradores.html', context)


@login_required
def colaborador_create(request):
    """Crear colaborador"""
    if request.method == 'POST':
        form = ColaboradorForm(request.POST)
        if form.is_valid():
            colaborador = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Colaboradores',
                descripcion=f'Colaborador creado: {colaborador.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Colaborador creado exitosamente')
            return redirect('colaboradores_list')
    else:
        form = ColaboradorForm()
    
    return render(request, 'core/colaboradores/create.html', {'form': form})


@login_required
def colaborador_edit(request, colaborador_id):
    """Editar colaborador"""
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    
    if request.method == 'POST':
        form = ColaboradorForm(request.POST, instance=colaborador)
        if form.is_valid():
            colaborador = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Colaboradores',
                descripcion=f'Colaborador editado: {colaborador.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Colaborador actualizado exitosamente')
            return redirect('colaboradores_list')
    else:
        form = ColaboradorForm(instance=colaborador)
    
    return render(request, 'core/colaboradores/edit.html', {'form': form, 'colaborador': colaborador})


@login_required
def colaborador_delete(request, colaborador_id):
    """Eliminar colaborador"""
    colaborador = get_object_or_404(Colaborador, id=colaborador_id)
    
    if request.method == 'POST':
        colaborador.delete()
        
        # Registrar actividad
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Colaboradores',
            descripcion=f'Colaborador eliminado: {colaborador.nombre}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Colaborador eliminado exitosamente')
        return redirect('colaboradores_list')
    
    return render(request, 'core/colaboradores/delete.html', {'colaborador': colaborador})


# ===== CRUD FACTURAS =====
@login_required
def facturas_list(request):
    """Lista de facturas con paginación"""
    
    # Obtener parámetros de paginación
    per_page = int(request.GET.get('per_page', 25))
    page = request.GET.get('page', 1)
    
    # Aplicar filtros si existen
    filters = {}
    estado = request.GET.get('estado')
    cliente_id = request.GET.get('cliente')
    proyecto_id = request.GET.get('proyecto')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    if estado:
        filters['estado'] = estado
    if cliente_id:
        filters['cliente_id'] = cliente_id
    if proyecto_id:
        filters['proyecto_id'] = proyecto_id
    
    # Query base optimizada
    facturas = Factura.objects.select_related(
        'cliente', 'proyecto'
    ).prefetch_related(
        'pagos'
    ).order_by('-fecha_emision')
    
    # Aplicar filtros de fecha si existen
    if fecha_desde:
        facturas = facturas.filter(fecha_emision__gte=fecha_desde)
    if fecha_hasta:
        facturas = facturas.filter(fecha_emision__lte=fecha_hasta)
    
    # Aplicar otros filtros
    for field, value in filters.items():
        if value:
            facturas = facturas.filter(**{field: value})
    
    # Paginar resultados
    from django.core.paginator import Paginator
    paginator = Paginator(facturas, per_page)
    
    try:
        page_obj = paginator.page(page)
    except:
        page_obj = paginator.page(1)
    
    # Obtener opciones de filtro
    clientes = Cliente.objects.filter(activo=True).order_by('razon_social')
    proyectos = Proyecto.objects.filter(activo=True).order_by('nombre')
    estados = Factura.ESTADO_CHOICES
    
    # Organizar proyectos por cliente para el filtro dinámico
    proyectos_por_cliente = {}
    for cliente in clientes:
        proyectos_por_cliente[cliente.id] = [
            {'id': p.id, 'nombre': p.nombre} 
            for p in proyectos.filter(cliente=cliente)
        ]
    
    # Obtener estadísticas totales
    total_facturas = Factura.objects.count()
    total_facturado = Factura.objects.aggregate(total=Sum('monto_total'))['total'] or 0.00
    
    # Calcular total cobrado sumando solo las facturas pagadas
    facturas_pagadas = Factura.objects.filter(estado='pagada')
    total_cobrado = facturas_pagadas.aggregate(total=Sum('monto_total'))['total'] or 0.00
    
    facturas_emitidas = Factura.objects.filter(estado='emitida').count()
    facturas_cobradas = Factura.objects.filter(estado='pagada').count()
    
    context = {
        'facturas': page_obj,
        'clientes': clientes,
        'proyectos': proyectos,
        'estados': estados,
        'proyectos_por_cliente': proyectos_por_cliente,
        'total_facturas': total_facturas,
        'total_facturado': total_facturado,
        'total_cobrado': total_cobrado,
        'facturas_emitidas': facturas_emitidas,
        'facturas_pagadas': facturas_cobradas,
        'filtros_activos': {
            'estado': request.GET.get('estado'),
            'cliente': request.GET.get('cliente'),
            'proyecto': request.GET.get('proyecto'),
            'fecha_desde': request.GET.get('fecha_desde'),
            'fecha_hasta': request.GET.get('fecha_hasta'),
        },
        'paginator': paginator,
        'page_obj': page_obj,
    }
    
    return render(request, 'core/facturas/list.html', context)


@login_required
def factura_detail(request, factura_id):
    """Detalle de la factura"""
    factura = get_object_or_404(Factura, id=factura_id)
    
    # Obtener pagos relacionados
    pagos = Pago.objects.filter(factura=factura)
    
    context = {
        'factura': factura,
        'pagos': pagos
    }
    
    return render(request, 'core/facturas/detail.html', context)


@login_required
def factura_create(request):
    """Crear factura"""
    # Inicializar form por defecto para GET requests
    form = FacturaForm()
    
    if request.method == 'POST':
        print("=== DEBUG: POST recibido ===")
        print(f"POST data: {request.POST}")
        
        form = FacturaForm(request.POST)
        print(f"Formulario creado: {form}")
        print(f"Formulario válido: {form.is_valid()}")
        
        if form.is_valid():
            print("=== DEBUG: Formulario válido, guardando ===")
            print(f"=== DEBUG: Datos del formulario: {form.cleaned_data}")
            
            factura = form.save(commit=False)
            factura.usuario_creacion = request.user
            factura.estado = 'emitida'
            
            print(f"=== DEBUG: Factura antes de guardar: {factura}")
            print(f"=== DEBUG: Usuario: {request.user}")
            print(f"=== DEBUG: Estado: {factura.estado}")
            
            factura.save()
            
            print(f"=== DEBUG: Factura guardada con ID: {factura.id} ===")
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Facturas',
                descripcion=f'Factura creada: {factura.numero_factura}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Factura creada exitosamente')
            return redirect('facturas_list')
        else:
            print("=== DEBUG: Formulario inválido ===")
            print(f"Errores del formulario: {form.errors}")
            print(f"Errores de campos: {form.errors.as_data()}")
    
    # Obtener clientes y proyectos activos para los dropdowns
    clientes = Cliente.objects.filter(activo=True).order_by('razon_social')
    proyectos = Proyecto.objects.filter(activo=True).order_by('nombre')
    
    # Organizar proyectos por cliente para el filtro dinámico
    proyectos_por_cliente = {}
    for cliente in clientes:
        proyectos_por_cliente[cliente.id] = [
            {'id': p.id, 'nombre': p.nombre} 
            for p in proyectos.filter(cliente=cliente)
        ]
    
    # Obtener estadísticas para el sidebar
    total_facturas = Factura.objects.count()
    total_facturado = Factura.objects.aggregate(total=Sum('monto_total'))['total'] or 0.00
    
    context = {
        'form': form,
        'clientes': clientes,
        'proyectos': proyectos,
        'proyectos_por_cliente': proyectos_por_cliente,
        'total_facturas': total_facturas,
        'total_facturado': total_facturado
    }
    
    return render(request, 'core/facturas/create.html', context)


@login_required
def factura_edit(request, factura_id):
    """Editar factura"""
    factura = get_object_or_404(Factura, id=factura_id)
    
    if request.method == 'POST':
        form = FacturaForm(request.POST, instance=factura)
        if form.is_valid():
            factura = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Facturas',
                descripcion=f'Factura editada: {factura.numero_factura}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Factura actualizada exitosamente')
            return redirect('facturas_list')
    else:
        form = FacturaForm(instance=factura)
    
    # Obtener clientes y proyectos activos para los dropdowns
    clientes = Cliente.objects.filter(activo=True).order_by('razon_social')
    proyectos = Proyecto.objects.filter(activo=True).order_by('nombre')
    
    # Obtener estadísticas para el sidebar
    total_facturas = Factura.objects.count()
    total_facturado = Factura.objects.aggregate(total=Sum('monto_total'))['total'] or 0.00
    
    context = {
        'form': form,
        'factura': factura,
        'clientes': clientes,
        'proyectos': proyectos,
        'total_facturas': total_facturas,
        'total_facturado': total_facturado
    }
    
    return render(request, 'core/facturas/edit.html', context)


@login_required
def factura_delete(request, factura_id):
    """Eliminar factura"""
    factura = get_object_or_404(Factura, id=factura_id)
    
    if request.method == 'POST':
        # Registrar actividad antes de eliminar
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Facturas',
            descripcion=f'Factura eliminada: {factura.numero_factura}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        factura.delete()
        messages.success(request, 'Factura eliminada exitosamente')
        return redirect('facturas_list')
    
    return render(request, 'core/facturas/delete.html', {'factura': factura})


@login_required
def factura_marcar_pagada(request, factura_id):
    """Marcar factura como pagada"""
    if request.method == 'POST':
        try:
            factura = get_object_or_404(Factura, id=factura_id)
            
            # Verificar que la factura no esté ya pagada o cancelada
            if factura.estado == 'pagada':
                return JsonResponse({
                    'success': False,
                    'error': 'La factura ya está marcada como pagada'
                })
            
            if factura.estado == 'cancelada':
                return JsonResponse({
                    'success': False,
                    'error': 'No se puede marcar como pagada una factura cancelada'
                })
            
            # Cambiar estado a pagada y establecer fecha de pago
            factura.estado = 'pagada'
            factura.fecha_pago = timezone.now().date()
            factura.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Marcar como Pagada',
                modulo='Facturas',
                descripcion=f'Factura marcada como pagada: {factura.numero_factura}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            return JsonResponse({
                'success': True,
                'message': f'Factura {factura.numero_factura} marcada como pagada exitosamente',
                'factura_id': factura.id,
                'nuevo_estado': factura.estado,
                'fecha_pago': factura.fecha_pago.strftime('%d/%m/%Y') if factura.fecha_pago else None
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar la solicitud: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    })


# ===== CRUD GASTOS =====
@login_required
def gastos_list(request):
    """Lista de gastos"""
    # Obtener todos los gastos sin filtros
    gastos = Gasto.objects.all().order_by('-fecha_gasto')
    
    # DEBUG: Imprimir información de gastos
    print(f"🔍 DEBUG - Total gastos en BD: {gastos.count()}")
    for g in gastos:
        print(f"   • {g.descripcion} - Q{g.monto} - Aprobado: {g.aprobado} - Fecha: {g.fecha_gasto}")
    
    # Calcular estadísticas
    total_gastos = sum(gasto.monto for gasto in gastos)
    gastos_aprobados = gastos.filter(aprobado=True).count()
    gastos_pendientes = gastos.filter(aprobado=False).count()
    
    context = {
        'gastos': gastos,
        'total_gastos': total_gastos,
        'gastos_aprobados': gastos_aprobados,
        'gastos_pendientes': gastos_pendientes,
    }
    
    return render(request, 'core/gastos/list.html', context)


@login_required
def gasto_create(request):
    """Crear gasto"""
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            gasto = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Gastos',
                descripcion=f'Gasto creado: {gasto.descripcion} - Q{gasto.monto}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Gasto creado exitosamente')
            return redirect('gastos_list')
    else:
        form = GastoForm()
    
    return render(request, 'core/gastos/create.html', {'form': form})


@login_required
def gasto_edit(request, gasto_id):
    """Editar gasto"""
    gasto = get_object_or_404(Gasto, id=gasto_id)
    
    if request.method == 'POST':
        form = GastoForm(request.POST, instance=gasto)
        if form.is_valid():
            gasto = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Gastos',
                descripcion=f'Gasto editado: {gasto.descripcion} - Q{gasto.monto}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Gasto actualizado exitosamente')
            return redirect('gastos_list')
    else:
        form = GastoForm(instance=gasto)
    
    return render(request, 'core/gastos/edit.html', {'form': form, 'gasto': gasto})


@login_required
def gasto_delete(request, gasto_id):
    """Eliminar gasto"""
    gasto = get_object_or_404(Gasto, id=gasto_id)
    
    if request.method == 'POST':
        # Registrar actividad antes de eliminar
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Gastos',
            descripcion=f'Gasto eliminado: {gasto.descripcion} - Q{gasto.monto}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        gasto.delete()
        messages.success(request, 'Gasto eliminado exitosamente')
        return redirect('gastos_list')
    
    return render(request, 'core/gastos/delete.html', {'gasto': gasto})


# ===== CRUD PAGOS =====
@login_required
def pagos_list(request):
    """Lista de pagos"""
    pagos = Pago.objects.all().order_by('-fecha_pago')
    return render(request, 'core/pagos/list.html', {'pagos': pagos})


@login_required
def pago_create(request):
    """Crear pago"""
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.registrado_por = request.user
            pago.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Pagos',
                descripcion=f'Pago registrado: Q{pago.monto} para factura {pago.factura.numero_factura}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Pago registrado exitosamente')
            return redirect('pagos_list')
    else:
        form = PagoForm()
    
    return render(request, 'core/pagos/create.html', {'form': form})


@login_required
def pago_edit(request, pago_id):
    """Editar pago"""
    pago = get_object_or_404(Pago, id=pago_id)
    
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Pagos',
                descripcion=f'Pago editado: Q{pago.monto} para factura {pago.factura.numero_factura}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Pago actualizado exitosamente')
            return redirect('pagos_list')
    else:
        form = PagoForm(instance=pago)
    
    return render(request, 'core/pagos/edit.html', {'form': form, 'pago': pago})


@login_required
def pago_delete(request, pago_id):
    """Eliminar pago"""
    pago = get_object_or_404(Pago, id=pago_id)
    
    if request.method == 'POST':
        # Registrar actividad antes de eliminar
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Pagos',
            descripcion=f'Pago eliminado: Q{pago.monto} para factura {pago.factura.numero_factura}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        pago.delete()
        messages.success(request, 'Pago eliminado exitosamente')
        return redirect('pagos_list')
    
    return render(request, 'core/pagos/delete.html', {'pago': pago})


# ===== CRUD CATEGORÍAS DE GASTO =====
@login_required
def categorias_gasto_list(request):
    """Lista de categorías de gasto"""
    categorias = CategoriaGasto.objects.all().order_by('nombre')
    return render(request, 'core/categorias_gasto/list.html', {'categorias': categorias})


@login_required
def categoria_gasto_create(request):
    """Crear categoría de gasto"""
    if request.method == 'POST':
        form = CategoriaGastoForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Categorías de Gasto',
                descripcion=f'Categoría creada: {categoria.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('categorias_gasto_list')
    else:
        form = CategoriaGastoForm()
    
    return render(request, 'core/categorias_gasto/create.html', {'form': form})


@login_required
def categoria_gasto_edit(request, categoria_id):
    """Editar categoría de gasto"""
    categoria = get_object_or_404(CategoriaGasto, id=categoria_id)
    
    if request.method == 'POST':
        form = CategoriaGastoForm(request.POST, instance=categoria)
        if form.is_valid():
            categoria = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Categorías de Gasto',
                descripcion=f'Categoría editada: {categoria.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('categorias_gasto_list')
    else:
        form = CategoriaGastoForm(instance=categoria)
    
    return render(request, 'core/categorias_gasto/edit.html', {'form': form, 'categoria': categoria})


@login_required
def categoria_gasto_delete(request, categoria_id):
    """Eliminar categoría de gasto"""
    categoria = get_object_or_404(CategoriaGasto, id=categoria_id)
    
    if request.method == 'POST':
        # Verificar si hay gastos usando esta categoría
        if Gasto.objects.filter(categoria=categoria).exists():
            messages.error(request, 'No se puede eliminar la categoría porque tiene gastos asociados')
            return redirect('categorias_gasto_list')
        
        # Registrar actividad antes de eliminar
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Categorías de Gasto',
            descripcion=f'Categoría eliminada: {categoria.nombre}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('categorias_gasto_list')
    
    return render(request, 'core/categorias_gasto/delete.html', {'categoria': categoria})


# ==================== VISTAS DE ANTICIPOS ====================

@login_required
def anticipos_list(request):
    """Lista de anticipos del sistema"""
    anticipos = Anticipo.objects.select_related('cliente', 'proyecto').all()
    
    # Filtros
    estado = request.GET.get('estado')
    cliente_id = request.GET.get('cliente')
    proyecto_id = request.GET.get('proyecto')
    
    if estado:
        anticipos = anticipos.filter(estado=estado)
    if cliente_id:
        anticipos = anticipos.filter(cliente_id=cliente_id)
    if proyecto_id:
        anticipos = anticipos.filter(proyecto_id=proyecto_id)
    
    # Estadísticas
    total_anticipos = anticipos.count()
    monto_total = anticipos.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    monto_aplicado = anticipos.aggregate(total=Sum('monto_aplicado'))['total'] or Decimal('0.00')
    monto_disponible = anticipos.aggregate(total=Sum('monto_disponible'))['total'] or Decimal('0.00')
    
    # Contar por estado
    anticipos_aplicados = anticipos.filter(estado='aplicado').count()
    anticipos_pendientes = anticipos.filter(estado='pendiente').count()
    
    context = {
        'anticipos': anticipos,
        'total_anticipos': total_anticipos,
        'monto_total': monto_total,
        'monto_aplicado': monto_aplicado,
        'monto_disponible': monto_disponible,
        'anticipos_aplicados': anticipos_aplicados,
        'anticipos_pendientes': anticipos_pendientes,
        'estados': Anticipo.ESTADO_CHOICES,
        'tipos': Anticipo.TIPO_CHOICES,
        'clientes': Cliente.objects.filter(activo=True),
        'proyectos': Proyecto.objects.filter(activo=True),
    }
    
    return render(request, 'core/anticipos/list.html', context)


@login_required
def anticipo_create(request):
    """Crear nuevo anticipo"""
    if request.method == 'POST':
        form = AnticipoForm(request.POST)
        if form.is_valid():
            anticipo = form.save(commit=False)
            anticipo.creado_por = request.user
            anticipo.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Anticipos',
                descripcion=f'Anticipo creado: {anticipo.numero_anticipo} - Q{anticipo.monto}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Anticipo creado exitosamente')
            return redirect('anticipos_list')
    else:
        form = AnticipoForm()
    
    context = {
        'form': form,
        'clientes': Cliente.objects.filter(activo=True),
        'proyectos': Proyecto.objects.filter(activo=True),
    }
    
    return render(request, 'core/anticipos/create.html', context)


@login_required
def anticipo_detail(request, anticipo_id):
    """Detalle de un anticipo"""
    anticipo = get_object_or_404(Anticipo, id=anticipo_id)
    
    # Obtener facturas donde se puede aplicar este anticipo
    facturas_aplicables = Factura.objects.filter(
        cliente=anticipo.cliente,
        proyecto=anticipo.proyecto,
        estado__in=['emitida', 'enviada', 'vencida']
    ).exclude(
        monto_anticipos__gte=F('monto_total')
    )
    
    context = {
        'anticipo': anticipo,
        'facturas_aplicables': facturas_aplicables,
    }
    
    return render(request, 'core/anticipos/detail.html', context)


@login_required
def anticipo_edit(request, anticipo_id):
    """Editar anticipo"""
    anticipo = get_object_or_404(Anticipo, id=anticipo_id)
    
    if request.method == 'POST':
        form = AnticipoForm(request.POST, instance=anticipo)
        if form.is_valid():
            anticipo = form.save(commit=False)
            anticipo.modificado_por = request.user
            anticipo.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Anticipos',
                descripcion=f'Anticipo editado: {anticipo.numero_anticipo}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Anticipo actualizado exitosamente')
            return redirect('anticipos_list')
    else:
        form = AnticipoForm(instance=anticipo)
    
    context = {
        'form': form,
        'anticipo': anticipo,
    }
    
    return render(request, 'core/anticipos/edit.html', context)


@login_required
def anticipo_delete(request, anticipo_id):
    """Eliminar anticipo"""
    anticipo = get_object_or_404(Anticipo, id=anticipo_id)
    
    if request.method == 'POST':
        numero_anticipo = anticipo.numero_anticipo
        anticipo.delete()
        
        # Registrar actividad
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar',
            modulo='Anticipos',
            descripcion=f'Anticipo eliminado: {numero_anticipo}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Anticipo eliminado exitosamente')
        return redirect('anticipos_list')
    
    return render(request, 'core/anticipos/delete.html', {'anticipo': anticipo})


@login_required
def aplicar_anticipo(request, anticipo_id):
    """Aplicar anticipo a facturas"""
    anticipo = get_object_or_404(Anticipo, id=anticipo_id)
    
    if request.method == 'POST':
        factura_id = request.POST.get('factura')
        monto_aplicar = Decimal(request.POST.get('monto_aplicar'))
        
        try:
            factura = Factura.objects.get(id=factura_id)
            anticipo.aplicar_a_factura(factura, monto_aplicar)
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Aplicar Anticipo',
                modulo='Anticipos',
                descripcion=f'Anticipo {anticipo.numero_anticipo} aplicado a factura {factura.numero_factura} por Q{monto_aplicar}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, f'Anticipo aplicado exitosamente a la factura {factura.numero_factura}')
            return redirect('anticipo_detail', anticipo_id=anticipo.id)
            
        except (Factura.DoesNotExist, ValueError) as e:
            messages.error(request, f'Error al aplicar anticipo: {str(e)}')
    
    # Obtener facturas aplicables
    facturas_aplicables = Factura.objects.filter(
        cliente=anticipo.cliente,
        proyecto=anticipo.proyecto,
        estado__in=['emitida', 'enviada', 'vencida']
    ).exclude(
        monto_anticipos__gte=F('monto_total')
    )
    
    context = {
        'anticipo': anticipo,
        'facturas_aplicables': facturas_aplicables,
    }
    
    return render(request, 'core/anticipos/aplicar.html', context)


# ==================== VISTAS DE ARCHIVOS DE PROYECTOS ====================

@login_required
def proyecto_dashboard(request, proyecto_id=None):
    """Dashboard específico de un proyecto con selector"""
    if proyecto_id:
        proyecto = get_object_or_404(Proyecto, id=proyecto_id, activo=True)
    else:
        # Si no se especifica proyecto, mostrar el primero activo o redirigir
        proyectos = Proyecto.objects.filter(activo=True)
        if proyectos.exists():
            proyecto = proyectos.first()
        else:
            messages.warning(request, 'No hay proyectos activos para mostrar')
            return redirect('proyectos_list')
    
    # Obtener todos los proyectos para el selector
    todos_proyectos = Proyecto.objects.filter(activo=True).order_by('nombre')
    
    # Estadísticas del proyecto específico
    facturas_proyecto = Factura.objects.filter(proyecto=proyecto)
    gastos_proyecto = Gasto.objects.filter(proyecto=proyecto, aprobado=True)
    anticipos_proyecto = Anticipo.objects.filter(proyecto=proyecto)
    
    # Totales financieros del proyecto
    total_facturado = facturas_proyecto.aggregate(total=Sum('monto_total'))['total'] or Decimal('0.00')
    total_cobrado = facturas_proyecto.aggregate(total=Sum('monto_pagado'))['total'] or Decimal('0.00')
    total_gastos = gastos_proyecto.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    total_anticipos = anticipos_proyecto.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
    
    # Rentabilidad del proyecto
    rentabilidad_proyecto = total_cobrado - total_gastos
    
    # Archivos del proyecto
    archivos_proyecto = ArchivoProyecto.objects.filter(proyecto=proyecto, activo=True)
    
    # Facturas recientes del proyecto
    facturas_recientes = facturas_proyecto.order_by('-fecha_emision')[:5]
    
    # Gastos recientes del proyecto
    gastos_recientes = gastos_proyecto.order_by('-fecha_gasto')[:5]
    
    context = {
        'proyecto': proyecto,
        'todos_proyectos': todos_proyectos,
        'total_facturado': total_facturado,
        'total_cobrado': total_cobrado,
        'total_gastos': total_gastos,
        'total_anticipos': total_anticipos,
        'rentabilidad_proyecto': rentabilidad_proyecto,
        'archivos_proyecto': archivos_proyecto,
        'facturas_recientes': facturas_recientes,
        'gastos_recientes': gastos_recientes,
        'total_archivos': archivos_proyecto.count(),
    }
    
    return render(request, 'core/proyecto_dashboard.html', context)


@login_required
def archivos_proyectos_list(request):
    """Lista de todos los proyectos para gestión de archivos"""
    proyectos = Proyecto.objects.filter(activo=True).order_by('nombre')
    
    # Estadísticas de archivos por proyecto
    for proyecto in proyectos:
        proyecto.total_archivos = ArchivoProyecto.objects.filter(
            proyecto=proyecto, 
            activo=True
        ).count()
    
    context = {
        'proyectos': proyectos,
        'total_proyectos': proyectos.count(),
    }
    
    return render(request, 'core/archivos/proyectos_list.html', context)


@login_required
def archivos_proyecto_list(request, proyecto_id):
    """Lista de archivos de un proyecto específico"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, activo=True)
    
    # Obtener carpeta actual (si se especifica)
    carpeta_id = request.GET.get('carpeta')
    carpeta_actual = None
    
    if carpeta_id:
        try:
            carpeta_actual = CarpetaProyecto.objects.get(id=carpeta_id, proyecto=proyecto, activa=True)
        except CarpetaProyecto.DoesNotExist:
            pass
    
    # Obtener archivos
    if carpeta_actual:
        archivos = ArchivoProyecto.objects.filter(proyecto=proyecto, carpeta=carpeta_actual, activo=True)
        subcarpetas = carpeta_actual.get_subcarpetas_activas()
    else:
        # Carpeta raíz - archivos sin carpeta y carpetas raíz
        archivos = ArchivoProyecto.objects.filter(proyecto=proyecto, carpeta__isnull=True, activo=True)
        subcarpetas = CarpetaProyecto.objects.filter(proyecto=proyecto, carpeta_padre__isnull=True, activa=True)
    
    # Filtros
    tipo = request.GET.get('tipo')
    if tipo:
        archivos = archivos.filter(tipo=tipo)
    
    # Obtener todas las carpetas del proyecto para el breadcrumb
    todas_carpetas = CarpetaProyecto.objects.filter(proyecto=proyecto, activa=True).order_by('nombre')
    
    context = {
        'proyecto': proyecto,
        'carpeta_actual': carpeta_actual,
        'archivos': archivos,
        'subcarpetas': subcarpetas,
        'todas_carpetas': todas_carpetas,
        'tipos': ArchivoProyecto.TIPO_CHOICES,
        'total_archivos': archivos.count(),
        'total_subcarpetas': subcarpetas.count(),
    }
    
    return render(request, 'core/archivos/list.html', context)


@login_required
def archivo_upload(request, proyecto_id):
    """Subir nuevo archivo a un proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, activo=True)
    
    if request.method == 'POST':
        form = ArchivoProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.save(commit=False)
            archivo.proyecto = proyecto
            archivo.subido_por = request.user
            archivo.save()
            
            # Generar thumbnail automáticamente
            try:
                archivo.generar_thumbnail()
            except Exception as e:
                print(f"Error generando thumbnail: {e}")
                pass
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Subir Archivo',
                modulo='Archivos',
                descripcion=f'Archivo subido: {archivo.nombre} al proyecto {proyecto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Archivo subido exitosamente')
            return redirect('archivos_proyecto_list', proyecto_id=proyecto.id)
    else:
        form = ArchivoProyectoForm(proyecto=proyecto)
    
    context = {
        'form': form,
        'proyecto': proyecto,
    }
    
    return render(request, 'core/archivos/upload.html', context)


@login_required
def archivo_download(request, archivo_id):
    """Descargar un archivo"""
    archivo = get_object_or_404(ArchivoProyecto, id=archivo_id, activo=True)
    
    # Verificar permisos (opcional: solo usuarios del proyecto)
    if not request.user.is_superuser and archivo.proyecto.activo == False:
        messages.error(request, 'No tienes permisos para acceder a este archivo')
        return redirect('proyectos_list')
    
    # Registrar descarga
    LogActividad.objects.create(
        usuario=request.user,
        accion='Descargar Archivo',
        modulo='Archivos',
        descripcion=f'Archivo descargado: {archivo.nombre}',
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    # Retornar archivo para descarga
    from django.http import FileResponse
    
    file_path = archivo.archivo.path
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{archivo.nombre}.{archivo.get_extension()}"'
        return response
    else:
        messages.error(request, 'El archivo no existe en el servidor')
        return redirect('archivos_proyecto_list', proyecto_id=archivo.proyecto.id)


@login_required
def archivo_delete(request, archivo_id):
    """Eliminar un archivo"""
    archivo = get_object_or_404(ArchivoProyecto, id=archivo_id, activo=True)
    
    if request.method == 'POST':
        # Registrar actividad antes de eliminar
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar Archivo',
            modulo='Archivos',
            descripcion=f'Archivo eliminado: {archivo.nombre} del proyecto {archivo.proyecto.nombre}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        archivo.delete()
        messages.success(request, 'Archivo eliminado exitosamente')
        return redirect('archivos_proyecto_list', proyecto_id=archivo.proyecto.id)
    
    return render(request, 'core/archivos/delete.html', {'archivo': archivo})


@login_required
def archivo_preview(request, archivo_id):
    """Vista previa de un archivo (para imágenes y PDFs)"""
    archivo = get_object_or_404(ArchivoProyecto, id=archivo_id, activo=True)
    
    context = {
        'archivo': archivo,
    }
    
    return render(request, 'core/archivos/preview.html', context)
 









# ===== VISTAS DEL SISTEMA =====
@login_required
def sistema_view(request):
    """Vista principal del sistema"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    # Estadísticas del sistema
    total_usuarios = User.objects.count()
    total_logs = LogActividad.objects.count()
    logs_recientes = LogActividad.objects.all().order_by('-fecha_actividad')[:10]
    
    context = {
        'total_usuarios': total_usuarios,
        'total_logs': total_logs,
        'logs_recientes': logs_recientes,
    }
    
    return render(request, 'core/sistema/index.html', context)


@login_required
def sistema_configurar(request):
    """Configuración del sistema"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Aquí se pueden agregar configuraciones del sistema
        messages.success(request, 'Configuración actualizada exitosamente')
        return redirect('sistema')
    
    return render(request, 'core/sistema/configurar.html')


@login_required
def sistema_logs(request):
    """Ver logs del sistema"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    logs = LogActividad.objects.all().order_by('-fecha_actividad')
    
    # Paginación
    paginator = Paginator(logs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'core/sistema/logs.html', context)


@login_required
def sistema_reset_app(request):
    """Reset completo de la aplicación - SOLO SUPERUSUARIOS"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            # Registrar la acción en logs
            LogActividad.objects.create(
                usuario=request.user,
                accion='RESET_APP',
                modulo='Sistema',
                descripcion=f'Usuario {request.user.username} inició RESET COMPLETO de la aplicación',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
            # LIMPIEZA COMPLETA DE DATOS - En orden para evitar problemas de integridad referencial
            print("🧹 Iniciando limpieza completa del sistema...")
            
            try:
                # 1. Eliminar datos de facturación
                print("📊 Eliminando datos de facturación...")
                Pago.objects.all().delete()
                Factura.objects.all().delete()
                print("✅ Facturación eliminada")
                
                # 2. Eliminar datos financieros
                print("💰 Eliminando datos financieros...")
                Anticipo.objects.all().delete()
                Gasto.objects.all().delete()
                CategoriaGasto.objects.all().delete()
                GastoFijoMensual.objects.all().delete()
                print("✅ Datos financieros eliminados")
                
                # 3. Eliminar presupuestos
                print("📋 Eliminando presupuestos...")
                PartidaPresupuesto.objects.all().delete()
                Presupuesto.objects.all().delete()
                print("✅ Presupuestos eliminados")
                
                # 4. Eliminar archivos
                print("📁 Eliminando archivos...")
                ArchivoProyecto.objects.all().delete()
                print("✅ Archivos eliminados")
                
                # 5. Eliminar colaboradores
                print("👥 Eliminando colaboradores...")
                Colaborador.objects.all().delete()
                print("✅ Colaboradores eliminados")
                
                # 6. Eliminar proyectos
                print("🏗️ Eliminando proyectos...")
                Proyecto.objects.all().delete()
                print("✅ Proyectos eliminados")
                
                # 7. Eliminar clientes
                print("👤 Eliminando clientes...")
                Cliente.objects.all().delete()
                print("✅ Clientes eliminados")
                
                # 8. Eliminar inventario
                print("📦 Eliminando inventario...")
                AsignacionInventario.objects.all().delete()
                ItemInventario.objects.all().delete()
                CategoriaInventario.objects.all().delete()
                print("✅ Inventario eliminado")
                
                # 9. Eliminar notificaciones básicas
                print("🔔 Eliminando notificaciones...")
                NotificacionSistema.objects.all().delete()
                print("✅ Notificaciones eliminadas")
                
                # 10. Limpiar logs de actividad (mantener solo el log actual del reset)
                print("📝 Limpiando logs de actividad...")
                LogActividad.objects.exclude(
                    accion__in=['RESET_APP', 'RESET_APP_SUCCESS', 'RESET_APP_ERROR']
                ).delete()
                print("✅ Logs limpiados")
                
                # 11. Limpiar perfiles de usuario (excepto el superusuario actual)
                print("👤 Limpiando perfiles de usuario...")
                PerfilUsuario.objects.exclude(usuario=request.user).delete()
                print("✅ Perfiles limpiados")
                
                # 12. Limpiar usuarios (excepto superusuarios)
                print("🔐 Limpiando usuarios...")
                User.objects.exclude(is_superuser=True).delete()
                print("✅ Usuarios limpiados")
                
                # 13. Limpiar roles
                print("🎭 Limpiando roles...")
                Rol.objects.all().delete()
                print("✅ Roles eliminados")
                
                # 14. Limpiar caché del sistema
                print("🗄️ Limpiando caché...")
                cache.clear()
                print("✅ Caché limpiado")
                
                # 15. Limpiar contadores de base de datos SQLite
                print("🗄️ Limpiando contadores de base de datos...")
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM sqlite_sequence")
                print("✅ Contadores limpiados")
                
                print("✅ Sistema limpiado completamente!")
                
            except Exception as e:
                print(f"❌ Error en paso específico: {e}")
                raise e
            
            messages.success(request, '✅ RESET COMPLETO realizado exitosamente. Todos los datos han sido eliminados.')
            
            # Registrar éxito en logs
            LogActividad.objects.create(
                usuario=request.user,
                accion='RESET_APP_SUCCESS',
                modulo='Sistema',
                descripcion='Reset COMPLETO de aplicación realizado exitosamente - Todos los datos eliminados',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
            
        except Exception as e:
            print(f"❌ Error durante la limpieza: {e}")
            messages.error(request, f'❌ Error durante el reset: {str(e)}')
            
            # Registrar error en logs
            LogActividad.objects.create(
                usuario=request.user,
                accion='RESET_APP_ERROR',
                modulo='Sistema',
                descripcion=f'Error durante reset COMPLETO de aplicación: {str(e)}',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return redirect('sistema')
    
    return render(request, 'core/sistema/reset_app.html')
 
# ===== VISTA DE RENTABILIDAD =====
@login_required
def rentabilidad_view(request):
    """Vista de rentabilidad y análisis financiero"""
    try:
        # Obtener parámetros de filtro
        periodo = request.GET.get('periodo', 'mes')  # mes, trimestre, año
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        
        # Fechas por defecto
        hoy = timezone.now()
        if periodo == 'mes':
            fecha_inicio = fecha_inicio or (hoy - timedelta(days=30)).strftime('%Y-%m-%d')
            fecha_fin = fecha_fin or hoy.strftime('%Y-%m-%d')
        elif periodo == 'trimestre':
            fecha_inicio = fecha_inicio or (hoy - timedelta(days=90)).strftime('%Y-%m-%d')
            fecha_fin = fecha_fin or hoy.strftime('%Y-%m-%d')
        elif periodo == 'año':
            fecha_inicio = fecha_inicio or (hoy - timedelta(days=365)).strftime('%Y-%m-%d')
            fecha_fin = fecha_fin or hoy.strftime('%Y-%m-%d')
        
        # Convertir fechas a datetime
        fecha_inicio_dt = timezone.make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%d'))
        fecha_fin_dt = timezone.make_aware(datetime.strptime(fecha_fin, '%Y-%m-%d'))
    
            # Calcular ingresos (SOLO lo cobrado, no lo facturado)
        ingresos = Factura.objects.filter(
            fecha_emision__range=[fecha_inicio_dt, fecha_fin_dt],
            estado='pagada'  # Solo facturas pagadas
        ).aggregate(total=Sum('monto_total'))['total'] or Decimal('0.00')
        
        # DEBUG: Mostrar diferencia entre facturado y cobrado
        total_facturado = Factura.objects.filter(
            fecha_emision__range=[fecha_inicio_dt, fecha_fin_dt]
        ).aggregate(total=Sum('monto_total'))['total'] or Decimal('0.00')
        
        print(f"🔍 DEBUG - Período: {fecha_inicio} a {fecha_fin}")
        print(f"🔍 DEBUG - Total facturado: Q{total_facturado}")
        print(f"🔍 DEBUG - Total cobrado (ingresos): Q{ingresos}")
        print(f"🔍 DEBUG - Diferencia: Q{total_facturado - ingresos}")
        
        # Calcular gastos
        gastos = Gasto.objects.filter(
            fecha_gasto__range=[fecha_inicio_dt, fecha_fin_dt],
            aprobado=True
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
        
        # Gastos fijos (por ahora 0)
        gastos_fijos = Decimal('0.00')
        
        # Calcular rentabilidad
        rentabilidad_bruta = ingresos - gastos
        rentabilidad_neta = rentabilidad_bruta - gastos_fijos
        
        # Margen de rentabilidad
        margen_rentabilidad = (rentabilidad_neta / ingresos * 100) if ingresos > 0 else Decimal('0.00')
        
        # Análisis por proyecto
        proyectos_rentabilidad = []
        proyectos = Proyecto.objects.filter(activo=True)
        
        for proyecto in proyectos:
            # Ingresos del proyecto (usando facturas con pagos realizados)
            ingresos_proyecto = Factura.objects.filter(
                proyecto=proyecto,
                fecha_emision__range=[fecha_inicio_dt, fecha_fin_dt],
                monto_pagado__gt=0
            ).aggregate(total=Sum('monto_pagado'))['total'] or Decimal('0.00')
            
            # Gastos del proyecto
            gastos_proyecto = Gasto.objects.filter(
                proyecto=proyecto,
                fecha_gasto__range=[fecha_inicio_dt, fecha_fin_dt],
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            
            rentabilidad_proyecto = ingresos_proyecto - gastos_proyecto
            margen_proyecto = (rentabilidad_proyecto / ingresos_proyecto * 100) if ingresos_proyecto > 0 else Decimal('0.00')
            
            proyectos_rentabilidad.append({
                'proyecto': proyecto,
                'ingresos': ingresos_proyecto,
                'gastos': gastos_proyecto,
                'rentabilidad': rentabilidad_proyecto,
                'margen': margen_proyecto
            })
        
        # Ordenar por rentabilidad
        proyectos_rentabilidad.sort(key=lambda x: x['rentabilidad'], reverse=True)
        
        # Análisis por categoría de gasto
        gastos_por_categoria = Gasto.objects.filter(
            fecha_gasto__range=[fecha_inicio_dt, fecha_fin_dt],
            aprobado=True
        ).values('categoria__nombre').annotate(
            total=Sum('monto'),
            cantidad=Count('id')
        ).order_by('-total')
        
        # Tendencias mensuales (últimos 12 meses)
        tendencias_mensuales = []
        for i in range(12):
            fecha = hoy - timedelta(days=30*i)
            mes = fecha.month
            año = fecha.year
            
            ingresos_mes = Factura.objects.filter(
                fecha_emision__month=mes,
                fecha_emision__year=año,
                monto_pagado__gt=0
            ).aggregate(total=Sum('monto_pagado'))['total'] or Decimal('0.00')
            
            gastos_mes = Gasto.objects.filter(
                fecha_gasto__month=mes,
                fecha_gasto__year=año,
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            
            rentabilidad_mes = ingresos_mes - gastos_mes
            
            tendencias_mensuales.append({
                'mes': fecha.strftime('%b %Y'),
                'ingresos': ingresos_mes,
                'gastos': gastos_mes,
                'rentabilidad': rentabilidad_mes
            })
        
        # Ordenar tendencias cronológicamente
        tendencias_mensuales.reverse()
        
        # Calcular rentabilidad del mes actual para el dashboard
        mes_actual = hoy.month
        año_actual = hoy.year
        
        ingresos_mes_actual = Factura.objects.filter(
            fecha_emision__month=mes_actual,
            fecha_emision__year=año_actual,
            monto_pagado__gt=0
        ).aggregate(total=Sum('monto_pagado'))['total'] or Decimal('0.00')
        
        gastos_mes_actual = Gasto.objects.filter(
            fecha_gasto__month=mes_actual,
            fecha_gasto__year=año_actual,
            aprobado=True
        ).aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
        
        rentabilidad_mes_actual = ingresos_mes_actual - gastos_mes_actual
        margen_mes_actual = (rentabilidad_mes_actual / ingresos_mes_actual * 100) if ingresos_mes_actual > 0 else Decimal('0.00')
        
        context = {
            'periodo': periodo,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'ingresos': ingresos,
            'gastos': gastos,
            'gastos_fijos': gastos_fijos,
            'rentabilidad_bruta': rentabilidad_bruta,
            'rentabilidad_neta': rentabilidad_neta,
            'margen_rentabilidad': margen_rentabilidad,
            'proyectos_rentabilidad': proyectos_rentabilidad,
            'gastos_por_categoria': gastos_por_categoria,
            'tendencias_mensuales': tendencias_mensuales,
            # Datos para el dashboard
            'ingresos_mes': ingresos_mes_actual,
            'gastos_mes': gastos_mes_actual,
            'rentabilidad_mes': margen_mes_actual,
        }
        
        return render(request, 'core/rentabilidad/index.html', context)
        
    except Exception as e:
        # En caso de error, devolver valores por defecto
        context = {
            'periodo': 'mes',
            'fecha_inicio': (timezone.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
            'fecha_fin': timezone.now().strftime('%Y-%m-%d'),
            'ingresos': Decimal('0.00'),
            'gastos': Decimal('0.00'),
            'gastos_fijos': Decimal('0.00'),
            'rentabilidad_bruta': Decimal('0.00'),
            'rentabilidad_neta': Decimal('0.00'),
            'margen_rentabilidad': Decimal('0.00'),
            'proyectos_rentabilidad': [],
            'gastos_por_categoria': [],
            'tendencias_mensuales': [],
            'ingresos_mes': Decimal('0.00'),
            'gastos_mes': Decimal('0.00'),
            'rentabilidad_mes': Decimal('0.00'),
            'error': str(e)
        }
        
        return render(request, 'core/rentabilidad/index.html', context)
 
# ===== VISTAS DE PRESUPUESTOS =====
@login_required
def presupuestos_list(request):
    """Lista de presupuestos del sistema"""
    presupuestos = Presupuesto.objects.select_related('proyecto', 'creado_por').filter(activo=True)
    
    # Filtros
    proyecto_id = request.GET.get('proyecto')
    estado = request.GET.get('estado')
    
    if proyecto_id:
        presupuestos = presupuestos.filter(proyecto_id=proyecto_id)
    if estado:
        presupuestos = presupuestos.filter(estado=estado)
    
    # Calcular estadísticas
    total_presupuestos = presupuestos.count()
    presupuestos_aprobados = presupuestos.filter(estado='aprobado').count()
    presupuestos_revision = presupuestos.filter(estado='en_revision').count()
    presupuestos_borrador = presupuestos.filter(estado='borrador').count()
    
    # Calcular variaciones para cada presupuesto
    for presupuesto in presupuestos:
        variacion = presupuesto.obtener_variacion()
        presupuesto.variacion_data = variacion
    
    context = {
        'presupuestos': presupuestos,
        'proyectos': Proyecto.objects.filter(activo=True),
        'estados': Presupuesto._meta.get_field('estado').choices,
        'selected_proyecto': request.GET.get('proyecto', ''),
        'selected_estado': request.GET.get('estado', ''),
        'total_presupuestos': total_presupuestos,
        'presupuestos_aprobados': presupuestos_aprobados,
        'presupuestos_revision': presupuestos_revision,
        'presupuestos_borrador': presupuestos_borrador,
    }
    
    return render(request, 'core/presupuestos/list.html', context)

@login_required
def presupuesto_create(request):
    """Crear nuevo presupuesto"""
    if request.method == 'POST':
        form = PresupuestoForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.proyecto_id = request.POST.get('proyecto')
            presupuesto.creado_por = request.user
            presupuesto.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear',
                modulo='Presupuestos',
                descripcion=f'Presupuesto creado: {presupuesto.nombre} para proyecto {presupuesto.proyecto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Presupuesto creado exitosamente')
            return redirect('presupuesto_detail', presupuesto_id=presupuesto.id)
    else:
        form = PresupuestoForm()
    
    context = {
        'form': form,
        'proyectos': Proyecto.objects.filter(activo=True),
    }
    
    return render(request, 'core/presupuestos/create.html', context)

@login_required
def presupuesto_detail(request, presupuesto_id):
    """Detalle de un presupuesto"""
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, activo=True)
    partidas = presupuesto.partidas.all()
    variaciones = presupuesto.variaciones.all()
    
    # Obtener datos de variación
    variacion_data = presupuesto.obtener_variacion()
    
    # Agregar valores absolutos para el template
    if variacion_data:
        variacion_data['variacion_abs'] = abs(variacion_data['variacion'])
        variacion_data['porcentaje_variacion_abs'] = abs(variacion_data['porcentaje_variacion'])
    
    # Obtener gastos reales por categoría para comparar
    gastos_reales = Gasto.objects.filter(
        proyecto=presupuesto.proyecto,
        aprobado=True
    ).values('categoria__nombre').annotate(
        total=Sum('monto')
    ).order_by('-total')
    
    context = {
        'presupuesto': presupuesto,
        'partidas': partidas,
        'variaciones': variaciones,
        'variacion_data': variacion_data,
        'gastos_reales': gastos_reales,
    }
    
    return render(request, 'core/presupuestos/detail.html', context)

@login_required
def presupuesto_edit(request, presupuesto_id):
    """Editar presupuesto"""
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, activo=True)
    
    if request.method == 'POST':
        form = PresupuestoForm(request.POST, instance=presupuesto)
        if form.is_valid():
            presupuesto = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar',
                modulo='Presupuestos',
                descripcion=f'Presupuesto editado: {presupuesto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Presupuesto actualizado exitosamente')
            return redirect('presupuesto_detail', presupuesto_id=presupuesto.id)
    else:
        form = PresupuestoForm(instance=presupuesto)
    
    context = {
        'form': form,
        'presupuesto': presupuesto,
    }
    
    return render(request, 'core/presupuestos/edit.html', context)

@login_required
def partida_create(request, presupuesto_id):
    """Crear nueva partida en un presupuesto"""
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, activo=True)
    
    if request.method == 'POST':
        form = PartidaPresupuestoForm(request.POST)
        if form.is_valid():
            partida = form.save(commit=False)
            partida.presupuesto = presupuesto
            partida.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear Partida',
                modulo='Presupuestos',
                descripcion=f'Partida creada: {partida.descripcion} en presupuesto {presupuesto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Partida creada exitosamente')
            return redirect('presupuesto_detail', presupuesto_id=presupuesto.id)
    else:
        form = PartidaPresupuestoForm()
    
    context = {
        'form': form,
        'presupuesto': presupuesto,
    }
    
    return render(request, 'core/presupuestos/partida_create.html', context)

@login_required
def presupuesto_aprobar(request, presupuesto_id):
    """Aprobar un presupuesto"""
    presupuesto = get_object_or_404(Presupuesto, id=presupuesto_id, activo=True)
    
    if request.method == 'POST':
        presupuesto.estado = 'aprobado'
        presupuesto.fecha_aprobacion = timezone.now()
        presupuesto.aprobado_por = request.user
        presupuesto.monto_aprobado = presupuesto.monto_total
        presupuesto.save()
        
        # Registrar actividad
        LogActividad.objects.create(
            usuario=request.user,
            accion='Aprobar',
            modulo='Presupuestos',
            descripcion=f'Presupuesto aprobado: {presupuesto.nombre}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        messages.success(request, 'Presupuesto aprobado exitosamente')
        return redirect('presupuesto_detail', presupuesto_id=presupuesto.id)
    
    return render(request, 'core/presupuestos/aprobar.html', {'presupuesto': presupuesto})
 
# ==================== VISTAS DE NOTIFICACIONES ====================

@login_required
def notificaciones_list(request):
    """Lista de notificaciones del usuario"""
    notificaciones = NotificacionSistema.objects.filter(usuario=request.user)
    
    # Filtros
    tipo = request.GET.get('tipo')
    prioridad = request.GET.get('prioridad')
    leida = request.GET.get('leida')
    
    if tipo:
        notificaciones = notificaciones.filter(tipo=tipo)
    if prioridad:
        notificaciones = notificaciones.filter(prioridad=prioridad)
    if leida is not None:
        notificaciones = notificaciones.filter(leida=leida == 'true')
    
    # Estadísticas
    total_notificaciones = notificaciones.count()
    no_leidas = notificaciones.filter(leida=False).count()
    urgentes = notificaciones.filter(prioridad='urgente', leida=False).count()
    
    context = {
        'notificaciones': notificaciones,
        'total_notificaciones': total_notificaciones,
        'no_leidas': no_leidas,
        'urgentes': urgentes,
        'tipos': NotificacionSistema.TIPO_CHOICES,
        'prioridades': NotificacionSistema.PRIORIDAD_CHOICES,
    }
    
    return render(request, 'core/notificaciones/list.html', context)


@login_required
def notificacion_marcar_leida(request, notificacion_id):
    """Marca una notificación como leída"""
    if request.method == 'POST':
        success = NotificacionService.marcar_como_leida(notificacion_id, request.user)
        if success:
            messages.success(request, 'Notificación marcada como leída')
        else:
            messages.error(request, 'Error al marcar la notificación')
    
    return redirect('notificaciones_list')


@login_required
def notificacion_marcar_todas_leidas(request):
    """Marca todas las notificaciones como leídas"""
    if request.method == 'POST':
        notificaciones = NotificacionSistema.objects.filter(
            usuario=request.user,
            leida=False
        )
        notificaciones.update(leida=True, fecha_lectura=timezone.now())
        messages.success(request, 'Todas las notificaciones han sido marcadas como leídas')
    
    return redirect('notificaciones_list')


@login_required
def notificaciones_configurar(request):
    """Configuración de notificaciones del usuario"""
    config, created = ConfiguracionNotificaciones.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        # Actualizar configuración
        config.facturas_vencidas = request.POST.get('facturas_vencidas') == 'on'
        config.pagos_pendientes = request.POST.get('pagos_pendientes') == 'on'
        config.gastos_aprobacion = request.POST.get('gastos_aprobacion') == 'on'
        config.cambios_proyecto = request.POST.get('cambios_proyecto') == 'on'
        config.anticipos_disponibles = request.POST.get('anticipos_disponibles') == 'on'
        config.presupuestos_revision = request.POST.get('presupuestos_revision') == 'on'
        config.archivos_subidos = request.POST.get('archivos_subidos') == 'on'
        config.notificaciones_sistema = request.POST.get('notificaciones_sistema') == 'on'
        
        config.frecuencia_email = request.POST.get('frecuencia_email', 'inmediato')
        config.horario_inicio = request.POST.get('horario_inicio', '08:00:00')
        config.horario_fin = request.POST.get('horario_fin', '18:00:00')
        
        config.save()
        messages.success(request, 'Configuración de notificaciones actualizada')
        return redirect('notificaciones_configurar')
    
    context = {
        'config': config,
    }
    
    return render(request, 'core/notificaciones/configurar.html', context)


@login_required
def notificaciones_historial(request):
    """Historial de notificaciones enviadas"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    historial = HistorialNotificaciones.objects.all()
    
    # Filtros
    usuario_id = request.GET.get('usuario')
    tipo = request.GET.get('tipo')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if usuario_id:
        historial = historial.filter(usuario_id=usuario_id)
    if tipo:
        historial = historial.filter(tipo=tipo)
    if fecha_inicio:
        historial = historial.filter(fecha_envio__gte=fecha_inicio)
    if fecha_fin:
        historial = historial.filter(fecha_envio__lte=fecha_fin)
    
    # Paginación
    paginator = Paginator(historial, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'usuarios': User.objects.filter(is_active=True),
        'tipos': NotificacionSistema.TIPO_CHOICES,
    }
    
    return render(request, 'core/notificaciones/historial.html', context)


# ==================== API PARA NOTIFICACIONES EN TIEMPO REAL ====================

@login_required
def api_notificaciones_no_leidas(request):
    """API para obtener notificaciones no leídas (para AJAX)"""
    notificaciones = NotificacionService.obtener_notificaciones_no_leidas(request.user)
    
    data = []
    for notif in notificaciones:
        data.append({
            'id': notif.id,
            'tipo': notif.tipo,
            'titulo': notif.titulo,
            'mensaje': notif.mensaje,
            'prioridad': notif.prioridad,
            'fecha_creacion': notif.fecha_creacion.strftime('%d/%m/%Y %H:%M'),
            'icono': notif.get_icono(),
            'color_clase': notif.get_color_clase(),
        })
    
    return JsonResponse({
        'notificaciones': data,
        'total': len(data)
    })


@login_required
def api_marcar_leida(request, notificacion_id):
    """API para marcar notificación como leída (para AJAX)"""
    success = NotificacionService.marcar_como_leida(notificacion_id, request.user)
    
    return JsonResponse({
        'success': success
    })


# ==================== VISTAS DE ADMINISTRACIÓN DE NOTIFICACIONES ====================

@login_required
def admin_notificaciones_sistema(request):
    """Administración de notificaciones del sistema (solo superusuarios)"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        titulo = request.POST.get('titulo')
        mensaje = request.POST.get('mensaje')
        prioridad = request.POST.get('prioridad')
        usuarios_ids = request.POST.getlist('usuarios')
        
        if tipo and titulo and mensaje and usuarios_ids:
            usuarios = User.objects.filter(id__in=usuarios_ids)
            
            for usuario in usuarios:
                NotificacionService.crear_notificacion(
                    usuario=usuario,
                    tipo=tipo,
                    titulo=titulo,
                    mensaje=mensaje,
                    prioridad=prioridad
                )
            
            messages.success(request, f'Notificación enviada a {len(usuarios)} usuarios')
            return redirect('admin_notificaciones_sistema')
        else:
            messages.error(request, 'Todos los campos son requeridos')
    
    context = {
        'tipos': NotificacionSistema.TIPO_CHOICES,
        'prioridades': NotificacionSistema.PRIORIDAD_CHOICES,
        'usuarios': User.objects.filter(is_active=True),
    }
    
    return render(request, 'core/notificaciones/admin_sistema.html', context)


@login_required
def admin_ejecutar_verificaciones(request):
    """Ejecuta las verificaciones automáticas del sistema"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            SistemaNotificacionesAutomaticas.ejecutar_verificaciones_diarias()
            messages.success(request, 'Verificaciones automáticas ejecutadas correctamente')
        except Exception as e:
            messages.error(request, f'Error ejecutando verificaciones: {str(e)}')
    
    return redirect('admin_notificaciones_sistema')

@login_required
def test_notification_email(request):
    """
    Vista de prueba para enviar una notificación por email
    """
    if request.method == 'POST':
        try:
            # Crear una notificación de prueba
            notificacion = NotificacionSistema.objects.create(
                usuario=request.user,
                tipo='sistema',
                titulo='🧪 Notificación de Prueba',
                mensaje='Esta es una notificación de prueba para verificar el sistema de emails. Si recibes este email, significa que el sistema está funcionando correctamente.',
                prioridad='normal'
            )
            
            # Enviar email
            resultado = NotificacionService.enviar_email_notificacion(notificacion)
            
            if resultado:
                # Enviar notificación push también
                NotificacionService.enviar_notificacion_push(notificacion)
                
                context = {
                    'mensaje': '¡Notificación enviada exitosamente! Revisa la terminal del servidor para ver el email.',
                    'tipo_mensaje': 'success',
                    'titulo_mensaje': 'Éxito',
                    'icono': 'check-circle',
                    'debug': settings.DEBUG
                }
            else:
                context = {
                    'mensaje': 'Error al enviar la notificación por email.',
                    'tipo_mensaje': 'danger',
                    'titulo_mensaje': 'Error',
                    'icono': 'exclamation-triangle',
                    'debug': settings.DEBUG
                }
        except Exception as e:
            context = {
                'mensaje': f'Error: {str(e)}',
                'tipo_mensaje': 'danger',
                'titulo_mensaje': 'Error',
                'icono': 'exclamation-triangle',
                'debug': settings.DEBUG
            }
    else:
        context = {
            'debug': settings.DEBUG
        }
    
    return render(request, 'core/test_notification.html', context)


@login_required
def push_notifications_setup(request):
    """
    Vista para configurar notificaciones push
    """
    if request.method == 'POST':
        try:
            # Aquí se procesaría la suscripción push
            # Por ahora solo simulamos el éxito
            context = {
                'mensaje': 'Notificaciones push configuradas exitosamente.',
                'tipo_mensaje': 'success',
                'titulo_mensaje': 'Configurado',
                'icono': 'check-circle'
            }
        except Exception as e:
            context = {
                'mensaje': f'Error al configurar: {str(e)}',
                'tipo_mensaje': 'danger',
                'titulo_mensaje': 'Error',
                'icono': 'exclamation-triangle'
            }
    else:
        context = {}
    
    return render(request, 'core/push_notifications_setup.html', context)


@login_required
def api_push_subscription(request):
    """
    API para manejar suscripciones push
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            subscription_info = data.get('subscription')
            
            # Guardar la suscripción en la base de datos
            # Por ahora solo simulamos el éxito
            return JsonResponse({'status': 'success', 'message': 'Suscripción guardada'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def perfil(request):
    """
    Vista del perfil del usuario
    """
    context = {
        'usuario': request.user,
    }
    return render(request, 'core/perfil.html', context)

# ===== VISTAS DEL MÓDULO DE INVENTARIO =====

@login_required
def inventario_dashboard(request):
    """Dashboard del módulo de inventario"""
    try:
        # Estadísticas generales
        total_items = ItemInventario.objects.count()
        total_categorias = CategoriaInventario.objects.count()
        items_bajo_stock = ItemInventario.objects.filter(stock_actual__lte=F('stock_minimo')).count()
        valor_total_inventario = ItemInventario.objects.aggregate(
            total=Sum('stock_actual')
        )['total'] or 0
        
        # Items más utilizados
        items_mas_asignados = ItemInventario.objects.annotate(
            total_asignaciones=Count('asignaciones')
        ).order_by('-total_asignaciones')[:5]
        
        # Categorías con más items
        categorias_con_items = CategoriaInventario.objects.annotate(
            total_items=Count('iteminventario')
        ).order_by('-total_items')
        
        # Asignaciones recientes
        asignaciones_recientes = AsignacionInventario.objects.select_related(
            'item', 'proyecto', 'asignado_por'
        ).order_by('-fecha_asignacion')[:10]
        
        context = {
            'total_items': total_items,
            'total_categorias': total_categorias,
            'items_bajo_stock': items_bajo_stock,
            'valor_total_inventario': valor_total_inventario,
            'items_mas_asignados': items_mas_asignados,
            'categorias_con_items': categorias_con_items,
            'asignaciones_recientes': asignaciones_recientes,
        }
        
        return render(request, 'core/inventario/dashboard.html', context)
        
    except Exception as e:
        logger.error(f'Error en inventario_dashboard: {e}')
        messages.error(request, 'Error al cargar el dashboard de inventario')
        return redirect('inventario_list')

# Vistas para Categorías
@login_required
def categoria_list(request):
    """Lista de categorías de inventario"""
    categorias = CategoriaInventario.objects.all().order_by('nombre')
    return render(request, 'core/inventario/categoria/list.html', {'categorias': categorias})

@login_required
def categoria_create(request):
    """Crear nueva categoría"""
    if request.method == 'POST':
        form = CategoriaInventarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('categoria_list')
    else:
        form = CategoriaInventarioForm()
    
    return render(request, 'core/inventario/categoria/create.html', {'form': form})

@login_required
def categoria_detail(request, pk):
    """Detalle de categoría"""
    categoria = get_object_or_404(CategoriaInventario, pk=pk)
    items = ItemInventario.objects.filter(categoria=categoria)
    return render(request, 'core/inventario/categoria/detail.html', {
        'categoria': categoria, 'items': items
    })

@login_required
def categoria_edit(request, pk):
    """Editar categoría"""
    categoria = get_object_or_404(CategoriaInventario, pk=pk)
    if request.method == 'POST':
        form = CategoriaInventarioForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('categoria_list')
    else:
        form = CategoriaInventarioForm(instance=categoria)
    
    return render(request, 'core/inventario/categoria/edit.html', {
        'form': form, 'categoria': categoria
    })

@login_required
def categoria_delete(request, pk):
    """Eliminar categoría"""
    categoria = get_object_or_404(CategoriaInventario, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('categoria_list')
    
    return render(request, 'core/inventario/categoria/delete.html', {'categoria': categoria})

# Vistas para Items
@login_required
def item_list(request):
    """Lista de items del inventario"""
    items = ItemInventario.objects.select_related('categoria').all().order_by('nombre')
    
    # Filtros
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        items = items.filter(categoria_id=categoria_id)
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(nombre__icontains=query) | 
            Q(codigo__icontains=query) | 
            Q(descripcion__icontains=query)
        )
    
    # Ordenamiento
    orden = request.GET.get('orden', 'nombre')
    if orden == 'stock':
        items = items.order_by('stock_actual')
    elif orden == 'categoria':
        items = items.order_by('categoria__nombre')
    
    # Estadísticas para el dashboard
    total_items = ItemInventario.objects.count()
    items_activos = ItemInventario.objects.filter(activo=True).count()
    categorias_count = CategoriaInventario.objects.count()
    
    categorias = CategoriaInventario.objects.all()
    
    context = {
        'items': items,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
        'query': query,
        'orden': orden,
        'total_items': total_items,
        'items_activos': items_activos,
        'categorias_count': categorias_count
    }
    
    return render(request, 'core/inventario/item/list.html', context)

@login_required
def item_create(request):
    """Crear nuevo item"""
    if request.method == 'POST':
        form = ItemInventarioForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.stock_disponible = item.stock_actual
            item.save()
            messages.success(request, 'Item creado exitosamente')
            return redirect('item_list')
    else:
        form = ItemInventarioForm()
    
    return render(request, 'core/inventario/item/create.html', {'form': form})

@login_required
def item_detail(request, pk):
    """Detalle de item"""
    item = get_object_or_404(ItemInventario, pk=pk)
    asignaciones = AsignacionInventario.objects.filter(item=item).select_related(
        'proyecto', 'asignado_por'
    ).order_by('-fecha_asignacion')
    
    context = {
        'item': item,
        'asignaciones': asignaciones
    }
    
    return render(request, 'core/inventario/item/detail.html', context)

@login_required
def item_edit(request, pk):
    """Editar item"""
    item = get_object_or_404(ItemInventario, pk=pk)
    if request.method == 'POST':
        form = ItemInventarioForm(request.POST, instance=item)
        if form.is_valid():
            # Actualizar stock disponible si cambió el stock actual
            old_stock = item.stock_actual
            item = form.save(commit=False)
            if item.stock_actual != old_stock:
                diferencia = item.stock_actual - old_stock
                item.stock_disponible += diferencia
            item.save()
            messages.success(request, 'Item actualizado exitosamente')
            return redirect('item_list')
    else:
        form = ItemInventarioForm(instance=item)
    
    return render(request, 'core/inventario/item/edit.html', {
        'form': form, 'item': item
    })

@login_required
def item_delete(request, pk):
    """Eliminar item"""
    item = get_object_or_404(ItemInventario, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Item eliminado exitosamente')
        return redirect('item_list')
    
    return render(request, 'core/inventario/item/delete.html', {'item': item})

# Vistas para Asignaciones
@login_required
def asignacion_list(request):
    """Lista de asignaciones de inventario"""
    asignaciones = AsignacionInventario.objects.select_related(
        'item', 'proyecto', 'asignado_por'
    ).all().order_by('-fecha_asignacion')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        asignaciones = asignaciones.filter(estado=estado)
    
    proyecto_id = request.GET.get('proyecto')
    if proyecto_id:
        asignaciones = asignaciones.filter(proyecto_id=proyecto_id)
    
    # Búsqueda
    query = request.GET.get('q')
    if query:
        asignaciones = asignaciones.filter(
            Q(item__nombre__icontains=query) | 
            Q(proyecto__nombre__icontains=query) |
            Q(notas__icontains=query)
        )
    
    proyectos = Proyecto.objects.all()
    
    context = {
        'asignaciones': asignaciones,
        'proyectos': proyectos,
        'estado_seleccionado': estado,
        'proyecto_seleccionado': proyecto_id,
        'query': query
    }
    
    return render(request, 'core/inventario/asignacion/list.html', context)

@login_required
def asignacion_create(request):
    """Crear nueva asignación"""
    if request.method == 'POST':
        form = AsignacionInventarioForm(request.POST)
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.asignado_por = request.user
            
            # Verificar stock disponible
            if asignacion.item.stock_disponible < asignacion.cantidad_asignada:
                messages.error(request, f'Stock insuficiente. Disponible: {asignacion.item.stock_disponible}')
                return render(request, 'core/inventario/asignacion/create.html', {'form': form})
            
            asignacion.save()
            messages.success(request, 'Asignación creada exitosamente')
            return redirect('asignacion_list')
    else:
        form = AsignacionInventarioForm()
    
    return render(request, 'core/inventario/asignacion/create.html', {'form': form})

@login_required
def asignacion_detail(request, pk):
    """Detalle de asignación"""
    asignacion = get_object_or_404(AsignacionInventario, pk=pk)
    return render(request, 'core/inventario/asignacion/detail.html', {'asignacion': asignacion})


# ============================================
# GESTIÓN DE USUARIOS Y ROLES
# ============================================

@login_required
def usuarios_lista(request):
    """Lista de usuarios del sistema - SOLO SUPERUSUARIOS"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    usuarios = User.objects.all().order_by('-date_joined')
    
    context = {
        'usuarios': usuarios,
        'total_usuarios': usuarios.count(),
    }
    
    return render(request, 'core/usuarios_lista.html', context)


@login_required
def usuario_crear(request):
    """Crear nuevo usuario - SOLO SUPERUSUARIOS"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    if request.method == 'POST':
        try:
            # Datos básicos del usuario
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            password = request.POST.get('password')
            rol_id = request.POST.get('rol')
            
            # Validaciones básicas
            if not username or not password or not rol_id:
                messages.error(request, 'Todos los campos marcados son obligatorios')
                return redirect('usuario_crear')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Ya existe un usuario con ese nombre')
                return redirect('usuario_crear')
            
            # Crear usuario
            usuario = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            
            # Crear perfil de usuario
            rol = Rol.objects.get(id=rol_id)
            PerfilUsuario.objects.create(
                usuario=usuario,
                rol=rol,
                telefono=request.POST.get('telefono', ''),
                direccion=request.POST.get('direccion', '')
            )
            
            messages.success(request, f'Usuario {username} creado exitosamente con rol {rol.nombre}')
            return redirect('usuarios_lista')
            
        except Exception as e:
            messages.error(request, f'Error al crear usuario: {str(e)}')
            return redirect('usuario_crear')
    
    # GET - Mostrar formulario
    roles = Rol.objects.all()
    
    context = {
        'roles': roles,
    }
    
    return render(request, 'core/usuario_crear.html', context)


@login_required
def usuario_editar(request, usuario_id):
    """Editar usuario existente - SOLO SUPERUSUARIOS"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    try:
        usuario = User.objects.get(id=usuario_id)
        perfil, created = PerfilUsuario.objects.get_or_create(usuario=usuario)
        
        if request.method == 'POST':
            # Actualizar datos básicos
            usuario.first_name = request.POST.get('first_name', '')
            usuario.last_name = request.POST.get('last_name', '')
            usuario.email = request.POST.get('email', '')
            usuario.is_active = request.POST.get('is_active') == 'on'
            usuario.save()
            
            # Actualizar perfil
            rol_id = request.POST.get('rol')
            if rol_id:
                perfil.rol = Rol.objects.get(id=rol_id)
            perfil.telefono = request.POST.get('telefono', '')
            perfil.direccion = request.POST.get('direccion', '')
            perfil.activo = request.POST.get('activo') == 'on'
            perfil.save()
            
            # Cambiar contraseña si se proporciona
            nueva_password = request.POST.get('password')
            if nueva_password:
                usuario.set_password(nueva_password)
                usuario.save()
            
            messages.success(request, f'Usuario {usuario.username} actualizado exitosamente')
            return redirect('usuarios_lista')
        
        # GET - Mostrar formulario
        roles = Rol.objects.all()
        
        context = {
            'usuario_obj': usuario,
            'perfil': perfil,
            'roles': roles,
        }
        
        return render(request, 'core/usuario_editar.html', context)
        
    except User.DoesNotExist:
        messages.error(request, 'Usuario no encontrado')
        return redirect('usuarios_lista')
    except Exception as e:
        messages.error(request, f'Error al editar usuario: {str(e)}')
        return redirect('usuarios_lista')


@login_required
def roles_lista(request):
    """Lista de roles del sistema - SOLO SUPERUSUARIOS"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    roles = Rol.objects.all().order_by('nombre')
    
    # Obtener permisos por rol
    roles_con_permisos = []
    for rol in roles:
        permisos = RolPermiso.objects.filter(rol=rol, activo=True).count()
        usuarios_count = PerfilUsuario.objects.filter(rol=rol).count()
        roles_con_permisos.append({
            'rol': rol,
            'permisos_count': permisos,
            'usuarios_count': usuarios_count
        })
    
    context = {
        'roles_con_permisos': roles_con_permisos,
        'total_roles': roles.count(),
    }
    
    return render(request, 'core/roles_lista.html', context)


@login_required
def rol_permisos(request, rol_id):
    """Gestionar permisos de un rol - SOLO SUPERUSUARIOS"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    try:
        rol = Rol.objects.get(id=rol_id)
        
        if request.method == 'POST':
            # Limpiar permisos actuales
            RolPermiso.objects.filter(rol=rol).delete()
            
            # Agregar nuevos permisos
            permisos_seleccionados = request.POST.getlist('permisos')
            for permiso_id in permisos_seleccionados:
                permiso = Permiso.objects.get(id=permiso_id)
                RolPermiso.objects.create(rol=rol, permiso=permiso)
            
            messages.success(request, f'Permisos del rol {rol.nombre} actualizados exitosamente')
            return redirect('roles_lista')
        
        # GET - Mostrar formulario
        modulos = Modulo.objects.all().order_by('orden')
        permisos_actuales = RolPermiso.objects.filter(rol=rol, activo=True).values_list('permiso_id', flat=True)
        
        # Organizar permisos por módulo
        modulos_con_permisos = []
        for modulo in modulos:
            permisos = Permiso.objects.filter(modulo=modulo)
            modulos_con_permisos.append({
                'modulo': modulo,
                'permisos': permisos
            })
        
        context = {
            'rol': rol,
            'modulos_con_permisos': modulos_con_permisos,
            'permisos_actuales': list(permisos_actuales),
        }
        
        return render(request, 'core/rol_permisos.html', context)
        
    except Rol.DoesNotExist:
        messages.error(request, 'Rol no encontrado')
        return redirect('roles_lista')
    except Exception as e:
        messages.error(request, f'Error al gestionar permisos: {str(e)}')
        return redirect('roles_lista')

@login_required
def asignacion_edit(request, pk):
    """Editar asignación"""
    asignacion = get_object_or_404(AsignacionInventario, pk=pk)
    if request.method == 'POST':
        form = AsignacionInventarioForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Asignación actualizada exitosamente')
            return redirect('asignacion_list')
    else:
        form = AsignacionInventarioForm(instance=asignacion)
    
    return render(request, 'core/inventario/asignacion/edit.html', {
        'form': form, 'asignacion': asignacion
    })

@login_required
def asignacion_delete(request, pk):
    """Eliminar asignación"""
    asignacion = get_object_or_404(AsignacionInventario, pk=pk)
    if request.method == 'POST':
        asignacion.delete()
        messages.success(request, 'Asignación eliminada exitosamente')
        return redirect('asignacion_list')
    
    return render(request, 'core/inventario/asignacion/delete.html', {'asignacion': asignacion})

@login_required
def asignacion_devolver(request, pk):
    """Marcar asignación como devuelta"""
    asignacion = get_object_or_404(AsignacionInventario, pk=pk)
    if request.method == 'POST':
        asignacion.estado = 'devuelto'
        asignacion.fecha_devolucion = timezone.now().date()
        asignacion.save()
        messages.success(request, 'Item marcado como devuelto exitosamente')
        return redirect('asignacion_list')
    
    return render(request, 'core/inventario/asignacion/devolver.html', {'asignacion': asignacion})


# ============================================
# DASHBOARD INTELIGENTE - FUNCIONES AVANZADAS
# ============================================

@login_required
def dashboard_intelligent_data(request):
    """API para obtener datos del dashboard inteligente"""
    try:
        # Datos de rentabilidad por proyecto
        proyectos_rentabilidad = []
        proyectos = Proyecto.objects.filter(activo=True)[:10]
        
        for proyecto in proyectos:
            # Calcular ingresos del proyecto
            ingresos_proyecto = Factura.objects.filter(
                proyecto=proyecto,
                estado__in=['pagada', 'enviada']
            ).aggregate(total=Sum('monto_total'))['total'] or 0
            
            # Calcular gastos del proyecto
            gastos_proyecto = Gasto.objects.filter(
                proyecto=proyecto,
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or 0
            
            # Calcular rentabilidad
            if ingresos_proyecto > 0:
                rentabilidad = ((ingresos_proyecto - gastos_proyecto) / ingresos_proyecto) * 100
            else:
                rentabilidad = 0
            
            proyectos_rentabilidad.append({
                'nombre': proyecto.nombre,
                'rentabilidad': round(rentabilidad, 2),
                'ingresos': float(ingresos_proyecto),
                'gastos': float(gastos_proyecto)
            })
        
        # Datos de flujo de caja mensual
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio']
        flujo_caja = []
        
        for i, mes in enumerate(meses):
            # Simular datos de flujo de caja (en producción se calcularían reales)
            ingresos_mes = float(Factura.objects.filter(
                fecha_emision__month=i+1,
                estado__in=['pagada', 'enviada']
            ).aggregate(total=Sum('monto_total'))['total'] or 0)
            
            gastos_mes = float(Gasto.objects.filter(
                fecha_gasto__month=i+1,
                aprobado=True
            ).aggregate(total=Sum('monto'))['total'] or 0)
            
            flujo_caja.append({
                'mes': mes,
                'ingresos': ingresos_mes,
                'gastos': gastos_mes,
                'neto': ingresos_mes - gastos_mes
            })
        
        # Métricas de productividad
        total_proyectos = Proyecto.objects.filter(activo=True).count()
        proyectos_completados = Proyecto.objects.filter(estado='completado').count()
        eficiencia_proyectos = (proyectos_completados / total_proyectos * 100) if total_proyectos > 0 else 0
        
        # Calcular tiempo promedio de proyectos
        proyectos_con_fechas = Proyecto.objects.filter(
            fecha_inicio__isnull=False,
            fecha_fin__isnull=False
        )
        
        tiempo_promedio = 0
        if proyectos_con_fechas.exists():
            total_dias = 0
            for proyecto in proyectos_con_fechas:
                dias = (proyecto.fecha_fin - proyecto.fecha_inicio).days
                total_dias += dias
            tiempo_promedio = total_dias / proyectos_con_fechas.count()
        
        # KPIs inteligentes
        satisfaccion_cliente = 85  # Simulado - en producción se calcularía de encuestas
        calidad_obra = 90  # Simulado - en producción se calcularía de inspecciones
        rentabilidad_general = 25  # Simulado - en producción se calcularía real
        eficiencia_general = round(eficiencia_proyectos, 1)
        
        # Datos de tendencias
        tendencias = {
            'ventas': '+12%',
            'clientes': '+8%',
            'costos': '-5%',
            'eficiencia': '+15%'
        }
        
        # Predicciones del sistema
        predicciones = {
            'ventas_proximo_mes': float(Factura.objects.filter(
                fecha_emision__month=timezone.now().month + 1
            ).aggregate(total=Sum('monto_total'))['total'] or 25000),
            'rentabilidad_esperada': 28.5
        }
        
        # Comparación de períodos
        mes_actual = timezone.now().month
        mes_anterior = mes_actual - 1 if mes_actual > 1 else 12
        
        periodo_actual = float(Factura.objects.filter(
            fecha_emision__month=mes_actual
        ).aggregate(total=Sum('monto_total'))['total'] or 0)
        
        periodo_anterior = float(Factura.objects.filter(
            fecha_emision__month=mes_anterior
        ).aggregate(total=Sum('monto_total'))['total'] or 0)
        
        crecimiento = ((periodo_actual - periodo_anterior) / periodo_anterior * 100) if periodo_anterior > 0 else 0
        
        data = {
            'rentabilidad': {
                'proyectos': proyectos_rentabilidad,
                'total': round(rentabilidad_general, 1),
                'proyectos_activos': total_proyectos
            },
            'flujoCaja': {
                'mensual': flujo_caja,
                'ingresos_mes': periodo_actual,
                'gastos_mes': float(Gasto.objects.filter(
                    fecha_gasto__month=mes_actual,
                    aprobado=True
                ).aggregate(total=Sum('monto'))['total'] or 0)
            },
            'productividad': {
                'eficiencia': round(eficiencia_proyectos, 1),
                'tiempo_promedio': round(tiempo_promedio, 0),
                'proyectos_completados': proyectos_completados,
                'total_proyectos': total_proyectos
            },
            'kpis': {
                'satisfaccion': satisfaccion_cliente,
                'calidad': calidad_obra,
                'rentabilidad': rentabilidad_general,
                'eficiencia': eficiencia_general
            },
            'tendencias': tendencias,
            'predicciones': predicciones,
            'comparacion': {
                'periodo_anterior': periodo_anterior,
                'periodo_actual': periodo_actual,
                'crecimiento': round(crecimiento, 1)
            }
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        logger.error(f'Error obteniendo datos del dashboard inteligente: {str(e)}')
        return JsonResponse({
            'error': 'Error obteniendo datos',
            'message': str(e)
        }, status=500)


@login_required
def dashboard_intelligent_analytics(request):
    """Vista para análisis avanzado del dashboard inteligente"""
    try:
        # Obtener métricas avanzadas
        context = {
            'titulo': 'Análisis Inteligente del Sistema',
            'fecha_analisis': timezone.now().strftime('%d/%m/%Y %H:%M'),
        }
        
        return render(request, 'core/dashboard_intelligent_analytics.html', context)
        
    except Exception as e:
        logger.error(f'Error en análisis inteligente: {str(e)}')
        messages.error(request, f'Error al cargar análisis: {str(e)}')
        return redirect('dashboard')

@login_required
def roles_resumen(request):
    """Mostrar resumen completo de todos los roles y sus permisos - SOLO SUPERUSUARIOS"""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder a esta sección')
        return redirect('dashboard')
    
    try:
        # Obtener todos los roles con sus permisos
        roles = Rol.objects.all().order_by('orden')
        modulos = Modulo.objects.all().order_by('orden')
        
        # Crear resumen detallado
        resumen_roles = []
        for rol in roles:
            permisos_rol = RolPermiso.objects.filter(rol=rol, activo=True).select_related('permiso__modulo')
            
            # Organizar permisos por módulo
            permisos_por_modulo = {}
            for rp in permisos_rol:
                modulo_nombre = rp.permiso.modulo.nombre
                if modulo_nombre not in permisos_por_modulo:
                    permisos_por_modulo[modulo_nombre] = []
                permisos_por_modulo[modulo_nombre].append(rp.permiso.nombre)
            
            resumen_roles.append({
                'rol': rol,
                'permisos_por_modulo': permisos_por_modulo,
                'total_permisos': permisos_rol.count()
            })
        
        # Estadísticas generales
        total_roles = roles.count()
        total_modulos = modulos.count()
        total_permisos = Permiso.objects.count()
        
        context = {
            'resumen_roles': resumen_roles,
            'modulos': modulos,
            'total_roles': total_roles,
            'total_modulos': total_modulos,
            'total_permisos': total_permisos,
        }
        
        return render(request, 'core/roles_resumen.html', context)
        
    except Exception as e:
        messages.error(request, f'Error al generar resumen: {str(e)}')
        return redirect('roles_lista')


def offline_page(request):
    """Página offline para PWA"""
    return render(request, 'offline.html')

def test_view(request):
    """Vista de prueba para diagnosticar problemas"""
    from django.utils import timezone
    context = {
        'now': timezone.now(),
    }
    return render(request, 'core/test.html', context)

@login_required
def planilla_proyecto(request, proyecto_id):
    """Planilla de personal del proyecto con control de anticipos"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Obtener colaboradores asignados al proyecto
    colaboradores_asignados = proyecto.colaboradores.all().order_by('nombre')
    
    # Obtener anticipos del proyecto
    anticipos = AnticipoProyecto.objects.filter(proyecto=proyecto).select_related('colaborador')
    
    # Calcular totales y salarios netos
    total_anticipos = anticipos.filter(estado='pendiente').aggregate(
        total=Sum('monto')
    )['total'] or 0
    
    total_liquidado = anticipos.filter(estado='liquidado').aggregate(
        total=Sum('monto')
    )['total'] or 0
    
    # Calcular salarios netos y totales de la planilla
    total_salarios = 0
    total_anticipos_aplicados = 0
    total_salarios_netos = 0
    
    for colaborador in colaboradores_asignados:
        salario_colaborador = colaborador.salario or 0
        
        # Anticipos pendientes (que se descuentan del salario)
        anticipos_pendientes = anticipos.filter(
            colaborador=colaborador, 
            estado='pendiente'
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        # Anticipos liquidados (que ya se pagaron y también se descuentan)
        anticipos_liquidados = anticipos.filter(
            colaborador=colaborador, 
            estado='liquidado'
        ).aggregate(total=Sum('monto'))['total'] or 0
        
        # Salario neto = Salario base - anticipos pendientes - anticipos liquidados
        salario_neto = salario_colaborador - anticipos_pendientes - anticipos_liquidados
        
        # Determinar el estado actual del colaborador
        if anticipos_pendientes > 0:
            colaborador.estado_actual = 'pendiente'
            colaborador.estado_display = 'Pendiente'
        elif anticipos_liquidados > 0:
            colaborador.estado_actual = 'liquidado'
            colaborador.estado_display = 'Liquidado'
        else:
            colaborador.estado_actual = 'sin_anticipos'
            colaborador.estado_display = 'Sin Anticipos'
        
        # Agregar campos calculados al colaborador
        colaborador.salario_neto = salario_neto
        colaborador.deuda_anticipos = anticipos_pendientes
        colaborador.anticipos_liquidados = anticipos_liquidados
        
        total_salarios += salario_colaborador
        total_anticipos_aplicados += anticipos_pendientes + anticipos_liquidados
        total_salarios_netos += salario_neto
    
    context = {
        'proyecto': proyecto,
        'colaboradores_asignados': colaboradores_asignados,
        'anticipos': anticipos,
        'total_anticipos': total_anticipos,
        'total_liquidado': total_liquidado,
        'saldo_pendiente': total_anticipos,  # Solo anticipos pendientes
        'total_salarios': total_salarios,
        'total_anticipos_aplicados': total_anticipos_aplicados,
        'total_salarios_netos': total_salarios_netos,
    }
    
    return render(request, 'core/proyectos/planilla.html', context)


@login_required
def planilla_proyecto_pdf(request, proyecto_id):
    """Generar PDF de la planilla del proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Obtener colaboradores asignados al proyecto
    colaboradores_asignados = proyecto.colaboradores.all().order_by('nombre')
    
    # Obtener anticipos del proyecto
    anticipos = AnticipoProyecto.objects.filter(proyecto=proyecto).select_related('colaborador')
    
    # Calcular totales
    total_anticipos = anticipos.filter(estado='pendiente').aggregate(
        total=Sum('monto')
    )['total'] or 0
    
    total_liquidado = anticipos.filter(estado='liquidado').aggregate(
        total=Sum('monto')
    )['total'] or 0
    
    total_salarios = sum(colaborador.salario or 0 for colaborador in colaboradores_asignados)
    total_anticipos_aplicados = total_anticipos + total_liquidado
    total_salarios_netos = total_salarios - total_anticipos_aplicados
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    # Título principal
    elements.append(Paragraph(f"PLANILLA DE PERSONAL", title_style))
    elements.append(Paragraph(f"Proyecto: {proyecto.nombre}", subtitle_style))
    
    # Información del proyecto
    info_proyecto = [
        ['Cliente:', proyecto.cliente.razon_social if proyecto.cliente else 'N/A'],
        ['Fecha Inicio:', proyecto.fecha_inicio.strftime('%d/%m/%Y') if proyecto.fecha_inicio else 'N/A'],
        ['Fecha Fin:', proyecto.fecha_fin.strftime('%d/%m/%Y') if proyecto.fecha_fin else 'N/A'],
        ['Estado:', proyecto.get_estado_display()],
        ['Presupuesto:', f"Q{proyecto.presupuesto:,.2f}" if proyecto.presupuesto else 'N/A'],
    ]
    
    info_table = Table(info_proyecto, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, -1), 10),
        ('BOTTOMPADDING', (0, 0), (0, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 20))
    
    # Tabla de colaboradores
    if colaboradores_asignados:
        # Encabezados de la tabla
        headers = ['Colaborador', 'Cargo', 'Salario Base', 'Anticipos', 'Salario Neto', 'Estado']
        data = [headers]
        
        for colaborador in colaboradores_asignados:
            salario_base = colaborador.salario or 0
            
            # Calcular anticipos del colaborador
            anticipos_colaborador = anticipos.filter(colaborador=colaborador)
            anticipos_pendientes = anticipos_colaborador.filter(estado='pendiente').aggregate(
                total=Sum('monto')
            )['total'] or 0
            anticipos_liquidados = anticipos_colaborador.filter(estado='liquidado').aggregate(
                total=Sum('monto')
            )['total'] or 0
            total_anticipos_colaborador = anticipos_pendientes + anticipos_liquidados
            
            salario_neto = salario_base - total_anticipos_colaborador
            
            # Determinar estado
            if anticipos_pendientes > 0:
                estado = 'Pendiente'
            elif anticipos_liquidados > 0:
                estado = 'Liquidado'
            else:
                estado = 'Sin Anticipos'
            
            data.append([
                colaborador.nombre,
                colaborador.cargo or 'N/A',
                f"Q{salario_base:,.2f}",
                f"Q{total_anticipos_colaborador:,.2f}",
                f"Q{salario_neto:,.2f}",
                estado
            ])
        
        # Crear tabla
        table = Table(data, colWidths=[1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),  # Alinear números a la derecha
            ('ALIGN', (0, 1), (1, 1), 'LEFT'),     # Alinear texto a la izquierda
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
    
    # Resumen financiero
    resumen_data = [
        ['CONCEPTO', 'MONTO'],
        ['Total Salarios Base', f"Q{total_salarios:,.2f}"],
        ['Total Anticipos', f"Q{total_anticipos_aplicados:,.2f}"],
        ['Total Salarios Netos', f"Q{total_salarios_netos:,.2f}"],
        ['Saldo Pendiente', f"Q{total_anticipos:,.2f}"],
    ]
    
    resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
    resumen_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, -1), 10),
        ('BOTTOMPADDING', (0, 0), (0, -1), 12),
        ('BACKGROUND', (1, 0), (1, -1), colors.white),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(resumen_table)
    
    # Pie de página
    elements.append(Spacer(1, 30))
    fecha_generacion = timezone.now().strftime('%d/%m/%Y %H:%M')
    elements.append(Paragraph(f"Reporte generado el: {fecha_generacion}", styles['Normal']))
    elements.append(Paragraph(f"Sistema ARCA Construcción", styles['Normal']))
    
    # Generar PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Crear respuesta HTTP
    filename = f"planilla_proyecto_{proyecto.nombre.replace(' ', '_')}_{timezone.now().strftime('%Y%m%d')}.pdf"
    
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required
def crear_anticipo_masivo(request, proyecto_id):
    """Crear anticipo masivo para todos los colaboradores del proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        monto = request.POST.get('monto')
        concepto = request.POST.get('concepto', 'Anticipo masivo por proyecto')
        
        if monto and monto.isdigit():
            monto = Decimal(monto)
            colaboradores = proyecto.colaboradores.all()
            
            # Crear anticipos para todos los colaboradores
            anticipos_creados = []
            for colaborador in colaboradores:
                anticipo = AnticipoProyecto.objects.create(
                    proyecto=proyecto,
                    colaborador=colaborador,
                    monto=monto,
                    tipo='masivo',
                    concepto=concepto,
                    observaciones=f"Anticipo masivo - {concepto}"
                )
                anticipos_creados.append(anticipo)
            
            messages.success(
                request, 
                f'Se crearon {len(anticipos_creados)} anticipos de Q{monto} cada uno para el proyecto {proyecto.nombre}'
            )
            
            return redirect('planilla_proyecto', proyecto_id=proyecto.id)
    
    context = {
        'proyecto': proyecto,
        'total_colaboradores': proyecto.colaboradores.count()
    }
    
    return render(request, 'core/proyectos/crear_anticipo_masivo.html', context)


@login_required
def crear_anticipo_individual(request, proyecto_id):
    """Crear anticipo individual para un colaborador específico"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    if request.method == 'POST':
        colaborador_id = request.POST.get('colaborador')
        monto = request.POST.get('monto')
        concepto = request.POST.get('concepto', 'Anticipo individual')
        observaciones = request.POST.get('observaciones', '')
        
        if colaborador_id and monto and monto.isdigit():
            colaborador = get_object_or_404(Colaborador, id=colaborador_id)
            monto = Decimal(monto)
            
            # Verificar que el colaborador esté asignado al proyecto
            if colaborador in proyecto.colaboradores.all():
                anticipo = AnticipoProyecto.objects.create(
                    proyecto=proyecto,
                    colaborador=colaborador,
                    monto=monto,
                    tipo='individual',
                    concepto=concepto,
                    observaciones=observaciones
                )
                
                messages.success(
                    request, 
                    f'Se creó anticipo de Q{monto} para {colaborador.nombre} en el proyecto {proyecto.nombre}'
                )
                
                return redirect('planilla_proyecto', proyecto_id=proyecto.id)
            else:
                messages.error(request, 'El colaborador no está asignado a este proyecto')
        else:
            messages.error(request, 'Por favor complete todos los campos requeridos')
    
    context = {
        'proyecto': proyecto,
        'colaboradores_disponibles': proyecto.colaboradores.all().order_by('nombre')
    }
    
    return render(request, 'core/proyectos/crear_anticipo_individual.html', context)


@login_required
def liquidar_anticipo(request, anticipo_id):
    """Liquidar un anticipo específico"""
    anticipo = get_object_or_404(AnticipoProyecto, id=anticipo_id)

    if request.method == 'POST':
        if anticipo.estado == 'pendiente':
            anticipo.liquidar_anticipo(request.user)
            messages.success(
                request, 
                f'Anticipo de Q{anticipo.monto} para {anticipo.colaborador.nombre} ha sido liquidado'
            )
        else:
            messages.warning(request, 'Este anticipo ya no está pendiente de liquidación')

    return redirect('planilla_proyecto', proyecto_id=anticipo.proyecto.id)


@login_required
def calendario_pagos_proyecto(request, proyecto_id):
    """Calendario de pagos y anticipos del proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Obtener mes y año de la URL o usar el actual
    mes = int(request.GET.get('mes', timezone.now().month))
    año = int(request.GET.get('año', timezone.now().year))
    
    # Obtener colaboradores asignados
    colaboradores = proyecto.colaboradores.all().order_by('nombre')
    
    # Obtener anticipos del mes
    anticipos_mes = AnticipoProyecto.objects.filter(
        proyecto=proyecto,
        fecha_anticipo__month=mes,
        fecha_anticipo__year=año
    ).order_by('fecha_anticipo')
    
    # Obtener anticipos liquidados del mes
    anticipos_liquidados_mes = AnticipoProyecto.objects.filter(
        proyecto=proyecto,
        fecha_liquidacion__month=mes,
        fecha_liquidacion__year=año
    ).order_by('fecha_liquidacion')
    
    # Calcular días del mes
    import calendar
    cal = calendar.monthcalendar(año, mes)
    nombre_mes = calendar.month_name[mes]
    
    # Crear eventos del calendario
    eventos_calendario = {}
    
    # Agregar día de pago (último día del mes)
    ultimo_dia = calendar.monthrange(año, mes)[1]
    eventos_calendario[ultimo_dia] = {
        'tipo': 'pago_salario',
        'titulo': 'Pago de Salarios',
        'descripcion': f'Pago mensual de salarios - Total: Q{sum(c.salario or 0 for c in colaboradores):.2f}',
        'color': 'success',
        'icono': 'fas fa-money-bill-wave'
    }
    
    # Agregar anticipos realizados
    for anticipo in anticipos_mes:
        dia = anticipo.fecha_anticipo.day
        if dia not in eventos_calendario:
            eventos_calendario[dia] = []
        elif not isinstance(eventos_calendario[dia], list):
            eventos_calendario[dia] = [eventos_calendario[dia]]
        
        eventos_calendario[dia].append({
            'tipo': 'anticipo_realizado',
            'titulo': f'Anticipo: {anticipo.colaborador.nombre}',
            'descripcion': f'Q{anticipo.monto} - {anticipo.concepto}',
            'color': 'warning',
            'icono': 'fas fa-hand-holding-usd',
            'anticipo_id': anticipo.id
        })
    
    # Agregar anticipos liquidados
    for anticipo in anticipos_liquidados_mes:
        dia = anticipo.fecha_liquidacion.day
        if dia not in eventos_calendario:
            eventos_calendario[dia] = []
        elif not isinstance(eventos_calendario[dia], list):
            eventos_calendario[dia] = [eventos_calendario[dia]]
        
        eventos_calendario[dia].append({
            'tipo': 'anticipo_liquidado',
            'titulo': f'Liquidado: {anticipo.colaborador.nombre}',
            'descripcion': f'Q{anticipo.monto} liquidado por {anticipo.liquidado_por.username if anticipo.liquidado_por else "Sistema"}',
            'color': 'success',
            'icono': 'fas fa-check-circle',
            'anticipo_id': anticipo.id
        })
    
    # Estadísticas del mes
    total_anticipos_mes = anticipos_mes.aggregate(total=Sum('monto'))['total'] or 0
    total_liquidado_mes = anticipos_liquidados_mes.aggregate(total=Sum('monto'))['total'] or 0
    saldo_pendiente_mes = total_anticipos_mes - total_liquidado_mes
    
    context = {
        'proyecto': proyecto,
        'colaboradores': colaboradores,
        'calendario': cal,
        'nombre_mes': nombre_mes,
        'mes': mes,
        'año': año,
        'eventos_calendario': eventos_calendario,
        'anticipos_mes': anticipos_mes,
        'anticipos_liquidados_mes': anticipos_liquidados_mes,
        'total_anticipos_mes': total_anticipos_mes,
        'total_liquidado_mes': total_liquidado_mes,
        'saldo_pendiente_mes': saldo_pendiente_mes,
        'meses': [(i, calendar.month_name[i]) for i in range(1, 13)],
        'años': range(año-2, año+3)
    }
    
    return render(request, 'core/proyectos/calendario_pagos.html', context)


@login_required
def administrar_anticipos_proyecto(request, proyecto_id):
    """Administrar anticipos del proyecto (editar, eliminar, cambiar estado)"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    
    # Obtener todos los anticipos del proyecto
    anticipos = AnticipoProyecto.objects.filter(proyecto=proyecto).select_related('colaborador').order_by('-fecha_anticipo')
    
    # Estadísticas de anticipos
    total_anticipos = anticipos.aggregate(total=Sum('monto'))['total'] or 0
    anticipos_pendientes = anticipos.filter(estado='pendiente').aggregate(total=Sum('monto'))['total'] or 0
    anticipos_liquidados = anticipos.filter(estado='liquidado').aggregate(total=Sum('monto'))['total'] or 0
    anticipos_cancelados = anticipos.filter(estado='cancelado').aggregate(total=Sum('monto'))['total'] or 0
    
    context = {
        'proyecto': proyecto,
        'anticipos': anticipos,
        'total_anticipos': total_anticipos,
        'anticipos_pendientes': anticipos_pendientes,
        'anticipos_liquidados': anticipos_liquidados,
        'anticipos_cancelados': anticipos_cancelados,
    }
    
    return render(request, 'core/proyectos/administrar_anticipos.html', context)


@login_required
def editar_anticipo(request, anticipo_id):
    """Editar un anticipo existente"""
    anticipo = get_object_or_404(AnticipoProyecto, id=anticipo_id)
    
    if request.method == 'POST':
        monto = request.POST.get('monto')
        concepto = request.POST.get('concepto')
        estado = request.POST.get('estado')
        
        if monto and concepto:
            try:
                anticipo.monto = Decimal(monto)
                anticipo.concepto = concepto
                anticipo.estado = estado
                anticipo.save()
                
                messages.success(request, f'Anticipo de {anticipo.colaborador.nombre} actualizado exitosamente')
                return redirect('administrar_anticipos_proyecto', proyecto_id=anticipo.proyecto.id)
            except ValueError:
                messages.error(request, 'El monto debe ser un número válido')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
    
    context = {
        'anticipo': anticipo,
        'estados_choices': AnticipoProyecto.ESTADO_CHOICES,
    }
    
    return render(request, 'core/proyectos/editar_anticipo.html', context)


@login_required
def eliminar_anticipo(request, anticipo_id):
    """Eliminar un anticipo"""
    anticipo = get_object_or_404(AnticipoProyecto, id=anticipo_id)
    proyecto_id = anticipo.proyecto.id
    
    if request.method == 'POST':
        colaborador_nombre = anticipo.colaborador.nombre
        anticipo.delete()
        messages.success(request, f'Anticipo de {colaborador_nombre} eliminado exitosamente')
        return redirect('administrar_anticipos_proyecto', proyecto_id=proyecto_id)
    
    context = {
        'anticipo': anticipo,
    }
    
    return render(request, 'core/proyectos/eliminar_anticipo.html', context)


@login_required
def cambiar_estado_anticipo(request, anticipo_id):
    """Cambiar el estado de un anticipo"""
    anticipo = get_object_or_404(AnticipoProyecto, id=anticipo_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('nuevo_estado')
        if nuevo_estado in ['pendiente', 'liquidado', 'cancelado']:
            anticipo.estado = nuevo_estado
            anticipo.save()
            
            estado_display = dict(AnticipoProyecto.ESTADO_CHOICES)[nuevo_estado]
            messages.success(request, f'Estado del anticipo de {anticipo.colaborador.nombre} cambiado a {estado_display}')
            return redirect('administrar_anticipos_proyecto', proyecto_id=anticipo.proyecto.id)
        else:
            messages.error(request, 'Estado no válido')
    
    context = {
        'anticipo': anticipo,
        'estados_choices': AnticipoProyecto.ESTADO_CHOICES,
    }
    
    return render(request, 'core/proyectos/cambiar_estado_anticipo.html', context)


@login_required
def carpeta_create(request, proyecto_id):
    """Crear nueva carpeta en un proyecto"""
    proyecto = get_object_or_404(Proyecto, id=proyecto_id, activo=True)
    
    if request.method == 'POST':
        form = CarpetaProyectoForm(request.POST, proyecto=proyecto)
        if form.is_valid():
            carpeta = form.save(commit=False)
            carpeta.proyecto = proyecto
            carpeta.creada_por = request.user
            carpeta.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Crear Carpeta',
                modulo='Archivos',
                descripcion=f'Carpeta creada: {carpeta.nombre} en el proyecto {proyecto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Carpeta creada exitosamente')
            return redirect('archivos_proyecto_list', proyecto_id=proyecto.id)
    else:
        form = CarpetaProyectoForm(proyecto=proyecto)
    
    context = {
        'form': form,
        'proyecto': proyecto,
        'accion': 'Crear',
        'titulo': 'Nueva Carpeta'
    }
    
    return render(request, 'core/archivos/carpeta_form.html', context)


@login_required
def carpeta_edit(request, carpeta_id):
    """Editar una carpeta existente"""
    carpeta = get_object_or_404(CarpetaProyecto, id=carpeta_id, activa=True)
    
    if request.method == 'POST':
        form = CarpetaProyectoForm(request.POST, instance=carpeta, proyecto=carpeta.proyecto, carpeta_actual=carpeta)
        if form.is_valid():
            carpeta = form.save()
            
            # Registrar actividad
            LogActividad.objects.create(
                usuario=request.user,
                accion='Editar Carpeta',
                modulo='Archivos',
                descripcion=f'Carpeta editada: {carpeta.nombre} en el proyecto {carpeta.proyecto.nombre}',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            
            messages.success(request, 'Carpeta actualizada exitosamente')
            return redirect('archivos_proyecto_list', proyecto_id=carpeta.proyecto.id)
    else:
        form = CarpetaProyectoForm(instance=carpeta, proyecto=carpeta.proyecto, carpeta_actual=carpeta)
    
    context = {
        'form': form,
        'carpeta': carpeta,
        'proyecto': carpeta.proyecto,
        'accion': 'Editar',
        'titulo': 'Editar Carpeta'
    }
    
    return render(request, 'core/archivos/carpeta_form.html', context)


@login_required
def carpeta_delete(request, carpeta_id):
    """Eliminar una carpeta"""
    carpeta = get_object_or_404(CarpetaProyecto, id=carpeta_id, activa=True)
    
    if request.method == 'POST':
        # Verificar que la carpeta se pueda eliminar
        if not carpeta.puede_eliminarse():
            messages.error(request, 'No se puede eliminar la carpeta porque contiene archivos o subcarpetas')
            return redirect('archivos_proyecto_list', proyecto_id=carpeta.proyecto.id)
        
        # Registrar actividad antes de eliminar
        LogActividad.objects.create(
            usuario=request.user,
            accion='Eliminar Carpeta',
            modulo='Archivos',
            descripcion=f'Carpeta eliminada: {carpeta.nombre} del proyecto {carpeta.proyecto.nombre}',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        carpeta.delete()
        messages.success(request, 'Carpeta eliminada exitosamente')
        return redirect('archivos_proyecto_list', proyecto_id=carpeta.proyecto.id)
    
    return render(request, 'core/archivos/carpeta_delete.html', {'carpeta': carpeta})


@login_required
def carpeta_detail(request, carpeta_id):
    """Ver detalles de una carpeta y su contenido"""
    carpeta = get_object_or_404(CarpetaProyecto, id=carpeta_id, activa=True)
    
    # Obtener archivos en esta carpeta
    archivos = ArchivoProyecto.objects.filter(carpeta=carpeta, activo=True)
    
    # Obtener subcarpetas activas
    subcarpetas = carpeta.get_subcarpetas_activas()
    
    # Filtros
    tipo = request.GET.get('tipo')
    if tipo:
        archivos = archivos.filter(tipo=tipo)
    
    context = {
        'carpeta': carpeta,
        'proyecto': carpeta.proyecto,
        'archivos': archivos,
        'subcarpetas': subcarpetas,
        'tipos': ArchivoProyecto.TIPO_CHOICES,
        'total_archivos': archivos.count(),
        'total_subcarpetas': subcarpetas.count(),
    }
    
    return render(request, 'core/archivos/carpeta_detail.html', context)