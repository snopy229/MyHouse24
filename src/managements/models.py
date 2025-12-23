from ckeditor.fields import RichTextField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class SeoBlock(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    keywords = models.TextField()


class MainPage(models.Model):
    slide1 = models.ImageField(upload_to="slides/")
    slide2 = models.ImageField(upload_to="slides/")
    slide3 = models.ImageField(upload_to="slides/")
    title = models.CharField(max_length=200)
    short_text = RichTextField()
    block_image_1 = models.ImageField(upload_to="slides/")
    block_title_1 = models.CharField(max_length=200)
    block_description_1 = RichTextField()
    block_image_2 = models.ImageField(upload_to="slides/")
    block_title_2 = models.CharField(max_length=200)
    block_description_2 = RichTextField()
    block_image_3 = models.ImageField(upload_to="slides/")
    block_title_3 = models.CharField(max_length=200)
    block_description_3 = RichTextField()
    block_image_4 = models.ImageField(upload_to="slides/")
    block_title_4 = models.CharField(max_length=200)
    block_description_4 = RichTextField()
    block_image_5 = models.ImageField(upload_to="slides/")
    block_title_5 = models.CharField(max_length=200)
    block_description_5 = RichTextField()
    block_image_6 = models.ImageField(upload_to="slides/")
    block_title_6 = models.CharField(max_length=200)
    block_description_6 = RichTextField()
    is_link = models.BooleanField(default=False, blank=True)
    seo_block = models.OneToOneField("SeoBlock", on_delete=models.CASCADE)


class Contacts(models.Model):
    title = models.CharField(max_length=200)
    short_text = RichTextField()
    link_site = models.URLField(blank=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    location = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = PhoneNumberField()
    map_fragment = models.TextField()
    seo_block = models.OneToOneField("SeoBlock", on_delete=models.CASCADE)


class ServicesAndSeoBlock(models.Model):
    seo_block = models.OneToOneField(SeoBlock, on_delete=models.CASCADE)


class ServicesForSite(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="services/")
    description = RichTextField()
    services_and_seo_block = models.OneToOneField(
        "ServicesAndSeoBlock", on_delete=models.CASCADE
    )
