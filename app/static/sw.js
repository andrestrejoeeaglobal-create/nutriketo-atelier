// NutriKeto Atelier Service Worker - Governance Rule RULE-2026-CROSS-DEVICE-MIRROR-001
const CACHE_NAME = 'nutriketo-v36-6-rev4-s41-pantry-fix-v18';

const ASSETS_TO_CACHE = [
  './',
  './index.html'
];

self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Install event triggered - Version:', CACHE_NAME);
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[ServiceWorker] Caching core static assets');
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('[ServiceWorker] Activate event triggered - Purging legacy caches');
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[ServiceWorker] Deleting legacy cache key:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => {
      console.log('[ServiceWorker] Claiming active clients');
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const reqUrl = event.request.url || '';
  if (!reqUrl.startsWith('http://') && !reqUrl.startsWith('https://')) return;

  // Network-First with Fallback to Cache
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache).catch((err) => {
              console.warn('[ServiceWorker] Cache put ignored for:', reqUrl, err);
            });
          });
        }
        return networkResponse;
      })
      .catch(() => {
        console.warn('[ServiceWorker] Network failed, falling back to cache for:', reqUrl);
        return caches.match(event.request);
      })
  );
});
