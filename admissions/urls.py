# admissions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admission_dashboard, name='dashboard'),
    path('register/', views.register_student, name='register_student'),
    path('students/', views.view_students, name='view_students'),
    path('register_fee_structure/', views.register_fee_structure, name='register_fee_structure'),
    path('list_fee_structures/', views.list_fee_structures, name='list_fee_structures'),
    path('update_fee_structure/<int:pk>/', views.update_fee_structure, name='update_fee_structure'),
    path('delete_fee_structure/<int:pk>/', views.delete_fee_structure, name='delete_fee_structure'),
    path('receipt/<int:payment_id>/', views.payment_receipt, name='payment_receipt'),
    path('payment/<int:student_id>/', views.register_payment, name='register_payment'),
]
