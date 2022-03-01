from django.db import models
from django.db.models.fields import CharField, DateTimeField
from django.urls import reverse
from moderator.models import Moderator


# Create your models here.

class BookCategory(models.Model):
    category = CharField(max_length=200,unique=True, null=True)
    date_created = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.category


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True, null=True)
    date_created = DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    isbn = models.BigIntegerField(unique=True)
    title = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    #description
    pages_no = models.IntegerField(null=True)
    publisher = models.CharField(max_length=200, null=True, blank=True)
    publish_year = models.IntegerField(null=True)
    edition = models.IntegerField(null=True, default=1)
    total_quantity = models.IntegerField(null=True, default=200)
    rented_count = models.IntegerField(default=0, null=True, blank=True)
    cover_img = models.ImageField(upload_to='static/media/book/covers', default="static/media/default_cover.png" , null=True, blank=True)
    rating = models.IntegerField(default=0, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    category = models.ForeignKey(BookCategory, null=True, default=1, on_delete=models.SET_NULL)
    contents = models.FileField(upload_to='static/media/book/contents', null=True, blank=True)
    added_by = models.ForeignKey(Moderator, null=True, blank=True, on_delete=models.SET_NULL)

    @property
    def filename(self):
        name = self.file.name.split("/")[1].replace('_',' ').replace('-',' ')
        return name
    def get_absolute_url(self):
        return reverse('thelib:document-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return self.title
    






