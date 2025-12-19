from django.urls import path
from . import views
from .views import RegisterOwner


urlpatterns = [
    path('test/', RegisterOwner.as_view())
]