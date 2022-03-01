from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Moderator(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email_verification = models.IntegerField(default=0, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def moderator_profile_url(self,instance):
        return f"static/media/users/moderator/{instance}"

    photo = models.ImageField(upload_to=moderator_profile_url, default='static/media/users/default.jpg', null=True)

    def __str__(self) -> str:
        return self.user.username