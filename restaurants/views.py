from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Restaurant
from .serializers import RestaurantSerializer
from users.permissions import IsAdminOrBusinessOwner, IsOwnerOrAdmin


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset           = Restaurant.objects.all()
    serializer_class   = RestaurantSerializer
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'city', 'cuisine_type']
    ordering_fields    = ['rating']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        if self.action == 'create':
            return [IsAdminOrBusinessOwner()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_path='similar')
    def similar(self, request, pk=None):
        rest    = self.get_object()
        similar = Restaurant.objects.filter(
            city=rest.city
        ).exclude(id=rest.id)[:4]
        return Response(RestaurantSerializer(similar, many=True).data)

    @action(detail=False, methods=['get'], url_path='my',
            permission_classes=[IsAuthenticated])
    def my_restaurants(self, request):
        rests = Restaurant.objects.filter(owner=request.user)
        return Response(RestaurantSerializer(rests, many=True).data)
