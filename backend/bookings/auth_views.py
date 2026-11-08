
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .auth_serializers import (
    CustomerRegistrationSerializer,
    CustomTokenObtainPairSerializer,
)
from .permissions import get_user_role

User = get_user_model()


class CustomerRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]


class RefreshTokenView(TokenRefreshView):
    permission_classes = [permissions.AllowAny]


class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        profile = getattr(user, "profile", None)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": get_user_role(user),
            "phone": profile.phone if profile else "",
        })
