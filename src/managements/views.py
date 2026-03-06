from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
)

from src.admin.views import RedirectMixin
from .forms import (
    MainPageForm,
    SeoBlockForm,
    ContactsForm,
    ServicesAndSeoBlockForm,
    ServicesForSiteFormSet,
    AboutUsAndSeoBlockForm,
    DocumentFormSet,
)
from .models import (
    MainPage,
    SeoBlock,
    Contacts,
    ServicesAndSeoBlock,
    ServicesForSite,
    TariffsForSite,
    AboutUsAndSeoBlock,
    Document,
    Images,
)

# Create your views here.
from django.shortcuts import redirect


class EditMainPage(RedirectMixin, PermissionRequiredMixin, UpdateView):
    model = MainPage
    form_class = MainPageForm
    template_name = "admin/main_page.html"
    context_object_name = "main_page"
    permission_required = "role.has_site_management"

    def get_object(self, queryset=None):
        obj = MainPage.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = MainPage.objects.create(seo_block=seo_block)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object.seo_block
        if self.request.POST:
            context["seo_form"] = SeoBlockForm(self.request.POST, instance=instance)
        else:
            context["seo_form"] = SeoBlockForm(instance=instance)
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        seo_form = context["seo_form"]

        if seo_form.is_valid():
            self.object = form.save()
            seo_form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse("admin:statistic")


class MainPageDetail(DetailView):
    model = MainPage
    template_name = "site/main_page.html"
    context_object_name = "main_page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.object
        raw_slides = [obj.slide1, obj.slide2, obj.slide3]
        context['slides'] = [s for s in raw_slides if s]

        return context

    def get_object(self, queryset=None):
        obj = MainPage.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = MainPage.objects.create(seo_block=seo_block)
        return obj


class EditContactsPage(RedirectMixin, PermissionRequiredMixin, UpdateView):
    model = Contacts
    form_class = ContactsForm
    template_name = "admin/contacts.html"
    context_object_name = "contacts"
    permission_required = "role.has_site_management"

    def get_object(self, queryset=None):
        obj = Contacts.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = Contacts.objects.create(seo_block=seo_block)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo_instance = self.object.seo_block
        if self.request.POST:
            context["seo_form"] = SeoBlockForm(self.request.POST, instance=seo_instance)
        else:
            context["seo_form"] = SeoBlockForm(instance=seo_instance)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_form = context["seo_form"]

        if seo_form.is_valid():
            self.object = form.save()

            seo_form.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("admin:statistic")


class ContactsDetail(DetailView):
    model = Contacts
    template_name = "site/contacts.html"
    context_object_name = "contacts"

    def get_object(self, queryset=None):
        obj = Contacts.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = Contacts.objects.create(seo_block=seo_block)
        return obj


class EditServicesPage(RedirectMixin, PermissionRequiredMixin, UpdateView):
    model = ServicesAndSeoBlock
    form_class = ServicesAndSeoBlockForm
    template_name = "admin/services.html"
    permission_required = "role.has_site_management"

    def get_object(self, queryset=None):
        obj = ServicesAndSeoBlock.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = ServicesAndSeoBlock.objects.create(seo_block=seo_block)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo_instance = self.object.seo_block
        if self.request.POST:
            context["seo_form"] = SeoBlockForm(self.request.POST, instance=seo_instance)
            context["services_formset"] = ServicesForSiteFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["seo_form"] = SeoBlockForm(instance=seo_instance)
            context["services_formset"] = ServicesForSiteFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_form = context["seo_form"]
        services_formset = context["services_formset"]

        if seo_form.is_valid() and services_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                seo_form.save()
                services_formset.save()
            return super().form_valid(form)
        else:
            print(f"ERRORS: {seo_form.errors}")
            print(f"ERRORS: {services_formset.errors}")

        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("admin:statistic")


class DeleteServiceView(RedirectMixin, PermissionRequiredMixin, DeleteView):
    model = ServicesForSite
    permission_required = "role.has_site_management"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class ServicesView(ListView):
    model = ServicesForSite
    template_name = "site/services.html"
    context_object_name = "services"


class DeleteTariffView(RedirectMixin, PermissionRequiredMixin, DeleteView):
    model = TariffsForSite
    permission_required = "role.has_site_management"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class EditAboutUsPage(RedirectMixin, PermissionRequiredMixin, UpdateView):
    model = AboutUsAndSeoBlock
    form_class = AboutUsAndSeoBlockForm
    template_name = "admin/about_us.html"
    context_object_name = "about_us"
    permission_required = "role.has_site_management"

    def get_object(self, queryset=None):
        obj = AboutUsAndSeoBlock.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = AboutUsAndSeoBlock.objects.create(seo_block=seo_block)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo_instance = self.object.seo_block
        if self.request.POST:
            context["seo_form"] = SeoBlockForm(self.request.POST, instance=seo_instance)
            context["documents"] = DocumentFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["seo_form"] = SeoBlockForm(instance=seo_instance)
            context["documents"] = DocumentFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_form = context["seo_form"]
        document_formset = context["documents"]

        if seo_form.is_valid() and document_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                seo_form.save()
            document_formset.save()
            return super().form_valid(form)
        else:
            print(f"ERRORS: {seo_form.errors}")
            print(f"ERRORS: {document_formset.errors}")

    def get_success_url(self):
        return reverse("admin:statistic")


class AboutUsPage(DetailView):
    model = AboutUsAndSeoBlock
    template_name = "site/about_us.html"

    def get_object(self, queryset=None):
        obj = AboutUsAndSeoBlock.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = AboutUsAndSeoBlock.objects.create(seo_block=seo_block)
        return obj


class DeleteImageView(RedirectMixin, PermissionRequiredMixin, DeleteView):
    model = Images
    success_url = reverse_lazy("admin:statistic")
    permission_required = "role.has_site_management"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class DeleteDocument(RedirectMixin, PermissionRequiredMixin, DeleteView):
    model = Document
    permission_required = "role.has_site_management"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class AboutUsView(ListView):
    model = AboutUsAndSeoBlock
    template_name = "site/about_us.html"
    context_object_name = "about_us"
