from django.db import models

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


class Section(models.Model):
    title = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Floor(models.Model):
    title = models.CharField(max_length=100)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
