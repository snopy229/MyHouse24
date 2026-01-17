from django.core.paginator import Paginator
from ninja import Router, Query

from src.settings.models import Tariffs
from src.user.models import User
from .models import House, Floor, Section, BankBook
from .schemas import Select2Response

# from .schemas import SectionSchema, FloorSchema, HouseSchema

router = Router()


def get_select2_reesult(page, qs):
    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)
    result = [{"id": item.id, "text": item.title} for item in current_page.object_list]
    return {"results": result, "pagination": {"more": current_page.has_next()}}


@router.get("/house", response=Select2Response)
def list_house(request, q: str = Query(None), page: int = 1):
    qs = House.objects.all()
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_reesult(page, qs)


@router.get("/section", response=Select2Response)
def list_section(
    request, house_id: int | None = Query(None), q: str = Query(None), page: int = 1
):
    if not house_id:
        return {"results": [], "pagination": {"more": False}}

    qs = Section.objects.filter(house_id=house_id)
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_reesult(page, qs)


@router.get("/floor", response=Select2Response)
def list_floor(
    request, house_id: int | None = Query(None), q: str = Query(None), page: int = 1
):
    if not house_id:
        return {"results": [], "pagination": {"more": False}}

    qs = Floor.objects.filter(house_id=house_id)
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_reesult(page, qs)


@router.get("/owner", response=Select2Response)
def list_owner(request, q: str = Query(None), page: int = 1):
    qs = User.objects.filter(is_staff=False)

    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_reesult(page, qs)


@router.get("/tariff", response=Select2Response)
def list_tariff(request, q: str = Query(None), page: int = 1):
    qs = Tariffs.objects.all()
    if q:
        qs = qs.filter(title__icontains=q)

    return get_select2_reesult(page, qs)


@router.get("/bank_book", response=Select2Response)
def list_bank_book(request, q: str = Query(None), page: int = 1):
    qs = BankBook.objects.filter(apartament=None)
    return get_select2_reesult(page, qs)
