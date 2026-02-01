from ajax_datatable import AjaxDatatableView
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import CharField, Value
from django.db.models.functions import Concat
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.html import format_html
from django.views.generic import (
    CreateView,
    UpdateView,
    TemplateView,
    DeleteView,
    DetailView,
    ListView,
)
from openpyxl import Workbook

from src.user.models import User
from src.user.choices import Status
from .choices import StatusBankBook, StatusCounter
from .forms import (
    FloorFormSet,
    StaffFormSet,
    ApartmentForm,
    HouseForm,
    SectionFormSet,
    OwnerForm,
    BankBookForm,
    CounterForm,
    MasterCallForm,
)
from src.admin.models import House, Apartment, BankBook, Counter, MasterCall


class CreateHouse(CreateView):
    model = House
    form_class = HouseForm
    context_object_name = "house"
    template_name = "house.html"
    success_url = reverse_lazy("admin:house-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["sections"] = SectionFormSet(self.request.POST, prefix="sections")
            context["floors"] = FloorFormSet(self.request.POST, prefix="floors")
            context["staff"] = StaffFormSet(self.request.POST, prefix="staff")
        else:
            context["sections"] = SectionFormSet(prefix="sections")
            context["floors"] = FloorFormSet(prefix="floors")
            context["staff"] = StaffFormSet(prefix="staff")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        sections = context["sections"]
        floors = context["floors"]
        staff = context["staff"]

        if sections.is_valid() and floors.is_valid() and staff.is_valid():
            with transaction.atomic():
                self.object = form.save()
                sections.instance = self.object
                floors.instance = self.object
                staff.instance = self.object
                sections.save()
                floors.save()
                staff.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class EditHouse(UpdateView):
    model = House
    form_class = HouseForm
    context_object_name = "house"
    template_name = "house.html"
    success_url = reverse_lazy("admin:house-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["sections"] = SectionFormSet(
                self.request.POST, instance=self.object, prefix="sections"
            )
            context["floors"] = FloorFormSet(
                self.request.POST, instance=self.object, prefix="floors"
            )
            context["staff"] = StaffFormSet(
                self.request.POST, instance=self.object, prefix="staff"
            )
        else:
            context["sections"] = SectionFormSet(
                instance=self.object, prefix="sections"
            )
            context["floors"] = FloorFormSet(instance=self.object, prefix="floors")
            context["staff"] = StaffFormSet(instance=self.object, prefix="staff")
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        sections = context["sections"]
        floors = context["floors"]
        staff = context["staff"]

        if sections.is_valid() and floors.is_valid() and staff.is_valid():
            with transaction.atomic():
                self.object = form.save()
                sections.instance = self.object
                floors.instance = self.object
                staff.instance = self.object
                sections.save()
                floors.save()
                staff.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class DetailHouse(DetailView):
    model = House
    template_name = "house_detail.html"
    context_object_name = "house"


class HouseAjaxTable(AjaxDatatableView):
    model = House
    title = "Дома"
    initial_order = [["id", "asc"]]
    column_defs = [
        {"name": "id", "visible": True, "searchable": False, "title": "#"},
        {
            "name": "title",
            "visible": True,
            "searchable": True,
            "title": "Название",
        },
        {
            "name": "address",
            "visible": True,
            "searchable": True,
            "title": "Адрес",
        },
        {
            "name": "actions",
            "visible": True,
            "searchable": False,
            "orderable": False,
            "title": "",
        },
    ]

    def customize_row(self, row, obj):
        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="/admin/house/edit/{0}/" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="/admin/house/delete/{0}/" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            obj.id,
        )

        detail_url = reverse("admin:detail-house", args=[obj.id])

        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}
        return


class DeleteHouse(DeleteView):
    model = House

    def get(self, request, pk):
        article = get_object_or_404(House, pk=pk)
        article.delete()
        return redirect("admin:house-list")


class HouseList(ListView):
    template_name = "houses.html"
    model = House
    context_object_name = "house"


