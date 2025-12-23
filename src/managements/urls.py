from django.urls import path

from .views import (
    EditMainPage,
    Statistic,
    MainPageDetail,
    EditContactsPage,
    ContactsDetail,
    EditServicesPage,
    DeleteServiceView,
    ServicesView,
)

app_name = "managements"

urlpatterns = [
    path("admin/main-page/", EditMainPage.as_view(), name="edit-main-page"),
    path("admin/statistic/", Statistic.as_view(), name="statistic"),
    path("admin/contacts/", EditContactsPage.as_view(), name="edit-contacts"),
    path("", MainPageDetail.as_view(), name="main-page"),
    path("contacts/", ContactsDetail.as_view(), name="contacts-page"),
    path("admin/services/", EditServicesPage.as_view(), name="edit-services"),
    path(
        "delete-service/<int:pk>/", DeleteServiceView.as_view(), name="delete_service"
    ),
    path("sirvices/", ServicesView.as_view(), name="services"),
]
