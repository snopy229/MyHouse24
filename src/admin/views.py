from ajax_datatable import AjaxDatatableView
from django.core.mail import send_mail
from django.db import transaction
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

from src.user.models import User
from .forms import (
    FloorFormSet,
    StaffFormSet,
    ApartmentForm,
    HouseForm,
    SectionFormSet,
    OwnerForm,
)
from src.admin.models import House, Apartment


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
    success_url = reverse_lazy("admin:flat-list")


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
        for key in row:
            if row[key] is None or row[key] == "":
                row[key] = '<span class="text-muted">(не задано)</span>'

        return row


class EditFlat(UpdateView):
    model = Apartment
    template_name = "flat.html"
    form_class = ApartmentForm
    success_url = reverse_lazy("admin:flat-list")


class DeleteFlat(DeleteView):
    model = Apartment

    def get(self, request, pk):
        flatt = get_object_or_404(Apartment, pk=pk)
        flatt.delete()
        return redirect("admin:flat-list")


class ListOwner(TemplateView):
    template_name = "owners.html"
    form_class = OwnerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "city" in self.request.GET:
            context["form"] = self.form_class(self.request.GET)
        else:
            context["form"] = self.form_class()

        return context


class CreateOwner(CreateView):
    template_name = "owner.html"
    form_class = OwnerForm
    model = User
    context_object_name = "owner"
    success_url = reverse_lazy("admin:flat-list")

    def form_valid(self, form):
        raw_password = form.cleaned_data.get("password1")
        user_email = form.cleaned_data.get("email")
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

        return super().form_valid(form)


class EditOwner(UpdateView):
    template_name = "owner.html"
    form_class = OwnerForm
    model = User
    context_object_name = "owner"
    success_url = reverse_lazy("admin:flat-list")

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
    initial_order = [["number", "asc"]]

    def get_column_defs(self, request):
        return [
            {
                "name": "id_user",
                "title": "ID",
                "searchable": True,
                "orderable": False,
            },
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
                "name": "house.title",
                "title": "Дом",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "flat.number",
                "title": "Квартира",
                "searchable": False,
                "orderable": False,
            },
            {
                "name": "created_at",
                "title": "Добавлен",
            },
        ]

    def customize_row(self, row, obj):
        row["full_name"] = f"{obj.second_name} {obj.first_name} {obj.last_name}"
