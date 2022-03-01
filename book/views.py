from unicodedata import category
from django.db import IntegrityError
from django.shortcuts import redirect, render
from .models import Book, Tag
from book.models import BookCategory
from .forms import BookForm
from moderator.models import Moderator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.decorators import allowed_users
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
# from main.filters import CategoryFilter

@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def add_new_book(request):
    
    form = BookForm()
    current_user = request.user
    user = Moderator.objects.get(user=current_user)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        current_user = request.user
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.added_by = user
            new_book.save()
            messages.success(request, "Book Added Successfully", "alert-success")
            return redirect(add_new_book)

    context={
        'form': form,
        'active_nav':'add_new_book',
    }

    return render(request, 'book/add_new_book.html', context)


@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def all_books_admin_view(request):
    books = Book.objects.all()

    context={
        'books': books,
        'active_nav':'all_books',
    }

    return render(request, 'book/all_books_admin_view.html', context)


# Update BOOK details
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def update_book(request, isbn):
    book = Book.objects.get(isbn=isbn)
    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Details Updated Successfully", "alert-success")
            return redirect(update_book, isbn)
    context={
        'form': form,
    }
    return render(request, 'book/update_book.html', context)

# Delete Book
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def delete_book(request, isbn):
    book = Book.objects.get(isbn=isbn)
    if request.method == 'POST':
        book.delete()
        messages.success(request, f"{book.title} Deleted Successfully", "alert-info")
        return redirect('all_books_admin_view')
    
    context={
        'book':book,
    }


# Add New Category
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def new_category(request):
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category').lower()
            new = BookCategory.objects.create(category=category_name)
            messages.success(request, f"{new.category} Category Added Successfully", "alert-info")
        except IntegrityError as error:
            messages.success(request, f"Category Already exists", "alert-info")
        return redirect('moderator_dashboard')

# Add New Tag
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def new_tag(request):
    if request.method == 'POST':
        try:
            tag_name = request.POST.get('tag_name').lower()
            new = Tag.objects.create(name=tag_name)
            messages.success(request, f"{new.name} Tag Added Successfully", "alert-info")
        except IntegrityError as error:
            messages.success(request, f"Tag Already exists", "alert-info")
        return redirect('moderator_dashboard')



# Update Category
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def update_category(request,id):
    category = BookCategory.objects.get(id=id)
    if request.method == 'POST':
        new_name = request.POST.get('category').lower()
        category.category = new_name
        category.save()
        messages.success(request, f"{category.category} Updated Successfully", "alert-info")
        return redirect('moderator_dashboard')

# Update Tag
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def update_tag(request,id):
    tag = Tag.objects.get(id=id)
    if request.method == 'POST':
        new_name = request.POST.get('tag_name').lower()
        tag.name = new_name
        tag.save()
        messages.success(request, f"{tag.name} Updated Successfully", "alert-info")
        return redirect('moderator_dashboard')


# Delete Tag
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def delete_tag(request,id):
    tag = Tag.objects.get(id=id)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, f"{tag.name} Deleted Successfully", "alert-info")
        return redirect('moderator_dashboard')


# Delete category
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['moderator'])
def delete_category(request,id):
    category = BookCategory.objects.get(id=id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, f"{category.category} Deleted Successfully", "alert-info")
        return redirect('moderator_dashboard')

# Studen View 
@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student'])
def display_book(request, isbn):
    book = Book.objects.get(isbn=isbn)


    context={
        'book':book,
    }

    return render(request,'book/display_book.html', context)

# Student View

@login_required(login_url='user_login')
@allowed_users(allowed_roles=['student'])
def books_by_category(request, category):
    category_ = BookCategory.objects.get(category=category)
    books = Book.objects.filter(category=category_).order_by('-created_date')
    categories = BookCategory.objects.all()
    
    # Searching For Books
    if request.method == 'POST':
        search_values = request.POST['search_for']
        keywords = search_values.split()
        qs = [Q(title__icontains=keyword)|Q(author__icontains=keyword)|Q(isbn__icontains=keyword)|Q(publisher__icontains=keyword) for keyword in keywords]
        query = qs.pop() #get the first element

        for q in qs:
            query |= q
        books = Book.objects.filter(query, category=category_).order_by('created_date')


    paginator = Paginator(books, 10) # 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'categories': categories,
        'page_obj': page_obj,
        'active_nav': 'all_books'
    }

    return render(request, 'book/all_books.html', context)