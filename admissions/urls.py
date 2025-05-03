# admissions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admission_dashboard, name='dashboard'),
    path('register/', views.register_student, name='register_student'),
    path('students/', views.view_students, name='view_students'),
    path('payment/<int:student_id>/', views.register_payment, name='register_payment'),
]
