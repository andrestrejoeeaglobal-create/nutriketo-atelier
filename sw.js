// NutriKeto Atelier Service Worker - Governance Rule RULE-2026-CROSS-DEVICE-MIRROR-001
const CACHE_NAME = 'nutriketo-v36-6-rev13-s42-delete-fix-v41';

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

  // Bypass cross-origin requests (e.g., cdn.tailwindcss.com, Google Fonts) so browser loads them natively without CORS blocks
  try {
    const parsedUrl = new URL(reqUrl);
    if (parsedUrl.origin !== self.location.origin) return;
  } catch (e) {
    return;
  }

  // Same-origin Network-First using URL string
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
      .catch(async () => {
        console.warn('[ServiceWorker] Network failed, falling back to cache for:', reqUrl);
        const cached = await caches.match(event.request);
        if (cached) return cached;
        const rootCached = await caches.match('./index.html') || await caches.match('./');
        if (rootCached) return rootCached;
        return new Response('Offline', { status: 503, statusText: 'Service Unavailable' });
      })
  );
});
