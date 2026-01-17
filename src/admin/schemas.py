from typing import List

from ninja import Schema


class Select2Option(Schema):
    id: int | str
    text: str


class Select2Response(Schema):
    results: List[Select2Option]
    pagination: dict
