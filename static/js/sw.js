// Service Worker para modo offline
const CACHE_NAME = 'sistema-construccion-v1';
const urlsToCache = [
    '/',
    '/static/css/global-styles.css',
    '/static/js/bootstrap.bundle.min.js',
    '/static/js/chart.min.js',
    '/static/js/fullcalendar.min.js',
    '/static/css/bootstrap.min.css',
    '/static/css/fullcalendar.min.css',
    '/static/css/fontawesome.min.css',
    '/dashboard/',
    '/proyectos/',
    '/clientes/',
    '/facturas/',
    '/gastos/',
    '/inventario/',
    '/anticipos/',
    '/usuarios/',
    '/roles/',
    '/sistema/'
];

// Instalación del Service Worker
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Cache abierto');
                return cache.addAll(urlsToCache);
            })
    );
});

// Activación del Service Worker
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Eliminando cache antiguo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Interceptar requests
self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Si está en cache, devolverlo
                if (response) {
                    return response;
                }
                
                // Si no está en cache, intentar fetch
                return fetch(event.request).then(function(response) {
                    // Verificar si la respuesta es válida
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    
                    // Clonar la respuesta
                    var responseToCache = response.clone();
                    
                    caches.open(CACHE_NAME)
                        .then(function(cache) {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                }).catch(function() {
                    // Si falla el fetch, devolver página offline
                    if (event.request.destination === 'document') {
                        return caches.match('/offline/');
                    }
                });
            })
    );
});

// Sincronización en segundo plano
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

function doBackgroundSync() {
    // Sincronizar datos pendientes cuando se recupere la conexión
    return new Promise(function(resolve) {
        // Aquí iría la lógica de sincronización
        console.log('Sincronizando datos pendientes...');
        resolve();
    });
}