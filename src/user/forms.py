from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from hcaptcha_field import hCaptchaField

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Почта"}
        ),
    )
    hcaptcha = hCaptchaField()

    class Meta:
        model = User
        fields = ("email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "username" in self.fields:
            del self.fields["username"]

        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Пароль"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Повторите пароль"}
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Эта почта уже зарегистрирована.")
        return email


class AuthenticationOwnerForm(AuthenticationForm):
    hcaptcha = hCaptchaField()
    username = forms.EmailField(
        label="Email или ID пользователя",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "E-mail или ID"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control custom-password",
                "placeholder": "Введите ваш пароль",
                "data-toggle": "password",
            }
        ),
    )
    remember_me = forms.BooleanField(required=False, initial=False)

    def confirm_login_allowed(self, user):
        if user.is_staff:
            raise forms.ValidationError(
                "Эта учетная запись не принадлежит персоналу.",
                code="not_staff",
            )
        super().confirm_login_allowed(user)


class AuthenticationStaffForm(AuthenticationForm):
    hcaptcha = hCaptchaField()
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "E-mail"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Пароль",
                "data-toggle": "password",
            }
        )
    )
    remember_me = forms.BooleanField(required=False, initial=False)

    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise forms.ValidationError(
                "Эта учетная запись принадлежит персоналу.",
                code="not_staff",
            )
        super().confirm_login_allowed(user)
