from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WishlistItem
from .serializers import WishlistItemSerializer


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle(self, request):
        """Toggle wishlist item — add if not exists, remove if exists"""
        user = request.user
        hotel = request.data.get('hotel')
        restaurant = request.data.get('restaurant')
        event = request.data.get('event')

        filters = {'user': user}
        if hotel:
            filters['hotel_id'] = hotel
        elif restaurant:
            filters['restaurant_id'] = restaurant
        elif event:
            filters['event_id'] = event
        else:
            return Response({'error': 'Provide hotel, restaurant, or event'}, status=400)

        existing = WishlistItem.objects.filter(**filters).first()
        if existing:
            existing.delete()
            return Response({'status': 'removed'})
        else:
            data = {}
            if hotel: data['hotel'] = hotel
            if restaurant: data['restaurant'] = restaurant
            if event: data['event'] = event
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'status': 'added', 'item': serializer.data}, status=201)

    @action(detail=False, methods=['get'], url_path='check')
    def check(self, request):
        """Check if item is in wishlist"""
        hotel = request.query_params.get('hotel')
        restaurant = request.query_params.get('restaurant')
        event = request.query_params.get('event')

        filters = {'user': request.user}
        if hotel: filters['hotel_id'] = hotel
        elif restaurant: filters['restaurant_id'] = restaurant
        elif event: filters['event_id'] = event

        exists = WishlistItem.objects.filter(**filters).exists()
        return Response({'in_wishlist': exists})