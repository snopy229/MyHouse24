from django.urls import path
from .views import EditMainPage, Statistic

app_name = "managements"

urlpatterns = [
    path("admin/main-page/", EditMainPage.as_view(), name="edit-main-page"),
    path("admin/statistic/", Statistic.as_view(), name="statistic"),
]
