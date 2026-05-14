from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NomadPackageViewSet, NomadBookingViewSet

router = DefaultRouter()
router.register(r'packages', NomadPackageViewSet)
router.register(r'bookings', NomadBookingViewSet, basename='nomad-booking')

urlpatterns = [
    path('', include(router.urls)),
]
