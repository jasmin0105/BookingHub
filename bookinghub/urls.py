from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from hotels.views import HotelViewSet
from restaurants.views import RestaurantViewSet
from events.views import EventViewSet
from users.views import RegisterView, ProfileView, EmailLoginView
from reviews.views import ReviewViewSet
from wishlist.views import WishlistViewSet
from core.views import AdminStatsView, GlobalSearchView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'hotels', HotelViewSet)
router.register(r'restaurants', RestaurantViewSet)
router.register(r'events', EventViewSet)
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/bookings/', include('bookings.urls')),
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/login/', EmailLoginView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/refresh/', TokenRefreshView.as_view()),
    path('api/auth/profile/', ProfileView.as_view()),
    path('api/stats/', AdminStatsView.as_view()),
    path('api/search/', GlobalSearchView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)