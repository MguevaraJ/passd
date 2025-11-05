from django.contrib.auth import get_user_model

User = get_user_model()

class AuthBO:
    @staticmethod
    def register_user(email, password, salt):
        user = User.objects.create_user(email=email, password=password, salt=salt)
        return user
