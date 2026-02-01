from django.conf import settings
from django.shortcuts import redirect


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == settings.LOGOUT_REDIRECT_URL:
            return self.get_response(request)

        if request.path.startswith("/admin/"):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect("managements:main-page")

        return self.get_response(request)
