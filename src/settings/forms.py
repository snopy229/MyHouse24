from django import forms
from django.forms import modelformset_factory

from src.settings.models import UnitsOfMeasurement, Service, Article, Requisite


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
