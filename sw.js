// NutriKeto Atelier Service Worker - Lightweight Pass-Through & Legacy Cache Cleanup
const CACHE_NAME = 'nutriketo-v36-6-rev23-live-pantry-ssot';

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(keys.map((key) => caches.delete(key)));
    }).then(() => {
      return self.clients.claim();
    })
  );
});
