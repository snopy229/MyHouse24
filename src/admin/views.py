# Create your views here.
from django.db import transaction
from django.views.generic import CreateView, UpdateView

from src.admin.forms import FloorFormSet, StaffFormSet
from src.admin.forms import HouseForm, SectionFormSet
from src.admin.models import House


class CreateHouse(CreateView):
    model = House
    form_class = HouseForm
    context_object_name = "house"
    template_name = "house.html"

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
