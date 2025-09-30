/**
 * Sistema de Notificaciones Toast - Sistema ARCA Construcción
 * Notificaciones elegantes que aparecen y desaparecen automáticamente
 */

class ToastNotification {
    constructor() {
        this.container = null;
        this.init();
    }

    init() {
        // Crear contenedor si no existe
        if (!document.querySelector('.toast-container')) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        } else {
            this.container = document.querySelector('.toast-container');
        }
    }

    /**
     * Mostrar notificación de éxito
     */
    success(title, message = '', duration = 4000) {
        this.show('success', 'fas fa-check-circle', title, message, duration);
    }

    /**
     * Mostrar notificación de error
     */
    error(title, message = '', duration = 5000) {
        this.show('error', 'fas fa-exclamation-circle', title, message, duration);
    }

    /**
     * Mostrar notificación de advertencia
     */
    warning(title, message = '', duration = 4500) {
        this.show('warning', 'fas fa-exclamation-triangle', title, message, duration);
    }

    /**
     * Mostrar notificación de información
     */
    info(title, message = '', duration = 4000) {
        this.show('info', 'fas fa-info-circle', title, message, duration);
    }

    /**
     * Mostrar notificación personalizada
     */
    show(type, icon, title, message, duration = 4000) {
        const toast = this.createToast(type, icon, title, message);
        this.container.appendChild(toast);

        // Trigger reflow para activar animación
        toast.offsetHeight;

        // Mostrar toast
        toast.classList.add('show', 'toast-slide-in');

        // Auto-remover después del tiempo especificado
        setTimeout(() => {
            this.hide(toast);
        }, duration);

        // Remover después de la animación
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, duration + 300);
    }

    /**
     * Crear elemento toast
     */
    createToast(type, icon, title, message) {
        const toast = document.createElement('div');
        toast.className = `toast-notification toast-${type}`;

        toast.innerHTML = `
            <div class="toast-icon">
                <i class="${icon}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                ${message ? `<div class="toast-message">${message}</div>` : ''}
            </div>
            <button class="toast-close" onclick="toastNotification.hide(this.parentNode)">
                <i class="fas fa-times"></i>
            </button>
        `;

        return toast;
    }

    /**
     * Ocultar toast
     */
    hide(toast) {
        toast.classList.remove('show');
        toast.classList.add('hide', 'toast-slide-out');
    }

    /**
     * Limpiar todas las notificaciones
     */
    clear() {
        const toasts = this.container.querySelectorAll('.toast-notification');
        toasts.forEach(toast => {
            this.hide(toast);
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        });
    }
}

// Instancia global
const toastNotification = new ToastNotification();

// Función global para usar desde Django
window.showToast = function(type, title, message, duration) {
    toastNotification[type](title, message, duration);
};

// Auto-inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Verificar si hay mensajes de Django para mostrar
    const messages = document.querySelectorAll('.alert');
    messages.forEach(alert => {
        const text = alert.textContent.trim();
        const type = alert.classList.contains('alert-success') ? 'success' :
                    alert.classList.contains('alert-danger') ? 'error' :
                    alert.classList.contains('alert-warning') ? 'warning' : 'info';
        
        // Extraer título y mensaje del texto
        let title, message;
        if (text.includes('!')) {
            const parts = text.split('!');
            title = parts[0] + '!';
            message = parts.slice(1).join('!').trim();
        } else {
            title = text;
            message = '';
        }
        
        // Mostrar toast
        toastNotification[type](title, message);
        
        // Ocultar alerta original
        alert.style.display = 'none';
    });
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ToastNotification;
}
