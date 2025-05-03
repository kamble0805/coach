# admissions/admin.py

from django.contrib import admin
from .models import Student, FeeStructure, Payment

# Register your models here
admin.site.register(Student)
admin.site.register(FeeStructure)
admin.site.register(Payment)
