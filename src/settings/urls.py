from django.urls import path

from settings.views import DetailUser
from src.settings.views import (
    EditServicesView,
    ArticleList,
    ArticleEdit,
    ArticleCreate,
    ArticleDelete,
    RequisiteEdit,
    UsersPageView,
    EditUsersPageView,
    SendInvite,
    DeleteUsersView,
    CreateUser,
    UserAjaxTable,
    TariffsList,
    TariffsCreateView,
)

app_name = "settings"

urlpatterns = [
    path("services/", EditServicesView.as_view(), name="edit-services"),
    path("article-list/", ArticleList.as_view(), name="article-list"),
    path("article-edit/<int:pk>/", ArticleEdit.as_view(), name="article-edit"),
    path("article-create/", ArticleCreate.as_view(), name="article-create"),
    path("article-delete/<int:pk>/", ArticleDelete.as_view(), name="article-delete"),
    path("requisite-edit/", RequisiteEdit.as_view(), name="requisite-edit"),
    path("users-list/", UsersPageView.as_view(), name="users-list"),
    path("users-list/table/", UserAjaxTable.as_view(), name="user-ajax-table"),
    path("user/edit/<int:pk>/", EditUsersPageView.as_view(), name="edit-user"),
    path("user/invite/<int:pk>/", SendInvite.as_view(), name="send-invite"),
    path("user/delete/<int:pk>/", DeleteUsersView.as_view(), name="delete-user"),
    path("user/detail/<int:pk>/", DetailUser.as_view(), name="user-detail"),
    path("user/create_user/", CreateUser.as_view(), name="create-user"),
    path("tariff/list/", TariffsList.as_view(), name="tariff-list"),
    path("tariff/create", TariffsCreateView.as_view(), name="tariff-create"),
]
