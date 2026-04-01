from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Booking
from hotels.models import Hotel
from restaurants.models import Restaurant
from events.models import Event


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def business_owner_dashboard(request):
    user = request.user
    if user.role not in ('business_owner', 'admin') and not user.is_staff:
        return Response({'error': 'Business Owner access required'}, status=403)

    # Все объекты владельца
    hotels      = Hotel.objects.filter(owner=user)
    restaurants = Restaurant.objects.filter(owner=user)
    events      = Event.objects.filter(owner=user)

    # Все брони по объектам владельца
    bookings = Booking.objects.filter(
        Q(hotel__owner=user) |
        Q(restaurant__owner=user) |
        Q(event__owner=user)
    )

    # Общая статистика
    total_bookings    = bookings.count()
    confirmed         = bookings.filter(status='confirmed')
    cancelled         = bookings.filter(status='cancelled')
    pending           = bookings.filter(status='pending')
    total_revenue     = confirmed.aggregate(s=Sum('total_price'))['s'] or 0
    cancelled_revenue = cancelled.aggregate(s=Sum('total_price'))['s'] or 0

    # Брони за последние 6 месяцев (по месяцам)
    monthly = []
    for i in range(5, -1, -1):
        d     = timezone.now() - timedelta(days=30 * i)
        count = bookings.filter(
            created_at__year=d.year,
            created_at__month=d.month
        ).count()
        rev = confirmed.filter(
            created_at__year=d.year,
            created_at__month=d.month
        ).aggregate(s=Sum('total_price'))['s'] or 0
        monthly.append({
            'month': d.strftime('%b'),
            'year':  d.year,
            'bookings': count,
            'revenue':  float(rev),
        })

    # Топ объекты по броням
    top_hotels = []
    for h in hotels:
        b = bookings.filter(hotel=h)
        top_hotels.append({
            'id':       h.id,
            'name':     h.name,
            'city':     h.city,
            'bookings': b.count(),
            'revenue':  float(b.filter(status='confirmed').aggregate(s=Sum('total_price'))['s'] or 0),
            'rating':   h.rating,
        })
    top_hotels.sort(key=lambda x: x['bookings'], reverse=True)

    top_restaurants = []
    for r in restaurants:
        b = bookings.filter(restaurant=r)
        top_restaurants.append({
            'id':       r.id,
            'name':     r.name,
            'city':     r.city,
            'bookings': b.count(),
            'revenue':  float(b.filter(status='confirmed').aggregate(s=Sum('total_price'))['s'] or 0),
            'rating':   r.rating,
        })

    top_events = []
    for e in events:
        b = bookings.filter(event=e)
        top_events.append({
            'id':       e.id,
            'name':     e.name,
            'city':     e.city,
            'bookings': b.count(),
            'revenue':  float(b.filter(status='confirmed').aggregate(s=Sum('total_price'))['s'] or 0),
        })

    # Последние 5 броней
    recent = bookings.order_by('-created_at')[:5]
    recent_list = []
    for b in recent:
        recent_list.append({
            'id':        b.id,
            'type':      b.booking_type,
            'name':      b.hotel.name if b.hotel else (b.restaurant.name if b.restaurant else (b.event.name if b.event else '')),
            'guest':     b.user.username,
            'guests':    b.guests,
            'price':     float(b.total_price),
            'status':    b.status,
            'check_in':  str(b.check_in) if b.check_in else None,
            'check_out': str(b.check_out) if b.check_out else None,
            'created':   b.created_at.strftime('%Y-%m-%d'),
        })

    return Response({
        'summary': {
            'total_listings':  hotels.count() + restaurants.count() + events.count(),
            'total_hotels':    hotels.count(),
            'total_rests':     restaurants.count(),
            'total_events':    events.count(),
            'total_bookings':  total_bookings,
            'confirmed':       confirmed.count(),
            'pending':         pending.count(),
            'cancelled':       cancelled.count(),
            'total_revenue':   float(total_revenue),
            'cancelled_revenue': float(cancelled_revenue),
            'conversion_rate': round(confirmed.count() / total_bookings * 100, 1) if total_bookings > 0 else 0,
        },
        'monthly':          monthly,
        'top_hotels':       top_hotels[:5],
        'top_restaurants':  top_restaurants[:5],
        'top_events':       top_events[:5],
        'recent_bookings':  recent_list,
    })
