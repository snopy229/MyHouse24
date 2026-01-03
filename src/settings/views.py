from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
)

from src.settings.forms import UnitsFormSet, ServiceFormSet, ArticleForm, RequisiteForm
from src.settings.models import Service, UnitsOfMeasurement, Article, Requisite


# Create your views here
class EditServicesView(TemplateView):
    template_name = "edit_services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Загружаем услуги (prefix='services')
        if "services" not in context:
            context["services"] = ServiceFormSet(
                queryset=Service.objects.all(), prefix="services"
            )

        # Загружаем единицы измерения (prefix='units')
        if "units" not in context:
            context["units"] = UnitsFormSet(
                queryset=UnitsOfMeasurement.objects.all(), prefix="units"
            )
        return context

    def post(self, request, *args, **kwargs):
        services_formset = ServiceFormSet(request.POST, prefix="services")
        units_formset = UnitsFormSet(request.POST, prefix="units")

        if services_formset.is_valid() and units_formset.is_valid():
            services_formset.save()
            units_formset.save()
            return redirect("managements:statistic")  # Ваш редирект

        return self.render_to_response(
            self.get_context_data(
                services=services_formset,
                units=units_formset,
            )
        )


class ArticleList(ListView):
    model = Article
    template_name = "article_list.html"
    context_object_name = "articles"
    ordering = ["-title"]


class ArticleEdit(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "article.html"
    success_url = reverse_lazy("settings:article-list")


class ArticleCreate(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "article.html"
    success_url = reverse_lazy("settings:article-list")


class ArticleDelete(DeleteView):
    def post(self, request, pk):
        article = get_object_or_404(Article, pk=pk)
        article.delete()
        return redirect("settings:article-list")


class RequisiteEdit(UpdateView):
    model = Requisite
    form_class = RequisiteForm
    template_name = "requisite.html"
    success_url = reverse_lazy("managements:statistic")

    def get_object(self, **kwargs):
        obj = Requisite.objects.first()
        if not obj:
            obj = Requisite.objects.create()

        return obj
