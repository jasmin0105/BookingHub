from rest_framework import serializers
from .models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    item_name = serializers.SerializerMethodField()
    item_type = serializers.SerializerMethodField()
    item_city = serializers.SerializerMethodField()
    item_price = serializers.SerializerMethodField()
    item_image = serializers.SerializerMethodField()
    item_id = serializers.SerializerMethodField()

    class Meta:
        model = WishlistItem
        fields = ['id', 'item_id', 'item_type', 'item_name', 'item_city',
                  'item_price', 'item_image', 'hotel', 'restaurant', 'event', 'created_at']
        read_only_fields = ['item_name', 'item_type', 'item_city', 'item_price', 'item_image', 'item_id']

    def get_item_type(self, obj):
        if obj.hotel: return 'hotel'
        if obj.restaurant: return 'restaurant'
        if obj.event: return 'event'
        return None

    def get_item_name(self, obj):
        item = obj.hotel or obj.restaurant or obj.event
        return item.name if item else None

    def get_item_city(self, obj):
        item = obj.hotel or obj.restaurant or obj.event
        return getattr(item, 'city', None)

    def get_item_price(self, obj):
        if obj.hotel: return obj.hotel.price_per_night
        if obj.restaurant: return getattr(obj.restaurant, 'price_range', None)
        if obj.event: return obj.event.price
        return None

    def get_item_image(self, obj):
        item = obj.hotel or obj.restaurant or obj.event
        return getattr(item, 'image', None)

    def get_item_id(self, obj):
        if obj.hotel: return obj.hotel.id
        if obj.restaurant: return obj.restaurant.id
        if obj.event: return obj.event.id
        return None

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)