class CreateFlat(CreateView):
    model = Apartment
    template_name = "flat.html"
    form_class = ApartmentForm

    def form_valid(self, form):
        self.object = form.save()

        if "save_and_copy" in self.request.POST:
            saved_data = {
                "house": self.object.house.id,
                "section": self.object.section.id,
                "floor": self.object.floor.id,
                "tariff": self.object.tariff.id,
            }
            self.request.session["copied_data"] = saved_data

            return redirect("admin:create-flat")

        return redirect("admin:flat-list")

    def get_initial(self):
        initial = super().get_initial()

        copied_data = self.request.session.pop("copied_data", None)
        if copied_data:
            initial.update(copied_data)

        return initial


class ListFlat(TemplateView):
    template_name = "flats.html"
    form_class = ApartmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "city" in self.request.GET:
            context["form"] = self.form_class(self.request.GET)
        else:
            context["form"] = self.form_class()

        return context


class FlatAjaxTable(AjaxDatatableView):
    model = Apartment
    title = "Квартиры"
    initial_order = [["number", "asc"]]

    def get_column_defs(self, request):
        house_choices = list(House.objects.all().values_list("id", "title"))
        return [
            {
                "name": "number",
                "title": "№ квартиры",
            },
            {
                "name": "house",
                "foreign_field": "house__title",
                "title": "Дом",
                "choices": house_choices,
            },
            {
                "name": "section",
                "foreign_field": "section__title",
                "title": "Секция",
                "visible": True,
                "searchable": False,
                "orderable": True,
            },
            {
                "name": "floor",
                "foreign_field": "floor__title",
                "title": "Секция",
                "visible": True,
                "searchable": False,
                "orderable": True,
            },
            {
                "name": "owner",
                "title": "Владелец",
                "visible": True,
                "searchable": True,
                "orderable": True,
            },
            {
                "name": "area",
                "title": "#",
                "visible": True,
                "searchable": True,
                "orderable": False,
            },
            {
                "name": "actions",
                "visible": True,
                "searchable": False,
                "orderable": False,
                "title": "",
            },
        ]

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset()

        house = self.request.POST.get("house")
        section = self.request.POST.get("section")
        floor = self.request.POST.get("floor")
        owner = self.request.POST.get("owner")

        if house:
            qs = qs.filter(house__id=house)
        if section:
            qs = qs.filter(section__id=section)
        if floor:
            qs = qs.filter(floor__id=floor)
        if owner:
            qs = qs.filter(owmer__id=owner)

        return qs

    def customize_row(self, row, obj):
        row["owner"] = f"{obj.owner.first_name} {obj.owner.second_name}"

        edit_url = reverse("admin:edit-flat", args=[obj.id])
        delete_url = reverse("admin:delete-flat", args=[obj.id])

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            edit_url,
            delete_url,
        )

        detail_url = reverse("admin:flat-detail", args=[obj.id])

        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}
        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'

        return row


class EditFlat(UpdateView):
    model = Apartment
    template_name = "flat.html"
    form_class = ApartmentForm
    success_url = reverse_lazy("admin:flat-list")


class FlatDetail(DetailView):
    model = Apartment
    template_name = "flat_detail.html"
    context_object_name = "apartment"


class DeleteFlat(DeleteView):
    model = Apartment

    def get(self, request, pk):
        flatt = get_object_or_404(Apartment, pk=pk)
        flatt.delete()
        return redirect("admin:flat-list")


class ListOwner(ListView):
    template_name = "owners.html"
    form_class = OwnerForm
    model = User
    context_object_name = "owner"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()

        return context

    def get_queryset(self):
        return User.objects.filter(is_staff=False)


class DetailOwner(DetailView):
    model = User
    template_name = "owner_detail.html"
    context_object_name = "owner"


