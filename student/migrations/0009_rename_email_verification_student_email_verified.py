# Generated by Django 4.0 on 2021-12-31 05:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0008_rename_email_verified_student_email_verification'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='email_verification',
            new_name='email_verified',
        ),
    ]