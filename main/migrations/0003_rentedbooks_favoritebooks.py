# Generated by Django 4.0 on 2021-12-21 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0011_delete_rentedbooks'),
        ('student', '0001_initial'),
        ('main', '0002_moderator_moderator'),
    ]

    operations = [
        migrations.CreateModel(
            name='RentedBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_rented', models.DateTimeField(auto_now_add=True)),
                ('date_returned', models.DateTimeField(blank=True, null=True)),
                ('fine_per_day', models.IntegerField(default=1)),
                ('fine_amount', models.IntegerField(default=0)),
                ('payment_status', models.IntegerField(default=0)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('moderator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.moderator')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteBooks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]