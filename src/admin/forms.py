from django import forms
from django.forms import inlineformset_factory

from src.admin.models import Floor
from src.admin.models import House, Section


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
    extra=1,
    can_delete=True,
)

SectionFormSet = inlineformset_factory(
    House,
    Section,
    fields=["title"],
    widgets={
        "title": forms.TextInput(attrs={"class": "form-control"}),
    },
    extra=1,
    can_delete=True,
)

FloorFormSet = inlineformset_factory(
    House,
    Floor,
    fields=["title"],
    widgets={
        "title": forms.TextInput(attrs={"class": "form-control"}),
    },
    extra=1,
    can_delete=True,
)
