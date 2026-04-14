import uuid
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Booking


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    booking_id = request.data.get('booking_id')
    method = request.data.get('method', 'mbank')

    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=404)

    if booking.status == 'paid':
        return Response({'error': 'Already paid'}, status=400)

    transaction_id = f"BH-{method.upper()}-{str(uuid.uuid4())[:8].upper()}"

    return Response({
        'transaction_id': transaction_id,
        'booking_id': booking.id,
        'amount': float(booking.total_price),
        'currency': 'KGS',
        'method': method,
        'status': 'pending',
        'message': f'Payment initiated via {method.upper()}',
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment(request):
    booking_id = request.data.get('booking_id')
    transaction_id = request.data.get('transaction_id')

    try:
        booking = Booking.objects.get(id=booking_id, user=request.user)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=404)

    success = random.random() > 0.05

    if success:
        booking.status = 'confirmed'
        booking.save()
        return Response({
            'success': True,
            'transaction_id': transaction_id,
            'booking_id': booking.id,
            'amount': float(booking.total_price),
            'currency': 'KGS',
            'message': 'Payment successful! Booking confirmed.',
            'receipt': f'MBANK-RECEIPT-{transaction_id}',
        })
    else:
        return Response({'success': False, 'message': 'Payment failed. Please try again.'}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_methods(request):
    return Response({
        'methods': [
            {'id': 'mbank', 'name': 'Mbank', 'color': 'E31E24', 'description': 'Mbank — largest bank in Kyrgyzstan', 'fee': 0},
            {'id': 'elcart', 'name': 'Elcart', 'color': '0066CC', 'description': 'National payment system of Kyrgyzstan', 'fee': 0},
            {'id': 'optima', 'name': 'Optima Bank', 'color': 'FF6B00', 'description': 'Pay with Optima Bank card', 'fee': 0},
        ]
    })
