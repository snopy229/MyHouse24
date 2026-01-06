from typing import List

from ninja import Query, Schema, Router
from ninja.pagination import paginate, PageNumberPagination
from src.user.models import User, Role
from src.user.choices import Status
from .schemas import UserOut, UserFilter, RoleOut

router = Router()


@router.get("/users", response=List[UserOut])
@paginate(PageNumberPagination, page_size=50)
def list_users(request, filters: UserFilter = Query(...)):
    qs = User.objects.filter(is_staff=True)

    if filters.search:
        search_q = filters.filter_full_name(filters.search)
        qs = qs.filter(search_q)

    if filters.role_id:
        qs = qs.filter(role_id=filters.role_id)

    if filters.status:
        qs = qs.filter(status=filters.status)

    if filters.phone_number:
        qs = qs.filter(phone_number__icontains=filters.phone_number)

    if filters.email:
        qs = qs.filter(email__icontains=filters.email)

    return qs


@router.get("/roles", response=List[RoleOut])
def get_roles(request):
    return Role.objects.all()


class StatusOption(Schema):
    value: str
    label: str


@router.get("/statuses", response=List[StatusOption])
def get_statuses(request):
    return [{"value": val, "label": str(label)} for val, label in Status.choices]
