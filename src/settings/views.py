from ajax_datatable import AjaxDatatableView
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.utils.html import format_html
from django.views.generic import (
    UpdateView,
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    RedirectView,
)

from src.settings.forms import (
    UnitsFormSet,
    ServiceFormSet,
    ArticleForm,
    RequisiteForm,
    UserForm,
)
from src.settings.models import Service, UnitsOfMeasurement, Article, Requisite
from src.user.models import User, Role
from src.user.choices import Status


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
        services_formset = ServiceFormSet(
            request.POST, queryset=Service.objects.all(), prefix="services"
        )
        units_formset = UnitsFormSet(
            request.POST, queryset=UnitsOfMeasurement.objects.all(), prefix="units"
        )

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


class UsersPageView(TemplateView):
    template_name = "users.html"


class UserAjaxTable(AjaxDatatableView):
    model = User
    title = "Пользователи"
    initial_order = [["id", "asc"]]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, "all"]]
    search_values_separator = "+"

    column_defs = [
        {"name": "id", "visible": True, "searchable": False, "title": "#"},
        {
            "name": "first_name",
            "visible": True,
            "searchable": True,
            "title": "Пользователь",
            "orderable": True,
        },
        {
            "name": "role",
            "foreign_field": "role__title",
            "visible": True,
            "searchable": True,
            "title": "Роль",
            "choices": list(Role.objects.values_list("id", "title")),
            "lookup_field": "__id",
        },
        {
            "name": "phone_number",
            "visible": True,
            "searchable": True,
            "title": "Телефон",
        },
        {"name": "email", "visible": True, "searchable": True, "title": "Email"},
        {
            "name": "status",
            "visible": True,
            "searchable": True,
            "title": "Статус",
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
        row["first_name"] = f"{obj.first_name} {obj.second_name}"
        row["role__title"] = obj.role.title if obj.role else "—"

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="/admin/settings/user/edit/{0}/" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="/admin/settings/user/delete/{0}/" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            obj.id,
        )
        return


class EditUsersPageView(UpdateView):
    model = User
    form_class = UserForm
    context_object_name = "user"
    template_name = "edit_user.html"
    success_url = reverse_lazy("managements:statistic")

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


class SendInvite(RedirectView):
    pattern_name = "settings:users-list"

    def get_redirect_url(self, **kwargs):
        user_id = self.kwargs.get("pk")
        user = get_object_or_404(User, pk=user_id)
        try:
            send_mail(
                subject="Тест",
                message=f"Пользователь:{user.email}, вернись на сайт",
                from_email=None,
                recipient_list=[user.email],
            )
        except Exception as e:
            print(f"Ошибка отправки: {e}")

        return super().get_redirect_url()


class DeleteUsersView(DeleteView):
    def post(self, request, pk):
        article = get_object_or_404(User, pk=pk)
        article.delete()
        return redirect("settings:users-list")


class CreateUser(CreateView):
    model = User
    form_class = UserForm
    template_name = "create_user.html"
    success_url = reverse_lazy("settings:users-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_staff = True

        raw_password = form.cleaned_data.get("password1")

        try:
            with transaction.atomic():
                user.save()

                role_name = form.cleaned_data.get("role")
                if role_name:
                    Role.objects.update_or_create(
                        user=user,
                        defaults={"name": role_name},
                    )

                user_email = form.cleaned_data.get("email")
                send_mail(
                    subject="Изменение пароля",
                    message=f"Новый пароль: {raw_password}",
                    from_email=None,
                    recipient_list=[user_email],
                )
        except Exception as e:
            print(f"ОШИБКА: {e}")
            import traceback

            traceback.print_exc()
            form.add_error(None, f"Ошибка: {e}")
            return self.form_invalid(form)

        return HttpResponseRedirect(reverse_lazy("settings:users-list"))
