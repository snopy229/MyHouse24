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
    EditTariffsPage,
    DeleteTariffView,
    DeleteImageView,
    EditAboutUsPage,
    DeleteDocument,
)

app_name = "managements"

urlpatterns = [
    # admin
    path("admin/main-page/", EditMainPage.as_view(), name="edit-main-page"),
    path("admin/statistic/", Statistic.as_view(), name="statistic"),
    path("admin/contacts/", EditContactsPage.as_view(), name="edit-contacts"),
    path("admin/services/", EditServicesPage.as_view(), name="edit-services"),
    path("admin/tariffs", EditTariffsPage.as_view(), name="edit-tariffs"),
    path("admin/about-us/", EditAboutUsPage.as_view(), name="edit-about-us"),
    # site
    path("", MainPageDetail.as_view(), name="main-page"),
    path("contacts/", ContactsDetail.as_view(), name="contacts-page"),
    path("sirvices/", ServicesView.as_view(), name="services"),
    # delete
    path(
        "delete-service/<int:pk>/", DeleteServiceView.as_view(), name="delete_service"
    ),
    path("delete/tariff/<int:px>/", DeleteTariffView.as_view(), name="delete_tariff"),
    path("delete/image/<int:pk>/", DeleteImageView.as_view(), name="delete_image"),
    path("delete/document/<int:pk>", DeleteDocument.as_view(), name="delete_document"),
]
