// Dashboard Charts - Gráficos profesionales para el dashboard

function initializeDashboardCharts(estadosProyectos, cantidadProyectos, categoriasGastos, montosGastos) {
    console.log('📊 Inicializando gráficos del dashboard...');
    
    // Ya NO inicializamos el gráfico de proyectos por estado (reemplazado por salud financiera)
    // initializeProyectosChart(estadosProyectos, cantidadProyectos);
    
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
    console.log('💼 Inicializando gráfico ejecutivo de gastos...');
    console.log('📊 Categorías:', categorias);
    console.log('💰 Montos:', montos);
    
    const container = document.getElementById('gastosTreemap');
    if (!container) {
        console.error('❌ No se encontró el contenedor gastosTreemap');
        return;
    }
    
    // Datos por defecto
    const labels = categorias && categorias.length > 0 ? categorias : ['Sin datos'];
    const data = montos && montos.length > 0 ? montos : [0];
    
    console.log('✅ Procesando datos...');
    
    // Limpiar contenedor
    container.innerHTML = '';
    
    // Si no hay datos
    if (data.length === 1 && data[0] === 0) {
        console.log('⚠️ No hay datos para mostrar');
        container.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #94a3b8; font-size: 1.1rem;"><i class="fas fa-chart-pie me-2"></i>No hay gastos registrados</div>';
        return;
    }
    
    console.log('✅ Generando cards con', data.length, 'categorías');
    
    // Calcular total
    const total = data.reduce((a, b) => a + b, 0);
    
    // Limitar a las TOP 6 categorías + "Otros"
    const MAX_CATEGORIAS = 6;
    let labelsFinales = [];
    let dataFinal = [];
    
    if (data.length > MAX_CATEGORIAS) {
        // Tomar las primeras 6
        labelsFinales = labels.slice(0, MAX_CATEGORIAS);
        dataFinal = data.slice(0, MAX_CATEGORIAS);
        
        // Agrupar el resto en "Otros"
        const otrosTotal = data.slice(MAX_CATEGORIAS).reduce((a, b) => a + b, 0);
        if (otrosTotal > 0) {
            labelsFinales.push('Otros');
            dataFinal.push(otrosTotal);
        }
        
        console.log(`📊 Agrupando ${data.length - MAX_CATEGORIAS} categorías en "Otros": $${otrosTotal.toFixed(2)}`);
    } else {
        labelsFinales = labels;
        dataFinal = data;
    }
    
    // Colores profesionales tipo Stripe/Notion
    const colors = [
        { primary: '#3b82f6', secondary: '#dbeafe', icon: 'fa-wallet' },
        { primary: '#10b981', secondary: '#d1fae5', icon: 'fa-coins' },
        { primary: '#f59e0b', secondary: '#fef3c7', icon: 'fa-shopping-cart' },
        { primary: '#ef4444', secondary: '#fee2e2', icon: 'fa-credit-card' },
        { primary: '#8b5cf6', secondary: '#ede9fe', icon: 'fa-receipt' },
        { primary: '#ec4899', secondary: '#fce7f3', icon: 'fa-money-bill' },
        { primary: '#64748b', secondary: '#f1f5f9', icon: 'fa-layer-group' }, // Color para "Otros"
    ];
    
    // Contenedor de cards
    const cardsContainer = document.createElement('div');
    cardsContainer.style.cssText = 'display: flex; flex-direction: column; gap: 0.85rem;';
    
    // Crear cada card con barra de progreso
    dataFinal.forEach((monto, index) => {
        const porcentaje = ((monto / total) * 100);
        const color = colors[index % colors.length];
        
        const card = document.createElement('div');
        card.style.cssText = `
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 1rem 1.25rem;
            transition: all 0.2s ease;
            cursor: pointer;
        `;
        
        card.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div style="width: 36px; height: 36px; background: ${color.secondary}; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: ${color.primary};">
                        <i class="fas ${color.icon}"></i>
                    </div>
                    <div>
                        <div style="font-size: 0.9rem; font-weight: 600; color: #1e293b; margin-bottom: 0.15rem;">
                            ${labelsFinales[index]}
                        </div>
                        <div style="font-size: 0.8rem; color: #64748b;">
                            ${porcentaje.toFixed(1)}% del total
                        </div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.3rem; font-weight: 700; color: ${color.primary};">
                        $${monto.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                    </div>
                </div>
            </div>
            <div style="width: 100%; height: 8px; background: #f1f5f9; border-radius: 4px; overflow: hidden;">
                <div style="width: ${porcentaje}%; height: 100%; background: linear-gradient(90deg, ${color.primary}, ${color.primary}dd); border-radius: 4px; transition: width 0.5s ease;"></div>
            </div>
        `;
        
        // Hover effect
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
            this.style.borderColor = color.primary;
            this.style.boxShadow = `0 4px 12px ${color.primary}30`;
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
            this.style.borderColor = '#e2e8f0';
            this.style.boxShadow = 'none';
        });
        
        cardsContainer.appendChild(card);
    });
    
    container.appendChild(cardsContainer);
    console.log('✅ Gráfico ejecutivo generado correctamente');
}

// Función alternativa con canvas treemap real (si necesitas)
function initializeGastosChartOLD(categorias, montos) {
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

// ===== NUEVAS FUNCIONES EJECUTIVAS =====

// 1. Salud Financiera de Proyectos (Semáforo)
function initializeSaludProyectos(proyectos) {
    console.log('💊 Inicializando salud financiera...');
    const container = document.getElementById('saludProyectos');
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!proyectos || proyectos.length === 0) {
        container.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 200px; color: #94a3b8;"><i class="fas fa-project-diagram me-2"></i>Sin proyectos</div>';
        return;
    }
    
    const cardsContainer = document.createElement('div');
    cardsContainer.style.cssText = 'display: flex; flex-direction: column; gap: 0.85rem;';
    
    proyectos.slice(0, 5).forEach(proyecto => {
        const rentabilidad = parseFloat(proyecto.rentabilidad) || 0;
        const ingresos = parseFloat(proyecto.ingresos) || 0;
        const margen = parseFloat(proyecto.margen) || 0;
        
        let estado, colorPrimary, colorSecondary, icono;
        if (margen >= 20) {
            estado = 'Excelente'; colorPrimary = '#10b981'; colorSecondary = '#d1fae5'; icono = 'fa-check-circle';
        } else if (margen >= 10) {
            estado = 'Bueno'; colorPrimary = '#3b82f6'; colorSecondary = '#dbeafe'; icono = 'fa-thumbs-up';
        } else if (margen >= 0) {
            estado = 'Aceptable'; colorPrimary = '#f59e0b'; colorSecondary = '#fef3c7'; icono = 'fa-exclamation-circle';
        } else {
            estado = 'Crítico'; colorPrimary = '#ef4444'; colorSecondary = '#fee2e2'; icono = 'fa-times-circle';
        }
        
        const card = document.createElement('div');
        card.style.cssText = `background: white; border-left: 4px solid ${colorPrimary}; border-radius: 8px; padding: 1rem; transition: all 0.2s; cursor: pointer; box-shadow: 0 1px 3px rgba(0,0,0,0.05);`;
        
        card.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                        <div style="width: 32px; height: 32px; background: ${colorSecondary}; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: ${colorPrimary};"><i class="fas ${icono}"></i></div>
                        <div><div style="font-size: 0.95rem; font-weight: 600; color: #1e293b;">${proyecto.nombre}</div><div style="font-size: 0.75rem; color: #64748b;">${proyecto.cliente}</div></div>
                    </div>
                    <div style="display: flex; gap: 1.5rem; margin-top: 0.75rem;">
                        <div><div style="font-size: 0.7rem; color: #64748b;">INGRESOS</div><div style="font-size: 0.9rem; font-weight: 600; color: #10b981;">$${ingresos.toFixed(2)}</div></div>
                        <div><div style="font-size: 0.7rem; color: #64748b;">RENTABILIDAD</div><div style="font-size: 0.9rem; font-weight: 700; color: ${colorPrimary};">$${rentabilidad.toFixed(2)}</div></div>
                        <div><div style="font-size: 0.7rem; color: #64748b;">MARGEN</div><div style="font-size: 0.9rem; font-weight: 600; color: ${colorPrimary};">${margen.toFixed(1)}%</div></div>
                    </div>
                </div>
                <div style="padding-left: 1rem;"><div style="padding: 0.5rem 1rem; background: ${colorSecondary}; color: ${colorPrimary}; border-radius: 8px; font-size: 0.8rem; font-weight: 600;">${estado}</div></div>
            </div>
        `;
        
        card.onmouseenter = () => { card.style.transform = 'translateX(4px)'; card.style.boxShadow = `0 4px 12px ${colorPrimary}30`; };
        card.onmouseleave = () => { card.style.transform = 'translateX(0)'; card.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)'; };
        
        cardsContainer.appendChild(card);
    });
    
    container.appendChild(cardsContainer);
}

// 2. Tendencia Financiera
function initializeTendenciaFinanciera(meses, ingresos, gastos) {
    console.log('📈 Inicializando tendencia...');
    const chartCtx = document.getElementById('tendenciaFinanciera');
    if (!chartCtx) return;
    
    const rentabilidad = ingresos.map((ing, i) => ing - gastos[i]);
    
    new Chart(chartCtx.getContext('2d'), {
        type: 'line',
        data: {
            labels: meses,
            datasets: [{
                label: 'Ingresos',
                data: ingresos,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16,185,129,0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }, {
                label: 'Gastos',
                data: gastos,
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239,68,68,0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }, {
                label: 'Rentabilidad',
                data: rentabilidad,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59,130,246,0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: true, position: 'top', align: 'end' },
                tooltip: {
                    callbacks: {
                        label: ctx => ctx.dataset.label + ': $' + ctx.parsed.y.toFixed(2)
                    }
                }
            },
            scales: {
                x: { grid: { display: false } },
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: v => v >= 1000 ? '$' + (v/1000).toFixed(1) + 'K' : '$' + v
                    }
                }
            }
        }
    });
}
