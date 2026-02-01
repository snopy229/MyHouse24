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
    DetailOwner,
    OwnerAjaxTable,
    DeleteOwner,
    FlatDetail,
    CreateBankBook,
    BankBookListView,
    BankBookAjaxTable,
    UpdateBankBook,
    DeleteBankBook,
    download_xlsx,
    CounterAjaxTable,
    CounterList,
    CreateCounter,
    CounterSpecificList,
    CounterSpecificAjaxTable,
    CounterEdit,
    CounterDetail,
    DeleteCounter,
    CreateMasterCall,
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
    path("flat/detail/<int:pk>/", FlatDetail.as_view(), name="flat-detail"),
    # Owner
    path("owner/create/", CreateOwner.as_view(), name="create-owner"),
    path("owner/list/", ListOwner.as_view(), name="owner-list"),
    path("owner/edit/<int:pk>/", EditOwner.as_view(), name="edit-owner"),
    path("owner/detail/<int:pk>/", DetailOwner.as_view(), name="detail-owner"),
    path("owner/ajax/table/", OwnerAjaxTable.as_view(), name="owner-ajax-table"),
    path("owner/delete/<int:pk>/", DeleteOwner.as_view(), name="delete-owner"),
    # BankBook
    path("bankbook/create/", CreateBankBook.as_view(), name="create-bankbook"),
    path("bankbook/list/", BankBookListView.as_view(), name="bankbook-list"),
    path("banbook/table/", BankBookAjaxTable.as_view(), name="bankbook-ajax-table"),
    path("bankbook/edit/<int:pk>/", UpdateBankBook.as_view(), name="bankbook-edit"),
    path("bankbook/delete/<int:pk>/", DeleteBankBook.as_view(), name="bankbook-delete"),
    path("bankbook/download/", download_xlsx, name="bankbook-download"),
    # Counter
    path("counter/table", CounterAjaxTable.as_view(), name="counter-ajax-table"),
    path("counter/list/", CounterList.as_view(), name="counter-list"),
    path("counter/create/", CreateCounter.as_view(), name="counter-create"),
    path(
        "counter/list-specific/",
        CounterSpecificList.as_view(),
        name="counter-specific-list",
    ),
    path(
        "counter/specific-table/",
        CounterSpecificAjaxTable.as_view(),
        name="counter-specific-ajax-table",
    ),
    path("counter/edit/<int:pk>/", CounterEdit.as_view(), name="counter-edit"),
    path("counter/detail/<int:pk>/", CounterDetail.as_view(), name="counter-detail"),
    path("counter/delete/<int:pk>/", DeleteCounter.as_view(), name="counter-delete"),
    # Master call
    path("master-call/create/", CreateMasterCall.as_view(), name="create-master-call"),
]
