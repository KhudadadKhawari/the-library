from django.contrib import admin
from django.contrib.admin.helpers import AdminForm
from .models import FavoriteBook, IssuedBook


# Register your models here.
admin.site.register(IssuedBook)
admin.site.register(FavoriteBook)