# import decimal
#
# from django.db import models
# from django.contrib.auth.models import User
#
#
# # Create your models here.
# class Topic(models.Model):
#     name = models.CharField(max_length=200)
#     category = models.CharField(max_length=200, default='Unclassified')
#
#     def __str__(self):
#         return self.name
#
#
# class Course(models.Model):
#     topic = models.ForeignKey(Topic, related_name='courses',
#                               on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     for_everyone = models.BooleanField(default=True)
#     description = models.TextField(max_length=300, null=True, blank=True)
#     interested = models.PositiveIntegerField(default=0)  # indicates people interested in a course
#     stages = models.PositiveIntegerField(default=3)
#
#     def discount(self):
#         disc = self.price * decimal.Decimal('0.10')
#         return disc
#
#     def __str__(self):
#         print("Inside str function: " + self.name)
#         return self.name
#
#
# class Student(User):
#     Windsor = 'WS'
#     Calgary = 'CG'
#     Montreal = 'MR'
#     Vancouver = 'VC'
#     CITY_CHOICES = [('WS', Windsor),
#                     ('CG', Calgary),
#                     ('MR', Montreal),
#                     ('VC', Vancouver)]
#     school = models.CharField(max_length=50, null=True, blank=True)
#     city = models.CharField(max_length=2, choices=CITY_CHOICES, default=Windsor)
#     interested_in = models.ManyToManyField(Topic)
#     address = models.CharField(max_length=60, null=True, blank=True)
#
#     def __str__(self):
#         return self.first_name + '\t' + self.last_name
#
#
# class Order(models.Model):
#     STATUS_VALUES = [(0, 'Cancelled'),
#                      (1, 'Order Confirmed')]
#     course = models.ForeignKey(Course, related_name='courses', on_delete=models.CASCADE)
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     levels = models.PositiveIntegerField(null=True, blank=True, default=0)
#     order_status = models.IntegerField(choices=STATUS_VALUES, default=1)
#     order_date = models.DateField(auto_now=False)
#
#     def __str__(self):
#         return ', '.join([self.student.first_name, self.student.last_name, self.total_cost()])
#
#     @staticmethod
#     def total_cost():
#         total = 0
#         for course in Order.objects.all()['course']:
#             total += course.price
#         return total

from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# for validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Topic(models.Model):
    name = models.CharField(max_length=200)
    length = models.IntegerField(default=12)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    # Project: Optional 2 : Validators
    def validate_between(value):
        if not 100 <= value <= 200:
            raise ValidationError(
                _('%(value)s price is not between 100 and 200'),
                params={'value': value},
            )
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_between]) #for optional 2
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(blank=True)  # new field description and making it optional by using blank=True
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def hours(self):
        return self.topic.length


class Student(User):
    LVL_CHOICES = [
        ('HS', 'High School'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate'), ('ND', 'No Degree'),
    ]
    level = models.CharField(choices=LVL_CHOICES, max_length=2, default='HS')
    address = models.CharField(max_length=300, blank=True)  # making address optional using blank=True
    province = models.CharField(max_length=2, default='ON')  # setting default value to 'ON'
    registered_courses = models.ManyToManyField(Course, blank=True)
    interested_in = models.ManyToManyField(Topic)
    profile_image = models.ImageField(blank=True, upload_to='myapp/static/images/')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    # project : 3
    def full_name(self):
        return str(self.first_name + ' ' + self.last_name).upper()
    full_name.short_description = 'Student Full Name'


# Adding new model Order
class Order(models.Model):
    courses = models.ManyToManyField(Course)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    # new integer field order_status which can choose value from ORDER_STATUS_CHOICES
    # with default choice 1
    ORDER_STATUS_CHOICES = [
        (0, 'Cancelled'), (1, 'Confirmed'), (2, 'On Hold')
    ]
    order_status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=1)
    order_date = models.DateField(default=timezone.now)  # default date set to current date/timezone.now

    def total_items(self):
        return self.courses.count()

    def __str__(self):
        return 'Order by: '+self.student.username + ' \ntotal:' + str(self.total_cost())


    def total_cost(self):
        total = 0
        for course in self.courses.all():
            total += course.price
        return total


class Review(models.Model):
    reviewer = models.EmailField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.reviewer + ' ' + self.course.title + ' Rating: ' + str(self.rating)

