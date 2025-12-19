from django.urls import path
from .views import RegisterOwner, LogInOwner


urlpatterns = [
    path("test/", RegisterOwner.as_view()),
    path("login/", LogInOwner.as_view()),]
