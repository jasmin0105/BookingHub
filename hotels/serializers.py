from rest_framework import serializers
from .models import Hotel

class HotelSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image and str(obj.image).startswith('http'):
            return str(obj.image)
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
