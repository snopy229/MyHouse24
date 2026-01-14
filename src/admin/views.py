# Create your views here.
from ajax_datatable import AjaxDatatableView
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.html import format_html
from django.views.generic import CreateView, UpdateView, TemplateView, DeleteView

from .forms import FloorFormSet, StaffFormSet, ApartmentForm, HouseForm, SectionFormSet
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
            context["section"] = SectionFormSet(self.request.POST, prefix="sections")
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
            "choices": list(House.objects.values_list("id", "title")),
        },
        {
            "name": "address",
            "visible": True,
            "searchable": True,
            "title": "Адрес",
            "choices": list(House.objects.values_list("id", "address")),
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
        return


class DeleteHouse(DeleteView):
    model = House

    def get(self, request, pk):
        article = get_object_or_404(House, pk=pk)
        article.delete()
        return redirect("admin:house-list")


class HouseList(TemplateView):
    template_name = "houses.html"


class CreateFlat(CreateView):
    model = Apartment
    template_name = "flat.html"
    form_class = ApartmentForm
    success_url = reverse_lazy("managements:statistic")


class ListFlat(TemplateView):
    template_name = "flats.html"
