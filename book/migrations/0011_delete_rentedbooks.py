# Generated by Django 4.0 on 2021-12-21 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_rentedbooks'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RentedBooks',
        ),
    ]