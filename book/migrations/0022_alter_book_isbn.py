# Generated by Django 4.0 on 2022-01-13 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0021_alter_book_category_alter_book_edition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.BigIntegerField(null=True, unique=True),
        ),
    ]
