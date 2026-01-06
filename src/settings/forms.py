from django import forms
from django.contrib.auth.password_validation import validate_password
from django.forms import modelformset_factory

from src.settings.models import UnitsOfMeasurement, Service, Article, Requisite
from src.user.models import User


class UnitForm(forms.ModelForm):
    class Meta:
        model = UnitsOfMeasurement
        # В вашем коде было fields=['units'], предполагаю поле называется 'units'
        fields = ["units"]
        widgets = {
            "units": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Например: шт, кг"}
            ),
        }


# Создаем формсет для единиц
UnitsFormSet = modelformset_factory(
    UnitsOfMeasurement,
    form=UnitForm,  # Подключаем форму с виджетами
    extra=0,  # Не выводить пустые строки по умолчанию
    can_delete=True,
)


# --- 2. Форма для Услуг ---
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_showing": forms.CheckboxInput(
                attrs={"class": "form-checkbox"}
            ),  # Чекбокс
            "units_of_measure": forms.Select(attrs={"class": "form-control"}),
        }


# Создаем формсет для услуг
ServiceFormSet = modelformset_factory(
    Service,
    form=ServiceForm,
    extra=0,  # Не выводить пустые строки по умолчанию
    can_delete=True,
)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "type": forms.Select(attrs={"class": "form-control"}),
        }


class RequisiteForm(forms.ModelForm):
    class Meta:
        model = Requisite
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "information": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


class UserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "second_name",
            "email",
            "phone_number",
            "status",
            "role",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "second_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if password1:
            validate_password(password1, user=self.instance)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password1 == password2:
            user.set_password(password1)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                current_role = self.instance.role_set.first()
                if current_role:
                    self.fields["role"].initial = current_role.title
            except Exception:
                pass
