from django.urls import path

from .views import (
    CreateHouse,
    HouseAjaxTable,
    HouseList,
    DeleteHouse,
    CreateFlat,
    ListFlat,
    EditHouse,
    FlatAjaxTable,
    EditFlat,
    DeleteFlat,
    CreateOwner,
    ListOwner,
    EditOwner,
    DetailHouse,
)

app_name = "admin"

urlpatterns = [
    # House
    path("house/create/", CreateHouse.as_view(), name="create-house"),
    path("house/ajax/table/", HouseAjaxTable.as_view(), name="house-ajax-table"),
    path("house/list/", HouseList.as_view(), name="house-list"),
    path("house/detail/<int:pk>/", DetailHouse.as_view(), name="detail-house"),
    path("house/delete/<int:pk>/", DeleteHouse.as_view(), name="delete-house"),
    path("house/edit/<int:pk>/", EditHouse.as_view(), name="edit-house"),
    # Flat
    path("flat/create/", CreateFlat.as_view(), name="create-flat"),
    path("flat/list/", ListFlat.as_view(), name="flat-list"),
    path("flat/ajax/table/", FlatAjaxTable.as_view(), name="flat-ajax-table"),
    path("flat/edit/<int:pk>/", EditFlat.as_view(), name="edit-flat"),
    path("flat/delete/<int:pk>/", DeleteFlat.as_view(), name="delete-flat"),
    # Owner
    path("owner/create/", CreateOwner.as_view(), name="create-owner"),
    path("owner/list/", ListOwner.as_view(), name="owner-list"),
    path("owner/edit/<int:pk>/", EditOwner.as_view(), name="edit-owner"),
]
