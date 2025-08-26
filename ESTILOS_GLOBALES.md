# 🎨 Sistema de Estilos Globales - Sistema de Construcción

Este documento explica cómo usar el sistema de estilos globales implementado para modernizar toda la interfaz del sistema de construcción.

## 📁 Archivos del Sistema

### 1. `static/css/global-styles.css`
Contiene todos los estilos CSS globales, variables y componentes reutilizables.

### 2. `static/js/global-functions.js`
Contiene funciones JavaScript globales para animaciones, validaciones y componentes de UI.

### 3. `templates/base.html`
Template base que incluye automáticamente los archivos globales.

## 🎯 Componentes Disponibles

### Hero Sections
```html
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">Título Principal</h1>
        <p class="hero-subtitle">Subtítulo descriptivo</p>
        
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-number">123</div>
                <div class="hero-stat-label">Etiqueta</div>
            </div>
        </div>
    </div>
</div>
```

### Contenedores de Formularios
```html
<div class="form-container">
    <div class="form-header">
        <div class="form-header-icon">
            <i class="fas fa-plus"></i>
        </div>
        <h3 class="form-header-title">Título del Formulario</h3>
    </div>
    
    <form>
        <div class="form-group">
            <label class="form-label">
                <i class="fas fa-user"></i>Campo
            </label>
            <input type="text" class="form-control">
            <div class="form-text">Texto de ayuda</div>
        </div>
        
        <div class="form-row">
            <div class="form-group">
                <!-- Campo 1 -->
            </div>
            <div class="form-group">
                <!-- Campo 2 -->
            </div>
        </div>
    </form>
</div>
```

### Tarjetas Modernas
```html
<div class="card-modern">
    <div class="card-header-modern">
        <div class="card-header-icon">
            <i class="fas fa-info"></i>
        </div>
        <h5 class="card-header-title">Título de la Tarjeta</h5>
    </div>
    <div class="p-3">
        <!-- Contenido de la tarjeta -->
    </div>
</div>
```

### Botones Estilizados
```html
<!-- Botones con gradientes -->
<button class="btn btn-primary">Botón Principal</button>
<button class="btn btn-success">Botón Éxito</button>
<button class="btn btn-warning">Botón Advertencia</button>
<button class="btn btn-danger">Botón Peligro</button>
<button class="btn btn-info">Botón Información</button>

<!-- Botón outline -->
<button class="btn btn-outline">Botón Outline</button>
```

### Sidebars Informativos
```html
<div class="info-sidebar">
    <div class="info-header">
        <div class="info-header-icon">
            <i class="fas fa-info-circle"></i>
        </div>
        <h4 class="info-header-title">Título del Sidebar</h4>
    </div>
    
    <div class="info-section info">
        <i class="fas fa-lightbulb"></i>
        <h6>Sección de Información</h6>
        <ul>
            <li>Elemento 1</li>
            <li>Elemento 2</li>
        </ul>
    </div>
</div>
```

### Grids de Información
```html
<div class="info-grid">
    <div class="info-card">
        <div class="info-card-header">
            <div class="info-card-icon">
                <i class="fas fa-chart"></i>
            </div>
            <h5 class="info-card-title">Título de la Tarjeta</h5>
        </div>
        <ul class="info-list">
            <li>
                <span class="info-label">Etiqueta:</span>
                <span class="info-value">Valor</span>
            </li>
        </ul>
    </div>
</div>
```

### Alertas Modernas
```html
<div class="alert-modern info">
    <h6><i class="fas fa-info-circle me-2"></i>Título de la Alerta</h6>
    <p>Mensaje de la alerta</p>
</div>

<div class="alert-modern success">
    <h6><i class="fas fa-check-circle me-2"></i>Éxito</h6>
    <p>Operación completada</p>
</div>

<div class="alert-modern warning">
    <h6><i class="fas fa-exclamation-triangle me-2"></i>Advertencia</h6>
    <p>Mensaje de advertencia</p>
</div>

<div class="alert-modern danger">
    <h6><i class="fas fa-times-circle me-2"></i>Error</h6>
    <p>Mensaje de error</p>
</div>
```

### Badges Modernos
```html
<span class="badge-modern success">Éxito</span>
<span class="badge-modern warning">Advertencia</span>
<span class="badge-modern danger">Peligro</span>
<span class="badge-modern info">Información</span>
```

### Timeline
```html
<div class="timeline">
    <div class="timeline-steps">
        <div class="timeline-step completed">
            <div class="timeline-step-number">
                <i class="fas fa-check"></i>
            </div>
            <div class="timeline-step-label">Completado</div>
        </div>
        <div class="timeline-step current">
            <div class="timeline-step-number">2</div>
            <div class="timeline-step-label">Actual</div>
        </div>
        <div class="timeline-step">
            <div class="timeline-step-number">3</div>
            <div class="timeline-step-label">Pendiente</div>
        </div>
    </div>
</div>
```

## 🎨 Variables CSS Disponibles

### Colores
```css
--azul-acero: #34495e
--azul-acero-claro: #5d6d7e
--amarillo-ocre: #f39c12
--amarillo-ocre-claro: #f7dc6f
--blanco-humo: #ecf0f1
--gris-concreto: #95a5a6
--gris-concreto-claro: #bdc3c7
```

### Colores de Estado
```css
--success: #27ae60
--success-light: #2ecc71
--warning: #f39c12
--warning-light: #f1c40f
--danger: #e74c3c
--danger-light: #c0392b
--info: #3498db
--info-light: #2980b9
```

### Sombras
```css
--shadow-sm: 0 2px 4px rgba(44, 62, 80, 0.1)
--shadow-md: 0 4px 15px rgba(44, 62, 80, 0.1)
--shadow-lg: 0 8px 30px rgba(44, 62, 80, 0.1)
--shadow-xl: 0 12px 40px rgba(44, 62, 80, 0.15)
```

### Bordes
```css
--border-radius-sm: 8px
--border-radius-md: 12px
--border-radius-lg: 16px
--border-radius-xl: 20px
```

### Transiciones
```css
--transition-fast: 0.2s ease
--transition-normal: 0.3s ease
--transition-slow: 0.5s ease
```

## 🚀 Funciones JavaScript Disponibles

### Animaciones
```javascript
// Animar elementos al cargar
SistemaConstruccion.animateElements('.mi-clase', 200);

// Aplicar efectos hover
SistemaConstruccion.applyHoverEffects('.mi-elemento');

// Aplicar efectos de clic
SistemaConstruccion.applyClickEffects('.mi-boton');
```

### Validación de Formularios
```javascript
// Validar un campo
SistemaConstruccion.validateField(input, validationElement, 'nombre', {
    required: true,
    minLength: 3,
    maxLength: 50
});

// Validar formulario completo
const validations = {
    nombre: { required: true, minLength: 3 },
    email: { required: true, pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/ }
};

SistemaConstruccion.applyRealTimeValidation(form, validations);
```

### Componentes de UI
```javascript
// Mostrar notificación toast
SistemaConstruccion.showToast('Mensaje de éxito', 'success', 3000);

// Mostrar modal de confirmación
SistemaConstruccion.showConfirmModal(
    'Confirmar Acción',
    '¿Estás seguro de que deseas continuar?',
    () => { /* Acción al confirmar */ },
    () => { /* Acción al cancelar */ }
);
```

### Utilidades
```javascript
// Formatear moneda
SistemaConstruccion.formatCurrency(1234.56, 'USD');

// Formatear fecha
SistemaConstruccion.formatDate(new Date(), 'dd/MM/yyyy');

// Debounce para optimizar eventos
const debouncedFunction = SistemaConstruccion.debounce(() => {
    // Función a ejecutar
}, 300);

// Throttle para limitar frecuencia
const throttledFunction = SistemaConstruccion.throttle(() => {
    // Función a ejecutar
}, 1000);
```

