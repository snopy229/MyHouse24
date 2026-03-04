# Create your views here.
import json

from ajax_datatable import AjaxDatatableView
from dateutil.relativedelta import relativedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.checks import messages
from django.core.mail import send_mail
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
from django.http import HttpResponseRedirect, request, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
    TemplateView,
    DeleteView,
    ListView,
    UpdateView,
)
from rest_framework.reverse import reverse_lazy
from weasyprint import HTML

from src.admin.forms import OwnerForm
from src.admin.choices import StatusCall, StatusReceipt
from src.owner.forms import MasterCallForm, CashBoxForm
from src.admin.models import (
    Apartment,
    MasterCall,
    MessageStatus,
    Message,
    Receipt,
    CashBox,
    Counter,
    ServiceFullCost,
)
from src.user.views import User


class Error(TemplateView):
    template_name = "owner_error.html"


class ApartmentOwnerDetail(DetailView):
    model = Apartment
    context_object_name = "apartment"
    template_name = "owner_apartment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        stats = CashBox.objects.filter(bank_book=self.object.bankbook).aggregate(
            total_cm=Sum("sum", filter=Q(status="CM", is_catch=True)),
            total_og=Sum("sum", filter=Q(status="OG", is_catch=True)),
        )

        receipts = Receipt.objects.filter(bankbook=self.object.bankbook)

        receipts_pay = (
            ServiceFullCost.objects.filter(receipt__in=receipts).aggregate(
                total=Sum("full_cost")
            )["total"]
            or 0
        )

        balance = (stats["total_cm"] or 0) - receipts_pay - (stats["total_og"] or 0)
        formatted_balance = "{:,.2f}".format(balance).replace(",", " ")
        context["balance"] = formatted_balance
        today = timezone.now().date()
        month_ago = today - relativedelta(months=1)
        receipts = Receipt.objects.filter(
            apartment=self.object, date__lte=today, date__gte=month_ago
        )
        debts = (
            receipts.aggregate(total=Sum("servicefullcost__full_cost"))["total"] or 0
        )
        context["middle_debt"] = (
            "{:,.2f}".format(debts / receipts.count()).replace(",", " ")
            if receipts
            else None
        )
        report = (
            ServiceFullCost.objects.filter(
                receipt__apartment=self.object,
                receipt__date__lte=today,
                receipt__date__gte=month_ago,
            )
            .values("service__title")
            .annotate(total_cost=Sum("full_cost"))
            .order_by("service__title")
        )
        colors = [f"hsl({(i * 137) % 360}, 70%, 60%)" for i in range(len(report))]
        context["expenses_month"] = report
        context["colors_month"] = json.dumps(colors)
        year_ago = today - relativedelta(years=1)
        report_year = (
            ServiceFullCost.objects.filter(
                receipt__apartment=self.object,
                receipt__date__lte=today,
                receipt__date__gte=year_ago,
            )
            .values("service__title")
            .annotate(total_cost=Sum("full_cost"))
            .order_by("service__title")
        )
        colors_year = [
            f"hsl({(i * 137) % 360}, 70%, 60%)" for i in range(len(report_year))
        ]
        context["expenses_year"] = report_year
        context["colors_year"] = json.dumps(colors_year)
        monthly_stats = (
            ServiceFullCost.objects.filter(receipt__in=receipts)
            .annotate(
                month=TruncMonth("receipt__date")  # Округляем дату до месяца
            )
            .values("month")
            .annotate(total=Sum("full_cost"))
            .order_by("month")
        )
        bar_data = [item["total"] for item in monthly_stats]
        context["bar_data"] = bar_data
        return context


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = "detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return self.request.user


