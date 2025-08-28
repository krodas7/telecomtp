// Service Worker para Sistema ARCA Construcción - PRODUCCIÓN
const CACHE_NAME = 'arca-construccion-v1.0.0';
const STATIC_CACHE = 'arca-static-v1.0.0';
const DYNAMIC_CACHE = 'arca-dynamic-v1.0.0';

// URLs a cachear estáticamente
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
    '/static/manifest.json',
    '/offline/'
];

// URLs externas a cachear
const externalUrlsToCache = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

// Instalación del Service Worker
self.addEventListener('install', event => {
    console.log('🔄 Service Worker instalándose...');
    event.waitUntil(
        Promise.all([
            // Cachear archivos estáticos
            caches.open(STATIC_CACHE)
                .then(cache => {
                    console.log('📦 Cache estático abierto');
                    return cache.addAll(urlsToCache);
                }),
            // Cachear recursos externos
            caches.open(STATIC_CACHE)
                .then(cache => {
                    console.log('🌐 Cacheando recursos externos...');
                    return cache.addAll(externalUrlsToCache);
                })
        ]).then(() => {
            console.log('✅ Service Worker instalado correctamente');
            return self.skipWaiting();
        }).catch(error => {
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
                    if (cacheName !== STATIC_CACHE && cacheName !== DYNAMIC_CACHE) {
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
    const { request } = event;
    
    // Solo manejar peticiones GET
    if (request.method !== 'GET') {
        return;
    }

    // Excluir peticiones a APIs o endpoints dinámicos
    if (request.url.includes('/admin/') || 
        request.url.includes('/api/') ||
        request.url.includes('/static/admin/') ||
        request.url.includes('/media/') ||
        request.url.includes('chrome-extension://') ||
        request.url.includes('moz-extension://')) {
        return;
    }

    event.respondWith(
        caches.match(request)
            .then(response => {
                // Si está en cache estático, devolverlo
                if (response) {
                    return response;
                }

                // Si no está en cache, hacer la petición a la red
                return fetch(request)
                    .then(response => {
                        // Verificar que la respuesta sea válida
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clonar la respuesta para poder cachearla
                        const responseToCache = response.clone();

                        // Cachear en cache dinámico
                        caches.open(DYNAMIC_CACHE)
                            .then(cache => {
                                cache.put(request, responseToCache);
                            })
                            .catch(error => {
                                console.warn('⚠️ No se pudo cachear la respuesta:', error);
                            });

                        return response;
                    })
                    .catch(() => {
                        // Si falla la red, devolver página offline
                        if (request.destination === 'document') {
                            return caches.match('/offline/');
                        }
                        
                        // Para otros recursos, devolver respuesta vacía
                        return new Response('', {
                            status: 503,
                            statusText: 'Service Unavailable',
                            headers: {
                                'Content-Type': 'text/plain'
                            }
                        });
                    });
            })
    );
});

// Manejo de mensajes del cliente
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'GET_VERSION') {
        event.ports[0].postMessage({
            version: CACHE_NAME,
            staticCache: STATIC_CACHE,
            dynamicCache: DYNAMIC_CACHE
        });
    }
});

// Limpieza periódica del cache dinámico
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.open(DYNAMIC_CACHE).then(cache => {
            return cache.keys().then(keys => {
                // Mantener solo los últimos 100 items
                if (keys.length > 100) {
                    const keysToDelete = keys.slice(0, keys.length - 100);
                    return Promise.all(
                        keysToDelete.map(key => cache.delete(key))
                    );
                }
            });
        })
    );
});

// Manejo de errores global
self.addEventListener('error', event => {
    console.error('❌ Error en Service Worker:', event.error);
});

// Manejo de promesas rechazadas
self.addEventListener('unhandledrejection', event => {
    console.error('❌ Promesa rechazada en Service Worker:', event.reason);
});
