from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils import timezone
from django_select2.forms import Select2Widget

from src.user.models import User, Role
from .models import (
    House,
    Section,
    Floor,
    Apartment,
    BankBook,
    Counter,
    MasterCall,
    Receipt,
    ServiceFullCost,
    Message,
    CashBox,
    XlsTemplate,
)


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


def get_staff_users_field(db_field, **kwargs):
    if db_field.name == "user":
        kwargs["queryset"] = User.objects.filter(is_staff=True)
    return db_field.formfield(**kwargs)


StaffFormSet = inlineformset_factory(
    House,
    House.owner.through,
    fields=["user"],
    widgets={
        "user": forms.Select(attrs={"class": "form-control"}),
    },
    extra=0,
    can_delete=True,
    formfield_callback=get_staff_users_field,
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
            "section": Select2Widget(attrs={"class": "form-control"}),
            "floor": Select2Widget(attrs={"class": "form-control"}),
            "owner": Select2Widget(attrs={"class": "form-control"}),
            "tariff": Select2Widget(attrs={"class": "form-control"}),
            "house": Select2Widget(attrs={"class": "form-control"}),
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
        DEFAULT_STATUS_FOR_NEW = "ACTIVE"

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
            "viber": forms.TextInput(attrs={"class": "form-control"}),
            "telegram": forms.TextInput(attrs={"class": "form-control"}),
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


class InviteForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "info@example.com"}
        ),
        label="Email",
    )


class BankBookForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        widget=Select2Widget, required=False, queryset=User.objects.all()
    )

    class Meta:
        model = BankBook
        fields = [
            "number",
            "status",
            "apartment",
            "house",
            "section",
        ]
        widgets = {
            "number": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "apartment": Select2Widget(attrs={"class": "form-control"}),
            "house": Select2Widget(attrs={"class": "form-control"}),
            "section": Select2Widget(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            last_book = BankBook.objects.last()
            today = timezone.now().date()
            date_part = today.strftime("%d%m%y")
            next_id = (last_book.id + 1) if last_book else 1
            next_id_str = str(next_id)[-5:].zfill(5)
            generated_number = f"{date_part}{next_id_str}"
            self.fields["number"].initial = generated_number


class CounterForm(forms.ModelForm):
    class Meta:
        model = Counter
        fields = "__all__"
        widgets = {
            "number": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "house": Select2Widget(attrs={"class": "form-control"}),
            "section": Select2Widget(attrs={"class": "form-control"}),
            "apartment": Select2Widget(attrs={"class": "form-control"}),
            "service": Select2Widget(attrs={"class": "form-control"}),
            "readings": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.1",
                    "min": "0",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields["date"].initial = timezone.now().date().strftime("%Y-%m-%d")
            last_counter = Counter.objects.last()
            today = timezone.now().date()
            date_part = today.strftime("%d%m%y")
            next_id = (last_counter.id + 1) if last_counter else 1
            next_id_str = str(next_id)[-5:].zfill(5)
            generated_number = f"{date_part}{next_id_str}"
            self.fields["number"].initial = generated_number
        else:
            if self.instance.date:
                self.initial["date"] = self.instance.date.strftime("%Y-%m-%d")


class MasterCallForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )

    class Meta:
        model = MasterCall
        fields = "__all__"

        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "call_status": forms.Select(attrs={"class": "form-control"}),
            "master_type": forms.Select(attrs={"class": "form-control"}),
            "owner": Select2Widget(attrs={"class": "form-control"}),
            "master": Select2Widget(attrs={"class": "form-control"}),
            "apartment": Select2Widget(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["master_type"].queryset = Role.objects.exclude(
            title__in=["Директор", "Управляющий", "Бухгалтер"]
        )

        self.fields["master_type"].empty_label = "Любой специалист"
        self.fields["master_type"].required = False
        self.fields["master_type"].initial = None
        if not self.instance.pk:
            self.fields["date"].initial = timezone.now().date().strftime("%Y-%m-%d")
            self.fields["time"].initial = timezone.now().time().strftime("%H:%M")
        else:
            if self.instance.date:
                self.initial["date"] = self.instance.date.strftime("%Y-%m-%d")
                self.fields["time"].initial = timezone.now().time().strftime("%H:%M")


class UserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.fullname


class ReceiptForm(forms.ModelForm):
    bankbook = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    owner = UserChoiceField(
        required=False,
        widget=Select2Widget(attrs={"class": "form-control"}),
        queryset=User.objects.filter(is_staff=False),
    )

    class Meta:
        model = Receipt
        fields = "__all__"
        widgets = {
            "number": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "house": Select2Widget(attrs={"class": "form-control"}),
            "section": Select2Widget(attrs={"class": "form-control"}),
            "apartment": Select2Widget(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "tariff": Select2Widget(attrs={"class": "form-control"}),
            "date_from": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "date_to": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "is_catch": forms.CheckboxInput(attrs={"class": "form-control-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.bankbook:
            self.initial["bankbook"] = self.instance.bankbook.number
            self.initial["date"] = self.instance.date
            self.initial["date_from"] = self.instance.date_from
            self.initial["date_to"] = self.instance.date_to
        if not self.instance.pk:
            last_receipt = Receipt.objects.order_by("id").last()
            today = timezone.now()
            date_part = today.strftime("%d%m%y")
            next_id = (last_receipt.id + 1) if last_receipt else 1
            next_id_str = str(next_id)[-5:].zfill(5)
            generated_number = f"{date_part}{next_id_str}"

            self.fields["number"].initial = generated_number
            self.fields["date"].initial = timezone.now().date().strftime("%Y-%m-%d")
            month_ago = today.date() - relativedelta(months=1)
            self.fields["date_from"].initial = month_ago.strftime("%Y-%m-%d")
            self.fields["date_to"].initial = timezone.now().date().strftime("%Y-%m-%d")

    def clean_bankbook(self):
        number = self.cleaned_data["bankbook"]
        try:
            return BankBook.objects.get(number=number)
        except BankBook.DoesNotExist:
            raise forms.ValidationError("Такого лицевого счета не существует")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.bankbook = self.cleaned_data["bankbook"]
        if commit:
            instance.save()
        return instance


class ServiceFullCostForm(forms.ModelForm):
    class Meta:
        model = ServiceFullCost
        fields = "__all__"
        exclude = ("receipt",)
        widgets = {
            "service": forms.Select(attrs={"class": "form-control"}),
            "cost": forms.NumberInput(attrs={"class": "form-control"}),
            "unit": forms.Select(attrs={"class": "form-control"}),
            "full_cost": forms.NumberInput(attrs={"class": "form-control"}),
            "consumption": forms.NumberInput(attrs={"class": "form-control"}),
        }


ServiceFullCostFormSet = inlineformset_factory(
    Receipt,
    ServiceFullCost,
    form=ServiceFullCostForm,
    extra=0,
    can_delete=True,
)


class MessageForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
                "placeholder": "Сообщение",
            }
        )
    )
    for_debtor = forms.BooleanField(required=False)

    class Meta:
        model = Message
        fields = "__all__"
        exclude = [
            "created_at",
        ]
        widgets = {
            "theme": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тема"}
            ),
            "house": Select2Widget(
                attrs={
                    "class": "form-control",
                }
            ),
            "service": Select2Widget(attrs={"class": "form-control"}),
            "flag": Select2Widget(attrs={"class": "form-control"}),
            "apartment": Select2Widget(attrs={"class": "form-control"}),
        }


class CashBoxForm(forms.ModelForm):
    class Meta:
        model = CashBox
        fields = "__all__"
        widgets = {
            "number": forms.NumberInput(attrs={"class": "form-control"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}, format="%Y-%m-%d"
            ),
            "bank_book": Select2Widget(attrs={"class": "form-control"}),
            "article": Select2Widget(attrs={"class": "form-control"}),
            "owner": Select2Widget(attrs={"class": "form-control"}),
            "manager": Select2Widget(attrs={"class": "form-control"}),
            "comment": forms.Textarea(attrs={"class": "form-control"}),
            "is_catch": forms.CheckboxInput(attrs={"class": "form-control-input"}),
            "sum": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial["date"] = self.instance.date
        if not self.instance.pk:
            today = timezone.now()
            date_part = today.strftime("%d%m%y")
            last_box = CashBox.objects.only("id").order_by("id").last()
            next_id = (last_box.id + 1) if last_box else 1
            generated_number = f"{date_part}{next_id}"
            self.fields["number"].initial = generated_number
            self.fields["date"].initial = timezone.now().date().strftime("%Y-%m-%d")


class XlsTemplateForm(forms.ModelForm):
    class Meta:
        model = XlsTemplate
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "template": forms.FileInput(),
        }


class XlsTemplateShowForm(forms.Form):
    templates = forms.ModelChoiceField(
        queryset=XlsTemplate.objects.all(),
        widget=forms.RadioSelect(attrs={"class": "form-control-input"}),
        initial=lambda: XlsTemplate.objects.filter(is_default=True).first(),
    )
