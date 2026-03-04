from django.urls import path

from .views import (
    EditMainPage,
    MainPageDetail,
    EditContactsPage,
    ContactsDetail,
    EditServicesPage,
    DeleteServiceView,
    ServicesView,
    DeleteTariffView,
    DeleteImageView,
    EditAboutUsPage,
    DeleteDocument,
    AboutUsView,
)

app_name = "managements"

urlpatterns = [
    # admin
    path("admin/main-page/", EditMainPage.as_view(), name="edit-main-page"),
    path("admin/contacts/", EditContactsPage.as_view(), name="edit-contacts"),
    path("admin/services/", EditServicesPage.as_view(), name="edit-services"),
    path("admin/about-us/", EditAboutUsPage.as_view(), name="edit-about-us"),
    # site
    path("", MainPageDetail.as_view(), name="main-page"),
    path("contacts/", ContactsDetail.as_view(), name="contacts-page"),
    path("sirvices/", ServicesView.as_view(), name="services"),
    path("about_us/", AboutUsView.as_view(), name="about_us"),
    # delete
    path(
        "delete-service/<int:pk>/", DeleteServiceView.as_view(), name="delete_service"
    ),
    path("delete/tariff/<int:px>/", DeleteTariffView.as_view(), name="delete_tariff"),
    path("delete/image/<int:pk>/", DeleteImageView.as_view(), name="delete_image"),
    path("delete/document/<int:pk>", DeleteDocument.as_view(), name="delete_document"),
]
