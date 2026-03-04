from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse
from ninja import Router, Query

from src.settings.models import Tariffs, Service, Article
from src.user.models import User
from .models import House, Floor, Section, BankBook, Apartment
from .schemas import Select2Response

router = Router()


def get_select2_result(page, qs):
    qs = qs.order_by("id")
    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)
    result = [{"id": item.id, "text": item.title} for item in current_page.object_list]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/house", response=Select2Response)
def list_house(request, q: str = Query(None), page: int = 1):
    qs = House.objects.all().order_by("id")
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_result(page, qs)


@router.get("/section", response=Select2Response)
def list_section(
    request, house_id: int | None = Query(None), q: str = Query(None), page: int = 1
):
    if not house_id:
        return {"results": [], "pagination": {"more": False}}

    qs = Section.objects.filter(house_id=house_id)
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_result(page, qs)


@router.get("/floor", response=Select2Response)
def list_floor(
    request, house_id: int | None = Query(None), q: str = Query(None), page: int = 1
):
    if not house_id:
        return {"results": [], "pagination": {"more": False}}

    qs = Floor.objects.filter(house_id=house_id)
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_result(page, qs)


@router.get("/owner", response=Select2Response)
def list_owner(request, q: str = Query(None), page: int = 1):
    qs = User.objects.filter(is_staff=False).order_by("id")

    if q:
        qs = qs.filter(title__icontains=q)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [
        {"id": item.id, "text": f"{item.fullname if item.fullname else item.email}"}
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/tariff", response=Select2Response)
def list_tariff(request, q: str = Query(None), page: int = 1):
    qs = Tariffs.objects.all()
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_result(page, qs)


@router.get("/bank_book", response=Select2Response)
def list_bank_book(request, q: str = Query(None), page: int = 1):
    qs = BankBook.objects.filter(apartment=None)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [
        {"id": item.id, "text": str(item.number)} for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/flat", response=Select2Response)
def list_flat(
    request,
    house_id: int | None = Query(None),
    section_id: int | None = Query(None),
    floor_id: int | None = Query(None),
    q: str = Query(None),
    page: int = 1,
):
    if not house_id:
        return {"results": [], "pagination": {"more": False}}

    if house_id:
        qs = Apartment.objects.filter(house_id=house_id).order_by("number")

    if section_id is not None:
        qs = Apartment.objects.filter(section_id=section_id).order_by("number")

    if floor_id is not None:
        qs = Apartment.objects.filter(floor_id=floor_id).order_by("number")

    if q:
        qs = qs.filter(number__icontains=q)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [
        {"id": item.id, "text": str(item.number)} for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/flat/master", response=Select2Response)
def list_flat_master(
    request,
    owner_id: str | int | None = Query(None),
    q: str = Query(None),
    page: int = 1,
):
    if not owner_id:
        qs = Apartment.objects.all().order_by("number")

    if owner_id:
        qs = Apartment.objects.filter(owner_id=owner_id).order_by("number")
    if q:
        qs = qs.filter(number__icontains=q)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [
        {"id": item.id, "text": str(item.number)} for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/apartment/{apartment_id}/owner")
def apartment_owner(request, apartment_id: int):
    apartment = Apartment.objects.select_related("owner").get(id=apartment_id)

    if not apartment.owner:
        return {
            "fullname": "не указано",
            "phone_number": "не указано",
            "url_owner": None,
            "url_phone": None,
        }

    return {
        "fullname": apartment.owner.fullname
        if apartment.owner.fullname
        else apartment.owner.email,
        "phone_number": str(apartment.owner.phone_number),
        "url_owner": reverse("admin:detail-owner", args=(apartment.owner.id,)),
        "url_phone": f"tel:{apartment.owner.phone_number}",
    }


@router.get("/services", response=Select2Response)
def list_service(request, q: str = Query(None), page: int = 1):
    qs = Service.objects.filter(is_showing=True).select_related("units_of_measure")
    if q:
        qs = qs.filter(title__icontains=q)
    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)
    result = [
        {"id": item.id, "text": f"{item.title} ({item.units_of_measure.units})"}
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/owner-with-apartments", response=Select2Response)
def list_owner_with_apartments(
    request,
    q: str = Query(None),
    page: int = 1,
    apartment_id: str | int | None = Query(None),
):
    if apartment_id:
        apartment = (
            Apartment.objects.select_related("owner").filter(id=apartment_id).first()
        )

        if not apartment or not apartment.owner:
            return {"results": [], "pagination": {"more": False}}

        owner = apartment.owner

        return {
            "results": [
                {
                    "id": owner.id,
                    "text": owner.fullname if owner.fullname else owner.email,
                }
            ],
            "pagination": {"more": False},
        }

    qs = User.objects.filter(apartment__isnull=False).distinct()

    if q:
        qs = qs.filter(
            Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
        )

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [
        {"id": item.id, "text": f"{item.fullname if item.fullname else item.email}"}
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/master", response=Select2Response)
def list_master(
    request,
    q: str = Query(None),
    page: int = 1,
    master_type_id: str | int | None = Query(None),
    house_id: str | int | None = Query(None),
):
    qs = User.objects.exclude(role__title__in=["Директор", "Управляющий", "Бухгалтер"])
    if q:
        qs = qs.filter(
            Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(role_title__icontains=q)
        )
    if master_type_id:
        qs = User.objects.filter(role__id=master_type_id)

    if house_id:
        qs = User.objects.filter(owner=house_id)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [
        {
            "id": item.id,
            "text": f"{item.role.title}-{item.fullname if item.fullname else item.email}",
        }
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/manager", response=Select2Response)
def list_manager(request, q: str = Query(None), page: int = 1):
    qs = User.objects.exclude(
        role__title__in=["Управляющий", "Бухгалтер", "Электрик"]
    ).order_by("role__title")
    if q:
        qs = qs.filter(
            Q(username__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(role_title__icontains=q)
        )
    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)
    result = [
        {
            "id": item.id,
            "text": f"{item.role.title}-{item.fullname if item.fullname else item.email}",
        }
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/article-coming", response=Select2Response)
def list_coming_article(request, q: str = Query(None), page: int = 1):
    qs = Article.objects.filter(type="IN")
    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)
    result = [
        {
            "id": item.id,
            "text": f"{item.title}",
        }
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/article-out-go", response=Select2Response)
def list_out_go_article(request, q: str = Query(None), page: int = 1):
    qs = Article.objects.filter(type="OUT")
    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)
    result = [
        {
            "id": item.id,
            "text": f"{item.title}",
        }
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/bank_book_owner", response=Select2Response)
def list_bank_book_owner(
    request,
    owner_id: str | int | None = Query(None),
    q: str = Query(None),
    page: int = 1,
):
    if owner_id:
        qs = BankBook.objects.filter(apartment__owner_id=owner_id).order_by("number")
    if not owner_id:
        return {"results": [], "pagination": {"more": False}}

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)
    result = [
        {
            "id": item.id,
            "text": str(item.number),
        }
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/get_bank_book_owner")
def get_bank_book(request, apartment_id):
    bank_book = get_object_or_404(BankBook, apartment_id=apartment_id)
    return {"bank_book": bank_book.number}


@router.get("/article", response=Select2Response)
def lisr_article(request, q: str = Query(None), page: int = 1):
    qs = Article.objects.all().order_by("id")
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_result(page, qs)
