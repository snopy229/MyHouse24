from django.core.paginator import Paginator
from ninja import Router, Query

from src.admin.models import Apartment
from src.admin.schemas import Select2Response

router = Router()


@router.get("/flat", response=Select2Response)
def list_flat(
    request, q: str = Query(None), owner_id: int | None = Query(None), page: int = 1
):
    if not owner_id:
        return {"results": [], "pagination": {"more": False}}

    qs = Apartment.objects.filter(owner_id=owner_id).order_by("number")
    if q:
        qs = qs.filter(number__icontains=q)

    paginator = Paginator(qs, 10)
    current_page = paginator.get_page(page)

    result = [
        {
            "id": item.id,
            "text": f"{str(item.number)}{f', {item.house.title}' if item.house else ''}",
        }
        for item in current_page.object_list
    ]
    return {"results": result, "pagination": {"more": current_page.has_next()}}
