// ===== CALENDARIO SIMPLE Y FUNCIONAL =====
// Archivo completamente nuevo desde cero

class CalendarioSimple {
    constructor() {
        this.calendario = null;
        this.eventos = [];
        this.inicializado = false;
        console.log('🚀 CalendarioSimple creado');
    }

    // Inicializar el calendario
    inicializar() {
        console.log('🚀 Inicializando calendario...');
        
        try {
            // Verificar que FullCalendar esté disponible
            if (typeof FullCalendar === 'undefined') {
                throw new Error('FullCalendar no está disponible');
            }

            // Verificar elemento del calendario
            const calendarEl = document.getElementById('calendario');
            if (!calendarEl) {
                throw new Error('Elemento calendario no encontrado');
            }

            // Limpiar elemento
            calendarEl.innerHTML = '';

            // Obtener eventos del servidor
            this.eventos = this.obtenerEventosServidor();
            console.log('📅 Eventos obtenidos:', this.eventos);

            // Crear configuración
            const config = {
                initialView: 'dayGridMonth',
                locale: 'es',
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,listWeek'
                },
                buttonText: {
                    today: 'Hoy',
                    month: 'Mes',
                    week: 'Semana',
                    list: 'Lista'
                },
                height: 'auto',
                events: this.eventos,
                editable: false,
                selectable: true,
                weekends: true,
                firstDay: 1,
                businessHours: {
                    daysOfWeek: [1, 2, 3, 4, 5],
                    startTime: '08:00',
                    endTime: '18:00'
                },
                eventClick: (info) => this.mostrarDetalleEvento(info.event),
                select: (arg) => this.abrirModalEvento(arg.startStr),
                eventDidMount: (info) => this.personalizarEvento(info.event)
            };

            // Crear instancia
            this.calendario = new FullCalendar.Calendar(calendarEl, config);
            
            // Renderizar
            this.calendario.render();
            
            // Agregar eventos de prueba si no hay eventos
            if (this.eventos.length === 0) {
                this.agregarEventosPrueba();
            }

            this.inicializado = true;
            console.log('✅ Calendario inicializado correctamente');

        } catch (error) {
            console.error('❌ Error inicializando calendario:', error);
            this.mostrarError(error.message);
        }
    }

    // Obtener eventos del servidor Django
    obtenerEventosServidor() {
        try {
            // Buscar datos en el DOM
            const eventosScript = document.querySelector('script[data-eventos]');
            if (eventosScript) {
                const eventosData = eventosScript.getAttribute('data-eventos');
                if (eventosData && eventosData !== '[]' && eventosData !== 'None') {
                    return JSON.parse(eventosData);
                }
            }
            
            // Fallback: buscar en window.dashboardData
            if (window.dashboardData && window.dashboardData.eventos_calendario) {
                return window.dashboardData.eventos_calendario;
            }
            
            return [];
        } catch (e) {
            console.warn('⚠️ Error obteniendo eventos:', e);
            return [];
        }
    }

    // Personalizar apariencia de eventos
    personalizarEvento(evento) {
        const props = evento.extendedProps || {};
        
        // Aplicar clases CSS según tipo
        if (props.tipo === 'factura') {
            evento.setProp('classNames', ['evento-factura']);
        } else if (props.tipo === 'proyecto') {
            evento.setProp('classNames', ['evento-proyecto']);
        } else if (props.tipo === 'anticipo') {
            evento.setProp('classNames', ['evento-anticipo']);
        } else {
            evento.setProp('classNames', ['evento-personalizado']);
        }
    }

    // Agregar eventos de prueba
    agregarEventosPrueba() {
        if (!this.calendario) return;

        try {
            const hoy = new Date();
            const mañana = new Date(hoy);
            mañana.setDate(hoy.getDate() + 1);

            const eventosPrueba = [
                {
                    id: 'prueba_1',
                    title: 'Reunión de Proyecto',
                    start: hoy.toISOString().split('T')[0],
                    backgroundColor: '#2563eb',
                    extendedProps: { tipo: 'reunion', descripcion: 'Reunión semanal del equipo' }
                },
                {
                    id: 'prueba_2',
                    title: 'Visita a Obra',
                    start: mañana.toISOString().split('T')[0],
                    backgroundColor: '#28a745',
                    extendedProps: { tipo: 'visita', descripcion: 'Inspección de avance' }
                }
            ];

            eventosPrueba.forEach(evento => {
                this.calendario.addEvent(evento);
            });

            console.log('✅ Eventos de prueba agregados');
        } catch (e) {
            console.error('❌ Error agregando eventos de prueba:', e);
        }
    }

    // Mostrar detalle del evento
    mostrarDetalleEvento(evento) {
        if (!evento) return;

        const props = evento.extendedProps || {};
        let mensaje = `📅 ${evento.title || 'Sin título'}\n\n`;
        mensaje += `📆 Fecha: ${evento.startStr || 'Sin fecha'}\n`;
        
        if (props.tipo) mensaje += `🏷️ Tipo: ${props.tipo}\n`;
        if (props.descripcion) mensaje += `📝 Descripción: ${props.descripcion}\n`;
        if (props.cliente) mensaje += `👤 Cliente: ${props.cliente}\n`;
        if (props.monto) mensaje += `💰 Monto: Q${props.monto.toLocaleString()}\n`;

        alert(mensaje);
    }

    // Abrir modal para nuevo evento
    abrirModalEvento(fechaSeleccionada = null) {
        const modal = document.getElementById('modalEvento');
        if (!modal) {
            alert('Modal no disponible');
            return;
        }

        // Resetear formulario
        const form = document.getElementById('formEvento');
        if (form) form.reset();

        // Establecer fechas
        const fechaInicio = document.getElementById('fechaInicio');
        const fechaFin = document.getElementById('fechaFin');
        
        if (fechaInicio && fechaFin) {
            const ahora = new Date();
            const fechaInicioStr = fechaSeleccionada || ahora.toISOString().slice(0, 16);
            const fechaFinStr = fechaSeleccionada || new Date(ahora.getTime() + 60*60*1000).toISOString().slice(0, 16);
            
            fechaInicio.value = fechaInicioStr;
            fechaFin.value = fechaFinStr;
        }

        // Mostrar modal
        if (typeof bootstrap !== 'undefined') {
            new bootstrap.Modal(modal).show();
        } else {
            modal.style.display = 'block';
        }
    }

    // Guardar evento nuevo
    guardarEvento() {
        if (!this.calendario) {
            alert('Calendario no disponible');
            return;
        }

        const titulo = document.getElementById('tituloEvento')?.value?.trim();
        const tipo = document.getElementById('tipoEvento')?.value;
        const fechaInicio = document.getElementById('fechaInicio')?.value;
        const fechaFin = document.getElementById('fechaFin')?.value;
        const descripcion = document.getElementById('descripcionEvento')?.value?.trim();
        const color = document.getElementById('colorEvento')?.value || '#2563eb';

        if (!titulo || !tipo || !fechaInicio || !fechaFin) {
            alert('Complete todos los campos requeridos');
            return;
        }

        try {
            const nuevoEvento = {
                id: 'evento_' + Date.now(),
                title: titulo,
                start: fechaInicio,
                end: fechaFin,
                backgroundColor: color,
                extendedProps: {
                    tipo: tipo,
                    descripcion: descripcion
                }
            };

            this.calendario.addEvent(nuevoEvento);
            
            // Cerrar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalEvento'));
            if (modal) modal.hide();

            alert('✅ Evento agregado exitosamente');
            console.log('✅ Evento guardado:', nuevoEvento);

        } catch (e) {
            console.error('❌ Error guardando evento:', e);
            alert('❌ Error al guardar el evento');
        }
    }

    // Exportar calendario
    exportar() {
        if (!this.calendario) {
            alert('Calendario no disponible');
            return;
        }

        try {
            const eventos = this.calendario.getEvents();
            let contenido = '📅 Calendario de Eventos\n';
            contenido += '========================\n\n';
            contenido += `📊 Total eventos: ${eventos.length}\n`;
            contenido += `📅 Fecha de exportación: ${new Date().toLocaleDateString('es-ES')}\n\n`;

            eventos.forEach((evento, index) => {
                contenido += `Evento ${index + 1}:\n`;
                contenido += `  📝 Título: ${evento.title || 'Sin título'}\n`;
                contenido += `  📆 Fecha: ${evento.startStr || 'Sin fecha'}\n`;
                
                const props = evento.extendedProps || {};
                if (props.tipo) contenido += `  🏷️ Tipo: ${props.tipo}\n`;
                if (props.descripcion) contenido += `  📄 Descripción: ${props.descripcion}\n`;
                if (props.cliente) contenido += `  👤 Cliente: ${props.cliente}\n`;
                if (props.monto) contenido += `  💰 Monto: Q${props.monto.toLocaleString()}\n`;
                
                contenido += '  ---\n';
            });

            // Crear y descargar archivo
            const blob = new Blob([contenido], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `calendario_${new Date().toISOString().split('T')[0]}.txt`;
            a.click();
            URL.revokeObjectURL(url);

            alert('✅ Calendario exportado exitosamente');

        } catch (e) {
            console.error('❌ Error exportando:', e);
            alert('❌ Error al exportar el calendario');
        }
    }

    // Reinicializar calendario
    reinicializar() {
        console.log('🔄 Reinicializando calendario...');
        
        if (this.calendario) {
            try {
                this.calendario.destroy();
            } catch (e) {
                console.warn('⚠️ Error destruyendo calendario:', e);
            }
        }
        
        this.calendario = null;
        this.inicializado = false;
        
        setTimeout(() => {
            this.inicializar();
        }, 500);
    }

    // Debug del calendario
    debug() {
        console.log('🔍 DEBUG CALENDARIO:');
        console.log('  - FullCalendar disponible:', typeof FullCalendar !== 'undefined');
        console.log('  - Elemento calendario:', !!document.getElementById('calendario'));
        console.log('  - Instancia calendario:', !!this.calendario);
        console.log('  - Inicializado:', this.inicializado);
        console.log('  - Eventos en calendario:', this.calendario ? this.calendario.getEvents().length : 0);
        console.log('  - Eventos del servidor:', this.eventos.length);
    }

    // Mostrar error
    mostrarError(mensaje) {
        const calendarEl = document.getElementById('calendario');
        if (calendarEl) {
            calendarEl.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <h5><i class="fas fa-exclamation-triangle me-2"></i>Error del Calendario</h5>
                    <p>${mensaje}</p>
                    <button class="btn btn-primary btn-sm" onclick="calendarioApp.reinicializar()">
                        <i class="fas fa-redo me-1"></i>Reintentar
                    </button>
                </div>
            `;
        }
    }
}

// ===== INICIALIZACIÓN AUTOMÁTICA =====

// Crear instancia global
window.calendarioApp = new CalendarioSimple();

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM cargado, inicializando calendario...');
    
    // Esperar un poco para que FullCalendar se cargue
    setTimeout(() => {
        if (typeof FullCalendar !== 'undefined') {
            window.calendarioApp.inicializar();
        } else {
            console.error('❌ FullCalendar no disponible después del timeout');
        }
    }, 1000);
});

// Función global para reinicializar desde HTML
window.reinicializarCalendario = function() {
    if (window.calendarioApp) {
        window.calendarioApp.reinicializar();
    }
};

// Función global para debug desde HTML
window.debugCalendario = function() {
    if (window.calendarioApp) {
        window.calendarioApp.debug();
    }
};

console.log('✅ CalendarioSimple.js cargado correctamente');
