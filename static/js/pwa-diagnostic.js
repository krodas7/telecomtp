// Script de diagnóstico para PWA - Sistema ARCA Construcción
class PWADiagnostic {
    constructor() {
        this.results = {
            manifest: false,
            serviceWorker: false,
            https: false,
            installable: false,
            cache: false
        };
    }

    // Verificar si el manifest está cargado
    async checkManifest() {
        try {
            const manifestLink = document.querySelector('link[rel="manifest"]');
            if (!manifestLink) {
                console.error('❌ No se encontró el link al manifest');
                return false;
            }

            const response = await fetch(manifestLink.href);
            if (!response.ok) {
                console.error('❌ No se pudo cargar el manifest');
                return false;
            }

            const manifest = await response.json();
            console.log('✅ Manifest cargado:', manifest.name);
            
            // Verificar campos requeridos
            const requiredFields = ['name', 'short_name', 'start_url', 'display'];
            const missingFields = requiredFields.filter(field => !manifest[field]);
            
            if (missingFields.length > 0) {
                console.error('❌ Manifest incompleto. Campos faltantes:', missingFields);
                return false;
            }

            return true;
        } catch (error) {
            console.error('❌ Error verificando manifest:', error);
            return false;
        }
    }

    // Verificar Service Worker
    async checkServiceWorker() {
        if (!('serviceWorker' in navigator)) {
            console.error('❌ Service Worker no soportado');
            return false;
        }

        try {
            const registrations = await navigator.serviceWorker.getRegistrations();
            if (registrations.length === 0) {
                console.error('❌ No hay Service Workers registrados');
                return false;
            }

            console.log('✅ Service Workers registrados:', registrations.length);
            
            // Verificar que el SW esté activo
            const activeSW = registrations.find(reg => reg.active);
            if (!activeSW) {
                console.error('❌ No hay Service Worker activo');
                return false;
            }

            console.log('✅ Service Worker activo:', activeSW.scope);
            return true;
        } catch (error) {
            console.error('❌ Error verificando Service Worker:', error);
            return false;
        }
    }

    // Verificar HTTPS
    checkHTTPS() {
        const isHTTPS = window.location.protocol === 'https:' || window.location.hostname === 'localhost';
        if (!isHTTPS) {
            console.error('❌ HTTPS requerido para PWA');
            return false;
        }
        console.log('✅ HTTPS detectado');
        return true;
    }

    // Verificar si es instalable
    async checkInstallable() {
        if (!('BeforeInstallPromptEvent' in window)) {
            console.log('⚠️ BeforeInstallPromptEvent no soportado');
            return false;
        }

        // Escuchar el evento de instalación
        window.addEventListener('beforeinstallprompt', (e) => {
            console.log('✅ PWA es instalable');
            this.results.installable = true;
        });

        return true;
    }

    // Verificar cache
    async checkCache() {
        if (!('caches' in window)) {
            console.error('❌ Cache API no soportada');
            return false;
        }

        try {
            const cacheNames = await caches.keys();
            const arcaCaches = cacheNames.filter(name => name.includes('arca'));
            
            if (arcaCaches.length === 0) {
                console.error('❌ No se encontraron caches de ARCA');
                return false;
            }

            console.log('✅ Caches encontrados:', arcaCaches);
            return true;
        } catch (error) {
            console.error('❌ Error verificando cache:', error);
            return false;
        }
    }

    // Ejecutar diagnóstico completo
    async runDiagnostic() {
        console.log('🔍 Iniciando diagnóstico de PWA...');
        
        this.results.manifest = await this.checkManifest();
        this.results.serviceWorker = await this.checkServiceWorker();
        this.results.https = this.checkHTTPS();
        this.results.installable = await this.checkInstallable();
        this.results.cache = await this.checkCache();

        this.showResults();
    }

    // Mostrar resultados
    showResults() {
        console.log('\n📊 RESULTADOS DEL DIAGNÓSTICO PWA:');
        console.log('=====================================');
        
        Object.entries(this.results).forEach(([test, result]) => {
            const status = result ? '✅' : '❌';
            const testName = test.charAt(0).toUpperCase() + test.slice(1);
            console.log(`${status} ${testName}: ${result ? 'OK' : 'FALLO'}`);
        });

        const passedTests = Object.values(this.results).filter(Boolean).length;
        const totalTests = Object.keys(this.results).length;
        
        console.log(`\n📈 Resumen: ${passedTests}/${totalTests} pruebas pasadas`);
        
        if (passedTests === totalTests) {
            console.log('🎉 ¡PWA completamente funcional!');
        } else {
            console.log('⚠️ PWA necesita ajustes');
        }
    }
}

// Ejecutar diagnóstico cuando se cargue la página
document.addEventListener('DOMContentLoaded', () => {
    const diagnostic = new PWADiagnostic();
    diagnostic.runDiagnostic();
});

// Función global para ejecutar diagnóstico manualmente
window.runPWADiagnostic = function() {
    const diagnostic = new PWADiagnostic();
    diagnostic.runDiagnostic();
};
