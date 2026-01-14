from django.db import models

from src.admin.choices import Status
from src.settings.models import Tariffs
from src.user.models import User


# Create your models here.
class House(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField()
    image1 = models.ImageField(upload_to="images/")
    image2 = models.ImageField(upload_to="images/")
    image3 = models.ImageField(upload_to="images/")
    image4 = models.ImageField(upload_to="images/")
    image5 = models.ImageField(upload_to="images/")
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
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariffs, on_delete=models.CASCADE)


class BankBook(models.Model):
    number = models.IntegerField(unique=True)
    status = models.CharField(choices=Status, max_length=10)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariffs, on_delete=models.CASCADE)
