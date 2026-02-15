from django.utils import timezone

from django import forms
from django_select2.forms import Select2Widget

from src.admin.models import MasterCall, CashBox


class MasterCallForm(forms.ModelForm):
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "rows": 5,
                "style": "width: 100%; min-width: 100%;",
            }
        ),
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
        if not self.instance.pk:
            self.fields["date"].initial = timezone.now().date().strftime("%Y-%m-%d")
            self.fields["time"].initial = timezone.now().time().strftime("%H:%M")
        else:
            if self.instance.date:
                self.initial["date"] = self.instance.date.strftime("%Y-%m-%d")
                self.fields["time"].initial = timezone.now().time().strftime("%H:%M")


class CashBoxForm(forms.ModelForm):
    class Meta:
        model = CashBox
        fields = ["sum", "number", "date"]
        widgets = {
            "sum": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "number" in self.fields:
            self.fields["number"].required = False
        if "date" in self.fields:
            self.fields["date"].required = False
