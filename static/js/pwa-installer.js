// PROTECCIÓN CONTRA DECLARACIONES MÚLTIPLES
if (typeof window.PWAInstaller === 'undefined') {
    class PWAInstaller {
    constructor() {
        this.deferredPrompt = null;
        this.installButton = null;
        this.isInstalled = false;
        this.init();
    }

    init() {
        console.log('🚀 Inicializando PWA Installer...');
        
        // Registrar service worker
        this.registerServiceWorker();
        
        // Escuchar eventos de instalación
        this.setupInstallListeners();
        
        // Verificar si ya está instalado
        this.checkInstallationStatus();
        
        // Configurar funcionalidades móviles
        this.setupMobileFeatures();
        
        // Mostrar botón automáticamente en móvil
        this.showInstallButtonOnMobile();
    }
    
    // NUEVO: Mostrar botón automáticamente en móvil
    showInstallButtonOnMobile() {
        if (this.isMobileDevice()) {
            console.log('📱 Dispositivo móvil detectado, mostrando botón de instalación');
            // En móvil, mostrar el botón automáticamente
            this.showInstallButton();
        } else {
            console.log('💻 Dispositivo de escritorio detectado');
            // En escritorio, mostrar instrucciones
            this.showDesktopInstructions();
        }
    }
    
    // NUEVO: Mostrar instrucciones para escritorio
    showDesktopInstructions() {
        const pwaInfo = document.getElementById('pwaInstallInfo');
        if (pwaInfo) {
            pwaInfo.innerHTML = `
                <i class="fas fa-info-circle me-1"></i>
                Para instalar: Abre en Chrome móvil y busca "Instalar app" en el menú
            `;
        }
    }

    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/static/js/sw.js');
                console.log('✅ Service Worker registrado:', registration);
                
                // Escuchar actualizaciones
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            this.showUpdateNotification();
                        }
                    });
                });
            } catch (error) {
                console.error('❌ Error registrando Service Worker:', error);
            }
        }
    }

    setupInstallListeners() {
        // Escuchar el evento beforeinstallprompt
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('📱 Evento de instalación detectado');
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallButton();
        });

        // Escuchar cuando se instala la PWA
        window.addEventListener('appinstalled', () => {
            console.log('✅ PWA instalada exitosamente');
            this.isInstalled = true;
            this.hideInstallButton();
            this.showInstallationSuccess();
        });
    }

    showInstallButton() {
        // Mostrar botón en el dashboard
        const pwaButton = document.getElementById('pwaInstallBtn');
        const pwaInfo = document.getElementById('pwaInstallInfo');
        
        if (pwaButton && pwaInfo) {
            pwaButton.style.display = 'inline-block';
            pwaInfo.style.display = 'none';
            
            // Remover event listeners anteriores para evitar duplicados
            pwaButton.removeEventListener('click', this.installPWA.bind(this));
            pwaButton.addEventListener('click', () => this.installPWA());
            
            console.log('✅ Botón de instalación PWA mostrado en dashboard');
        } else {
            console.log('⚠️ No se encontró el botón PWA en el dashboard');
        }
    }

    hideInstallButton() {
        const pwaButton = document.getElementById('pwaInstallBtn');
        const pwaInfo = document.getElementById('pwaInstallInfo');
        
        if (pwaButton && pwaInfo) {
            pwaButton.style.display = 'none';
            pwaInfo.style.display = 'block';
        }
    }

    async installPWA() {
        if (!this.deferredPrompt) {
            console.log('❌ No hay prompt de instalación disponible');
            return;
        }

        try {
            console.log('📱 Iniciando instalación...');
            this.deferredPrompt.prompt();
            
            const { outcome } = await this.deferredPrompt.userChoice;
            console.log('📱 Resultado de instalación:', outcome);
            
            if (outcome === 'accepted') {
                this.showInstallationSuccess();
            }
            
            this.deferredPrompt = null;
            this.hideInstallButton();
        } catch (error) {
            console.error('❌ Error durante la instalación:', error);
        }
    }

    showInstallationSuccess() {
        const toast = document.createElement('div');
        toast.className = 'toast position-fixed';
        toast.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
        `;
        toast.innerHTML = `
            <div class="toast-header bg-success text-white">
                <i class="fas fa-check-circle me-2"></i>
                <strong class="me-auto">¡Instalado!</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                La app se ha instalado correctamente en tu dispositivo.
            </div>
        `;
        
        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Remover después de 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    showUpdateNotification() {
        const updateNotification = document.createElement('div');
        updateNotification.className = 'alert alert-info alert-dismissible fade show position-fixed';
        updateNotification.style.cssText = `
            top: 20px;
            left: 20px;
            right: 20px;
            z-index: 9999;
        `;
        updateNotification.innerHTML = `
            <i class="fas fa-sync-alt me-2"></i>
            <strong>Nueva versión disponible</strong>
            <br>
            <small>Haz clic en "Actualizar" para obtener la última versión.</small>
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            <div class="mt-2">
                <button class="btn btn-primary btn-sm" onclick="location.reload()">
                    <i class="fas fa-sync-alt me-1"></i>Actualizar
                </button>
            </div>
        `;
        
        document.body.appendChild(updateNotification);
        
        // Auto-remover después de 10 segundos
        setTimeout(() => {
            if (updateNotification.parentNode) {
                updateNotification.parentNode.removeChild(updateNotification);
            }
        }, 10000);
    }

    checkInstallationStatus() {
        // Verificar si está en modo standalone (instalado)
        if (window.matchMedia('(display-mode: standalone)').matches || 
            window.navigator.standalone === true) {
            this.isInstalled = true;
            console.log('✅ PWA ya está instalada');
        }
    }

    setupMobileFeatures() {
        // Detectar si es dispositivo móvil
        if (this.isMobileDevice()) {
            console.log('📱 Dispositivo móvil detectado');
            this.enableMobileFeatures();
        }
    }

    isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }

    enableMobileFeatures() {
        // Añadir clase CSS para móvil
        document.body.classList.add('mobile-device');
        
        // Configurar viewport para móvil
        this.setupMobileViewport();
        
        // Habilitar gestos táctiles
        this.enableTouchGestures();
        
        // Configurar notificaciones push
        this.setupPushNotifications();
    }

    setupMobileViewport() {
        const viewport = document.querySelector('meta[name="viewport"]');
        if (viewport) {
            viewport.setAttribute('content', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no');
        }
    }

    enableTouchGestures() {
        let startX = 0;
        let startY = 0;
        let endX = 0;
        let endY = 0;

        document.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
            startY = e.touches[0].clientY;
        });

        document.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            endY = e.changedTouches[0].clientY;
            this.handleSwipe();
        });

        // Gestos de swipe para navegación
        document.addEventListener('swipeleft', () => {
            console.log('👈 Swipe izquierda detectado');
        });

        document.addEventListener('swiperight', () => {
            console.log('👉 Swipe derecha detectado');
        });
    }

    handleSwipe() {
        const diffX = startX - endX;
        const diffY = startY - endY;
        const minSwipeDistance = 50;

        if (Math.abs(diffX) > Math.abs(diffY) && Math.abs(diffX) > minSwipeDistance) {
            if (diffX > 0) {
                // Swipe izquierda
                console.log('👈 Swipe izquierda');
            } else {
                // Swipe derecha
                console.log('👉 Swipe derecha');
            }
        }
    }

    async setupPushNotifications() {
        if ('Notification' in window && 'serviceWorker' in navigator) {
            try {
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    console.log('✅ Notificaciones push habilitadas');
                }
            } catch (error) {
                console.log('❌ Error configurando notificaciones:', error);
            }
        }
    }

    // Método para mostrar estado de conexión
    showConnectionStatus() {
        const status = document.createElement('div');
        status.id = 'connection-status';
        status.className = 'position-fixed';
        status.style.cssText = `
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        `;

        if (navigator.onLine) {
            status.className += ' bg-success text-white';
            status.innerHTML = '<i class="fas fa-wifi me-1"></i>En línea';
        } else {
            status.className += ' bg-warning text-dark';
            status.innerHTML = '<i class="fas fa-exclamation-triangle me-1"></i>Sin conexión';
        }

        document.body.appendChild(status);

        // Remover después de 3 segundos
        setTimeout(() => {
            if (status.parentNode) {
                status.parentNode.removeChild(status);
            }
        }, 3000);
    }
}



        // Inicializar solo una vez
        if (!window.pwaInstallerInitialized) {
            window.pwaInstallerInitialized = true;
            
            document.addEventListener('DOMContentLoaded', () => {
                if (!window.pwaInstaller) {
                    window.pwaInstaller = new PWAInstaller();
                    
                    // Eventos de conexión
                    window.addEventListener('online', () => {
                        if (window.pwaInstaller) {
                            window.pwaInstaller.showConnectionStatus();
                        }
                    });
                    
                    window.addEventListener('offline', () => {
                        if (window.pwaInstaller) {
                            window.pwaInstaller.showConnectionStatus();
                        }
                    });
                }
            });
        }
    } else {
        console.log('⚠️ PWAInstaller ya está definido, saltando inicialización...');
    }
