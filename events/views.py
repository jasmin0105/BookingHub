from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer
from users.permissions import IsAdminOrBusinessOwner, IsOwnerOrAdmin


class EventViewSet(viewsets.ModelViewSet):
    queryset           = Event.objects.all()
    serializer_class   = EventSerializer
    filter_backends    = [filters.SearchFilter, filters.OrderingFilter]
    search_fields      = ['name', 'city', 'venue']
    ordering_fields    = ['date', 'price']

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
        event   = self.get_object()
        similar = Event.objects.filter(
            city=event.city
        ).exclude(id=event.id)[:4]
        return Response(EventSerializer(similar, many=True).data)

    @action(detail=False, methods=['get'], url_path='my',
            permission_classes=[IsAuthenticated])
    def my_events(self, request):
        events = Event.objects.filter(owner=request.user)
        return Response(EventSerializer(events, many=True).data)
