from django.urls import path

from .views import ApartmentOwnerDetail, ProfileDetail

app_name = "owner"

urlpatterns = [
    path(
        "apartment/<int:pk>/", ApartmentOwnerDetail.as_view(), name="apartment-detail"
    ),
    path("profile/detail/", ProfileDetail.as_view(), name="profile-detail"),
]
