// NutriKeto Atelier Service Worker - Lightweight Pass-Through & Legacy Cache Cleanup
const CACHE_NAME = 'nutriketo-v36-6-rev20-pure-farm-nouns-v48';

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
