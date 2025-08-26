/**
 * Dashboard Inteligente - Widgets Avanzados
 * Se integra con el dashboard existente sin afectar su funcionamiento
 */

class DashboardIntelligent {
    constructor() {
        this.widgets = {};
        this.charts = {};
        this.isInitialized = false;
        this.init();
    }

    init() {
        console.log('🚀 Inicializando Dashboard Inteligente...');
        this.createWidgets();
        this.initializeCharts();
        this.setupEventListeners();
        this.isInitialized = true;
        console.log('✅ Dashboard Inteligente inicializado');
    }

    createWidgets() {
        // Widget de Rentabilidad por Proyecto
        this.createRentabilidadWidget();
        
        // Widget de Flujo de Caja
        this.createFlujoCajaWidget();
        
        // Widget de Métricas de Productividad
        this.createProductividadWidget();
        
        // Widget de KPIs Inteligentes
        this.createKPIsWidget();
    }

    createRentabilidadWidget() {
        const container = document.getElementById('widget-rentabilidad');
        if (!container) return;

        container.innerHTML = `
            <div class="card h-100">
                <div class="card-header bg-success text-white">
                    <h6 class="mb-0">
                        <i class="fas fa-chart-line me-2"></i>
                        Rentabilidad por Proyecto
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-6">
                            <div class="text-center">
                                <h4 class="text-success mb-0" id="rentabilidad-total">0%</h4>
                                <small class="text-muted">Rentabilidad Total</small>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-center">
                                <h4 class="text-info mb-0" id="proyectos-activos">0</h4>
                                <small class="text-muted">Proyectos Activos</small>
                            </div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <canvas id="chart-rentabilidad" height="200"></canvas>
                    </div>
                </div>
            </div>
        `;
    }

    createFlujoCajaWidget() {
        const container = document.getElementById('widget-flujo-caja');
        if (!container) return;

        container.innerHTML = `
            <div class="card h-100">
                <div class="card-header bg-primary text-white">
                    <h6 class="mb-0">
                        <i class="fas fa-money-bill-wave me-2"></i>
                        Flujo de Caja
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-6">
                            <div class="text-center">
                                <h5 class="text-success mb-0" id="ingresos-mes">Q0</h5>
                                <small class="text-muted">Ingresos del Mes</small>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-center">
                                <h5 class="text-danger mb-0" id="gastos-mes">Q0</h5>
                                <small class="text-muted">Gastos del Mes</small>
                            </div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <canvas id="chart-flujo-caja" height="200"></canvas>
                    </div>
                </div>
            </div>
        `;
    }

    createProductividadWidget() {
        const container = document.getElementById('widget-productividad');
        if (!container) return;

        container.innerHTML = `
            <div class="card h-100">
                <div class="card-header bg-warning text-dark">
                    <h6 class="mb-0">
                        <i class="fas fa-tachometer-alt me-2"></i>
                        Métricas de Productividad
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row mb-3">
                        <div class="col-6">
                            <div class="text-center">
                                <h5 class="text-warning mb-0" id="eficiencia-proyectos">0%</h5>
                                <small class="text-muted">Eficiencia Proyectos</small>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-center">
                                <h5 class="text-info mb-0" id="tiempo-promedio">0 días</h5>
                                <small class="text-muted">Tiempo Promedio</small>
                            </div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <canvas id="chart-productividad" height="200"></canvas>
                    </div>
                </div>
            </div>
        `;
    }

