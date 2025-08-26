class FotosMovil {
    constructor() {
        this.camera = null;
        this.currentPhoto = null;
        this.geolocation = null;
        this.init();
    }

    init() {
        console.log('📸 Inicializando sistema de fotos móvil...');
        
        // Verificar capacidades del dispositivo
        this.checkDeviceCapabilities();
        
        // Configurar geolocalización
        this.setupGeolocation();
        
        // Crear interfaz de fotos
        this.createPhotoInterface();
        
        // Configurar eventos
        this.setupEventListeners();
    }

    checkDeviceCapabilities() {
        // Verificar si es dispositivo móvil
        if (!this.isMobileDevice()) {
            console.log('⚠️ No es dispositivo móvil, algunas funciones pueden no estar disponibles');
            return;
        }

        // Verificar acceso a cámara
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            console.log('✅ Cámara disponible');
        } else {
            console.log('❌ Cámara no disponible');
        }

        // Verificar geolocalización
        if ('geolocation' in navigator) {
            console.log('✅ Geolocalización disponible');
        } else {
            console.log('❌ Geolocalización no disponible');
        }
    }

    isMobileDevice() {
        return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) ||
               window.innerWidth <= 768;
    }

    setupGeolocation() {
        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.geolocation = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy
                    };
                    console.log('📍 Ubicación obtenida:', this.geolocation);
                },
                (error) => {
                    console.error('❌ Error obteniendo ubicación:', error);
                },
                {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 60000
                }
            );
        }
    }

    createPhotoInterface() {
        // Crear botón flotante para fotos
        const photoButton = document.createElement('button');
        photoButton.id = 'mobile-photo-btn';
        photoButton.className = 'btn btn-success position-fixed';
        photoButton.style.cssText = `
            bottom: 80px;
            right: 20px;
            z-index: 9999;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-size: 24px;
        `;
        photoButton.innerHTML = '<i class="fas fa-camera"></i>';
        photoButton.title = 'Tomar Foto';
        
        photoButton.addEventListener('click', () => this.openPhotoModal());
        document.body.appendChild(photoButton);

        // Crear modal para fotos
        this.createPhotoModal();
    }

    createPhotoModal() {
        const modal = document.createElement('div');
        modal.id = 'photo-modal';
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-camera me-2"></i>Documentación de Obra
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="camera-container mb-3">
                                    <video id="camera-preview" autoplay playsinline style="width: 100%; border-radius: 8px;"></video>
                                    <canvas id="photo-canvas" style="display: none;"></canvas>
                                </div>
                                <div class="camera-controls text-center">
                                    <button class="btn btn-primary btn-lg me-2" id="capture-btn">
                                        <i class="fas fa-camera me-2"></i>Capturar
                                    </button>
                                    <button class="btn btn-secondary btn-lg" id="switch-camera-btn">
                                        <i class="fas fa-sync-alt me-2"></i>Cambiar
                                    </button>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="photo-form">
                                    <div class="mb-3">
                                        <label class="form-label">Tipo de Documentación</label>
                                        <select class="form-select" id="photo-type">
                                            <option value="progreso">Progreso de Obra</option>
                                            <option value="calidad">Control de Calidad</option>
                                            <option value="seguridad">Seguridad</option>
                                            <option value="incidente">Incidente/Problema</option>
                                            <option value="materiales">Materiales</option>
                                            <option value="equipos">Equipos</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Descripción</label>
                                        <textarea class="form-control" id="photo-description" rows="3" placeholder="Describe lo que se ve en la foto..."></textarea>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Proyecto</label>
                                        <select class="form-select" id="photo-project">
                                            <option value="">Seleccionar proyecto...</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Ubicación en Obra</label>
                                        <input type="text" class="form-control" id="photo-location" placeholder="Ej: Planta baja, Fachada norte...">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Prioridad</label>
                                        <select class="form-select" id="photo-priority">
                                            <option value="baja">Baja</option>
                                            <option value="media">Media</option>
                                            <option value="alta">Alta</option>
                                            <option value="urgente">Urgente</option>
                                        </select>
                                    </div>
                                    <div class="location-info mb-3">
                                        <small class="text-muted">
                                            <i class="fas fa-map-marker-alt me-1"></i>
                                            <span id="current-location">Obteniendo ubicación...</span>
                                        </small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-success" id="save-photo-btn" disabled>
                            <i class="fas fa-save me-2"></i>Guardar Foto
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
    }

    setupEventListeners() {
        // Evento para abrir modal
        document.addEventListener('click', (e) => {
            if (e.target.id === 'mobile-photo-btn') {
                this.openPhotoModal();
            }
        });

        // Eventos del modal
        document.addEventListener('click', (e) => {
            if (e.target.id === 'capture-btn') {
                this.capturePhoto();
            } else if (e.target.id === 'switch-camera-btn') {
                this.switchCamera();
            } else if (e.target.id === 'save-photo-btn') {
                this.savePhoto();
            }
        });
    }

    async openPhotoModal() {
        const modal = document.getElementById('photo-modal');
        const bsModal = new bootstrap.Modal(modal);
        
        // Cargar proyectos
        await this.loadProjects();
        
        // Iniciar cámara
        await this.startCamera();
        
        // Mostrar modal
        bsModal.show();
        
        // Actualizar ubicación
        this.updateLocationDisplay();
    }

    async startCamera() {
        try {
            const constraints = {
                video: {
                    facingMode: 'environment', // Cámara trasera
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            };

            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            const video = document.getElementById('camera-preview');
            video.srcObject = stream;
            this.camera = stream;
            
            console.log('📸 Cámara iniciada');
        } catch (error) {
            console.error('❌ Error iniciando cámara:', error);
            this.showCameraError();
        }
    }

    async switchCamera() {
        if (this.camera) {
            this.camera.getTracks().forEach(track => track.stop());
        }

        try {
            const constraints = {
                video: {
                    facingMode: this.camera && this.camera.getVideoTracks()[0]?.getSettings().facingMode === 'user' ? 'environment' : 'user'
                }
            };

            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            const video = document.getElementById('camera-preview');
            video.srcObject = stream;
            this.camera = stream;
            
            console.log('📸 Cámara cambiada');
        } catch (error) {
            console.error('❌ Error cambiando cámara:', error);
        }
    }

    capturePhoto() {
        const video = document.getElementById('camera-preview');
        const canvas = document.getElementById('photo-canvas');
        const context = canvas.getContext('2d');

        // Configurar canvas
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        // Capturar frame
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Obtener imagen como blob
        canvas.toBlob((blob) => {
            this.currentPhoto = blob;
            this.showPhotoPreview();
            this.enableSaveButton();
        }, 'image/jpeg', 0.8);

        console.log('📸 Foto capturada');
    }

    showPhotoPreview() {
        const video = document.getElementById('camera-preview');
        const canvas = document.getElementById('photo-canvas');
        
        // Ocultar video y mostrar canvas
        video.style.display = 'none';
        canvas.style.display = 'block';
        
        // Mostrar mensaje de éxito
        this.showMessage('✅ Foto capturada correctamente', 'success');
    }

    enableSaveButton() {
        const saveBtn = document.getElementById('save-photo-btn');
        saveBtn.disabled = false;
        saveBtn.classList.remove('btn-secondary');
        saveBtn.classList.add('btn-success');
    }

    async loadProjects() {
        try {
            // Aquí cargarías los proyectos desde la API
            const projects = [
                { id: 1, name: 'Edificio Residencial Centro' },
                { id: 2, name: 'Centro Comercial Plaza Mayor' },
                { id: 3, name: 'Hospital Regional Norte' }
            ];

            const select = document.getElementById('photo-project');
            select.innerHTML = '<option value="">Seleccionar proyecto...</option>';
            
            projects.forEach(project => {
                const option = document.createElement('option');
                option.value = project.id;
                option.textContent = project.name;
                select.appendChild(option);
            });
        } catch (error) {
            console.error('❌ Error cargando proyectos:', error);
        }
    }

    updateLocationDisplay() {
        const locationSpan = document.getElementById('current-location');
        
        if (this.geolocation) {
            locationSpan.textContent = `${this.geolocation.latitude.toFixed(6)}, ${this.geolocation.longitude.toFixed(6)}`;
        } else {
            locationSpan.textContent = 'Ubicación no disponible';
        }
    }

    async savePhoto() {
        if (!this.currentPhoto) {
            this.showMessage('❌ No hay foto para guardar', 'error');
            return;
        }

        try {
            // Crear FormData
            const formData = new FormData();
            formData.append('photo', this.currentPhoto, `foto_${Date.now()}.jpg`);
            formData.append('type', document.getElementById('photo-type').value);
            formData.append('description', document.getElementById('photo-description').value);
            formData.append('project_id', document.getElementById('photo-project').value);
            formData.append('location', document.getElementById('photo-location').value);
            formData.append('priority', document.getElementById('photo-priority').value);
            
            if (this.geolocation) {
                formData.append('latitude', this.geolocation.latitude);
                formData.append('longitude', this.geolocation.longitude);
                formData.append('accuracy', this.geolocation.accuracy);
            }

            // Enviar al servidor
            const response = await fetch('/api/fotos/upload/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': this.getCSRFToken()
                }
            });

            if (response.ok) {
                this.showMessage('✅ Foto guardada exitosamente', 'success');
                this.resetPhotoForm();
                this.closePhotoModal();
            } else {
                throw new Error('Error en el servidor');
            }
        } catch (error) {
            console.error('❌ Error guardando foto:', error);
            this.showMessage('❌ Error guardando foto', 'error');
        }
    }

    resetPhotoForm() {
        // Limpiar formulario
        document.getElementById('photo-description').value = '';
        document.getElementById('photo-location').value = '';
        document.getElementById('photo-type').selectedIndex = 0;
        document.getElementById('photo-project').selectedIndex = 0;
        document.getElementById('photo-priority').selectedIndex = 0;
        
        // Resetear foto
        this.currentPhoto = null;
        
        // Mostrar video nuevamente
        const video = document.getElementById('camera-preview');
        const canvas = document.getElementById('photo-canvas');
        video.style.display = 'block';
        canvas.style.display = 'none';
        
        // Deshabilitar botón de guardar
        const saveBtn = document.getElementById('save-photo-btn');
        saveBtn.disabled = true;
    }

    closePhotoModal() {
        const modal = document.getElementById('photo-modal');
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) {
            bsModal.hide();
        }
        
        // Detener cámara
        if (this.camera) {
            this.camera.getTracks().forEach(track => track.stop());
            this.camera = null;
        }
    }

    getCSRFToken() {
        const token = document.querySelector('meta[name="csrf-token"]');
        return token ? token.getAttribute('content') : '';
    }

    showMessage(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast position-fixed`;
        toast.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 10000;
        `;
        
        const bgClass = type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info';
        const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-triangle' : 'info-circle';
        
        toast.innerHTML = `
            <div class="toast-header ${bgClass} text-white">
                <i class="fas fa-${icon} me-2"></i>
                <strong class="me-auto">Sistema de Fotos</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();
        
        // Auto-remover
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }

    showCameraError() {
        const modal = document.getElementById('photo-modal');
        const modalBody = modal.querySelector('.modal-body');
        
        modalBody.innerHTML = `
            <div class="text-center py-5">
                <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                <h5>Error de Cámara</h5>
                <p class="text-muted">No se pudo acceder a la cámara del dispositivo.</p>
                <p class="text-muted">Verifica los permisos de cámara en tu navegador.</p>
                <button class="btn btn-primary" onclick="location.reload()">
                    <i class="fas fa-refresh me-2"></i>Reintentar
                </button>
            </div>
        `;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    if (window.pwaInstaller && window.pwaInstaller.isMobileDevice()) {
        window.fotosMovil = new FotosMovil();
    }
});

// Exportar para uso global
window.FotosMovil = FotosMovil;
