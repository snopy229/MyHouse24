from django.db import models
from django.utils.translation import gettext_lazy as _


class StatusBankBook(models.TextChoices):
    ACTIVE = "ACTIVE", _("Активен")
    INACTIVE = "INACTIVE", _("Неактивен")


class StatusCounter(models.TextChoices):
    NEW = "NEW", _("Новое")
    TAKEN = "TAKEN", _("Учтено")
    TAKEN_AND_PAID = "TAKEN_AND_PAID", _("Учтено и оплочено")
    NULLABLE = "NULLABLE", _("Нулевое")


class StatusCall(models.TextChoices):
    NEW = "NEW", _("Новое")
    IN_WORK = "IN WORK", _("В работе")
    COMPLETED = "COMPLETED", _("Выполнена")


class MasterType(models.TextChoices):
    PLUMBER = "PL", _("Сантехник")
    ELECTRICIAN = "EL", _("Электрик")
    LOCKSMITH = "LS", _("Слесарь")
    ANY = "ANY", _("Любой специалист")


class StatusReceipt(models.TextChoices):
    PAID = "PD", _("Оплачена")
    PART = "PT", _("Частично оплачена")
    UNPAID = "UPD", _("Неоплачена")
