from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from .bo.auth_bo import AuthBO

User = get_user_model()

class UserListSerializer(serializers.ModelSerializer):
    """Serializer para listar usuarios registrados"""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'email', 'username', 'is_active', 'created_at', 'updated_at']

class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Puedes agregar claims personalizados aquí si lo necesitas
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Puedes agregar datos extra a la respuesta si lo necesitas
        return data


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    salt = serializers.CharField(write_only=True)
    username = serializers.CharField(required=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'salt', 'access', 'refresh']

    def create(self, validated_data):
        user = AuthBO.register_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            salt=validated_data['salt']
        )
        
        # Generar tokens para el usuario recién registrado
        refresh = RefreshToken.for_user(user)
        
        return {
            'email': user.email,
            'username': user.username,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
    
    def to_representation(self, instance):
        """
        Sobrescribir para manejar el dict retornado por create
        """
        if isinstance(instance, dict):
            return instance
        return super().to_representation(instance)
