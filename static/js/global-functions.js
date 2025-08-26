/**
 * SISTEMA ARCA CONSTRUCCIÓN - FUNCIONES GLOBALES
 * JavaScript esencial para el sidebar y funcionalidad básica
 */

// ========================================
// FUNCIONES DEL SIDEBAR
// ========================================

/**
 * Inicializa la funcionalidad del sidebar
 */
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggleMobile = document.getElementById('sidebarToggleMobile');
    
    if (!sidebar) {
        console.warn('❌ Sidebar no encontrado');
        return;
    }
    
    console.log('✅ Sidebar encontrado, inicializando...');
    
    // Toggle del sidebar en móviles
    if (sidebarToggleMobile) {
        sidebarToggleMobile.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            console.log('📱 Sidebar toggle:', sidebar.classList.contains('active'));
        });
    }
    
    // Cerrar sidebar al hacer clic en enlaces (móvil)
    const sidebarLinks = sidebar.querySelectorAll('a');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
                console.log('🔗 Sidebar cerrado por clic en enlace');
            }
        });
    });
    
    // Cerrar sidebar al hacer clic fuera (móvil)
    document.addEventListener('click', function(event) {
        if (window.innerWidth <= 768 && 
            !sidebar.contains(event.target) && 
            !sidebarToggleMobile.contains(event.target)) {
            sidebar.classList.remove('active');
        }
    });
    
    console.log('✅ Sidebar inicializado correctamente');
}

/**
 * Inicializa el menú de usuario
 */
function initializeUserMenu() {
    const userMenu = document.querySelector('.user-menu');
    const userDropdown = document.querySelector('.user-dropdown');
    
    if (!userMenu || !userDropdown) {
        console.warn('❌ Menú de usuario no encontrado');
        return;
    }
    
    console.log('✅ Menú de usuario encontrado, inicializando...');
    
    // Mostrar dropdown al hacer hover
    userMenu.addEventListener('mouseenter', function() {
        userDropdown.style.opacity = '1';
        userDropdown.style.visibility = 'visible';
        userDropdown.style.transform = 'translateY(0)';
    });
    
    // Ocultar dropdown al salir del menú
    userMenu.addEventListener('mouseleave', function() {
        userDropdown.style.opacity = '0';
        userDropdown.style.visibility = 'hidden';
        userDropdown.style.transform = 'translateY(-15px)';
    });
    
    console.log('✅ Menú de usuario inicializado correctamente');
}

// ========================================
// FUNCIONES DE UTILIDAD
// ========================================

/**
 * Muestra un mensaje de debug en la consola
 */
function debug(message, data = null) {
    const timestamp = new Date().toLocaleTimeString();
    if (data) {
        console.log(`[${timestamp}] ${message}`, data);
    } else {
        console.log(`[${timestamp}] ${message}`);
    }
}

/**
 * Verifica que todos los elementos necesarios estén presentes
 */
function verifyElements() {
    const elements = {
        sidebar: document.getElementById('sidebar'),
        mainContent: document.getElementById('mainContent'),
        sidebarToggleMobile: document.getElementById('sidebarToggleMobile'),
        userMenu: document.querySelector('.user-menu'),
        userDropdown: document.querySelector('.user-dropdown')
    };
    
    console.log('🔍 Verificación de elementos del sistema:');
    Object.entries(elements).forEach(([name, element]) => {
        if (element) {
            console.log(`✅ ${name}: Presente`);
        } else {
            console.warn(`❌ ${name}: No encontrado`);
        }
    });
    
    return elements;
}

/**
 * Verifica el estado de la página actual
 */
function checkPageStatus() {
    console.log('📄 Estado de la página actual:');
    console.log('   URL:', window.location.href);
    console.log('   Título:', document.title);
    console.log('   Usuario:', document.querySelector('.user-name')?.textContent || 'No identificado');
    console.log('   Ancho de pantalla:', window.innerWidth);
    console.log('   Sidebar visible:', !document.getElementById('sidebar')?.classList.contains('active'));
}

// ========================================
// FUNCIONES DE NAVEGACIÓN
// ========================================

/**
 * Navega a una URL específica
 */
function navigateTo(url) {
    console.log('🧭 Navegando a:', url);
    window.location.href = url;
}

/**
 * Recarga la página actual
 */
function reloadPage() {
    console.log('🔄 Recargando página...');
    window.location.reload();
}

// ========================================
// FUNCIONES DE UI
// ========================================

/**
 * Muestra un mensaje de éxito
 */
function showSuccess(message) {
    console.log('✅ Éxito:', message);
    // Aquí podrías implementar un toast o notificación
}

/**
 * Muestra un mensaje de error
 */
function showError(message) {
    console.error('❌ Error:', message);
    // Aquí podrías implementar un toast o notificación
}

/**
 * Muestra un mensaje de información
 */
function showInfo(message) {
    console.log('ℹ️ Info:', message);
    // Aquí podrías implementar un toast o notificación
}

// ========================================
// INICIALIZACIÓN AL CARGAR LA PÁGINA
// ========================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Sistema ARCA Construcción iniciando...');
    
    // Verificar elementos
    const elements = verifyElements();
    
    // Inicializar funcionalidades
    initializeSidebar();
    initializeUserMenu();
    
    // Verificar estado de la página
    checkPageStatus();
    
    // Debug: información adicional
    console.log('📊 Información del sistema:');
    console.log('   Django funcionando:', typeof Django !== 'undefined');
    console.log('   Bootstrap disponible:', typeof bootstrap !== 'undefined');
    console.log('   FontAwesome disponible:', document.querySelector('.fas') !== null);
    
    console.log('✅ Sistema ARCA Construcción inicializado completamente');
});

// ========================================
// FUNCIONES GLOBALES
// ========================================

// Hacer funciones disponibles globalmente
window.SistemaConstruccion = {
    // Funciones principales
    initializeSidebar,
    initializeUserMenu,
    
    // Utilidades
    debug,
    verifyElements,
    checkPageStatus,
    
    // Navegación
    navigateTo,
    reloadPage,
    
    // UI
    showSuccess,
    showError,
    showInfo
};

// ========================================
// FUNCIONES DE DESARROLLO
// ========================================

/**
 * Función para desarrollo - muestra información del sistema
 */
function systemInfo() {
    console.log('🏗️ SISTEMA ARCA CONSTRUCCIÓN - INFORMACIÓN COMPLETA');
    console.log('==================================================');
    console.log('Versión:', '1.0.0');
    console.log('Fecha:', new Date().toLocaleDateString());
    console.log('Hora:', new Date().toLocaleTimeString());
    console.log('URL:', window.location.href);
    console.log('Usuario:', document.querySelector('.user-name')?.textContent || 'No identificado');
    console.log('Sidebar:', document.getElementById('sidebar') ? 'Presente' : 'No encontrado');
    console.log('Contenido principal:', document.getElementById('mainContent') ? 'Presente' : 'No encontrado');
    console.log('==================================================');
}

// Ejecutar información del sistema en desarrollo
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    setTimeout(systemInfo, 1000);
}
