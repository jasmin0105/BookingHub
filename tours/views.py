from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import Tour
from .serializers import TourSerializer
from users.permissions import IsAdminOrBusinessOwner

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all().order_by('-rating')
    serializer_class = TourSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'destination', 'difficulty']
    ordering_fields = ['price', 'rating', 'duration']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'similar']:
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminOrBusinessOwner()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def similar(self, request, pk=None):
        tour = self.get_object()
        similar = Tour.objects.filter(city=tour.city).exclude(id=tour.id)[:4]
        if similar.count() < 2:
            similar = Tour.objects.exclude(id=tour.id)[:4]
        return Response(TourSerializer(similar, many=True).data)
