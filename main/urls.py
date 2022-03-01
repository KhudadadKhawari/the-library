from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('', views.home, name='home'),
    path('accounts/login/', views.user_login, name='user_login'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/logout/', views.user_logout, name='user_logout'),
    path('accounts/profile/', views.edit_profile, name='edit_profile'),
    path('accounts/change_password/', views.change_password, name='change_password'),
    path('confirm_email/<uidb64>/<token>', views.confirm_email, name='confirm_email'),

    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(template_name='main/forgot_password/password_reset.html'), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/forgot_password/password_reset_done.html'), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/forgot_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/forgot_password/password_reset_complete.html'), name='password_reset_complete'),

    path('moderator/', views.moderator_dashboard, name='moderator_dashboard'),
    
    path('book/issue', views.issue_book, name="issue_book"),
    path('book/return', views.return_book, name="return_book"),
    path('book/returned', views.returned_books, name="returned_books"),
    path('book/rented', views.rented_books, name="rented_books"),

    path('student/', views.student_home, name='student_home'),
    path('student/favourites', views.favourites, name='favourites'),
    path('student/favourites/add/<str:isbn>', views.add_to_favourites, name='add_to_favourites'),
    path('student/favourites/remove/<str:isbn>', views.remove_from_favourites, name='remove_from_favourites'),
    path('student/book/current_rented', views.current_rented_by_student, name='current_rented_by_student'),
    path('student/book/previously_rented', views.previously_rented_by_student, name='previously_rented_by_student'),
]