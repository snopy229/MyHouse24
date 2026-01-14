from ninja import NinjaAPI
from src.admin.api import router as admin_router

api = NinjaAPI()

api.add_router("/admin", admin_router, tags=["Admin"])
