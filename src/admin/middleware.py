from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse


class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == settings.LOGOUT_REDIRECT_URL:
            return self.get_response(request)

        if request.path.startswith("/admin/"):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect("home")

        return self.get_response(request)


class Redirect404ToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            if request.user.is_staff:
                return redirect(reverse("admin:error"))

        return response
