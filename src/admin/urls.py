from django.urls import path

from src.admin.views import CreateHouse, HouseAjaxTable, HouseList

app_name = "admin"

urlpatterns = [
    path("house/create/", CreateHouse.as_view(), name="create-house"),
    path("house/ajax/table/", HouseAjaxTable.as_view(), name="house-ajax-table"),
    path("house/list/", HouseList.as_view(), name="house-list"),
]
