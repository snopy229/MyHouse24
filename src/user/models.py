from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


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
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    id_user = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(auto_now=False, blank=True, null=True)
    about_owner = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    viber = PhoneNumberField(blank=True, null=True)
    telegram = models.CharField(blank=True, null=True, max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = MyUserManager()
