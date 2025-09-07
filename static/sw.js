const CACHE_NAME = 'depenses-couple-v1.0.0';
const urlsToCache = [
  '/',
  '/static/css/style.css',
  '/static/js/app.js',
  '/static/manifest.json',
  '/expenses',
  '/subscriptions',
  '/budgets',
  'https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://cdn.jsdelivr.net/npm/chart.js'
];

// Install event
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Cache opened');
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Return cached version or fetch from network
        if (response) {
          return response;
        }
        
        // Clone the request
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest).then(
          (response) => {
            // Check if we received a valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Clone the response
            const responseToCache = response.clone();
            
            caches.open(CACHE_NAME)
              .then((cache) => {
                cache.put(event.request, responseToCache);
              });
              
            return response;
          }
        ).catch(() => {
          // Return offline page for navigation requests
          if (event.request.mode === 'navigate') {
            return caches.match('/');
          }
        });
      })
  );
});

// Activate event
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Background Sync for offline expense submission
self.addEventListener('sync', (event) => {
  if (event.tag === 'expense-sync') {
    event.waitUntil(syncExpenses());
  }
});

async function syncExpenses() {
  try {
    // Get pending expenses from IndexedDB
    const pendingExpenses = await getPendingExpenses();
    
    for (const expense of pendingExpenses) {
      try {
        const response = await fetch('/api/expenses', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(expense.data)
        });
        
        if (response.ok) {
          // Remove from pending expenses
          await removePendingExpense(expense.id);
          console.log('Expense synced successfully');
        }
      } catch (error) {
        console.error('Failed to sync expense:', error);
      }
    }
  } catch (error) {
    console.error('Background sync failed:', error);
  }
}

// IndexedDB helpers (simplified)
async function getPendingExpenses() {
  // Implementation would use IndexedDB to get pending expenses
  return [];
}

async function removePendingExpense(id) {
  // Implementation would remove expense from IndexedDB
  console.log('Removing pending expense:', id);
}

// Push notification event
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle notification de Dépenses Couple',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [200, 100, 200],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'view',
        title: 'Voir',
        icon: '/static/icons/view-icon.png'
      },
      {
        action: 'close',
        title: 'Fermer',
        icon: '/static/icons/close-icon.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('Dépenses Couple', options)
  );
});

// Notification click event
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'view') {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});