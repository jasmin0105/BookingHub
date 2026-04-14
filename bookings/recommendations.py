from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking
from hotels.models import Hotel
from restaurants.models import Restaurant
from events.models import Event


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendations(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).select_related('hotel', 'restaurant', 'event')

    booked_hotel_ids = []
    booked_rest_ids = []
    booked_event_ids = []
    cities = set()
    price_ranges = []

    for b in bookings:
        if b.hotel:
            booked_hotel_ids.append(b.hotel.id)
            cities.add(b.hotel.city)
            price_ranges.append(float(b.hotel.price_per_night))
        if b.restaurant:
            booked_rest_ids.append(b.restaurant.id)
            cities.add(b.restaurant.city)
        if b.event:
            booked_event_ids.append(b.event.id)
            cities.add(b.event.city)

    avg_price = sum(price_ranges) / len(price_ranges) if price_ranges else 100

    # Hotels — same city, similar price, not booked before
    hotels_qs = Hotel.objects.exclude(id__in=booked_hotel_ids)
    if cities:
        hotels_qs = hotels_qs.filter(city__in=cities)
    hotels = list(hotels_qs.order_by('-rating')[:4])

    # If not enough — fill with top rated
    if len(hotels) < 4:
        extra = Hotel.objects.exclude(id__in=booked_hotel_ids + [h.id for h in hotels]).order_by('-rating')[:4-len(hotels)]
        hotels += list(extra)

    # Restaurants
    rests_qs = Restaurant.objects.exclude(id__in=booked_rest_ids)
    if cities:
        rests_qs = rests_qs.filter(city__in=cities)
    rests = list(rests_qs.order_by('-rating')[:4])
    if len(rests) < 4:
        extra = Restaurant.objects.exclude(id__in=booked_rest_ids + [r.id for r in rests]).order_by('-rating')[:4-len(rests)]
        rests += list(extra)

    # Events
    events_qs = Event.objects.exclude(id__in=booked_event_ids)
    if cities:
        events_qs = events_qs.filter(city__in=cities)
    events = list(events_qs.order_by('-date')[:4])
    if len(events) < 4:
        extra = Event.objects.exclude(id__in=booked_event_ids + [e.id for e in events]).order_by('-date')[:4-len(events)]
        events += list(extra)

    return Response({
        'based_on': len(bookings),
        'cities': list(cities),
        'hotels': [{'id':h.id,'name':h.name,'city':h.city,'price':float(h.price_per_night),'rating':float(h.rating),'type':'hotel'} for h in hotels],
        'restaurants': [{'id':r.id,'name':r.name,'city':r.city,'cuisine':r.cuisine_type,'rating':float(r.rating),'type':'restaurant'} for r in rests],
        'events': [{'id':e.id,'name':e.name,'city':e.city,'price':float(e.price),'type':'event'} for e in events],
    })
