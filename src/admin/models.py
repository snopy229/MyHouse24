from ckeditor.fields import RichTextField
from django.db import models

from src.admin.choices import StatusBankBook, StatusCounter, StatusCall, MasterType
from src.settings.models import Tariffs, Service
from src.user.models import User


# Create your models here.
class House(models.Model):
    title = models.CharField(blank=True, null=True, max_length=100)
    address = models.CharField(blank=True, null=True, max_length=100)
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
    area = models.IntegerField(blank=True, null=True)
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
    tariff = models.ForeignKey(Tariffs, on_delete=models.CASCADE, blank=True, null=True)

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
    date = models.DateField()
    status = models.CharField(choices=StatusCounter, default="NEW")
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    readings = models.FloatField()


class MasterCall(models.Model):
    date = models.DateField()
    time = models.TimeField()
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="owner_set"
    )
    master_type = models.CharField(choices=MasterType, default="ANY")
    description = models.TextField(blank=True, null=True)
    comment = RichTextField(blank=True, null=True)
    master = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="master_set"
    )
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    call_status = models.CharField(choices=StatusCall, default="NEW")
