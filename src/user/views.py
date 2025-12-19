from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, AuthenticationOwnerForm
from django.contrib.auth.views import LoginView

# Create your views here.
User = get_user_model()


class RegisterOwner(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class LogInOwner(LoginView):
    form_class = AuthenticationOwnerForm
    template_name = "LogInOwner.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


