// Dashboard Charts - Manejo de gráficos del dashboard
function initializeDashboardCharts(evolucionData, categoriasGastos, montosGastos) {
    console.log('Inicializando gráficos del dashboard...');
    
    // Gráfico de evolución de proyectos
    initializeEvolucionChart(evolucionData);
    
    // Gráfico de gastos por categoría
    initializeGastosChart(categoriasGastos, montosGastos);
}

function initializeEvolucionChart(evolucionData) {
    const evolucionCtx = document.getElementById('evolucionChart');
    if (!evolucionCtx) {
        console.error('No se encontró el canvas evolucionChart');
        return;
    }
    
    // Datos por defecto si no hay datos
    const data = evolucionData && evolucionData.length > 0 ? evolucionData : [0, 0, 0, 0, 0];
    const labels = ['Planificación', 'Ejecución', 'Control', 'Cierre', 'Evaluación'];
    
    const evolucionCtx2d = evolucionCtx.getContext('2d');
    new Chart(evolucionCtx2d, {
        type: 'radar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Proyectos Activos',
                data: data,
                backgroundColor: 'rgba(37, 99, 235, 0.2)',
                borderColor: '#2563eb',
                borderWidth: 3,
                pointBackgroundColor: '#2563eb',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff'
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 100,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    },
                    ticks: {
                        stepSize: 20,
                        font: {
                            weight: '600'
                        },
                        color: '#2C3E50'
                    },
                    pointLabels: {
                        color: '#2C3E50',
                        font: {
                            weight: '600'
                        }
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

function initializeGastosChart(categoriasGastos, montosGastos) {
    const gastosCtx = document.getElementById('gastosChart');
    if (!gastosCtx) {
        console.error('No se encontró el canvas gastosChart');
        return;
    }
    
    // Datos por defecto si no hay datos
    const categorias = categoriasGastos && categoriasGastos.length > 0 ? categoriasGastos : ['Sin datos'];
    const montos = montosGastos && montosGastos.length > 0 ? montosGastos : [0];
    
    const gastosCtx2d = gastosCtx.getContext('2d');
    new Chart(gastosCtx2d, {
        type: 'bar',
        data: {
            labels: categorias,
            datasets: [{
                label: 'Gastos (Q)',
                data: montos,
                backgroundColor: [
                    '#6b7280',  // Gris suave
                    '#9ca3af',  // Gris claro
                    '#d1d5db',  // Gris muy claro
                    '#e5e7eb',  // Gris ultra claro
                    '#f3f4f6',  // Gris casi blanco
                    '#8b5cf6',  // Violeta suave
                    '#a78bfa',  // Violeta claro
                    '#c4b5fd',  // Violeta ultra claro
                    '#6366f1',  // Índigo suave
                    '#818cf8',  // Índigo claro
                    '#a5b4fc',  // Índigo ultra claro
                    '#3b82f6',  // Azul suave
                    '#60a5fa',  // Azul claro
                    '#93c5fd',  // Azul ultra claro
                    '#0ea5e9',  // Azul cielo suave
                    '#38bdf8',  // Azul cielo claro
                    '#7dd3fc',  // Azul cielo ultra claro
                    '#06b6d4',  // Cian suave
                    '#22d3ee',  // Cian claro
                    '#67e8f9',  // Cian ultra claro
                    '#10b981',  // Verde suave
                    '#34d399',  // Verde claro
                    '#6ee7b7',  // Verde ultra claro
                    '#84cc16',  // Verde lima suave
                    '#a3e635',  // Verde lima claro
                    '#bef264',  // Verde lima ultra claro
                    '#f59e0b',  // Ámbar suave
                    '#fbbf24',  // Ámbar claro
                    '#fcd34d',  // Ámbar ultra claro
                    '#f97316',  // Naranja suave
                    '#fb923c',  // Naranja claro
                    '#fdba74',  // Naranja ultra claro
                    '#ef4444',  // Rojo suave
                    '#f87171',  // Rojo claro
                    '#fca5a5'   // Rojo ultra claro
                ],
                borderColor: [
                    '#6b7280',  // Gris suave
                    '#9ca3af',  // Gris claro
                    '#d1d5db',  // Gris muy claro
                    '#e5e7eb',  // Gris ultra claro
                    '#f3f4f6',  // Gris casi blanco
                    '#8b5cf6',  // Violeta suave
                    '#a78bfa',  // Violeta claro
                    '#c4b5fd',  // Violeta ultra claro
                    '#6366f1',  // Índigo suave
                    '#818cf8',  // Índigo claro
                    '#a5b4fc',  // Índigo ultra claro
                    '#3b82f6',  // Azul suave
                    '#60a5fa',  // Azul claro
                    '#93c5fd',  // Azul ultra claro
                    '#0ea5e9',  // Azul cielo suave
                    '#38bdf8',  // Azul cielo claro
                    '#7dd3fc',  // Azul cielo ultra claro
                    '#06b6d4',  // Cian suave
                    '#22d3ee',  // Cian claro
                    '#67e8f9',  // Cian ultra claro
                    '#10b981',  // Verde suave
                    '#34d399',  // Verde claro
                    '#6ee7b7',  // Verde ultra claro
                    '#84cc16',  // Verde lima suave
                    '#a3e635',  // Verde lima claro
                    '#bef264',  // Verde lima ultra claro
                    '#f59e0b',  // Ámbar suave
                    '#fbbf24',  // Ámbar claro
                    '#fcd34d',  // Ámbar ultra claro
                    '#f97316',  // Naranja suave
                    '#fb923c',  // Naranja claro
                    '#fdba74',  // Naranja ultra claro
                    '#ef4444',  // Rojo suave
                    '#f87171',  // Rojo claro
                    '#fca5a5'   // Rojo ultra claro
                ],
                borderWidth: 2,
                borderRadius: 8,
                borderSkipped: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    callbacks: {
                        label: function(context) {
                            return 'Q' + context.parsed.y.toLocaleString();
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        font: {
                            weight: '600'
                        },
                        color: '#2C3E50'
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return 'Q' + (value / 1000) + 'K';
                        },
                        font: {
                            weight: '600'
                        },
                        color: '#2C3E50'
                    }
                }
            },
            animation: {
                duration: 2000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

// Función para inicializar cuando se carga la página
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard charts script cargado');
});