class EditUser(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "owner_edit.html"
    context_object_name = "owner"
    form_class = OwnerForm

    def get_object(self, queryset=...):
        return self.request.user

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        user_email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        if len(raw_password) != 0:
            try:
                send_mail(
                    subject="Создания пароля",
                    message=f"Новый пароль: {raw_password}",
                    from_email=None,
                    recipient_list=[user_email],
                )
            except Exception as e:
                print(f"Ошибка отправки: {e}")

        return HttpResponseRedirect(reverse_lazy("owner:profile-detail"))


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
    initial_order = [[1, "asc"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "checkbox",
                "title": "",
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
        row["theme"] = f"<span>{obj.theme}-{obj.message}</span>"

        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset()
        return qs.filter(
            messagestatus__user=self.request.user,
            messagestatus__is_read=False,
            messagestatus__is_deleted=False,
        )


def message_bulk_delete(request):
    if request.method == "POST":
        item_ids = request.POST.getlist("item_ids")
        if item_ids:
            MessageStatus.objects.filter(
                message__id__in=item_ids, user=request.user
            ).update(is_deleted=True)

    return redirect("owner:message-list")


class ReceiptDetail(DetailView):
    model = Receipt
    template_name = "owner_receipt_detail.html"
    context_object_name = "receipt"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receipt = self.object
        services_cost = receipt.servicefullcost_set.all()
        context["fullcost"] = sum(a.full_cost for a in services_cost)

        return context


class ReceiptList(LoginRequiredMixin, ListView):
    model = Receipt
    template_name = "owner_receipt_list.html"


class ReceiptListConcrete(LoginRequiredMixin, DetailView):
    model = Apartment
    template_name = "owner_receipt_list.html"


class ReceiptAjaxTable(AjaxDatatableView):
    model = Receipt
    initial_order = [[1, "desc"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "number",
                "title": "№",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "date",
                "title": "Дата",
                "searchable": True,
                "orderable": True,
            },
            {
                "name": "status",
                "title": "Статус",
                "searchable": True,
                "orderable": False,
                "choices": StatusReceipt.choices,
            },
            {
                "name": "sum",
                "title": "Сумма",
                "searchable": False,
                "orderable": False,
            },
        ]
        return columns

    def customize_row(self, row, obj):
        css_class = ""
        if obj.status == StatusReceipt.PAID:
            css_class = "label label-success"
        elif obj.status == StatusReceipt.PART:
            css_class = "label label-warning"
        elif obj.status == StatusReceipt.UNPAID:
            css_class = "label label-danger"
        row["status"] = f'<small class="{css_class}">{obj.get_status_display()}</small>'

        detail_url = reverse("owner:receipt-detail", args=[obj.id])
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        row["sum"] = (
            f"<small>{sum(a.full_cost for a in obj.servicefullcost_set.all())}</small>"
        )

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset()

        qs = qs.filter(apartment__owner=self.request.user)

        apartment_id = self.kwargs.get("pk")
        if apartment_id:
            qs = qs.filter(apartment_id=apartment_id)

        return qs


class ReceiptConcreteAjaxTable(AjaxDatatableView):
    model = Receipt
    initial_order = [[1, "desc"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "number",
                "title": "№",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "date",
                "title": "Дата",
                "searchable": True,
                "orderable": True,
            },
            {
                "name": "status",
                "title": "Статус",
                "searchable": True,
                "orderable": False,
                "choices": StatusReceipt.choices,
            },
            {
                "name": "sum",
                "title": "Сумма",
                "searchable": False,
                "orderable": False,
            },
        ]
        return columns

    def customize_row(self, row, obj):
        if obj.status == StatusReceipt.PAID:
            css_class = "label label-success"
        elif obj.status == StatusReceipt.PART:
            css_class = "label label-warning"
        elif obj.status == StatusReceipt.UNPAID:
            css_class = "label label-danger"
        row["status"] = f'<small class="{css_class}">{obj.get_status_display()}</small>'

        detail_url = reverse("owner:receipt-detail", args=[obj.id])
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        row["sum"] = (
            f"<small>{sum(a.full_cost for a in obj.servicefullcost_set.all())}</small>"
        )

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset()

        qs = qs.filter(apartment__owner=self.request.user)

        apartment_id = self.kwargs.get("pk")
        if apartment_id:
            qs = qs.filter(apartment_id=apartment_id)

        print(
            f"DEBUG: User: {self.request.user}, PK: {apartment_id}, Count: {qs.count()}"
        )
        return qs


class ReceiptPrint(DetailView):
    model = Receipt
    template_name = "receipt_example.html"


def download_receipt(request, pk):
    receipt = Receipt.objects.get(pk=pk)

    services_cost = receipt.servicefullcost_set.all()
    fullcost = sum(a.full_cost for a in services_cost)
    context = {
        "receipt": receipt,
        "fullcost": fullcost,
    }

    html_content = render_to_string("receipt_example.html", context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{receipt.number}.pdf"'

    HTML(string=html_content).write_pdf(response)

    return response


class ReceiptPay(CreateView):
    model = CashBox
    template_name = "owner_receipt_pay.html"
    form_class = CashBoxForm

    def get_receipt(self):
        return get_object_or_404(Receipt, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receipt_obj = self.get_receipt()
        context["receipt"] = receipt_obj
        full_cost = (
            receipt_obj.servicefullcost_set.aggregate(total=Sum("full_cost"))["total"]
            or 0
        )
        paid = receipt_obj.cashbox_set.aggregate(total=Sum("sum"))["total"] or 0
        context["fullcost"] = full_cost - paid
        return context

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        receipt_obj = self.get_receipt()
        full_cost = (
            receipt_obj.servicefullcost_set.aggregate(total=Sum("full_cost"))["total"]
            or 0
        )
        paid = receipt_obj.cashbox_set.aggregate(total=Sum("sum"))["total"] or 0
        cost = full_cost - paid
        sum = form.cleaned_data.get("sum")
        if sum < cost:
            receipt_obj.status = "PT"
        elif sum >= cost and receipt_obj.bankbook:
            receipt_obj.status = "PD"

            receipt_obj.save()

            Counter.objects.filter(
                id__in=receipt_obj.counter_ids, status="TAKEN"
            ).update(status="TAKEN_AND_PAID")

        elif sum == cost and not receipt_obj.bankbook:
            receipt_obj.status = "PD"

        elif sum > cost and not receipt_obj.bankbook:
            messages.error(
                request, "Сумма превышает стоимость, а лицевой счет не указан."
            )
            return redirect(request.path)

        receipt_obj.save()
        self.object = form.save(commit=False)
        self.object.status = "CM"
        self.object.receipt = receipt_obj
        self.object.bank_book = receipt_obj.bankbook
        self.object.save(generate_number=True)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("owner:receipt-detail", kwargs={"pk": self.object.receipt.pk})


class TariffDetail(DetailView):
    model = Apartment
    template_name = "owner_tariff.html"
    context_object_name = "tariff"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        tatiff = self.object.tariff
        context["tariff"] = tatiff
        return context
