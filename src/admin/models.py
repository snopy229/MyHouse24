from django.db import models

from src.admin.choices import StatusBankBook, StatusCounter
from src.settings.models import Tariffs, Service
from src.user.models import User


# Create your models here.
class House(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField()
    image1 = models.ImageField(upload_to="images/", blank=True, null=True)
    image2 = models.ImageField(upload_to="images/", blank=True, null=True)
    image3 = models.ImageField(upload_to="images/", blank=True, null=True)
    image4 = models.ImageField(upload_to="images/", blank=True, null=True)
    image5 = models.ImageField(upload_to="images/", blank=True, null=True)
    owner = models.ManyToManyField(User, related_name="owner")

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Floor(models.Model):
    title = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Apartment(models.Model):
    number = models.IntegerField()
    area = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": False},
        blank=True,
        null=True,
    )
    tariff = models.ForeignKey(Tariffs, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)


class BankBook(models.Model):
    number = models.IntegerField(unique=True)
    status = models.CharField(
        choices=StatusBankBook, max_length=10, blank=True, null=True
    )
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Counter(models.Model):
    number = models.IntegerField(unique=True)
    created_at = models.DateField(auto_now_add=True)
    status = models.CharField(choices=StatusCounter, default="NEW")
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    readings = models.FloatField()
