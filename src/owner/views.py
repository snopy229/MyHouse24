# Create your views here.
from ajax_datatable import AjaxDatatableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import format_html
from django.views.generic import DetailView, CreateView, TemplateView
from rest_framework.reverse import reverse_lazy

from src.admin.choices import StatusCall
from owner.forms import MasterCallForm
from src.admin.models import Apartment, MasterCall
from src.user.views import User


class ApartmentOwnerDetail(DetailView):
    model = Apartment
    context_object_name = "apartment"
    template_name = "owner_apartment.html"


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = "detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user


class MasterCallListView(LoginRequiredMixin, TemplateView):
    model = MasterCall
    template_name = "owner_master_calls.html"


class MasterCallAjaxDatatable(AjaxDatatableView):
    model = MasterCall
    initial_order = [[0, "des"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "id",
                "title": "№ заявки",
                "orderable": True,
                "searchable": False,
            },
            {
                "name": "master_type",
                "title": "Тип мастера",
                "orderable": False,
                "searchable": False,
            },
            {
                "name": "date_time",
                "title": "Удобное время",
                "orderable": False,
                "searchable": False,
            },
            {
                "name": "status",
                "title": "Статус",
                "orderable": False,
                "searchable": False,
            },
        ]
        return columns

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset()
        return qs.filter(owner=self.request.user)

    def customize_row(self, row, obj):
        row["date_time"] = format_html("<span>{}-{}</span>", obj.date, obj.time)
        status = obj.get_call_status_display()

        css_class = "label label-default"
        if obj.call_status == StatusCall.IN_WORK:
            css_class = "label label-warning"
        elif obj.call_status == StatusCall.COMPLETED:
            css_class = "label label-success"
        elif obj.call_status == StatusCall.NEW:
            css_class = "label label-primary"
        row["status"] = f'<small class="{css_class}">{status}</small>'


class CreateMasterCall(LoginRequiredMixin, CreateView):
    model = MasterCall
    template_name = "owner_master_call_create.html"
    form_class = MasterCallForm
    success_url = reverse_lazy("owner:master-call-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
