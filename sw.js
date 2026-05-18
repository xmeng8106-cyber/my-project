// Service Worker：网络优先，离线时回退缓存
const CACHE = 'web3news-v1';
const CACHED = ['./index.html', './icon-192.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CACHED)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  // 清除旧版本缓存
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    // 优先走网络，失败时返回缓存（离线也能看到最后一次内容）
    fetch(e.request)
      .then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
