from django import forms
from django.forms import inlineformset_factory

from .models import (
    SeoBlock,
    MainPage,
    Contacts,
    ServicesForSite,
    ServicesAndSeoBlock,
    TariffsForSite,
    TariffsAndSeoBlock,
)


class SeoBlockForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ("title", "description", "keywords")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "keywords": forms.Textarea(attrs={"class": "form-control"}),
        }


class MainPageForm(forms.ModelForm):
    short_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_short_text",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )
    block_description_1 = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_block_description_1",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )
    block_description_2 = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_block_description_2",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )
    block_description_3 = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_block_description_3",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )
    block_description_4 = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_block_description_4",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )
    block_description_5 = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_block_description_5",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )
    block_description_6 = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_block_description_6",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )

    class Meta:
        model = MainPage
        fields = "__all__"
        exclude = ("seo_block",)
        widgets = {
            "slides1": forms.FileInput(),
            "slides2": forms.FileInput(),
            "slides3": forms.FileInput(),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "block_title_1": forms.TextInput(attrs={"class": "form-control"}),
            "block_title_2": forms.TextInput(attrs={"class": "form-control"}),
            "block_title_3": forms.TextInput(attrs={"class": "form-control"}),
            "block_title_4": forms.TextInput(attrs={"class": "form-control"}),
            "block_title_5": forms.TextInput(attrs={"class": "form-control"}),
            "block_title_6": forms.TextInput(attrs={"class": "form-control"}),
        }


class ContactsForm(forms.ModelForm):
    short_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_short_text",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )

    class Meta:
        model = Contacts
        fields = "__all__"
        exclude = ("seo_block",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "link_site": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "map_fragment": forms.Textarea(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
        }


class ServicesForSiteForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )

    class Meta:
        model = ServicesForSite
        fields = "__all__"
        exclude = ("seo_block",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class ServicesAndSeoBlockForm(forms.ModelForm):
    class Meta:
        model = ServicesAndSeoBlock
        fields = []


ServicesForSiteFormSet = inlineformset_factory(
    ServicesAndSeoBlock,
    ServicesForSite,
    form=ServicesForSiteForm,
    extra=0,
)


class TariffsForSiteForm(forms.ModelForm):
    class Meta:
        model = TariffsForSite
        fields = "__all__"
        exclude = ("seo_block",)
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
        }


class TariffsAndSeoBlockForm(forms.ModelForm):
    short_text = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "id": "id_short_text",
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        )
    )

    class Meta:
        model = TariffsAndSeoBlock
        fields = ["title", "short_text"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
        }


TariffsForSiteFormSet = inlineformset_factory(
    TariffsAndSeoBlock,
    TariffsForSite,
    form=TariffsForSiteForm,
    extra=0,
)
