from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'booking_type', 'status', 'total_price', 'created_at']
    list_filter = ['status', 'booking_type']