from django.urls import path

from .views import (
    ApartmentOwnerDetail,
    ProfileDetail,
    MasterCallListView,
    CreateMasterCall,
    MasterCallAjaxDatatable,
    MessageDetail,
    DeleteMasterCall,
    MessageList,
    MessageAjaxDatatable,
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
    path(
        "master/delet/<int:pk>/", DeleteMasterCall.as_view(), name="master-call-delete"
    ),
    path("message/detail/<int:pk>/", MessageDetail.as_view(), name="message-detail"),
    path("message/list/", MessageList.as_view(), name="message-list"),
    path("message/teble/", MessageAjaxDatatable.as_view(), name="message-ajax-table"),
]
