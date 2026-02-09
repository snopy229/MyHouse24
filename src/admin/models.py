from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models

from .choices import (
    StatusBankBook,
    StatusCounter,
    StatusCall,
    MasterType,
    StatusReceipt,
)
from src.settings.models import Tariffs, Service, UnitsOfMeasurement
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

    def __str__(self):
        return str(self.number)


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
    call_status = models.CharField(
        choices=StatusCall, blank=True, null=True, default="NEW"
    )


class Receipt(models.Model):
    number = models.IntegerField()
    date = models.DateField()
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.CharField(choices=StatusReceipt, default="UPD", max_length=10)
    tariff = models.ForeignKey(Tariffs, on_delete=models.CASCADE, blank=True, null=True)
    date_from = models.DateField()
    date_to = models.DateField()
    bankbook = models.ForeignKey(
        BankBook, on_delete=models.CASCADE, blank=True, null=True
    )
    is_catch = models.BooleanField(default=True)

    def clean(self):
        super().clean()
        if self.date_from > self.date_to:
            raise ValidationError(
                {"date_from": "Дата начала не может быть позже даты окончания."}
            )


class ServiceFullCost(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    cost = models.FloatField(blank=True, null=True)
    unit = models.ForeignKey(UnitsOfMeasurement, on_delete=models.CASCADE)
    full_cost = models.FloatField(blank=True, null=True)
    consumption = models.FloatField(blank=True, null=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)


class Message(models.Model):
    theme = models.CharField()
    message = RichTextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)


class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("message", "user")
