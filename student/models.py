from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from moderator.models import Moderator

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    clg_reg_no = models.CharField(max_length=50, null=True)
    graduation_year = models.IntegerField(null=True)
    phone = models.CharField(max_length=20, null=True)
    email_verified = models.IntegerField(default=0, null=True)
    qr_code = models.ImageField(upload_to='static/media/users/qr_codes', null=True, blank=True)
    approved = models.IntegerField(default=0, null=True)
    approved_by = models.ForeignKey(Moderator, null=True, blank=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)
    def student_profile_url(self,instance):
        return f"static/media/users/student/{instance}"

    photo = models.ImageField(upload_to=student_profile_url, default='static/media/users/default.jpg', null=True)

    def __str__(self) -> str:
        return self.user.username


# @receiver(post_save, sender=User)
# def create_student_profile(sender, instance, created, **kwargs):
#     if created:
#         Student.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_student_profile(sender, instance, **kwargs):
#     instance.student.save()