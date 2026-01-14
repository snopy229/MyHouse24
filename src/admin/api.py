from typing import List, Optional

from ninja import Router

from src.user.models import User
from .models import House, Floor, Section, BankBook
from .schemas import (
    HouseSchema,
    FloorSchema,
    SectionSchema,
    OwnerSchema,
    BankBookSchema,
)

router = Router()


@router.get("/house", response=List[HouseSchema])
# @paginate(PageNumberPagination, page_size=10)
def lisr_house(request):
    return House.objects.all()


@router.get("/floor", response=List[FloorSchema])
# @paginate(PageNumberPagination, page_size=10)
def lisr_floors(request, house_id: Optional[int] = None):
    if house_id:
        return Floor.objects.filter(house_id=house_id)
    return []


@router.get("/section", response=List[SectionSchema])
# @paginate(PageNumberPagination, page_size=10)
def lisr_sections(request, house_id: Optional[int] = None):
    if house_id:
        return Section.objects.filter(house_id=house_id)
    return []


@router.get("/owner", response=List[OwnerSchema])
# @paginate(PageNumberPagination, page_size=10)
def lisr_owner(request):
    return User.objects.filter(is_staff=False)


@router.get("/bank_book", response=List[BankBookSchema])
def list_bank_books(request, owner_id: Optional[int] = None):
    if owner_id:
        return BankBook.objects.filter(owner_id=owner_id)
