from django.contrib import admin
from .models import WishlistItem


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'restaurant', 'event', 'created_at']
    list_filter = ['created_at']