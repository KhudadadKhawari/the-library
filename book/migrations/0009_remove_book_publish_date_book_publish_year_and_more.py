# Generated by Django 4.0 on 2021-12-15 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_remove_book_content_table_img_book_contents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='publish_date',
        ),
        migrations.AddField(
            model_name='book',
            name='publish_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='pages_no',
            field=models.IntegerField(null=True),
        ),
    ]