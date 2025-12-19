from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Role(models.Model):
    title = models.CharField(max_length=100)
    has_statics = models.BooleanField(default=False)
    has_cashbox = models.BooleanField(default=False)
    has_invoices = models.BooleanField(default=False)
    has_personal_accounts = models.BooleanField(default=False)
    has_apartaments = models.BooleanField(default=False)
    has_owners = models.BooleanField(default=False)
    has_messages = models.BooleanField(default=False)
    has_master_requests = models.BooleanField(default=False)
    has_meters = models.BooleanField(default=False)
    has_site_managment = models.BooleanField(default=False)
    has_services = models.BooleanField(default=False)
    has_tariffs = models.BooleanField(default=False)
    has_roles = models.BooleanField(default=False)
    has_users = models.BooleanField(default=False)
    has_payment_details = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='email address',
        max_length=255,
        unique=True,
    )
    id_user = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(auto_now=False, blank=True, null=True)
    about_owner = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    viber = PhoneNumberField(blank=True, null=True)
    telegram = models.CharField(blank=True, null=True, max_length=50)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
