
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserListSerializer
from .bo.auth_bo import AuthBO

from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = []

class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

class UserListView(generics.ListAPIView):
    """Vista para listar todos los usuarios registrados"""
    serializer_class = UserListSerializer
    permission_classes = []
    
    def get_queryset(self):
        return AuthBO.list_users()
