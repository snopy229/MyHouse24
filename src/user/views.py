from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator

from .forms import (
    UserRegistrationForm,
    AuthenticationOwnerForm,
    AuthenticationStaffForm,
)
from django.contrib.auth.views import LoginView

from .utils import send_email_verify

# Create your views here.
User = get_user_model()


class RegisterOwner(CreateView):
    form_class = UserRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("user:email-verify")

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)

        last_box = User.objects.only("id").order_by("id").last()
        next_id = (last_box.id + 1) if last_box else 1
        new_id_user = "00" + str(next_id)
        if not User.objects.filter(id_user=new_id_user).exists():
            user.id_user = new_id_user
        user.save()
        send_email_verify(self.request, user)

        return HttpResponseRedirect(self.get_success_url())


class EmailVerifyTemplateView(TemplateView):
    template_name = "email_verify.html"


class LogInOwner(LoginView):
    form_class = AuthenticationOwnerForm
    template_name = "LogInOwner.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        user = self.request.user

        apartment = user.apartment_set.first()
        if apartment:
            return reverse("owner:apartment-detail", kwargs={"pk": apartment.pk})

        return reverse_lazy("owner:profile-detail")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        remember_me = form.cleaned_data.get("remember_me")

        user = form.get_user()

        if not user.email_verify and not user.status == "active":
            url = reverse("owner:login") + "?error=no_verified&&no_active"
            return redirect(url)
        elif not user.email_verify:
            url = reverse("owner:login") + "?error=no_verified"
            return redirect(url)
        elif not user.status == "active":
            url = reverse("owner:login") + "?error=no_active"
            return redirect(url)

        if remember_me:
            self.request.session.set_expiry(1209600)
        else:
            self.request.session.set_expiry(0)

        return response


class LogInStaff(LoginView):
    form_class = AuthenticationStaffForm
    template_name = "LogInStuff.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse_lazy("admin:statistic")

    def form_valid(self, form):
        response = super().form_valid(form)

        remember_me = form.cleaned_data.get("remember_me")

        if not remember_me:
            self.request.session.set_expiry(0)
        else:
            self.request.session.set_expiry(None)

        return response


class EmailVerifyView(View):
    def get(self, request, uidb64, token, **kwargs):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            return redirect(reverse("user:email-verified"))

        return redirect("user:email-error")

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=int(uid))
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class EmailVerifiedView(TemplateView):
    template_name = "email_verifyed.html"


class EmailError(TemplateView):
    template_name = "email_error.html"


class AuthentificationError(TemplateView):
    template_name = "authentification_error.html"
