# Design Patterns in BookingHub

## 1. Repository Pattern (Django ORM)
Instead of writing raw SQL, we use Django ORM as a Repository layer.
All database queries go through model managers.

Example:
```python
# Instead of: SELECT * FROM hotels WHERE city = 'Bishkek'
Hotel.objects.filter(city='Bishkek')
```

## 2. Singleton Pattern (Pinia Store)
The auth store exists as a single instance across the entire Vue.js app.
Only one user session exists at any time.

Example: `src/stores/auth.js` — one global store for authentication state.

## 3. Observer Pattern (Vue.js Reactivity)
When a reactive variable changes, all components that use it update automatically.

Example: When `locale.value = 'ru'` — NavBar, buttons and text update instantly.

## 4. Factory Pattern (DRF Serializers)
Serializers act as factories — they create validated objects from raw request data.

Example: `BookingSerializer` takes POST data and creates a Booking instance.

## 5. Decorator Pattern (Django Permissions)
`@permission_classes([IsAuthenticated])` decorates views with authentication checks.

Example:
```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    ...
```

## 6. Strategy Pattern (Payment System)
Different payment strategies (Mbank, Elcart, Optima) share the same interface
but have different implementations.

Example: `bookings/payment.py` — each method follows the same initiate/confirm flow.
