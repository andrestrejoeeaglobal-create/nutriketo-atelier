// NutriKeto Atelier Service Worker - Governance Rule RULE-2026-CROSS-DEVICE-MIRROR-001
const CACHE_NAME = 'nutriketo-v36-6-rev11-s42-fruits-fix-v39';

const ASSETS_TO_CACHE = [
  './',
  './index.html'
];

self.addEventListener('install', (event) => {
  console.log('[ServiceWorker] Install event triggered - Version:', CACHE_NAME);
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      console.log('[ServiceWorker] Caching core static assets with cache-busting');
      for (const url of ASSETS_TO_CACHE) {
        try {
          const bustUrl = url + (url.includes('?') ? '&' : '?') + '_sw_bust=' + encodeURIComponent(CACHE_NAME) + '_' + Date.now();
          const res = await fetch(bustUrl, { cache: 'no-store' });
          if (res && res.status === 200) {
            await cache.put(url, res.clone());
          }
        } catch (e) {
          console.warn('[ServiceWorker] Pre-cache failed for:', url, e);
        }
      }
    }).then(() => {
      return self.skipWaiting();
    })
  );
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

  // Network-First using URL string (avoids Chromium TypeError when Request.mode === 'navigate' + non-empty RequestInit)
  event.respondWith(
    fetch(reqUrl, { cache: 'no-store' })
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
