// Sistema de sincronización offline
class OfflineSync {
    constructor() {
        this.pendingChanges = [];
        this.isOnline = navigator.onLine;
        this.init();
    }
    
    init() {
        // Escuchar cambios de conexión
        window.addEventListener('online', () => this.handleOnline());
        window.addEventListener('offline', () => this.handleOffline());
        
        // Verificar conexión cada 30 segundos
        setInterval(() => this.checkConnection(), 30000);
        
        // Cargar cambios pendientes
        this.loadPendingChanges();
    }
    
    // Manejar cuando se recupera la conexión
    handleOnline() {
        console.log('Conexión recuperada, sincronizando...');
        this.isOnline = true;
        this.syncPendingChanges();
        this.showNotification('Conexión recuperada', 'success');
    }
    
    // Manejar cuando se pierde la conexión
    handleOffline() {
        console.log('Conexión perdida, modo offline activado');
        this.isOnline = false;
        this.showNotification('Modo offline activado', 'warning');
    }
    
    // Verificar conexión
    checkConnection() {
        fetch('/api/health/', { method: 'HEAD' })
            .then(() => {
                if (!this.isOnline) {
                    this.handleOnline();
                }
            })
            .catch(() => {
                if (this.isOnline) {
                    this.handleOffline();
                }
            });
    }
    
    // Agregar cambio pendiente
    addPendingChange(change) {
        const pendingChange = {
            id: Date.now(),
            timestamp: new Date().toISOString(),
            ...change
        };
        
        this.pendingChanges.push(pendingChange);
        this.savePendingChanges();
        
        console.log('Cambio agregado a cola:', pendingChange);
    }
    
    // Sincronizar cambios pendientes
    async syncPendingChanges() {
        if (this.pendingChanges.length === 0) return;
        
        console.log(`Sincronizando ${this.pendingChanges.length} cambios pendientes...`);
        
        for (const change of this.pendingChanges) {
            try {
                await this.syncChange(change);
                this.removePendingChange(change.id);
            } catch (error) {
                console.error('Error sincronizando cambio:', error);
            }
        }
        
        this.savePendingChanges();
        this.updateLastSync();
    }
    
    // Sincronizar un cambio específico
    async syncChange(change) {
        const response = await fetch(change.url, {
            method: change.method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify(change.data)
        });
        
        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    // Guardar cambios pendientes en localStorage
    savePendingChanges() {
        localStorage.setItem('pendingChanges', JSON.stringify(this.pendingChanges));
    }
    
    // Cargar cambios pendientes desde localStorage
    loadPendingChanges() {
        const stored = localStorage.getItem('pendingChanges');
        if (stored) {
            this.pendingChanges = JSON.parse(stored);
        }
    }
    
    // Remover cambio pendiente
    removePendingChange(id) {
        this.pendingChanges = this.pendingChanges.filter(change => change.id !== id);
    }
    
    // Actualizar última sincronización
    updateLastSync() {
        localStorage.setItem('ultimaSincronizacion', new Date().toISOString());
    }
    
    // Obtener token CSRF
    getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
    
    // Mostrar notificación
    showNotification(message, type = 'info') {
        // Usar el sistema de notificaciones existente
        if (typeof showNotification === 'function') {
            showNotification(message, type);
        } else {
            console.log(`[${type.toUpperCase()}] ${message}`);
        }
    }
    
    // Obtener estado de sincronización
    getSyncStatus() {
        return {
            isOnline: this.isOnline,
            pendingChanges: this.pendingChanges.length,
            lastSync: localStorage.getItem('ultimaSincronizacion')
        };
    }
}

// Instanciar el sistema de sincronización
const offlineSync = new OfflineSync();

// Función para enviar datos offline
function sendOffline(url, method, data) {
    if (offlineSync.isOnline) {
        // Si hay conexión, enviar directamente
        return fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': offlineSync.getCSRFToken()
            },
            body: JSON.stringify(data)
        });
    } else {
        // Si no hay conexión, agregar a cola
        offlineSync.addPendingChange({ url, method, data });
        return Promise.resolve({ status: 'queued' });
    }
}

// Función para verificar estado de sincronización
function checkSyncStatus() {
    const status = offlineSync.getSyncStatus();
    console.log('Estado de sincronización:', status);
    return status;
}
