from typing import Optional

from django.db.models import Q
from ninja import FilterSchema, ModelSchema
from ninja import Field

from src.user.models import User, Role


class RoleOut(ModelSchema):
    class Meta:
        model = Role
        fields = ["id", "title"]


class UserOut(ModelSchema):
    role: Optional[RoleOut] = None
    status_label: str
    phone_number: str | None = None

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "second_name",
            "phone_number",
            "email",
            "status",
            "role",
        ]

    @staticmethod
    def resolve_status_label(obj):
        return obj.get_status_display()

    @staticmethod
    def resolve_phone_number(obj):
        if not obj.phone_number:
            return None
        return str(obj.phone_number)


class UserFilter(FilterSchema):
    search: Optional[str] = Field(None, alias="q")
    role_id: Optional[int] = Field(None, alias="role")
    status: Optional[str] = Field(None, alias="status")
    phone_number: Optional[str] = Field(None, alias="phone_number")
    email: Optional[str] = Field(None, alias="email")

    def filter_full_name(self, value: str) -> Q:
        if not value:
            return Q()

        parts = value.split()
        if len(parts) == 1:
            term = parts[0]
            return Q(first_name__icontains=term) | Q(second_name__icontains=term)

        if len(parts) >= 2:
            first_name = parts[0]
            last_name = parts[1]

            query_normal = Q(first_name__icontains=first_name) & Q(
                second_name__icontains=last_name
            )
            query_reverse = Q(first_name__icontains=last_name) & Q(
                second_name__icontains=first_name
            )

            return query_normal | query_reverse

        return Q()
