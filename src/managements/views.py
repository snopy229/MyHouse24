from django.urls import reverse
from django.views.generic import TemplateView, UpdateView, DetailView

from .forms import MainPageForm, SeoBlockForm, ContactsForm
from .models import MainPage, SeoBlock, Contacts


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
        seo_form = context["seo_block_form"]

        if seo_form.is_valid():
            self.object = form.save()

            seo_form.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("management:statistic")


class Statistic(TemplateView):
    model = "ModelName"
    template_name = "admin/statistic.html"


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
        seo_form = context["seo_block_form"]

        if seo_form.is_valid():
            self.object = form.save()

            seo_form.save()

            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse("management:statistic")


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
