# Generated by Django 4.0 on 2022-01-09 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0020_alter_book_cover_img'),
        ('main', '0009_alter_favoritebook_book'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritebook',
            name='book',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book'),
        ),
    ]
