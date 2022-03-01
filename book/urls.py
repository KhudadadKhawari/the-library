from django.urls import path 
from . import views

urlpatterns=[
     path('book/isbn/<str:isbn>', views.display_book, name='display_book'),
     path('book/add', views.add_new_book, name='add_new_book'),
     path('book/all', views.all_books_admin_view, name='all_books_admin_view'),
     path('book/all/<str:category>', views.books_by_category, name='books_by_category'),
     path('book/isbn/<str:isbn>/update', views.update_book, name='update_book'),
     path('book/isbn/<str:isbn>/delete', views.delete_book, name='delete_book'),

     path('tag/new', views.new_tag, name='new_tag'),
     path('tag/<str:id>/delete', views.delete_tag, name='delete_tag'),
     path('tag/<str:id>/update', views.update_tag, name='update_tag'),

     path('category/new', views.new_category, name='new_category'),
     path('category/<str:id>/delete', views.delete_category, name='delete_category'),
     path('category/<str:id>/update', views.update_category, name='update_category'),
]