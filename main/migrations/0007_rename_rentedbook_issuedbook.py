# Generated by Django 4.0 on 2022-01-02 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0019_alter_book_added_by_alter_book_cover_img_and_more'),
        ('moderator', '0003_rename_moderator_moderator_user_and_more'),
        ('student', '0009_rename_email_verification_student_email_verified'),
        ('main', '0006_alter_rentedbook_moderator_delete_moderator'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RentedBook',
            new_name='IssuedBook',
        ),
    ]