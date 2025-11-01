// Dashboard Charts - Gráficos profesionales para el dashboard

function initializeDashboardCharts(estadosProyectos, cantidadProyectos, categoriasGastos, montosGastos) {
    console.log('📊 Inicializando gráficos del dashboard...');
    
    // Gráfico de proyectos por estado
    initializeProyectosChart(estadosProyectos, cantidadProyectos);
    
    // Gráfico de gastos por categoría
    initializeGastosChart(categoriasGastos, montosGastos);
}

function initializeProyectosChart(estados, cantidades) {
    const chartCtx = document.getElementById('evolucionChart');
    if (!chartCtx) return;
    
    // Datos por defecto
    const labels = estados && estados.length > 0 ? estados : ['Sin datos'];
    const data = cantidades && cantidades.length > 0 ? cantidades : [0];
    
    new Chart(chartCtx.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: [
                    '#3b82f6',  // Azul - Planificación
                    '#10b981',  // Verde - En Progreso
                    '#f59e0b',  // Naranja - En Pausa
                    '#8b5cf6',  // Púrpura - Completado
                ],
                borderColor: '#ffffff',
                borderWidth: 3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12,
                            weight: '500'
                        },
                        color: '#1e293b',
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.9)',
                    titleColor: '#ffffff',
                    bodyColor: '#ffffff',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function initializeGastosChart(categorias, montos) {
    const chartCtx = document.getElementById('gastosChart');
    if (!chartCtx) return;
    
    // Datos por defecto
    const labels = categorias && categorias.length > 0 ? categorias : ['Sin datos'];
    const data = montos && montos.length > 0 ? montos : [0];
    
    new Chart(chartCtx.getContext('2d'), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Gastos ($)',
                data: data,
                backgroundColor: '#3b82f6',
                borderColor: '#2563eb',
                borderWidth: 0,
                borderRadius: 8,
                barThickness: 40
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
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            return '$' + context.parsed.y.toLocaleString('en-US', {
                                minimumFractionDigits: 2,
                                maximumFractionDigits: 2
                            });
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
                            weight: '500',
                            size: 11
                        },
                        color: '#64748b'
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)',
                        borderDash: [5, 5]
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + (value / 1000).toFixed(1) + 'K';
                        },
                        font: {
                            weight: '500',
                            size: 11
                        },
                        color: '#64748b'
                    }
                }
            }
        }
    });
}
