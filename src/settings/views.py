from ajax_datatable import AjaxDatatableView
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.html import format_html
from django.views.generic import (
    UpdateView,
    TemplateView,
    ListView,
    CreateView,
    DeleteView,
    RedirectView,
    DetailView,
    FormView,
)

from src.admin.tasks import send_password, send_invite
from src.settings.forms import (
    UnitsFormSet,
    ServiceFormSet,
    ArticleForm,
    RequisiteForm,
    UserForm,
    ServiceCostFormSet,
    TariffsForm,
    RoleFormSet,
    ServicesCostForm,
)
from src.settings.models import (
    Service,
    UnitsOfMeasurement,
    Article,
    Requisite,
    Tariffs,
    ServicesCost,
)
from src.user.models import User, Role
from src.user.choices import Status


class EditServicesView(TemplateView):
    template_name = "edit_services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "services" not in context:
            context["services"] = ServiceFormSet(
                queryset=Service.objects.all(), prefix="services"
            )

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
            return redirect("admin:statistic")  # Ваш редирект

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


class ArticleAjaxTable(AjaxDatatableView):
    model = Article
    title = "Статьи"
    column_defs = [
        {
            "name": "title",
            "title": "Название",
            "visible": True,
            "searchable": False,
            "orderable": False,
        },
        {
            "name": "type",
            "title": "Приход/расход",
            "visible": True,
            "searchable": False,
            "orderable": True,
        },
        {"name": "actions", "visible": True, "searchable": False, "orderable": False},
    ]

    def customize_row(self, row, obj):
        detail_url = reverse("settings:article-edit", args=[obj.id])
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        edit_url = reverse("settings:article-edit", args=[obj.id])
        delete_url = reverse("settings:article-delete", args=[obj.id])

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            edit_url,
            delete_url,
        )


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
    success_url = reverse_lazy("admin:settings")

    def get_object(self, **kwargs):
        obj = Requisite.objects.first()
        if not obj:
            obj = Requisite.objects.create()

        return obj


class UsersPageView(ListView):
    model = User
    template_name = "users.html"
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class()
        return context


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
            "searchable": False,
            "title": "Роль",
            "orderable": True,
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

        edit_url = reverse("settings:edit-user", args=[obj.id])
        delete_url = reverse("settings:delete-user", args=[obj.id])

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            edit_url,
            delete_url,
        )

        status_text = obj.get_status_display()

        if obj.status == Status.active:
            css_class = "label label-success"
        elif obj.status == Status.new:
            css_class = "label label-warning"
        elif obj.status == Status.inactive:
            css_class = "label label-danger"

        row["status"] = f'<small class="{css_class}">{status_text}</small>'

        detail_url = reverse("settings:user-detail", args=[obj.id])
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}

        return

    def get_initial_queryset(self, request=None):
        qs = super().get_initial_queryset().order_by("id")
        qs = qs.filter(is_staff=True)
        role = self.request.POST.get("role")
        if role:
            qs = qs.filter(role_id=role)
        return qs


class EditUsersPageView(UpdateView):
    model = User
    form_class = UserForm
    context_object_name = "staff"
    template_name = "edit_user.html"
    success_url = reverse_lazy("settings:users-list")

    def form_valid(self, form):
        raw_password = form.cleaned_data.get("password1")
        user_email = form.cleaned_data.get("email")
        if len(raw_password) != 0:
            send_password(raw_password, user_email).delay()

        return super().form_valid(form)


class SendInvite(RedirectView):
    pattern_name = "settings:users-list"

    def get_redirect_url(self, **kwargs):
        user_id = self.kwargs.get("pk")
        user = get_object_or_404(User, pk=user_id)
        send_invite(user.email).delay()

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
        user.save()

        role_name = form.cleaned_data.get("role")
        if role_name:
            Role.objects.update_or_create(
                user=user,
                defaults={"name": role_name},
            )

        raw_password = form.cleaned_data.get("password1")
        send_password.delay(raw_password, user.email)

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class DetailUser(DetailView):
    model = User
    template_name = "user_detail.html"
    context_object_name = "staff"


