import imp
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from .models import Student
from main.models import IssuedBook
from book.models import Book
from book.models import BookCategory
from moderator.models import Moderator
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.core.paginator import Paginator
# Create your views here.




# Moderator User Views
# all current Approved Students
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def all_students_moderator_view(request):
    students = Student.objects.filter(approved=1)
    print(students)
    context={
        'user_type': 'moderator',
        'students': students,
        'active_nav':'approved_students',
    }

    return render(request, 'student/all_students_admin_view.html', context)


# Students in WAITING LIST to Join
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def student_approval(request):
    students = Student.objects.filter(approved=0)

    context={
        'user_type': 'moderator',
        'students': students,
        'active_nav':'student_approval',
    }
    return render(request, 'student/student_approval.html', context)


# students who got declined 
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def declined_students(request):
    students = Student.objects.filter(approved=2)

    context={
        'user_type': 'moderator',
        'students': students,
        'active_nav':'declined_students',
    }
    return render(request, 'student/declined_students.html', context)


# OPERATIONS ON STUDENT
# Approve Student
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def confirm_student_approval(request, username):
    redirect_view = request.GET.get('redirect_view','')
    if request.method == 'POST':
        user = User.objects.get(username=username)
        student = Student.objects.get(user = user)
        current_user = request.user
        moderator  = Moderator.objects.get(user=current_user)

        if not user.is_active:
            user.is_active = True
            user.save()
        student.approved = 1
        student.approved_by = moderator 
        student.save()
    return redirect(redirect_view)


# Decline The student joining request / Disable Approved users Account
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def decline_student_approval(request, username):
    redirect_view = request.GET.get('redirect_view','')
    if request.method == 'POST':
        user = User.objects.get(username=username)
        student = Student.objects.get(user = user)
        
        user.is_active = False
        student.approved = 2 # 1 for Approved, 2 for Declined, 0 for Waiting
        user.save()
        student.save()
    return redirect(redirect_view)


# Delete Student
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def delete_student(request,username):
    redirect_view = request.GET.get('redirect_view','')
    if request.method == 'POST':
        user = User.objects.get(username=username)
        student = Student.objects.get(user=user)
        # Check if Sutudent Doesn't have any not returned book 
        rented_books_by_user = IssuedBook.objects.filter(student=student, date_returned__isnull=True)
        if len(rented_books_by_user) > 0: 
            messages.warning(request,f"Unsuccessful! This user has not returned Books", 'alert-danger')
            # TODO: Returned to the page where you can get the books issued to the student(user)
            return redirect(redirect_view)
        else:
            user.delete()
    return redirect(redirect_view)