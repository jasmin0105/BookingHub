from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from .models import Booking
from .emails import send_booking_confirmation, send_booking_cancelled, send_owner_notification
from .serializers import BookingSerializer
from hotels.models import Hotel


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class   = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin' or user.is_staff:
            return Booking.objects.all().order_by('-created_at')
        if user.role == 'business_owner':
            return Booking.objects.filter(
                Q(hotel__owner=user) | Q(restaurant__owner=user) |
                Q(event__owner=user) | Q(user=user)
            ).order_by('-created_at')
        return Booking.objects.filter(user=user).order_by('-created_at')

    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        send_booking_confirmation(booking)
        send_owner_notification(booking)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.user != request.user and not (request.user.role == 'admin' or request.user.is_staff):
            return Response({'error': 'Not allowed'}, status=403)
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'cancelled'})


@api_view(['GET'])
@permission_classes([AllowAny])
def check_availability(request):
    item_type = request.query_params.get('type')
    item_id   = request.query_params.get('id')
    check_in  = request.query_params.get('check_in')
    check_out = request.query_params.get('check_out')

    if not all([item_type, item_id, check_in, check_out]):
        return Response({'error': 'type, id, check_in, check_out обязательны'}, status=400)

    overlapping = Booking.objects.filter(
        booking_type=item_type,
        status__in=['pending', 'confirmed'],
        check_in__lt=check_out,
        check_out__gt=check_in,
        **{f'{item_type}_id': item_id}
    )

    total_rooms = 1
    if item_type == 'hotel':
        try:
            hotel = Hotel.objects.get(id=item_id)
            total_rooms = hotel.available_rooms
        except Hotel.DoesNotExist:
            return Response({'error': 'Hotel not found'}, status=404)

    booked    = overlapping.count()
    available = total_rooms - booked

    return Response({
        'available':       available > 0,
        'available_rooms': available,
        'total_rooms':     total_rooms,
        'booked':          booked,
        'check_in':        check_in,
        'check_out':       check_out,
    })
