from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    UpdateView,
    DetailView,
    DeleteView,
    ListView,
)

from .forms import (
    MainPageForm,
    SeoBlockForm,
    ContactsForm,
    ServicesAndSeoBlockForm,
    ServicesForSiteFormSet,
    TariffsAndSeoBlockForm,
    TariffsForSiteFormSet,
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
    TariffsAndSeoBlock,
    AboutUsAndSeoBlock,
    Document,
    Images,
)


# Create your views here.
class EditMainPage(UpdateView):
    model = "MainPage"
    form_class = MainPageForm
    template_name = "admin/main_page.html"
    context_object_name = "main_page"

    def get_object(self, queryset=None):
        obj = MainPage.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = MainPage.objects.create(seo_block=seo_block)
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
        return reverse("managements:statistic")


class MainPageDetail(DetailView):
    model = "MainPage"
    template_name = "site/main_page.html"
    context_object_name = "main_page"

    def get_object(self, queryset=None):
        obj = MainPage.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = MainPage.objects.create(seo_block=seo_block)
        return obj


class EditContactsPage(UpdateView):
    model = "Contacts"
    form_class = ContactsForm
    template_name = "admin/contacts.html"
    context_object_name = "contacts"

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
    model = "Contacts"
    template_name = "site/contacts.html"
    context_object_name = "contacts"

    def get_object(self, queryset=None):
        obj = Contacts.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = Contacts.objects.create(seo_block=seo_block)
        return obj


class EditServicesPage(UpdateView):
    model = ServicesAndSeoBlock
    form_class = ServicesAndSeoBlockForm
    template_name = "admin/services.html"

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


class DeleteServiceView(DeleteView):
    model = ServicesForSite

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class ServicesView(ListView):
    model = ServicesForSite
    template_name = "site/services.html"
    context_object_name = "services"


class EditTariffsPage(UpdateView):
    model = TariffsAndSeoBlock
    form_class = TariffsAndSeoBlockForm
    template_name = "admin/tariffs.html"

    def get_object(self, queryset=None):
        obj = TariffsAndSeoBlock.objects.first()
        if not obj:
            seo_block = SeoBlock.objects.create()
            obj = TariffsAndSeoBlock.objects.create(seo_block=seo_block)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seo_instance = self.object.seo_block
        if self.request.POST:
            context["seo_form"] = SeoBlockForm(self.request.POST, instance=seo_instance)
            context["tariffs_formset"] = TariffsForSiteFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            context["seo_form"] = SeoBlockForm(instance=seo_instance)
            context["tariffs_formset"] = TariffsForSiteFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        seo_form = context["seo_form"]
        tariffs_formset = context["tariffs_formset"]

        if seo_form.is_valid() and tariffs_formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                seo_form.save()
                tariffs_formset.save()
            return super().form_valid(form)
        else:
            print(f"ERRORS: {seo_form.errors}")
            print(f"ERRORS: {tariffs_formset.errors}")

    def get_success_url(self):
        return reverse("admin:statistic")


class DeleteTariffView(DeleteView):
    model = TariffsForSite

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class EditAboutUsPage(UpdateView):
    model = AboutUsAndSeoBlock
    form_class = AboutUsAndSeoBlockForm
    template_name = "admin/about_us.html"
    context_object_name = "about_us"

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


class DeleteImageView(DeleteView):
    model = Images
    success_url = reverse_lazy("admin:statistic")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class DeleteDocument(DeleteView):
    model = Document

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({"success": True})

    post = delete


class AboutUsView(ListView):
    model = AboutUsAndSeoBlock
    template_name = "site/about_us.html"
    context_object_name = "about_us"
