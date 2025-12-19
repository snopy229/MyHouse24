from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm

# Create your views here.
User = get_user_model()


class RegisterOwner(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
