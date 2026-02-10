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
    ReceiptAjaxTable,
    ReceiptList,
    ReceiptListConcrete,
    ReceiptDetail,
    download_receipt,
    ReceiptPrint,
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
    path("receipt/table/", ReceiptAjaxTable.as_view(), name="receipt-ajax-table"),
    path("receipt/list/", ReceiptList.as_view(), name="receipt-list"),
    path(
        "receipt/list/<int:pk>",
        ReceiptListConcrete.as_view(),
        name="receipt-list-concrete",
    ),
    path("receipt/detail/<int:pk>/", ReceiptDetail.as_view(), name="receipt-detail"),
    path("receipt/download/<int:pk>/", download_receipt, name="download-receipt"),
    path("receipt/print/<int:pk>/", ReceiptPrint.as_view(), name="receipt-print"),
]
