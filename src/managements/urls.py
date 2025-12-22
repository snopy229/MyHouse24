from django.urls import path

from .views import (
    EditMainPage,
    Statistic,
    MainPageDetail,
    EditContactsPage,
    ContactsDetail,
)

app_name = "managements"

urlpatterns = [
    path("admin/main-page/", EditMainPage.as_view(), name="edit-main-page"),
    path("admin/statistic/", Statistic.as_view(), name="statistic"),
    path("admin/contacts/", EditContactsPage.as_view(), name="edit-contacts"),
    path("", MainPageDetail.as_view(), name="main-page"),
    path("contacts/", ContactsDetail.as_view(), name="contacts-page"),
]
