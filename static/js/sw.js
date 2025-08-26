// Service Worker para Sistema ARCA Construcción
const CACHE_NAME = 'arca-construccion-v1.0.0';
const urlsToCache = [
    '/',
    '/dashboard/',
    '/static/css/global-styles.css',
    '/static/css/neostructure-theme.css',
    '/static/css/sidebar-layout.css',
    '/static/css/mobile-styles.css',
    '/static/css/neostructure-enhanced.css',
    '/static/js/global-functions.js',
    '/static/images/icon-192x192.png',
    '/static/images/icon-512x512.png',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Instalación del Service Worker
self.addEventListener('install', event => {
    console.log('🔄 Service Worker instalándose...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('📦 Cache abierto');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('✅ Service Worker instalado correctamente');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('❌ Error durante la instalación:', error);
            })
    );
});

// Activación del Service Worker
self.addEventListener('activate', event => {
    console.log('🚀 Service Worker activándose...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('🗑️ Eliminando cache antiguo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('✅ Service Worker activado correctamente');
            return self.clients.claim();
        })
    );
});

// Interceptar peticiones de red
self.addEventListener('fetch', event => {
    // Solo manejar peticiones GET
    if (event.request.method !== 'GET') {
        return;
    }

    // Excluir peticiones a APIs o endpoints dinámicos
    if (event.request.url.includes('/admin/') || 
        event.request.url.includes('/api/') ||
        event.request.url.includes('/static/admin/')) {
        return;
    }

    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Si está en cache, devolverlo
                if (response) {
                    return response;
                }

                // Si no está en cache, hacer la petición a la red
                return fetch(event.request)
                    .then(response => {
                        // Verificar que la respuesta sea válida
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clonar la respuesta para poder cachearla
                        const responseToCache = response.clone();

                        caches.open(CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseToCache);
                            });

                        return response;
                    })
                    .catch(() => {
                        // Si falla la red, devolver página offline
                        if (event.request.destination === 'document') {
                            return caches.match('/offline.html');
                        }
                    });
            })
    );
});

// Manejar mensajes del cliente
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// Manejar notificaciones push (para futuras implementaciones)
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body || 'Nueva notificación del sistema',
            icon: '/static/images/icon-192x192.png',
            badge: '/static/images/icon-32x32.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: 1
            },
            actions: [
                {
                    action: 'explore',
                    title: 'Ver',
                    icon: '/static/images/icon-32x32.png'
                },
                {
                    action: 'close',
                    title: 'Cerrar',
                    icon: '/static/images/icon-32x32.png'
                }
            ]
        };

        event.waitUntil(
            self.registration.showNotification(data.title || 'Sistema ARCA', options)
        );
    }
});

// Manejar clics en notificaciones
self.addEventListener('notificationclick', event => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/dashboard/')
        );
    }
});

console.log('🔄 Service Worker cargado correctamente');
