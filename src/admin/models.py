from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .choices import (
    StatusBankBook,
    StatusCounter,
    StatusCall,
    MasterType,
    StatusReceipt,
    StatusCashBox,
)
from src.settings.models import Tariffs, Service, UnitsOfMeasurement, Article
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
    counter_ids = models.JSONField(
        blank=True, null=True, default=list, verbose_name="ID счетчиков"
    )

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
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, blank=True, null=True)
    apartment = models.ForeignKey(
        Apartment, on_delete=models.CASCADE, blank=True, null=True
    )


class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ("message", "user")


class XlsTemplate(models.Model):
    name = models.CharField(max_length=40)
    template = models.FilePathField()
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_default:
            XlsTemplate.objects.exclude(pk=self.pk).filter(is_default=True).update(
                is_default=False
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}{" (по умолчанию)" if self.is_default else ''}"


class CashBox(models.Model):
    sum = models.FloatField()
    comment = models.TextField(blank=True, null=True)
    number = models.CharField(max_length=11, unique=True)
    date = models.DateField()
    is_catch = models.BooleanField(default=True)
    status = models.CharField(
        choices=StatusCashBox, max_length=10, blank=True, null=True
    )
    bank_book = models.ForeignKey(
        BankBook, on_delete=models.CASCADE, blank=True, null=True
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, blank=True, null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="cashbox_owner_set",
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="cashbox_manager_set",
    )
    receipt = models.ForeignKey(
        Receipt, on_delete=models.SET_NULL, blank=True, null=True
    )

    def save(self, *args, generate_number=False, **kwargs):
        if generate_number and not self.number:
            today = timezone.now().strftime("%d%m%Y%")
            last_box = CashBox.objects.order_by("-id").first()
            next_id = (last_box.id + 1) if last_box else 0
            self.number = f"{next_id}{today}"
            self.date = timezone.now().date().strftime("%Y-%m-%d")
        super().save(*args, **kwargs)
