# Generated by Django 4.0 on 2021-12-23 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moderator', '0001_initial'),
        ('book', '0017_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='added_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='moderator.moderator'),
        ),
    ]
