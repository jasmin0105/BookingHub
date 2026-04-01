from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Review
        fields = ['id', 'user_email', 'rating', 'comment', 'created_at', 'hotel', 'restaurant', 'event']
        read_only_fields = ['user_email']
    
    def get_user_email(self, obj):
        return obj.user.email.split('@')[0]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)