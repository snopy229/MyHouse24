# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

from src.admin.models import Apartment
from src.user.views import User


class ApartmentOwnerDetail(DetailView):
    model = Apartment
    context_object_name = "apartment"
    template_name = "owner_apartment.html"


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = "detail.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        return self.request.user
