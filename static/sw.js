self.addEventListener("install", e => {
  console.log("Service Worker installed");
  self.skipWaiting();
});

self.addEventListener("fetch", e => {
  // For offline handling, cache logic can go here
});