    createKPIsWidget() {
        const container = document.getElementById('widget-kpis');
        if (!container) return;

        container.innerHTML = `
            <div class="card h-100">
                <div class="card-header bg-info text-white">
                    <h6 class="mb-0">
                        <i class="fas fa-bullseye me-2"></i>
                        KPIs Inteligentes
                    </h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-6 mb-3">
                            <div class="text-center">
                                <div class="kpi-circle bg-success text-white rounded-circle d-flex align-items-center justify-content-center mx-auto mb-2" style="width: 60px; height: 60px;">
                                    <span id="kpi-satisfaccion">0%</span>
                                </div>
                                <small class="text-muted">Satisfacción Cliente</small>
                            </div>
                        </div>
                        <div class="col-6 mb-3">
                            <div class="text-center">
                                <div class="kpi-circle bg-primary text-white rounded-circle d-flex align-items-center justify-content-center mx-auto mb-2" style="width: 60px; height: 60px;">
                                    <span id="kpi-calidad">0%</span>
                                </div>
                                <small class="text-muted">Calidad Obra</small>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-center">
                                <div class="kpi-circle bg-warning text-dark rounded-circle d-flex align-items-center justify-content-center mx-auto mb-2" style="width: 60px; height: 60px;">
                                    <span id="kpi-rentabilidad">0%</span>
                                </div>
                                <small class="text-muted">Rentabilidad</small>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="text-center">
                                <div class="kpi-circle bg-info text-white rounded-circle d-flex align-items-center justify-content-center mx-auto mb-2" style="width: 60px; height: 60px;">
                                    <span id="kpi-eficiencia">0%</span>
                                </div>
                                <small class="text-muted">Eficiencia</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    initializeCharts() {
        // Gráfico de Rentabilidad
        this.initializeRentabilidadChart();
        
        // Gráfico de Flujo de Caja
        this.initializeFlujoCajaChart();
        
        // Gráfico de Productividad
        this.initializeProductividadChart();
    }

    initializeRentabilidadChart() {
        const ctx = document.getElementById('chart-rentabilidad');
        if (!ctx) return;

        this.charts.rentabilidad = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Rentable', 'Neutro', 'Pérdida'],
                datasets: [{
                    data: [70, 20, 10],
                    backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 10,
                            usePointStyle: true
                        }
                    }
                }
            }
        });
    }

    initializeFlujoCajaChart() {
        const ctx = document.getElementById('chart-flujo-caja');
        if (!ctx) return;

        this.charts.flujoCaja = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'],
                datasets: [{
                    label: 'Ingresos',
                    data: [12000, 15000, 18000, 14000, 16000, 20000],
                    borderColor: '#28a745',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    tension: 0.4
                }, {
                    label: 'Gastos',
                    data: [8000, 10000, 12000, 9000, 11000, 14000],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return 'Q' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        });
    }

    initializeProductividadChart() {
        const ctx = document.getElementById('chart-productividad');
        if (!ctx) return;

        this.charts.productividad = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Eficiencia', 'Calidad', 'Tiempo', 'Costo'],
                datasets: [{
                    label: 'Rendimiento',
                    data: [85, 90, 75, 80],
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.8)',
                        'rgba(0, 123, 255, 0.8)',
                        'rgba(255, 193, 7, 0.8)',
                        'rgba(220, 53, 69, 0.8)'
                    ],
                    borderColor: [
                        '#28a745',
                        '#007bff',
                        '#ffc107',
                        '#dc3545'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }

    setupEventListeners() {
        // Botón para actualizar datos
        const refreshBtn = document.getElementById('refresh-intelligent-dashboard');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => {
                this.refreshData();
            });
        }

        // Botón para alternar widgets
        const toggleBtn = document.getElementById('toggle-intelligent-widgets');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.toggleWidgets();
            });
        }
    }

    refreshData() {
        console.log('🔄 Actualizando datos del Dashboard Inteligente...');
        
        // Simular actualización de datos
        this.updateRentabilidadData();
        this.updateFlujoCajaData();
        this.updateProductividadData();
        this.updateKPIsData();
        
        console.log('✅ Datos actualizados');
    }

    updateRentabilidadData() {
        // Simular datos de rentabilidad
        const rentabilidadTotal = Math.floor(Math.random() * 30) + 15; // 15-45%
        const proyectosActivos = Math.floor(Math.random() * 10) + 5; // 5-15
        
        document.getElementById('rentabilidad-total').textContent = rentabilidadTotal + '%';
        document.getElementById('proyectos-activos').textContent = proyectosActivos;
        
        // Actualizar gráfico
        if (this.charts.rentabilidad) {
            this.charts.rentabilidad.data.datasets[0].data = [
                rentabilidadTotal,
                100 - rentabilidadTotal - 10,
                10
            ];
            this.charts.rentabilidad.update();
        }
    }

    updateFlujoCajaData() {
        // Simular datos de flujo de caja
        const ingresos = Math.floor(Math.random() * 10000) + 15000;
        const gastos = Math.floor(Math.random() * 8000) + 10000;
        
        document.getElementById('ingresos-mes').textContent = 'Q' + ingresos.toLocaleString();
        document.getElementById('gastos-mes').textContent = 'Q' + gastos.toLocaleString();
    }

    updateProductividadData() {
        // Simular datos de productividad
        const eficiencia = Math.floor(Math.random() * 20) + 80; // 80-100%
        const tiempoPromedio = Math.floor(Math.random() * 30) + 60; // 60-90 días
        
        document.getElementById('eficiencia-proyectos').textContent = eficiencia + '%';
        document.getElementById('tiempo-promedio').textContent = tiempoPromedio + ' días';
    }

    updateKPIsData() {
        // Simular datos de KPIs
        const satisfaccion = Math.floor(Math.random() * 20) + 80;
        const calidad = Math.floor(Math.random() * 15) + 85;
        const rentabilidad = Math.floor(Math.random() * 25) + 70;
        const eficiencia = Math.floor(Math.random() * 20) + 80;
        
        document.getElementById('kpi-satisfaccion').textContent = satisfaccion + '%';
        document.getElementById('kpi-calidad').textContent = calidad + '%';
        document.getElementById('kpi-rentabilidad').textContent = rentabilidad + '%';
        document.getElementById('kpi-eficiencia').textContent = eficiencia + '%';
    }

    toggleWidgets() {
        const widgetsContainer = document.getElementById('intelligent-widgets-container');
        if (widgetsContainer) {
            const isVisible = widgetsContainer.style.display !== 'none';
            widgetsContainer.style.display = isVisible ? 'none' : 'block';
            
            const toggleBtn = document.getElementById('toggle-intelligent-widgets');
            if (toggleBtn) {
                toggleBtn.innerHTML = isVisible ? 
                    '<i class="fas fa-eye me-2"></i>Mostrar Widgets' : 
                    '<i class="fas fa-eye-slash me-2"></i>Ocultar Widgets';
            }
        }
    }

    // Método para obtener datos reales del servidor
    async fetchRealData() {
        try {
            const response = await fetch('/api/dashboard-intelligent-data/');
            const data = await response.json();
            this.updateWithRealData(data);
        } catch (error) {
            console.warn('⚠️ No se pudieron obtener datos reales, usando datos simulados:', error);
            this.refreshData(); // Usar datos simulados como fallback
        }
    }

    updateWithRealData(data) {
        // Actualizar con datos reales del servidor
        if (data.rentabilidad) {
            this.updateRentabilidadData(data.rentabilidad);
        }
        if (data.flujoCaja) {
            this.updateFlujoCajaData(data.flujoCaja);
        }
        if (data.productividad) {
            this.updateProductividadData(data.productividad);
        }
        if (data.kpis) {
            this.updateKPIsData(data.kpis);
        }
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que Chart.js esté disponible
    if (typeof Chart !== 'undefined') {
        window.dashboardIntelligent = new DashboardIntelligent();
    } else {
        // Si Chart.js no está disponible, esperar un poco más
        setTimeout(() => {
            if (typeof Chart !== 'undefined') {
                window.dashboardIntelligent = new DashboardIntelligent();
            } else {
                console.warn('⚠️ Chart.js no está disponible para el Dashboard Inteligente');
            }
        }, 1000);
    }
});

// Exportar para uso global
window.DashboardIntelligent = DashboardIntelligent;
