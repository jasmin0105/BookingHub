from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, check_availability
from .dashboard import business_owner_dashboard

router = DefaultRouter()
router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('availability/', check_availability),
    path('dashboard/', business_owner_dashboard),
    path('', include(router.urls)),
]
