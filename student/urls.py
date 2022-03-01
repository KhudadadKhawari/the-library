from django.urls import path 
from . import views

urlpatterns=[
    #admin views
    path('student/all', views.all_students_moderator_view, name='all_students_moderator_view'),
    path('student/not_approved', views.student_approval, name='student_approval'),
    path('student/declined_students', views.declined_students, name='declined_students'),
    path('student/user/<str:username>/delete', views.delete_student, name='delete_student'),
    path('student/user/<str:username>/confirm_approval', views.confirm_student_approval, name='confirm_student_approval'),
    path('student/user/<str:username>/decline_approval', views.decline_student_approval, name='decline_student_approval'),
    

    #student views
    
]