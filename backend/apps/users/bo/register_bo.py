# This file has been removed as it has been replaced by auth_bo.py
from apps.users.models import User

class AuthBO:
    @staticmethod
    def register_user(email, password, salt):
        user = User.objects.create_user(email=email, password=password, salt=salt)
        return user