class CreateOwner(CreateView):
    template_name = "owner.html"
    form_class = OwnerForm
    model = User
    context_object_name = "owner"
    success_url = reverse_lazy("admin:flat-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = False
        raw_password = form.cleaned_data.get("password1")
        user_email = form.cleaned_data.get("email")

        try:
            send_mail(
                subject="Создания пароля",
                message=f"Новый пароль: {raw_password}",
                from_email=None,
                recipient_list=[user_email],
            )
        except Exception as e:
            print(f"Ошибка отправки: {e}")

        return HttpResponseRedirect(reverse_lazy("admin:owner-list"))

    def form_invalid(self, form):
        print(">>> ОШИБКИ В ФОРМЕ:", form.errors)
        print(">>> ПРИШЕДШИЕ ДАННЫЕ:", form.data)

        return super().form_invalid(form)


class EditOwner(UpdateView):
    template_name = "owner.html"
    form_class = OwnerForm
    model = User
    context_object_name = "owner"
    success_url = reverse_lazy("admin:owner-list")

    def form_valid(self, form):
        raw_password = form.cleaned_data.get("password1")
        user_email = form.cleaned_data.get("email")
        if len(raw_password) != 0:
            try:
                send_mail(
                    subject="Изменение пароля",
                    message=f"Новый пароль: {raw_password}",
                    from_email=None,
                    recipient_list=[user_email],
                )
            except Exception as e:
                print(f"Ошибка отправки: {e}")

        return super().form_valid(form)


class OwnerAjaxTable(AjaxDatatableView):
    model = User
    title = "Квартиры"
    initial_order = [["full_name", "asc"]]

    def get_column_defs(self, request):
        return [
            {"name": "id_user", "title": "ID", "searchable": True, "orderable": False},
            {
                "name": "full_name",
                "title": "ФИО",
                "searchable": True,
                "orderable": True,
            },
            {
                "name": "phone_number",
                "title": "Телефон",
                "searchable": True,
                "orderable": False,
            },
            {
                "name": "email",
                "title": "E-mail",
                "searchable": True,
                "orderable": False,
            },
            {
                "name": "virtual_house",
                "title": "Дом",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "virtual_apartment",
                "title": "Квартира",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "date_joined",
                "title": "Добавлен",
                "searchable": True,
                "orderable": True,
            },
            {
                "name": "status",
                "title": "Статус",
                "searchable": True,
                "orderable": True,
                "choices": Status.choices,
            },
            {
                "name": "actions",
                "visible": True,
                "searchable": False,
                "orderable": False,
                "title": "",
            },
        ]

    def customize_row(self, row, obj):
        parts = [obj.second_name, obj.first_name, obj.last_name]
        row["full_name"] = " ".join(filter(None, parts))
        row["phone_number"] = obj.phone_number if obj.phone_number else ""

        detail_url = reverse("admin:detail-owner", args=[obj.id])
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        edit_url = reverse("admin:edit-owner", args=[obj.id])
        delete_url = reverse("admin:delete-owner", args=[obj.id])

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            edit_url,
            delete_url,
        )

        apartments = obj.apartment_set.all()

        if apartments:
            houses = set(a.house.title for a in apartments if a.house)
            row["virtual_house"] = ", ".join(houses)

            numbers = [str(a.number) for a in apartments if a.number]
            row["virtual_apartment"] = ", ".join(numbers)
        else:
            row["virtual_house"] = "(не задано)"
            row["virtual_apartment"] = "(не задано)"

        status_text = obj.get_status_display()

        if obj.status == Status.active:
            css_class = "label label-success"
        elif obj.status == Status.new:
            css_class = "label label-warning"
        elif obj.status == Status.inactive:
            css_class = "label label-danger"

        row["status"] = f'<small class="{css_class}">{status_text}</small>'

        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'

        return row

    def get_initial_queryset(self, request=None):
        qs = User.objects.filter(is_staff=False)

        qs = qs.annotate(
            full_name=Concat(
                "second_name",
                Value(" "),
                "first_name",
                Value(" "),
                "last_name",
                output_field=CharField(),
            )
        )

        qs = qs.annotate(
            virtual_house=Value("", output_field=CharField()),
            virtual_apartment=Value("", output_field=CharField()),
        )

        house_id = self.request.POST.get("house")
        apartment_id = self.request.POST.get("apartment")
        created_at = self.request.POST.get("created_at")

        if house_id:
            qs = qs.filter(apartment__house__id=house_id)

        if apartment_id:
            qs = qs.filter(apartment__id=apartment_id)

        if created_at:
            qs = qs.filter(date_joined__date=created_at)

        if house_id or apartment_id:
            qs = qs.distinct()

        return qs


class DeleteOwner(DeleteView):
    model = User

    def get(self, request, pk):
        house = get_object_or_404(User, pk=pk)
        house.delete()
        return redirect("admin:owner-list")


class CreateBankBook(CreateView):
    model = BankBook
    template_name = "bankbook.html"
    form_class = BankBookForm
    success_url = reverse_lazy("admin:bankbook-list")


