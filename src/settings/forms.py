from django import forms
from django.contrib.auth.password_validation import validate_password
from django.forms import modelformset_factory, inlineformset_factory

from src.settings.models import (
    UnitsOfMeasurement,
    Service,
    Article,
    Requisite,
    Tariffs,
    ServicesCost,
)
from src.user.models import User, Role


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


UnitsFormSet = modelformset_factory(
    UnitsOfMeasurement,
    form=UnitForm,
    extra=0,
    can_delete=True,
)


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "is_showing": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
            "units_of_measure": forms.Select(attrs={"class": "form-control"}),
        }


ServiceFormSet = modelformset_factory(
    Service,
    form=ServiceForm,
    extra=0,
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
            "role": forms.Select(
                attrs={
                    "class": "form-control",
                    "required": True,
                }
            ),
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


class TariffsForm(forms.ModelForm):
    class Meta:
        model = Tariffs
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "edited_at": forms.DateTimeInput(attrs={"class": "form-control"}),
        }


class ServicesCostForm(forms.ModelForm):
    class Meta:
        model = ServicesCost
        fields = "__all__"
        exclude = ("tariff",)
        widgets = {
            "cost": forms.TextInput(attrs={"class": "form-control"}),
            "service": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            try:
                current_service = self.instance.service_set.first()
                if current_service:
                    self.fields["service"].initial = current_service.title
            except Exception:
                pass


ServiceCostFormSet = inlineformset_factory(
    Tariffs,
    ServicesCost,
    form=ServicesCostForm,
    extra=0,
    can_delete=True,
)


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "has_statistics": forms.CheckboxInput(
                attrs={"class": "form-control-input"}
            ),
            "has_cashbox": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_invoices": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_personal_accounts": forms.CheckboxInput(
                attrs={"class": "form-control-input"}
            ),
            "has_apartments": forms.CheckboxInput(
                attrs={"class": "form-control-input"}
            ),
            "has_owners": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_houses": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_messages": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_master_requests": forms.CheckboxInput(
                attrs={"class": "form-control-input"}
            ),
            "has_meters": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_site_management": forms.CheckboxInput(
                attrs={"class": "form-control-input"}
            ),
            "has_services": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_tariffs": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_roles": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_users": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "has_payment_details": forms.CheckboxInput(
                attrs={"class": "form-control-input"}
            ),
            "has_article": forms.CheckboxInput(attrs={"class": "form-control-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields["title"]
        self.fields["title"].disabled = True
        field.widget.attrs.update(
            {
                "style": "border: none; background: transparent; padding: 0; color: inherit; outline: none; appearance: none;",
                "readonly": "readonly",
            }
        )


RoleFormSet = modelformset_factory(
    Role,
    form=RoleForm,
    extra=0,
    can_delete=False,
)
