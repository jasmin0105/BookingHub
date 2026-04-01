from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser
from .serializers import UserSerializer, RegisterSerializer, UserListSerializer
from users.permissions import IsAdminRole


class RegisterView(generics.CreateAPIView):
    queryset           = CustomUser.objects.all()
    serializer_class   = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAdminRole])
def admin_users_list(request):
    """Только Admin видит всех пользователей"""
    users = CustomUser.objects.all().order_by('-date_joined')
    return Response(UserListSerializer(users, many=True).data)


@api_view(['PATCH'])
@permission_classes([IsAdminRole])
def admin_change_role(request, user_id):
    """Только Admin меняет роли"""
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    new_role = request.data.get('role')
    if new_role not in ['user', 'business_owner', 'admin']:
        return Response({'error': 'Invalid role'}, status=400)

    user.role = new_role
    user.save()
    return Response({'success': True, 'email': user.email, 'role': user.role})


from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('username')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
            attrs['username'] = user.username
        except User.DoesNotExist:
            pass
        return super().validate(attrs)

class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenSerializer
