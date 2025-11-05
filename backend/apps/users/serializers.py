from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate, get_user_model
from .bo.auth_bo import AuthBO

User = get_user_model()

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

    class Meta:
        model = User
        fields = ['email', 'password', 'salt']

    def create(self, validated_data):
        user = AuthBO.register_user(
            email=validated_data['email'],
            password=validated_data['password'],
            salt=validated_data['salt']
        )
        return user
