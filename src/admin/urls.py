from django.urls import path

from src.admin.views import CreateHouse

app_name = "admin"

urlpatterns = [
    path("house/create/", CreateHouse.as_view(), name="create-house"),
]
