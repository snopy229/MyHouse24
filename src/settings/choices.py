from django.db import models
from django.utils.translation import gettext_lazy as _


class TransactionType(models.TextChoices):
    INCOME = "IN", _("Приход")
    EXPENSE = "OUT", _("Расход")
