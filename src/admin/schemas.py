from ninja import Schema


class HouseSchema(Schema):
    id: int
    title: str
    address: str


class SectionSchema(Schema):
    id: int
    title: str
    house_id: int


class FloorSchema(Schema):
    id: int
    title: str
    house_id: int


class OwnerSchema(Schema):
    id: int
    first_name: str
    last_name: str


class BankBookSchema(Schema):
    id: int
    number: int
    owner_id: int
