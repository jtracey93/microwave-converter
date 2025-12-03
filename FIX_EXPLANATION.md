# Fix for GitHub Pages Not Showing Latest Changes

## Problem
The latest changes from PR #6 (iPhone display improvements with increment/decrement controls) were merged to `main` and the GitHub Actions deployment workflow ran successfully, but the live site at https://jtracey93.github.io/microwave-converter/ was still showing the old version.

## Root Cause
The issue was caused by the **service worker** (`sw.js`) caching the old version of the site. The service worker was using a cache-first strategy, which meant:

1. When users visited the site, the service worker served the **cached version** of the files
2. The cached files were from before PR #6 was merged
3. Even though the deployment succeeded, users continued to see the old cached version
4. The cache version was `'microwave-timer-v1'` and hadn't been updated

## Solution
Three changes were made to `sw.js` to fix this issue:

### 1. Updated Cache Version
```javascript
const CACHE_NAME = 'microwave-timer-v2'; // Changed from v1 to v2
```
This forces the service worker to create a new cache and delete the old one.

### 2. Changed to Network-First Caching Strategy
```javascript
// OLD: Cache-first strategy
caches.match(event.request).then((response) => {
    return response || fetch(event.request);
})

// NEW: Network-first strategy
fetch(event.request)
    .then((response) => {
        // Update cache with fresh content
        if (response && response.status === 200) {
            const responseClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
                cache.put(event.request, responseClone);
            });
        }
        return response;
    })
    .catch(() => {
        // Fall back to cache when offline
        return caches.match(event.request);
    })
```
This ensures users always get the latest version when online, while still supporting offline use.

### 3. Added Immediate Activation
```javascript
// In install event:
return self.skipWaiting();

// In activate event:
return self.clients.claim();
```
This makes the new service worker take control immediately without requiring users to close all tabs.

## Impact
After this fix is merged and deployed:
1. Users will immediately get the new service worker (v2)
2. The old cache (v1) will be deleted
3. Users will see the latest changes from PR #6:
   - New increment/decrement controls for wattage, minutes, and seconds
   - Updated default values (800W for recipe, 700W for microwave, 8:00 for time)
   - Optimized layout for iPhone 14 Pro
4. Future updates will always show immediately (network-first strategy)

## Testing
Once deployed, you can verify the fix by:
1. Opening DevTools → Application → Service Workers
2. Verifying the active service worker is version `microwave-timer-v2`
3. Checking that the increment/decrement controls are visible
4. Clearing cache and refreshing to confirm new content loads

## Prevention
Going forward, whenever significant changes are made to the site:
1. Increment the CACHE_NAME version (v2 → v3, etc.)
2. The network-first strategy will ensure users get updates quickly
3. Consider adding a "Update Available" notification for better UX
