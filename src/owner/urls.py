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
    message_bulk_delete,
    ReceiptPay,
    ReceiptConcreteAjaxTable,
    TariffDetail,
    EditUser,
    Error,
)

app_name = "owner"

urlpatterns = [
    path(
        "apartment/<int:pk>/", ApartmentOwnerDetail.as_view(), name="apartment-detail"
    ),
    path("profile/detail/", ProfileDetail.as_view(), name="profile-detail"),
    path("profile/edit/", EditUser.as_view(), name="profile-edit"),
    # master
    path("master/list/", MasterCallListView.as_view(), name="master-call-list"),
    path(
        "master/table/",
        MasterCallAjaxDatatable.as_view(),
        name="master-call-ajax-table",
    ),
    path("master/create/", CreateMasterCall.as_view(), name="master-call-create"),
    path(
        "master/delete/<int:pk>/", DeleteMasterCall.as_view(), name="master-call-delete"
    ),
    path("message/bulk/delete", message_bulk_delete, name="message_bulk_delete"),
    path("message/detail/<int:pk>/", MessageDetail.as_view(), name="message-detail"),
    path("message/list/", MessageList.as_view(), name="message-list"),
    path("message/table/", MessageAjaxDatatable.as_view(), name="message-ajax-table"),
    path("receipt/table/", ReceiptAjaxTable.as_view(), name="receipt-ajax-table"),
    path(
        "receipt/concrete/table/<int:pk>/",
        ReceiptConcreteAjaxTable.as_view(),
        name="receipt-concrete-ajax-table",
    ),
    path("receipt/list/", ReceiptList.as_view(), name="receipt-list"),
    path(
        "receipt/concrete/list/<int:pk>",
        ReceiptListConcrete.as_view(),
        name="receipt-list-concrete",
    ),
    path("receipt/pay/<int:pk>/", ReceiptPay.as_view(), name="receipt-pay"),
    path("receipt/detail/<int:pk>/", ReceiptDetail.as_view(), name="receipt-detail"),
    path("receipt/download/<int:pk>/", download_receipt, name="download-receipt"),
    path("receipt/print/<int:pk>/", ReceiptPrint.as_view(), name="receipt-print"),
    path("tariff/<int:pk>/", TariffDetail.as_view(), name="tariff-list"),
    path("error/", Error.as_view(), name="error"),
]
