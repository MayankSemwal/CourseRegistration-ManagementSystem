from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order

# Register your models here.
admin.site.register(Topic)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Order)
