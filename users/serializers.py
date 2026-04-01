from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    role_display = serializers.SerializerMethodField()

    class Meta:
        model  = CustomUser
        fields = ['id', 'email', 'username', 'phone', 'avatar',
                  'is_admin', 'role', 'role_display', 'date_joined']
        read_only_fields = ['id', 'role', 'date_joined']

    def get_role_display(self, obj):
        return obj.get_role_display()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    role     = serializers.ChoiceField(
                   choices=['user', 'business_owner'],
                   default='user',
                   required=False
               )

    class Meta:
        model  = CustomUser
        fields = ['email', 'username', 'password', 'role', 'phone']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user'),
            phone=validated_data.get('phone', ''),
        )
        return user


class UserListSerializer(serializers.ModelSerializer):
    """Для Admin — список всех пользователей"""
    class Meta:
        model  = CustomUser
        fields = ['id', 'email', 'username', 'role', 'phone',
                  'date_joined', 'is_active']
