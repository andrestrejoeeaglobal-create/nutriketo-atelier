// NutriKeto Atelier Service Worker - Governance Rule RULE-2026-CROSS-DEVICE-MIRROR-001
const CACHE_NAME = 'nutriketo-v36-6-rev3-s40-ui-order-v10';

const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './sw.js'
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

  // Network-First with Fallback to Cache
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        console.warn('[ServiceWorker] Network failed, falling back to cache for:', event.request.url);
        return caches.match(event.request);
      })
  );
});
