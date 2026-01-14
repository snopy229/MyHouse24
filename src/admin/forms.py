from django import forms
from django.forms import inlineformset_factory

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
        queryset=BankBook.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Apartment
        fields = ["number", "area", "house", "floor", "section", "owner", "tariff"]
        widgets = {
            "number": forms.NumberInput(attrs={"class": "form-control"}),
            "area": forms.NumberInput(attrs={"class": "form-control"}),
            "house": forms.Select(attrs={"class": "form-control"}),
            "floor": forms.Select(attrs={"class": "form-control"}),
            "section": forms.Select(attrs={"class": "form-control"}),
            "owner": forms.Select(attrs={"class": "form-control"}),
            "tariff": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["section"].queryset = Section.objects.none()
        self.fields["floor"].queryset = Floor.objects.none()
        self.fields["bank_book_select"].queryset = BankBook.objects.none()

        if "owner" in self.data:
            owner_id = int(self.data["owner"])
            self.fields["bank_book_select"].queryset = BankBook.objects.filter(
                owner_id=owner_id
            ).order_by("number")

        if "house" in self.data:
            try:
                house_id = int(self.data.get("house"))
                self.fields["section"].queryset = Section.objects.filter(
                    house_id=house_id
                ).order_by("title")
                self.fields["floor"].queryset = Floor.objects.filter(
                    house_id=house_id
                ).order_by("title")
            except (ValueError, TypeError):
                pass

        elif self.instance.pk and self.instance.house:
            self.fields["section"].queryset = self.instance.house.section.order_by(
                "title"
            )
            self.fields["floor"].queryset = self.instance.house.floor.order_by("title")
            self.fields[
                "bank_book_select"
            ].queryset = self.instance.owner.bank_book_select.order_by("number")

    def save(self, commit=True):
        apartment = super().save(commit=commit)

        selected_bank_book = self.cleaned_data.get("bank_book_select")

        if selected_bank_book:
            selected_bank_book.apartment = apartment
            selected_bank_book.save()

        elif self.instance.pk:
            try:
                if hasattr(self.instance, "bank_book"):
                    old_bank_book = self.instance.bank_book
                    old_bank_book.apartment = None
                    old_bank_book.save()
            except BankBook.DoesNotExist:
                pass

        return apartment
