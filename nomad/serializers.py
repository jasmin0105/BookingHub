from rest_framework import serializers
from .models import NomadPackage, NomadBooking

class NomadPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NomadPackage
        fields = '__all__'

class NomadBookingSerializer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='package.name', read_only=True)
    class Meta:
        model = NomadBooking
        fields = '__all__'
        read_only_fields = ['user', 'total_price', 'created_at']
