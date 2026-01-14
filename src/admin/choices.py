from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.TextChoices):
    PAID = "PAID", _("Оплачена")
    PARTIALLY = "PARTIALLY", _("Частично")
    UNPAID = "UNPAID", _("Неоплачен")
