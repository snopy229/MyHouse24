from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth import get_user_model

from .forms import (
    UserRegistrationForm,
    AuthenticationOwnerForm,
    AuthenticationStaffForm,
)
from django.contrib.auth.views import LoginView


# Create your views here.
User = get_user_model()


class RegisterOwner(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("owner:apartment-none")

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class LogInOwner(LoginView):
    form_class = AuthenticationOwnerForm
    template_name = "LogInOwner.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user

        apartment = user.apartment_set.first()
        if apartment:
            return reverse("owner:apartment-detail", kwargs={"pk": apartment.pk})

        return reverse_lazy("owner:profile-detail")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class LogInStaff(LoginView):
    form_class = AuthenticationStaffForm
    template_name = "LogInStuff.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy("managements:statistic")
