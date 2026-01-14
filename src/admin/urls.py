from django.urls import path

from .views import (
    CreateHouse,
    HouseAjaxTable,
    HouseList,
    DeleteHouse,
    CreateFlat,
    ListFlat,
    EditHouse,
)

app_name = "admin"

urlpatterns = [
    path("house/create/", CreateHouse.as_view(), name="create-house"),
    path("house/ajax/table/", HouseAjaxTable.as_view(), name="house-ajax-table"),
    path("house/list/", HouseList.as_view(), name="house-list"),
    path("house/delete/<int:pk>/", DeleteHouse.as_view(), name="delete-house"),
    path("house/edit/<int:pk>/", EditHouse.as_view(), name="edit-house"),
    path("flat/create/", CreateFlat.as_view(), name="create-flat"),
    path("flat/list/", ListFlat.as_view(), name="list-flat"),
]
