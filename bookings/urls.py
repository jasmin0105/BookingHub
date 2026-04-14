from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, check_availability
from .recommendations import get_recommendations
from .payment import initiate_payment, confirm_payment, payment_methods
from .dashboard import business_owner_dashboard

router = DefaultRouter()
router.register(r'', BookingViewSet, basename='booking')

urlpatterns = [
    path('availability/', check_availability),
    path('payment/initiate/', initiate_payment),
    path('payment/confirm/', confirm_payment),
    path('payment/methods/', payment_methods),
    path('recommendations/', get_recommendations),
    path('dashboard/', business_owner_dashboard),
    path('', include(router.urls)),
]
