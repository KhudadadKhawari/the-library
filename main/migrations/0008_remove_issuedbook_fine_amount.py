# Generated by Django 4.0 on 2022-01-02 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_rentedbook_issuedbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuedbook',
            name='fine_amount',
        ),
    ]