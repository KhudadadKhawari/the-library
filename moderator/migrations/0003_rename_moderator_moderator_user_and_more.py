# Generated by Django 4.0 on 2021-12-31 04:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moderator', '0002_remove_moderator_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moderator',
            old_name='moderator',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='moderator',
            name='email',
        ),
        migrations.RemoveField(
            model_name='moderator',
            name='name',
        ),
        migrations.RemoveField(
            model_name='moderator',
            name='surname',
        ),
    ]
