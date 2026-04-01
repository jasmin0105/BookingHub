from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Hotel
from .serializers import HotelSerializer
from users.permissions import IsAdminOrBusinessOwner, IsOwnerOrAdmin


class HotelViewSet(viewsets.ModelViewSet):
    queryset           = Hotel.objects.all()
    serializer_class   = HotelSerializer
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'city', 'description']
    ordering_fields    = ['price_per_night', 'rating']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'similar']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAdminOrBusinessOwner()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_path='similar', permission_classes=[AllowAny])
    def similar(self, request, pk=None):
        hotel   = self.get_object()
        similar = Hotel.objects.filter(city=hotel.city).exclude(id=hotel.id)[:4]
        if similar.count() < 2:
            similar = Hotel.objects.filter(
                price_per_night__gte=hotel.price_per_night * 0.5,
                price_per_night__lte=hotel.price_per_night * 1.5,
            ).exclude(id=hotel.id)[:4]
        return Response(HotelSerializer(similar, many=True).data)

    @action(detail=False, methods=['get'], url_path='my', permission_classes=[IsAuthenticated])
    def my_hotels(self, request):
        return Response(HotelSerializer(Hotel.objects.filter(owner=request.user), many=True).data)
