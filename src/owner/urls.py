from django.urls import path

from .views import (
    ApartmentOwnerDetail,
    ProfileDetail,
    MasterCallListView,
    CreateMasterCall,
    MasterCallAjaxDatatable,
)

app_name = "owner"

urlpatterns = [
    path(
        "apartment/<int:pk>/", ApartmentOwnerDetail.as_view(), name="apartment-detail"
    ),
    path("profile/detail/", ProfileDetail.as_view(), name="profile-detail"),
    # master
    path("master/list/", MasterCallListView.as_view(), name="master-call-list"),
    path(
        "master/table/",
        MasterCallAjaxDatatable.as_view(),
        name="master-call-ajax-table",
    ),
    path("master/create/", CreateMasterCall.as_view(), name="master-call-create"),
]
