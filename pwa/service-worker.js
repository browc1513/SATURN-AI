const CACHE_NAME = "saturn-pwa-v3";

const APP_SHELL = [
    "/",
    "/app/style.css?v=3",
    "/app/app.js?v=3",
    "/app/manifest.json",
    "/app/icon-192.png",
    "/app/icon-512.png"
];


self.addEventListener(
    "install",
    (event) => {
        event.waitUntil(
            caches.open(CACHE_NAME)
                .then(
                    (cache) => cache.addAll(APP_SHELL)
                )
        );

        self.skipWaiting();
    }
);


self.addEventListener(
    "activate",
    (event) => {
        event.waitUntil(
            caches.keys()
                .then(
                    (keys) => Promise.all(
                        keys
                            .filter(
                                (key) => key !== CACHE_NAME
                            )
                            .map(
                                (key) => caches.delete(key)
                            )
                    )
                )
        );

        self.clients.claim();
    }
);


self.addEventListener(
    "fetch",
    (event) => {
        if (event.request.method !== "GET") {
            return;
        }

        const url = new URL(event.request.url);

        if (url.pathname.startsWith("/api/")) {
            return;
        }

        event.respondWith(
            fetch(event.request, { cache: "no-store" })
                .then(
                    (response) => {
                        const copy = response.clone();

                        caches.open(CACHE_NAME)
                            .then(
                                (cache) => {
                                    cache.put(
                                        event.request,
                                        copy
                                    );
                                }
                            );

                        return response;
                    }
                )
                .catch(
                    () => caches.match(event.request)
                )
        );
    }
);
