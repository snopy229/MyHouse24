from ninja import NinjaAPI

from src.settings.api import router as settings_router

api = NinjaAPI()

api.add_router("/settings", settings_router, tags=["settings"])