class TariffsCreateView(CreateView):
    model = Tariffs
    form_class = TariffsForm
    template_name = "tariff.html"
    success_url = reverse_lazy("settings:tariff-list")

    def get_initial(self):
        initial = super().get_initial()
        duplicate_id = self.request.GET.get("duplicate")
        if duplicate_id:
            original = Tariffs.objects.get(pk=duplicate_id)
            initial.update(
                {
                    "title": f"{original.title} (копия)",
                    "description": original.description,
                }
            )
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        duplicate_id = self.request.GET.get("duplicate")

        if self.request.POST:
            context["services"] = ServiceCostFormSet(
                self.request.POST, prefix="services"
            )
        else:
            if duplicate_id:
                original = Tariffs.objects.get(pk=duplicate_id)

                initial_data = [
                    {"service": sc.service_id, "cost": sc.cost}
                    for sc in original.services.all()
                ]

                DuplicateFormSet = inlineformset_factory(
                    Tariffs,
                    ServicesCost,
                    form=ServicesCostForm,
                    extra=len(initial_data),
                    can_delete=True,
                )

                context["services"] = DuplicateFormSet(
                    instance=None,
                    prefix="services",
                    initial=initial_data,
                    queryset=ServicesCost.objects.none(),
                )
            else:
                context["services"] = ServiceCostFormSet(
                    instance=None, prefix="services"
                )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["services"]

        if not formset.is_valid():
            return self.form_invalid(form)

        with transaction.atomic():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return redirect(self.success_url)


class TariffUpdateView(UpdateView):
    model = Tariffs
    form_class = TariffsForm
    template_name = "tariff.html"
    success_url = reverse_lazy("tariff_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = ServiceCostFormSet(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = ServiceCostFormSet(instance=self.object)
        context["title"] = "Редактирование тарифа"
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]

        with transaction.atomic():
            if formset.is_valid():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
                return super().form_valid(form)
            else:
                return self.form_invalid(form)


class TariffsList(ListView):
    model = Tariffs
    context_object_name = "tariffs"
    template_name = "tariffs.html"


class TariffsAjaxTable(AjaxDatatableView):
    model = Tariffs
    initial_order = [[0, "asc"]]

    def get_column_defs(self, request):
        columns = [
            {
                "name": "title",
                "title": "Название тарифа",
                "orderable": True,
                "searchable": False,
            },
            {
                "name": "description",
                "title": "Описание тарифа,",
                "orderable": False,
                "searchable": False,
            },
            {
                "name": "edited_at",
                "title": "Дата редактирования",
                "orderable": False,
                "searchable": False,
            },
            {
                "name": "actions",
                "title": "",
                "orderable": False,
                "searchable": False,
            },
        ]
        return columns

    def customize_row(self, row, obj):
        base_url = reverse("settings:tariff-create")
        duplicate_url = f"{base_url}?duplicate={obj.id}"
        edit_url = reverse("settings:tariff-edit", args=[obj.id])
        delete_url = reverse("settings:tariff-delete", args=[obj.id])

        row["actions"] = format_html(
            '<div class="btn-group btn-group-sm">'
            '<a href="{}" class="btn btn-default"><i class="fa fa-clone"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-default"><i class="fa fa-trash"></i></a>'
            "</div>",
            duplicate_url,
            edit_url,
            delete_url,
        )

        detail_url = reverse("settings:tariff-detail", args=[obj.id])
        row["DT_RowAttr"] = {"data-href": detail_url, "style": "cursor: pointer;"}


class TariffDetail(DetailView):
    model = Tariffs
    context_object_name = "tariff"
    template_name = "tariff_detail.html"


class TariffDelete(DeleteView):
    def get(self, request, pk):
        tariff = get_object_or_404(Tariffs, pk=pk)
        tariff.delete()
        return redirect("settings:tariff-list")


class EditRoles(FormView):
    template_name = "roles.html"

    def get_form(self, form_class=None):
        return RoleFormSet(self.request.POST or None, queryset=Role.objects.all())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
