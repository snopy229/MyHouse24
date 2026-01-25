from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusBankBook(models.TextChoices):
    ACTIVE = "ACTIVE", _("Активен")
    INACTIVE = "INACTIVE", _("Неактивен")
