from django.contrib import admin
from .models import Tour

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'price', 'duration', 'difficulty', 'rating']
    search_fields = ['name', 'city']
    list_filter = ['difficulty', 'city']
