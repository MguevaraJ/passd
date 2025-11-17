from django.contrib.auth import get_user_model

User = get_user_model()

class AuthBO:
    @staticmethod
    def register_user(email, username, password, salt):
        user = User.objects.create_user(
            email=email,
            password=password,
            salt=salt,
            username=username
        )
        return user

    @staticmethod
    def list_users():
        """
        Retorna la lista de todos los usuarios registrados.
        """
        return User.objects.all().order_by('-created_at')
