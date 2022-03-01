# Generated by Django 4.0 on 2021-12-22 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_alter_book_contents'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='category',
        ),
    ]