## 📱 Responsive Design

Todos los componentes están optimizados para dispositivos móviles y incluyen:

- Grids que se adaptan automáticamente
- Sidebars que se convierten en contenido normal en móviles
- Botones que se apilan verticalmente en pantallas pequeñas
- Timeline que se convierte en lista vertical en móviles

## 🎭 Clases de Animación

### Animaciones de Entrada
```html
<div class="animate-fade-in-up">Aparece desde abajo</div>
<div class="animate-slide-in-left">Aparece desde la izquierda</div>
<div class="animate-slide-in-right">Aparece desde la derecha</div>
```

### Efectos Hover
```html
<div class="shadow-hover">Sombra aumenta en hover</div>
<div class="transform-hover">Se eleva en hover</div>
```

## 🔧 Cómo Aplicar a Templates Existentes

### 1. Reemplazar Contenedores Básicos
```html
<!-- Antes -->
<div class="card">
    <div class="card-header">
        <h5>Título</h5>
    </div>
    <div class="card-body">
        Contenido
    </div>
</div>

<!-- Después -->
<div class="card-modern">
    <div class="card-header-modern">
        <div class="card-header-icon">
            <i class="fas fa-icon"></i>
        </div>
        <h5 class="card-header-title">Título</h5>
    </div>
    <div class="p-3">
        Contenido
    </div>
</div>
```

### 2. Reemplazar Botones
```html
<!-- Antes -->
<button class="btn btn-primary">Botón</button>

<!-- Después -->
<button class="btn btn-primary">
    <i class="fas fa-icon me-2"></i>Botón
</button>
```

### 3. Reemplazar Alertas
```html
<!-- Antes -->
<div class="alert alert-info">Mensaje</div>

<!-- Después -->
<div class="alert-modern info">
    <h6><i class="fas fa-info-circle me-2"></i>Título</h6>
    <p>Mensaje</p>
</div>
```

### 4. Agregar Hero Section
```html
<!-- Agregar al inicio del contenido -->
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">Título de la Página</h1>
        <p class="hero-subtitle">Descripción de la página</p>
        
        <div class="hero-stats">
            <!-- Estadísticas relevantes -->
        </div>
    </div>
</div>
```

## 📋 Checklist de Modernización

- [ ] Reemplazar `<div class="card">` por `<div class="card-modern">`
- [ ] Reemplazar `<div class="card-header">` por `<div class="card-header-modern">`
- [ ] Agregar iconos a los headers de tarjetas
- [ ] Reemplazar botones básicos por botones con iconos
- [ ] Reemplazar alertas básicas por alertas modernas
- [ ] Agregar hero section al inicio de la página
- [ ] Usar info-grid para información organizada
- [ ] Agregar info-sidebar para información contextual
- [ ] Implementar timeline para procesos
- [ ] Agregar animaciones de entrada
- [ ] Usar funciones JavaScript globales
- [ ] Verificar responsive design

## 🎯 Beneficios del Sistema

1. **Consistencia Visual**: Todos los módulos tienen el mismo estilo
2. **Mantenibilidad**: Cambios centralizados en un solo lugar
3. **Experiencia de Usuario**: Interfaz moderna y profesional
4. **Responsive**: Funciona perfectamente en todos los dispositivos
5. **Accesibilidad**: Colores contrastantes y navegación clara
6. **Performance**: CSS y JS optimizados y reutilizables

## 🚀 Próximos Pasos

1. Aplicar estos estilos a todos los templates existentes
2. Crear componentes adicionales según necesidades específicas
3. Implementar temas personalizables
4. Agregar más animaciones y transiciones
5. Optimizar para diferentes navegadores

---

**Nota**: Este sistema de estilos está diseñado para ser escalable y fácil de mantener. Cualquier modificación debe hacerse en los archivos globales para mantener la consistencia en todo el sistema.
