from django.core.paginator import Paginator
from django.urls import reverse
from ninja import Router, Query

from src.settings.models import Tariffs
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
        {"id": item.id, "text": f"{item.fullname}"} for item in current_page.object_list
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
    qs = BankBook.objects.filter(apartament=None)
    return get_select2_result(page, qs)


@router.get("/flat", response=Select2Response)
def list_flat(
    request, house_id: int | None = Query(None), q: str = Query(None), page: int = 1
):
    if not house_id:
        return {"results": [], "pagination": {"more": False}}

    qs = Apartment.objects.filter(house_id=house_id).order_by("number")
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
            "url": None,
        }

    return {
        "fullname": apartment.owner.fullname,
        "phone_number": apartment.owner.phone_number,
        "url": reverse("admin:detail-owner", args=(apartment.owner.id,)),
    }
