from django.db import models
from book.models import Book
from student.models import Student
from moderator.models import Moderator
import datetime

# Create your models here.



class IssuedBook(models.Model):

    book = models.ForeignKey(Book, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    moderator = models.ForeignKey(Moderator, null=True, on_delete=models.SET_NULL)
    date_rented = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    fine_per_day = models.IntegerField(default=1)
    payment_status = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.book.title} rented by {self.student.user.username}"

    @property
    def fine_amount_(self):
        try:
            days_diff = self.date_returned.date() - self.date_rented.date()
            if days_diff.days > 4:
                return (days_diff.days * self.fine_per_day)
            else:
                return 0
        except AttributeError:
            now_date = datetime.datetime.now().date()
            days_diff = now_date - self.date_rented.date()
            if days_diff.days > 4:
                return (days_diff.days * self.fine_per_day)
            else:
                return 0



class FavoriteBook(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    book = models.OneToOneField(Book, null=True, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.book.title