from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django_select2.forms import Select2Widget

from src.user.models import User
from .models import House, Section, Floor, Apartment, BankBook


class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        fields = "__all__"
        exclude = ["owner"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "image1": forms.FileInput(attrs={"class": "form-control"}),
            "image2": forms.FileInput(attrs={"class": "form-control"}),
            "image3": forms.FileInput(attrs={"class": "form-control"}),
            "image4": forms.FileInput(attrs={"class": "form-control"}),
            "image5": forms.FileInput(attrs={"class": "form-control"}),
        }


class SectionForm(forms.Form):
    class Meta:
        model = Section
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


class FloorForm(forms.ModelForm):
    class Meta:
        model = Floor
        fields = [
            "title",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


StaffFormSet = inlineformset_factory(
    House,
    House.owner.through,
    fields=["user"],
    widgets={
        "user": forms.Select(attrs={"class": "form-control"}),
    },
    extra=0,
    can_delete=True,
)

SectionFormSet = inlineformset_factory(
    House,
    Section,
    fields=["title"],
    widgets={
        "title": forms.TextInput(attrs={"class": "form-control"}),
    },
    extra=0,
    can_delete=True,
)

FloorFormSet = inlineformset_factory(
    House,
    Floor,
    fields=["title"],
    widgets={
        "title": forms.TextInput(attrs={"class": "form-control"}),
    },
    extra=0,
    can_delete=True,
)


class ApartmentForm(forms.ModelForm):
    bank_book_select = forms.ModelChoiceField(
        widget=Select2Widget,
        required=False,
        queryset=BankBook.objects.all(),
    )
    bank_book_input = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=False,
    )

    class Meta:
        model = Apartment
        fields = ["number", "area", "house", "floor", "section", "owner", "tariff"]
        widgets = {
            "number": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "area": forms.NumberInput(attrs={"class": "form-control"}),
            "house": Select2Widget(
                attrs={
                    "class": "form-control",
                }
            ),
            "section": Select2Widget(attrs={"class": "form-control"}),
            "floor": Select2Widget(attrs={"class": "form-control"}),
            "owner": Select2Widget(attrs={"class": "form-control"}),
            "tariff": Select2Widget(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            bank_book = BankBook.objects.filter(apartment=self.instance).first()

            if bank_book:
                self.fields["bank_book_input"].initial = bank_book.number

    def clean(self):
        cleaned_data = super(ApartmentForm, self).clean()

        input_num = self.cleaned_data.get("bank_book_input")
        if input_num:
            bank_book = BankBook.objects.filter(number=input_num).first()
            if (
                bank_book
                and bank_book.apartment
                and bank_book.apartment != self.instance
            ):
                raise ValidationError(
                    {
                        "bank_book_input": "Счет уже занят",
                    }
                )
        return cleaned_data

    def save(self, commit=True):
        apartment = super().save(commit=commit)
        input_num = self.cleaned_data.get("bank_book_input")
        selected_obj = self.cleaned_data["bank_book_select"]
        section = self.cleaned_data["section"]
        floor = self.cleaned_data["floor"]
        house = self.cleaned_data["house"]
        owner = self.cleaned_data["owner"]
        tariff = self.cleaned_data["tariff"]
        new_bank_book = None
        DEFAULT_STATUS_FOR_NEW = "NEW"

        if input_num:
            new_bank_book, created = BankBook.objects.update_or_create(
                number=input_num,
                defaults={
                    "house": house,
                    "owner": owner,
                    "apartment": apartment,
                    "section": section,
                    "floor": floor,
                    "status": DEFAULT_STATUS_FOR_NEW,
                    "tariff": tariff,
                },
            )
        elif selected_obj:
            new_bank_book = selected_obj
            new_bank_book.apartment = apartment
            new_bank_book.section = section
            new_bank_book.floor = floor
            new_bank_book.save()

        try:
            if hasattr(apartment, "bankbook"):
                old_account = apartment.bankbook

                if not new_bank_book or (old_account.pk != new_bank_book.pk):
                    old_account.apartment = None
                    old_account.section = None
                    old_account.floor = None
                    old_account.save()

        except Exception:
            pass

        return apartment


class OwnerForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}), required=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=False,
    )
    house = forms.ModelChoiceField(
        widget=Select2Widget, required=False, queryset=House.objects.all()
    )
    apartment = forms.ModelChoiceField(
        widget=Select2Widget, required=False, queryset=Apartment.objects.all()
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "second_name",
            "last_name",
            "photo",
            "birth_date",
            "phone_number",
            "viber",
            "telegram",
            "email",
            "id_user",
            "status",
            "about_owner",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "second_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(
                attrs={
                    "class": "form-control w-100",
                    "type": "date",
                    "style": "width: 100%; box-sizing: border-box;",
                }
            ),
            "phone_number": forms.NumberInput(attrs={"class": "form-control"}),
            "viber": forms.Select(attrs={"class": "form-control"}),
            "telegram": forms.Select(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "id_user": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "about_owner": forms.Textarea(attrs={"class": "form-control"}),
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
