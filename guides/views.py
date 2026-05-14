from rest_framework import viewsets, permissions
from .models import Guide
from .serializers import GuideSerializer

class GuideViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Guide.objects.filter(is_available=True)
    serializer_class = GuideSerializer
    permission_classes = [permissions.AllowAny]
