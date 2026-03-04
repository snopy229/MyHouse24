from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrIdUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if username.isdigit():
                user = User.objects.get(id_user=username)
            else:
                user = User.objects.get(email__iexact=username)
        except Exception:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