class BankBookListView(ListView):
    model = BankBook
    template_name = "bankbooks.html"
    context_object_name = "bankbook"
    form_class = BankBookForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()

        return context


class UpdateBankBook(UpdateView):
    model = BankBook
    template_name = "bankbook.html"
    form_class = BankBookForm
    context_object_name = "bankbook"
    success_url = reverse_lazy("admin:bankbook-list")


def download_xlsx(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "XLSX"

    columns = ["Лицевой счет", "Статус", "Дом", "Секция", "Квартира", "Владелец"]
    ws.append(columns)
    qs = BankBook.objects.select_related("house", "apartment", "section").all()

    for book in qs:
        row = [
            book.number,
            book.get_status_display()
            if hasattr(book, "get_status_display")
            else book.status,
            book.house.title if book.house else "",
            book.section.title if book.section else "",
            book.apartment.number if book.apartment else "",
            book.apartment.owner.fullname if book.apartment.owner else "",
        ]
        ws.append(row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="bank_books.xlsx"'
    wb.save(response)

    return response


class DeleteBankBook(DeleteView):
    model = BankBook

    def get(self, request, pk):
        bankbook = get_object_or_404(BankBook, pk=pk)
        bankbook.delete()
        return redirect("admin:bankbook-list")


class BankBookAjaxTable(AjaxDatatableView):
    model = BankBook
    # initial_order = [['id', 'asc']]
    template_name = "bankbook.html"

    def get_column_defs(self, request=None):
        columns = [
            {"name": "number", "title": "№", "searchable": True},
            {
                "name": "status",
                "title": "Статус",
                "searchable": True,
                "choices": StatusBankBook.choices,
            },
            {
                "name": "apartment",
                "foreign_field": "apartment__number",
                "title": "Квартира",
                "searchable": True,
            },
            {
                "name": "house",
                "foreign_field": "house__title",
                "title": "Дом",
                "searchable": False,
            },
            {
                "name": "section",
                "foreign_field": "section__title",
                "title": "Секция",
                "searchable": False,
            },
            {
                "name": "owner",
                "foreign_field": "apartment__owner__last_name",
                "title": "Владелец",
                "searchable": False,
            },
            {
                "name": "actions",
                "title": "",
                "searchable": False,
            },
        ]
        return columns

    def customize_row(self, row, obj):
        status = obj.get_status_display()
        css_class = "label label-default"
        if obj.status == StatusBankBook.ACTIVE:
            css_class = "label label-success"
        elif obj.status == StatusBankBook.INACTIVE:
            css_class = "label label-danger"
        row["status"] = f'<small class="{css_class}">{status}</small>'

        detail_url = "#"
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        if obj.apartment.owner:
            row["owner"] = obj.apartment.owner.fullname

        edit_url = reverse("admin:bankbook-edit", args=[obj.id])
        delete_url = reverse("admin:bankbook-delete", args=[obj.id])

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            edit_url,
            delete_url,
        )

        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'

        return row

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset().order_by("id")

        house = self.request.POST.get("house")
        section = self.request.POST.get("section")
        owner = self.request.POST.get("owner")

        if house:
            qs = qs.filter(house__id=house)
        if section:
            qs = qs.filter(section__id=section)
        if owner:
            qs = qs.filter(apartment__owner__fullname=owner)

        return qs


class CreateCounter(CreateView):
    model = Counter
    form_class = CounterForm
    template_name = "counter.html"
    success_url = reverse_lazy("admin:counter-list")

    def get_initial(self):
        initial = super().get_initial()
        source_id = self.request.GET.get("source_id")

        if source_id:
            try:
                original = Counter.objects.get(pk=source_id)
                initial.update(
                    {
                        "house": original.house,
                        "section": original.section,
                        "apartment": original.apartment,
                        "service": original.service,
                    }
                )
            except Counter.DoesNotExist:
                pass
        return initial


class CounterList(ListView):
    model = Counter
    form_class = CounterForm
    template_name = "counters.html"
    context_object_name = "counters"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()

        return context


class CounterAjaxTable(AjaxDatatableView):
    model = Counter
    title = "Счетчики"
    initial_order = [[2, "asc"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "house",
                "title": "Дом",
                "foreign_field": "house__title",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "section",
                "title": "Секция",
                "foreign_field": "section__title",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "apartment",
                "title": "№ квартиры",
                "foreign_field": "apartment__number",
                "searchable": True,
                "orderable": True,
            },
            {
                "name": "service",
                "title": "Счетчик",
                "foreign_field": "service__title",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "readings",
                "title": "Текущие показания",
                "searchable": False,
                "orderable": False,
                "className": "rows",
            },
            {
                "name": "units",
                "foreign_field": "service__units_of_measure__units",
                "title": "Текущие показания",
                "className": "rows",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "actions",
                "searchable": False,
                "orderable": False,
            },
        ]
        return columns

    def customize_row(self, row, obj):
        detail_url = (
            reverse("admin:counter-specific-list") + f"?apartment_id={obj.apartment.id}"
        )
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        duplicate_url = reverse("admin:counter-create") + f"?source_id={obj.pk}"
        story_url = (
            reverse("admin:counter-specific-list") + f"?apartment_id={obj.apartment.id}"
        )

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-dashboard"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-eye"></i></a>'
            "</div>",
            duplicate_url,
            story_url,
        )

        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'

        return row

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset().order_by("id")

        house = self.request.POST.get("house")
        section = self.request.POST.get("section")
        service = self.request.POST.get("service")
        if house:
            qs = qs.filter(house__id=house)
        if section:
            qs = qs.filter(section__id=section)
        if service:
            qs = qs.filter(service__id=service)

        return qs


