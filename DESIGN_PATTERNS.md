# Design Patterns in BookingHub

## 1. Repository Pattern (Django ORM)

Instead of writing raw SQL, we use Django ORM as a Repository layer.
All database queries go through model managers.

Example:

```python
# Instead of: SELECT * FROM hotels WHERE city = 'Bishkek'
Hotel.objects.filter(city='Bishkek')
```

Когда пользователь открывает страницу отелей — Vue.js просит Django дать список отелей. Django не пишет сырой SQL запрос. Вместо этого пишет:
pythonHotel.objects.filter(city='Bishkek')
Django ORM сам переводит это в SQL и идёт в базу. Ты никогда не работаешь с базой напрямую — только через эту прослойку.
Файл: hotels/views.py

## 2. Singleton Pattern (Pinia Store)

The auth store exists as a single instance across the entire Vue.js app.
Only one user session exists at any time.

Example: `src/stores/auth.js` — one global store for authentication state.

Когда ты логинишься в BookingHub — твои данные (имя, роль, токен) сохраняются в Pinia store. Это один объект на весь сайт.
Ты переходишь со страницы отелей на страницу ресторанов — данные о тебе не теряются. Все страницы читают из одного места.
Файл: src/stores/auth.js

## 3. Observer Pattern (Vue.js Reactivity)

When a reactive variable changes, all components that use it update automatically.

Example: When `locale.value = 'ru'` — NavBar, buttons and text update instantly.
Ты нажимаешь KY в навбаре — меняется одна переменная locale. Vue.js автоматически видит это изменение и перерисовывает весь текст на сайте на кыргызском. Ты не перезагружаешь страницу — всё само меняется.
Файл: src/i18n/index.js

## 4. Factory Pattern (DRF Serializers)

Serializers act as factories — they create validated objects from raw request data.

Example: `BookingSerializer` takes POST data and creates a Booking instance.

Пользователь нажимает Book Now и отправляет данные — какой отель, какие даты, сколько гостей. Serializer получает эти данные, проверяет их и создаёт готовый объект Booking в базе данных.
Файл: bookings/serializers.py

## 5. Decorator Pattern (Django Permissions)

`@permission_classes([IsAuthenticated])` decorates views with authentication checks.

Example:

```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    ...
```

В файле bookings/views.py над каждой функцией стоит:
python@permission_classes([IsAuthenticated])
Это означает — перед тем как выполнить функцию, проверь есть ли у пользователя токен. Если нет — верни ошибку 401. Ты добавила эту проверку одной строкой не меняя саму функцию.
Файл: bookings/views.py

## 6. Strategy Pattern (Payment System)

Different payment strategies (Mbank, Elcart, Optima) share the same interface
but have different implementations.

Example: `bookings/payment.py` — each method follows the same initiate/confirm flow.
Когда пользователь платит — он выбирает Mbank, Элкарт или Optima. Каждый способ оплаты — отдельный класс. Но все три работают одинаково для системы — у всех есть метод process_payment(). Хочешь добавить новый банк — просто добавляешь новый класс.
Файл: bookings/payment.py
