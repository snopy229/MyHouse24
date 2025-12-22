from django import forms

from .models import SeoBlock, MainPage, Contacts


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
