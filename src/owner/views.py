# Create your views here.
from ajax_datatable import AjaxDatatableView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
    TemplateView,
    DeleteView,
    ListView,
)
from rest_framework.reverse import reverse_lazy

from src.admin.choices import StatusCall
from owner.forms import MasterCallForm
from src.admin.models import Apartment, MasterCall, MessageStatus, Message
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
    initial_order = [[0, "asc"]]

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
            {
                "name": "action",
                "title": "",
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

        delete_url = reverse("owner:master-call-delete", args=[obj.id])
        if obj.call_status == StatusCall.NEW:
            row["action"] = format_html(
                '<div class="btn-group btn-group-sm">'
                '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
                "</div>",
                delete_url,
            )
        else:
            row["action"] = format_html(
                '<div class="btn-group btn-group-sm">'
                '<button class="btn btn-default btn-sm disabled"><i class="fa fa-trash"></i></button>'
                "</div>",
            )


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


class DeleteMasterCall(DeleteView):
    model = MasterCall

    def get(self, request, pk):
        master_call = get_object_or_404(MasterCall, pk=pk)
        master_call.delete()
        return redirect("owner:master-call-list")


class MessageDetail(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "owner_message_detail.html"
    context_object_name = "message"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status = MessageStatus.objects.get(
            message=self.object,
            user=self.request.user,
        )
        if not status.is_read:
            status.is_read = True
            status.save(update_fields=["is_read"])

        return context


class MessageList(LoginRequiredMixin, ListView):
    model = Message
    template_name = "owner_message_list.html"


class DeleteMessage(View):
    def post(self, request, pk):
        message = Message.objects.get(pk=pk)
        status = MessageStatus.objects.get(
            message=message,
            user=self.request.user,
        )
        status.is_deleted = True
        status.save(update_fields=["is_deleted"])
        return redirect("owner:master-call-list")


class MessageAjaxDatatable(AjaxDatatableView):
    model = Message
    initial_order = [[2, "asc"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "checkbox",
                "title": "",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "recipient",
                "title": "Получатели",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "theme",
                "title": "Получатели",
                "searchable": True,
                "orderable": True,
            },
            {
                "name": "created_at",
                "title": "Дата",
                "searchable": False,
                "orderable": False,
            },
        ]
        return columns

    def customize_row(self, row, obj):
        row["checkbox"] = mark_safe(
            f'<input type="checkbox" name="item_ids" value="{obj.id}" class="item-checkbox">'
        )

        if not obj.house:
            row["receipent"] = '<span><a href="#">Всем</a></span>'
        else:
            row["receipent"] = (
                f'<span><a href="#">{obj.house.title}{f', {obj.section.title}' if obj.section else ''}{f', {obj.floor.title}' if obj.floor else ''}{f', кв.{obj.apartment.number}' if obj.apartment else ''}</a></span>'
            )

        row["theme"] = f"<span>{obj.theme}-{obj.message}</span>"

        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'

    def initialize_row(self, row, obj):
        qs = super().get_initial_queryset()
        return qs.filter(
            user=self.request.user, messagestatus__is_read=False, is_deleted=False
        )


def message_bulk_delete(request):
    if request.method == "POST":
        item_ids = request.POST.getlist("item_ids")
        if item_ids:
            MessageStatus.objects.filter(message__id__in=item_ids)
            Message.objects.filter(id__in=item_ids).update(
                messagestatus__is_deleted=True
            )

    return redirect("admin:message-list")
