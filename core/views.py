from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Sum, Q
from bookings.models import Booking
from hotels.models import Hotel
from restaurants.models import Restaurant
from events.models import Event


class AdminStatsView(APIView):
    """Admin dashboard statistics"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        total_bookings = Booking.objects.count()
        active_bookings = Booking.objects.exclude(status='cancelled').count()
        total_revenue = Booking.objects.exclude(status='cancelled').aggregate(
            total=Sum('total_price')
        )['total'] or 0

        bookings_by_type = Booking.objects.values('booking_type').annotate(
            count=Count('id')
        )

        return Response({
            'total_bookings': total_bookings,
            'active_bookings': active_bookings,
            'cancelled_bookings': total_bookings - active_bookings,
            'total_revenue': float(total_revenue),
            'total_hotels': Hotel.objects.count(),
            'total_restaurants': Restaurant.objects.count(),
            'total_events': Event.objects.count(),
            'bookings_by_type': list(bookings_by_type),
        })


class GlobalSearchView(APIView):
    """Search across all categories at once"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response({'hotels': [], 'restaurants': [], 'events': [], 'query': ''})

        hotels = Hotel.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query) | Q(description__icontains=query)
        )[:5]

        restaurants = Restaurant.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query) | Q(cuisine__icontains=query)
        )[:5]

        events = Event.objects.filter(
            Q(name__icontains=query) | Q(city__icontains=query) | Q(description__icontains=query)
        )[:5]

        def hotel_data(h):
            return {'id': h.id, 'name': h.name, 'city': h.city,
                    'price': str(h.price_per_night), 'image': h.image if hasattr(h, 'image') else None,
                    'rating': str(h.rating) if hasattr(h, 'rating') and h.rating else '4.8', 'type': 'hotel'}

        def restaurant_data(r):
            return {'id': r.id, 'name': r.name, 'city': r.city,
                    'price': str(getattr(r, 'price_range', 0)), 'image': r.image if hasattr(r, 'image') else None,
                    'rating': str(r.rating) if hasattr(r, 'rating') and r.rating else '4.8',
                    'cuisine': getattr(r, 'cuisine', ''), 'type': 'restaurant'}

        def event_data(e):
            return {'id': e.id, 'name': e.name, 'city': e.city,
                    'price': str(e.price), 'image': e.image if hasattr(e, 'image') else None,
                    'rating': str(e.rating) if hasattr(e, 'rating') and e.rating else '4.8',
                    'date': str(e.date) if hasattr(e, 'date') and e.date else None, 'type': 'event'}

        return Response({
            'query': query,
            'hotels': [hotel_data(h) for h in hotels],
            'restaurants': [restaurant_data(r) for r in restaurants],
            'events': [event_data(e) for e in events],
            'total': hotels.count() + restaurants.count() + events.count(),
        })