// Script PWA Simple - Se ejecuta inmediatamente
console.log('🚀 PWA Simple iniciando...');

// Función para mostrar el botón de instalación
function mostrarBotonInstalacion() {
    const pwaButton = document.getElementById('pwaInstallBtn');
    const pwaInfo = document.getElementById('pwaInstallInfo');
    
    if (pwaButton && pwaInfo) {
        // Detectar si es dispositivo móvil
        const esMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        
        if (esMobile) {
            console.log('📱 Dispositivo móvil detectado, mostrando botón');
            pwaButton.style.display = 'inline-block';
            pwaInfo.style.display = 'none';
            
            // Agregar funcionalidad de instalación
            pwaButton.addEventListener('click', async () => {
                try {
                    // Intentar instalar usando la API nativa
                    if ('serviceWorker' in navigator) {
                        // Registrar service worker
                        const registration = await navigator.serviceWorker.register('/static/js/sw.js');
                        console.log('✅ Service Worker registrado');
                        
                        // Mostrar instrucciones de instalación
                        alert('📱 Para instalar la app:\n\n1. Toca el menú (3 puntos) en Chrome\n2. Selecciona "Instalar app" o "Add to Home Screen"\n\n¡La app se instalará en tu pantalla de inicio!');
                    }
                } catch (error) {
                    console.error('❌ Error:', error);
                    alert('📱 Para instalar:\n\n1. Menú (3 puntos) → "Instalar app"\n2. O "Add to Home Screen"');
                }
            });
            
        } else {
            console.log('💻 Dispositivo de escritorio detectado');
            pwaInfo.innerHTML = `
                <i class="fas fa-info-circle me-1"></i>
                Para instalar: Abre en Chrome móvil y busca "Instalar app" en el menú
            `;
        }
    } else {
        console.log('⚠️ Elementos PWA no encontrados');
    }
}

// Ejecutar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mostrarBotonInstalacion);
} else {
    mostrarBotonInstalacion();
}

console.log('✅ PWA Simple cargado');
