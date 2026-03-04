from django.shortcuts import redirect
from django.urls import reverse


class OwnerRedirect404ToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            if not request.user.is_staff:
                return redirect(reverse("owner:error"))

        return response