class CounterSpecificList(ListView):
    model = Counter
    form_class = CounterForm
    template_name = "counter_specific.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()

        return context


class CounterSpecificAjaxTable(AjaxDatatableView):
    model = Counter
    title = "Счетчики"
    initial_order = [[2, "des"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "number",
                "title": "№",
                "searchable": True,
                "orderable": False,
            },
            {
                "name": "status",
                "title": "Статус",
                "searchable": True,
                "orderable": False,
                "choices": StatusCounter.choices,
            },
            {
                "name": "date",
                "title": "Дата",
                "orderable": True,
                "searchable": True,
            },
            {
                "name": "service",
                "foreign_field": "service__title",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "readings",
                "title": "Показания",
                "searchable": False,
                "orderable": False,
                "className": "rows",
            },
            {
                "name": "units",
                "foreign_field": "service__units_of_measure__units",
                "searchable": False,
                "orderable": False,
                "className": "rows",
            },
            {
                "name": "actions",
                "searchable": False,
                "orderable": False,
            },
        ]
        return columns

    def customize_row(self, row, obj):
        status = obj.get_status_display()
        css_class = "label label-default"
        if obj.status == StatusCounter.NEW:
            css_class = "label label-warning"
        elif obj.status == StatusBankBook.TAKEN:
            css_class = "label label-success"
        elif obj.status == StatusBankBook.TAKEN_AND_PAID:
            css_class = "label label-success"
        elif obj.status == StatusBankBook.NULLABLE:
            css_class = "label label-primary"
        row["status"] = f'<small class="{css_class}">{status}</small>'

        detail_url = reverse("admin:counter-detail", args=[obj.id])
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        edit_url = reverse("admin:counter-edit", args=[obj.id])
        delete_url = reverse("admin:counter-delete", args=[obj.id])

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            edit_url,
            delete_url,
        )

        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'
        return row

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset(request)
        apartment_id = (
            self.request.POST.get("apartment_id")
            or self.request.GET.get("apartment_id")
            or self.request.POST.get("extra_data[apartment_id]")
        )
        return qs.filter(apartment_id=apartment_id)


class CounterDetail(DetailView):
    model = Counter
    template_name = "counter_detail.html"
    context_object_name = "counter"


class CounterEdit(UpdateView):
    model = Counter
    form_class = CounterForm
    template_name = "counter.html"
    success_url = reverse_lazy("admin:counter-list")
    context_object_name = "counter"


class DeleteCounter(DeleteView):
    model = Counter

    def get(self, request, pk):
        counter = get_object_or_404(Counter, pk=pk)
        counter.delete()
        return redirect("admin:counter-list")


class CreateMasterCall(CreateView):
    model = MasterCall
    form_class = MasterCallForm
    template_name = "master_call.html"
    success_url = reverse_lazy("managements:statistic")
