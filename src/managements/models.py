from ckeditor.fields import RichTextField
from django.db import models


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
    block_description_1 = models.TextField()
    block_image_2 = models.ImageField(upload_to="slides/")
    block_title_2 = models.CharField(max_length=200)
    block_description_2 = models.TextField()
    block_image_3 = models.ImageField(upload_to="slides/")
    block_title_3 = models.CharField(max_length=200)
    block_description_3 = models.TextField()
    block_image_4 = models.ImageField(upload_to="slides/")
    block_title_4 = models.CharField(max_length=200)
    block_description_4 = models.TextField()
    block_image_5 = models.ImageField(upload_to="slides/")
    block_title_5 = models.CharField(max_length=200)
    block_description_5 = models.TextField()
    block_image_6 = models.ImageField(upload_to="slides/")
    block_title_6 = models.CharField(max_length=200)
    block_description_6 = models.TextField()
    is_link = models.BooleanField(default=False, blank=True)
    seo_block = models.OneToOneField("SeoBlock", on_delete=models.CASCADE)
