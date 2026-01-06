from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    active = "active", _("Активные")
    new = "new", _("Новые")
    inactive = "inactive", _("Отключенный")
