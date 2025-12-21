from django.urls import path, reverse_lazy
from .views import RegisterOwner, LogInOwner, LogInStaff
from django.contrib.auth import views as auth_views

app_name = "user"

urlpatterns = [
    path("register/", RegisterOwner.as_view(), name="register"),
    path("login-owner/", LogInOwner.as_view(), name="login-owner"),
    path("login-staff/", LogInStaff.as_view(), name="login-staff"),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=reverse_lazy("user:login-owner")),
        name="logout",
    ),
]
