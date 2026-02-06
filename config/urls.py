"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from src.managements.views import MainPageDetail
from .api import api

urlpatterns = [
    path("user/", include("src.user.urls")),
    path("managements/", include("src.managements.urls")),
    path("admin/settings/", include("src.settings.urls")),
    path("admin/", include("src.admin.urls")),
    path("api/", api.urls),
    path("select2/", include("django_select2.urls")),
    path("owner/", include("src.owner.urls")),
    path("", MainPageDetail.as_view(), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
