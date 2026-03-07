from django.db import models

# Create your models here.

from src.settings.choices import TransactionType


class UnitsOfMeasurement(models.Model):
    units = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.units or "---"


class Service(models.Model):
    title = models.CharField("Название", max_length=200)
    is_showing = models.BooleanField("Показывать", default=False)
    units_of_measure = models.ForeignKey(UnitsOfMeasurement, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Requisite(models.Model):
    title = models.CharField(max_length=200)
    information = models.TextField()


class Article(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(choices=TransactionType)

    def __str__(self):
        return self.title


class Tariffs(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ServicesCost(models.Model):
    tariff = models.ForeignKey(
        Tariffs, on_delete=models.PROTECT, related_name="services"
    )
    service = models.ForeignKey("Service", on_delete=models.PROTECT)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        unique_together = ("tariff", "service")