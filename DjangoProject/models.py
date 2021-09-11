from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, default='Development')

    def __str__(self):
        return self.name


class Course(models.Model):
    courseName = Topic.name
    topic = models.ForeignKey(Topic, related_name='courses', default=courseName, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return '%s %s %s' % (self.name, ' ', self.price)  # Return multiple values


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'), ('CG', 'Calgary'), ('MR', 'Montreal'), ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return '%s %s %s' % (self.first_name, ' ', self.last_name)


class Order(models.Model):
    ORDER_CHOICES = [(0, 'Cancelled'), (1, 'Order Confirmed')]
    course = models.ManyToManyField(Course)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(null=True)
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField(default=datetime.date.today)

    __original_status = None

    def __init__(self, *args, **kwargs):
        super(Order, self).__init__(*args, **kwargs)
        self.__original_status = self.order_status
        self.__original_pk = self.pk

    # override save to update order_date if order_status changes
    def save(self, *args, **kwargs):
        if self.order_status != self.__original_status:
            self.order_date = timezone.now()
        super(Order, self).save(*args, **kwargs)
        self.__original_status = self.order_status

    def __str__(self):
        return "Order of :  %s" % self.Student.first_name

    def total_cost(self):
        return Order.objects.filter(pk=self.__original_pk).aggregate(Sum('course__price'))


