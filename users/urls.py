from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('profile/',  views.ProfileView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    # Admin endpoints
    path('admin/users/',                    views.admin_users_list),
    path('admin/users/<int:user_id>/role/', views.admin_change_role),
]
