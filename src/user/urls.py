from django.urls import path
from .views import RegisterOwner


urlpatterns = [path("test/", RegisterOwner.as_view())]
