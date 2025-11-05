
from rest_framework import generics
from .serializers import UserRegisterSerializer, UserLoginSerializer


from rest_framework_simplejwt.views import TokenObtainPairView

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = []

class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer
