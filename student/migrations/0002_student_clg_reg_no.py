# Generated by Django 4.0 on 2021-12-24 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='clg_reg_no',
            field=models.CharField(max_length=50, null=True),
        ),
    ]