import json


def service_worker() -> str:
    with open('./manifest.json') as f:
        manifest = json.load(f)
    return '''
        const CACHE_NAME = "bevyframe-offline-pages";
        const OFFLINE_PAGE = "''' + manifest['app']['offlineview'] + '''";
        self.addEventListener("install", (event) => {
            event.waitUntil(caches.open(CACHE_NAME).then((cache) => { return cache.add(OFFLINE_PAGE); }));
        });
        self.addEventListener("activate", (event) => {
            event.waitUntil(
                caches.keys().then((cacheNames) => {
                    return Promise.all( cacheNames.map((name) => { if (name !== CACHE_NAME) return caches.delete(name); }));
                })
            );
        });
        self.addEventListener("fetch", (event) => {
            event.respondWith(
                (async () => {
                    try {
                        const networkResponse = await fetch(event.request);
                        if (event.request.destination === 'document') {
                            const cache = await caches.open(CACHE_NAME);
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    } catch (error) {
                        const cache = await caches.open(CACHE_NAME);
                        const cachedResponse = await cache.match(event.request);
                        return cachedResponse || cache.match(OFFLINE_PAGE);
                    }
                })()
            );
        });
    '''