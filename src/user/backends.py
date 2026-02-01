from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailOrIdUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print("BACKEND CALLED:", username)

        if not username or not password:
            print("NO USERNAME OR PASSWORD")
            return None

        try:
            if username.isdigit():
                user = User.objects.get(id_user=username)
            else:
                user = User.objects.get(email__iexact=username)
        except Exception as e:
            print("USER NOT FOUND:", e)
            return None

        print("FOUND USER:", user)
        print("IS ACTIVE:", user.is_active)
        print("IS STAFF:", user.is_staff)
        print("PASSWORD OK:", user.check_password(password))

        if user.check_password(password) and self.user_can_authenticate(user):
            print("AUTH SUCCESS")
            return user

        print("AUTH FAILED")
        return None
