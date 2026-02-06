from ninja import NinjaAPI
from src.admin.api import router as admin_router
from src.owner.api import router as owner_router

api = NinjaAPI()

api.add_router("/admin", admin_router, tags=["Admin"])
api.add_router("/owner", owner_router, tags=["Owner"])
