from datetime import datetime
from tokenize import group
from django.shortcuts import redirect, render, HttpResponse
from book.models import Book, BookCategory, Tag
from student.models import Student
from moderator.models import Moderator
from .models import FavoriteBook, IssuedBook
from .forms import UserCreateForm, UserProfileForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import Group, User
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator

from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Q
import datetime


@login_required(login_url='user_login')
def home(request):
    if request.user.is_authenticated:
        l = request.user.groups.values_list('name',flat = True) # QuerySet Object
        groups = list(l)                                     # QuerySet to `list`
        if 'student' in groups or 'demo_student' in groups:
            return redirect('student_home')
        elif 'moderator' in groups or 'demo_moderator' in groups:
            return redirect('moderator_dashboard')
        elif 'admin' in groups:
            return redirect('/admin')
    else:
        return redirect('user_login')


@unauthenticated_user
def register(request):
    if request.user.is_authenticated:
        return redirect('user_login')
    form = UserCreateForm()
    user_group = Group.objects.get(name='student')
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        try: 
            if form.is_valid():
                user = form.save(commit=False)
                user.username = form.cleaned_data.get('username').lower()
                user.is_active = False
                user.save()
                user_group.user_set.add(user)
                # Send Email to USER

                user_email = user.email
                site = get_current_site(request) # Getting the domain
                message = render_to_string('main/email_confirmation_mail.html', {
                    'user': user,
                    'protocol': 'http',
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                # filling the  activation mail template w/ all the variables 

                send_mail(
                    'Verify Your Email Address',
                    message,
                    'NoReply@TheLibrary.com',
                    [user_email]
                )
                messages.success(request, "Account Created Successfully Please Check Your E-mail For Verification", "alert-success")
                return redirect('home')
            else:
                messages.info(request, "User not created, Error", 'alert-info')
        except IntegrityError as e:
            messages.warning(request, "Username already exists please use another username ", 'alert-warning')
            return redirect('register')
        

    context = {
        'form':form,
    }
    return render(request, 'main/register.html', context)


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # if the username does not exist in the database
        try:
            the_user = User.objects.get(username=username)
        except:
            messages.info(request, f"User with the username\"{username}\" does not exist", 'alert-info')
            return redirect('user_login')
        
        l = the_user.groups.values_list('name', flat=True) # getting user groups query set
        groups = list(l)  # adding them to the list

        # if it is the moderator or Admin
        if 'moderator' in groups or 'admin' in groups or 'demo_moderator' in groups:
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Password is Incorrect', 'alert-info')
        else:
            # if the user hasn't verified his email
            if the_user.student.email_verified == 0:
                messages.info(request, f"your E-mail is not verified yet, please verify your email first", 'alert-info')
                return redirect('user_login')
            # if the user joining request hasn't approved yet
            elif the_user.student.approved == 0:
                messages.info(request, "Your joining Request is not Approved Yet, Please Be patiend while one of our Staffs approve your request", "alert-info")    
                return redirect('user_login')
            # if user account is disabled or user joining request is declined
            elif the_user.student.approved == 2:
                messages.info(request, "We're Sorry, our Staff Declined Your Joining Request/Disabled Your Account, If you think this is a mistake please contact our staff at Office", "alert-info")    
                return redirect('user_login')
            else:
                if user is not None:
                    login(request, user)
                    return redirect('home')
                else:
                    messages.info(request,'Password is Incorrect', 'alert-info')
    return render(request, 'main/user_login.html')


def user_logout(request):
    logout(request)
    return redirect('user_login')


def confirm_email(request, uidb64, token):
    """Check the activation token sent via mail."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        messages.warning(request, str(e), 'alert-warning' )
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # now we're activating the user
        user.student.email_verified = 1  # and we're changing the boolean field so that the token link becomes invalid
        user.save()
        user.student.save()
        messages.success(request, f'Email is Verified', 'alert-success')
    else:
        messages.warning(request, 'Account activation link is invalid.', 'alert-warning')

    return redirect('home')
    
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student','moderator', 'demo_student','demo_moderator'])
# Edit Profile and Change Password
def edit_profile(request):
    user = request.user
    form = UserProfileForm(instance=user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)

        ## WE DON'T ALLOW DEMO USERS TO CHANGE PROFILE DETAILS
        if 'demo_student' in user.groups.values_list('name', flat=True) or 'demo_moderator' in user.groups.values_list('name', flat=True):
            messages.warning(request, "DEMO ACCOUNTS CAN'T CHANGE PROFILE DETAILS", 'alert-warning')
            return redirect('edit_profile')

        if form.is_valid():
            the_user = form.save(commit=False)
            the_user.username = form.cleaned_data.get('username').lower()
            the_user.save()
            
#TODO: If the User Changes the Email They'll have to re-verify the New E-mail Address

            messages.success(request, "Profile Details Updated Successfully", "alert-success")
            return redirect('edit_profile')
    context = {
        'form':form,
    }

    return render(request, 'main/profile.html', context)


@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student','moderator','demo_student','demo_moderator'])
def change_password(request):
    user = request.user
    form = PasswordChangeForm(user)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)

        ## WE DON'T ALLOW DEMO USERS TO CHANGE PASSWORD
        if 'demo_student' in user.groups.values_list('name', flat=True) or 'demo_moderator' in user.groups.values_list('name', flat=True):
            messages.info(request, "You're a Demo User, You're not allowed to change your password", 'alert-info')
            return redirect('change_password')

        if form.is_valid():
            form.save()
            messages.success(request, "Password Changed Successfully", "alert-success")
            return redirect('change_password')
    context={
        'form':form,
    }

    return render(request, 'main/change_password.html', context)

# Student's Views
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student', 'demo_student'])
def student_home(request):
    books = Book.objects.all().order_by('-created_date')
    categories = BookCategory.objects.all()

    # Searching For Books
    if request.method == 'POST':
        search_values = request.POST['search_for']
        keywords = search_values.split()
        qs = [Q(title__icontains=keyword)|Q(author__icontains=keyword)|Q(isbn__icontains=keyword)|Q(publisher__icontains=keyword) for keyword in keywords]
        query = qs.pop() #get the first element

        for q in qs:
            query |= q
        books = Book.objects.filter(query).order_by('created_date')
    paginator = Paginator(books, 10) # 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={
        'page_obj':page_obj,
        'active_nav': 'home',
        'categories': categories
    }

    return render(request, 'book/all_books.html', context)

@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student', 'demo_student'])
def favourites(request):
    user = request.user
    student = Student.objects.get(user=user)
    books = FavoriteBook.objects.filter(student=student)

    context = {
        'books': books,
    }
    return render(request, 'main/favourites.html', context)


@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student', 'demo_student'])
def add_to_favourites(request, isbn):
    redirect_view = request.GET.get('redirect_view', 'home')
    user = request.user
    student = Student.objects.get(user=user)
    try:
        book = Book.objects.get(isbn=isbn)
        try:
            FavoriteBook.objects.create(
                book=book,
                student=student,
            )
            messages.success(request,f"{book.title} Added To your Favourites", 'alert-success')
        except IntegrityError as error:
            messages.info(request, f"\"{book.title}\" already exists in your favourites", 'alert-info')
    except ObjectDoesNotExist as error:
        messages.info(request,f"{error}", 'alert-info')
    return redirect(redirect_view)


# Remove Book from Favourites
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student', 'demo_student'])
def remove_from_favourites(request, isbn):
    try:
        book = Book.objects.get(isbn=isbn)
        user = request.user
        student = Student.objects.get(user=user)
        item = FavoriteBook.objects.get(book=book, student=student)
        item.delete()
        messages.info(request, f"\"{book.title}\" was removed from favourites", 'alert-info')
    except ObjectDoesNotExist as error:
        messages.info(request,f"{error}", 'alert-info')
    return redirect('favourites')


@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student', 'demo_student'])
def current_rented_by_student(request):
    user = request.user
    student = Student.objects.get(user=user)
    current_issued_books = IssuedBook.objects.filter(student=student, date_returned__isnull=True)
    context = {
        'current_issued_books': current_issued_books,
    }
    return render(request, "main/current_rented_by_student.html", context)


@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student', 'demo_student'])
def previously_rented_by_student(request):
    user = request.user
    student = Student.objects.get(user=user)
    current_issued_books = IssuedBook.objects.filter(student=student, date_returned__isnull=False)
    context = {
        'current_issued_books': current_issued_books,
    }
    return render(request, "main/previously_rented_by_student.html", context)


# Moderator's Views
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator', 'demo_moderator'])
def moderator_dashboard(request):
    categories_ = BookCategory.objects.all().order_by('id')
    tags_ = Tag.objects.all().order_by('id')
    # Searching For Tags and Categroies
    if request.method == 'POST':
        try:
            search_values = request.POST['search_for_cat'].lower()
            keywords = search_values.split()
            qs = [Q(category__icontains=keyword) for keyword in keywords]
            query = qs.pop() #get the first element
            for q in qs:
                query |= q
            categories_ = BookCategory.objects.filter(query).order_by('id')
        except:
            pass
        try:
            search_values2 = request.POST['search_for_tag'].lower()
            keywords2 = search_values2.split()
            qs2 = [Q(name__icontains=keyword) for keyword in keywords2]
            query2 = qs2.pop() #get the first element
            for q in qs2:
                query2 |= q
            tags_ = Tag.objects.filter(query2).order_by('id')
        except:
            pass
    # Pagination for Category
    cat_pag = Paginator(categories_, 5) # 10 object per page
    page_number = request.GET.get('cat_page')
    categories = cat_pag.get_page(page_number)
    # Patination For tags
    key_page = Paginator(tags_, 5) # 10 object per page
    page_number = request.GET.get('key_page')
    tags = key_page.get_page(page_number)

    context={
        'active_nav':'dashboard',
        'tags': tags,
        'categories': categories,
    }
    return render(request, 'main/moderator_dashboard.html', context)


# OPERATIONS ON BOOKS
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator', 'demo_moderator'])
def issue_book(request):
    students = Student.objects.all()
    user = request.user
    books = Book.objects.all()
    if request.method == 'POST':
        isbn = request.POST.get('isbn').strip()
        stid = request.POST.get('stid').strip()
        try:
            student_ = Student.objects.get(id=stid)
            book_ = Book.objects.get(isbn=isbn)
            moderator = Moderator.objects.get(user=user)
            present_rented_books_by_student = IssuedBook.objects.filter(student=student_, date_returned=None)
            # Students Can't Lend more than 2 books
            if len(present_rented_books_by_student) >= 2:
                messages.warning(request, "Operation Unsuccessfull!! \n Student Can't lend more than 2 Books. Please Return the previous books first", 'alert-danger')
                return redirect('issue_book')
            
            # Check if book is not available
            if (book_.total_quantity - book_.rented_count) == 0:
                messages.warning(request, "Operation Unsuccessfull!! \n Book is not available", 'alert-danger')
                return redirect('issue_book')

            # Students can't lend a copy of the same book they haven't returned yet
            for obj in present_rented_books_by_student:
                    if isbn in str(obj.book.isbn) and obj.date_returned is None:
                            messages.warning(request, "Operation Unsuccessfull!! \n This Book is already Issued to the student", 'alert-danger')
                            return redirect('issue_book')
            # if Student's Account is Disabled
            if not student_.user.is_active:
                messages.warning(request, "Operation Unsuccessfull!! \n This User's Account is Disabled", 'alert-danger')
                return redirect('issue_book')
        
            record = IssuedBook.objects.create(
                book=book_,
                student=student_,
                moderator=moderator,
            )
            book_.rented_count += 1
            book_.save()
            record.save()
            messages.success(request, f"Operation Successfull, {book_.title} rented by {student_.user.first_name} {student_.user.last_name}", 'alert-success')
            return redirect('issue_book')
        except ObjectDoesNotExist as error:
            messages.info(request, f"{error} Please Make Sure To Enter The Complete Student's ID and Book's ISBN", 'alert-info')
    context={
        'books': books,
        'students': students,
        'active_nav':'issue_book',
    }

    return render(request, 'main/issue_book.html', context)


# Operation: Return book By Student 
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator', 'demo_moderator'])
def return_book(request):
    issued_books = IssuedBook.objects.filter(date_returned__isnull=True)


    if request.method == 'POST':
        isbn = request.POST.get('isbn').strip()
        stid = request.POST.get('stid').strip()
        try:
            student_ = Student.objects.get(id=stid)
            book_ = Book.objects.get(isbn=isbn)
            record = IssuedBook.objects.get(student=student_, book=book_, date_returned__isnull=True)
            record.date_returned = datetime.datetime.now()
# TODO: Have to Caluclate the Fine amount and Save the Payment Status in Database
            book_.rented_count -= 1
            book_.save()
            record.save()
            messages.success(request,f"Operation Successfull! \n {book_.title} was received From {student_.user.username}", 'alert-success')
            return redirect('return_book')
        except ObjectDoesNotExist as error:
            messages.info(request, f"{error} Please Make Sure To Enter The Complete Student's ID and Book's ISBN", 'alert-info')
    context={
        'issued_books':issued_books,
        'active_nav':'return_book',
    }
    return render(request, "main/return_book.html", context)


@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator', 'demo_moderator'])
def returned_books(request):
    books = IssuedBook.objects.filter(date_returned__isnull=False)

    context = {
        'books':books,
        'active_nav':'returned_books',
    }
    return render(request, "main/returned_books.html", context)


@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator', 'demo_moderator'])
def rented_books(request):
    books = IssuedBook.objects.filter(date_returned__isnull=True)

    context = {
        'books':books,
        'active_nav':'rented_books',
    }
    return render(request, "main/rented_books.html", context)
