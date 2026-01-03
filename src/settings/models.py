from django.db import models

# Create your models here.

from settings.choices import TransactionType


class UnitsOfMeasurement(models.Model):
    units = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.units or "---"


class Service(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    is_showing = models.BooleanField("Показывать", default=False)
    units_of_measure = models.ForeignKey(UnitsOfMeasurement, on_delete=models.CASCADE)


class Requisite(models.Model):
    title = models.CharField(max_length=200)
    information = models.TextField()


class Article(models.Model):
    title = models.CharField(max_length=200)
    type = models.CharField(choices=TransactionType)
