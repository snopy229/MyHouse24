from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from .choices import Status


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
    has_statistics = models.BooleanField(default=False)
    has_cashbox = models.BooleanField(default=False)
    has_invoices = models.BooleanField(default=False)
    has_personal_accounts = models.BooleanField(default=False)
    has_apartments = models.BooleanField(default=False)
    has_owners = models.BooleanField(default=False)
    has_houses = models.BooleanField(default=False)
    has_messages = models.BooleanField(default=False)
    has_master_requests = models.BooleanField(default=False)
    has_meters = models.BooleanField(default=False)
    has_site_management = models.BooleanField(default=False)
    has_services = models.BooleanField(default=False)
    has_tariffs = models.BooleanField(default=False)
    has_roles = models.BooleanField(default=False)
    has_users = models.BooleanField(default=False)
    has_payment_details = models.BooleanField(default=False)
    has_article = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    photo = models.ImageField(blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    id_user = models.CharField(blank=True, null=True, unique=True)
    second_name = models.CharField(blank=True, null=True, max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(auto_now=False, blank=True, null=True)
    about_owner = models.TextField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    viber = PhoneNumberField(blank=True, null=True)
    telegram = models.CharField(blank=True, null=True, max_length=50)
    status = models.CharField(choices=Status, default=Status.new)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    @property
    def fullname(self):
        if self.second_name or self.first_name or self.last_name:
            parts = [self.second_name, self.first_name, self.last_name]
            return " ".join(filter(None, parts))
        else:
            return self.email

    def __str__(self):
        return f"{self.first_name} {self.second_name}"

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

        if perm.startswith("role.") and self.role:
            field_name = perm.split(".")[-1]
            return getattr(self.role, field_name, False)

        return super().has_perm(perm, obj)
