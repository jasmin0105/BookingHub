from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NomadPackage, NomadBooking
from .serializers import NomadPackageSerializer, NomadBookingSerializer

class NomadPackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NomadPackage.objects.filter(is_active=True)
    serializer_class = NomadPackageSerializer
    permission_classes = [permissions.AllowAny]

class NomadBookingViewSet(viewsets.ModelViewSet):
    serializer_class = NomadBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NomadBooking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        package = serializer.validated_data['package']
        people = serializer.validated_data.get('people', 1)
        total = package.price * people
        serializer.save(user=self.request.user, total_price=total)
