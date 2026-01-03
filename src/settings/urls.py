from django.urls import path

from settings.views import (
    EditServicesView,
    ArticleList,
    ArticleEdit,
    ArticleCreate,
    ArticleDelete,
    RequisiteEdit,
)

app_name = "settings"

urlpatterns = [
    path("services/", EditServicesView.as_view(), name="edit-services"),
    path("article-list/", ArticleList.as_view(), name="article-list"),
    path("article-edit/<int:pk>/", ArticleEdit.as_view(), name="article-edit"),
    path("article-create/", ArticleCreate.as_view(), name="article-create"),
    path("article-delete/<int:pk>/", ArticleDelete.as_view(), name="article-delete"),
    path("requisite-edit/", RequisiteEdit.as_view(), name="requisite-edit"),
]
