import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

'''
Basic profile model attached to user. Based on this function the base.html shows the navbar and different functionalities
'''

class Profile(models.Model):
    function_choices = [
        ("Customer", "Customer"),
        ("Staff", "Staff"),
        ("Manager", "Manager"),
        ("HR", "HR"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    function = models.CharField(max_length=10, choices=function_choices, default="Customer")


'''
Basic shift model used to create "shifts" for all user types, apart from a regular customer.
The idea behind the model is that Manager or HR users are able to create working shifts for "Staff", "Manager" and "HR" users.
'''

class Shift(models.Model):
    shift_choices = [
        ("6:00 - 14:00", "6:00 - 14:00"),
        ("12:00 - 20:00", "12:00 - 20:00"),
        ("18:00 - 2:00", "18:00 - 2:00"),
        ("0:00 - 8:00", "0:00 - 8:00")
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    shift = models.CharField(max_length=50, choices=shift_choices)


'''
Daysoff model is used by all users apart from Customer users, to indicate in which days and for which reason a person would like to request a leave.
'''


class DaysOff(models.Model):
    leave_type = [
        ("Paid time off", "Paid time off"),
        ("Unpaid leave", "Unpaid leave"),
        ("On demand", "On demand"),
        ("Bereavement", "Bereavement"),
    ]

    leave_status = [
        ("Pending", "Pending"),
        ("Accepted", "Accepted"),
        ("Denied", "Denied"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=30, choices=leave_type)
    status = models.CharField(max_length=30, choices=leave_status, default="Pending")


'''
Customer model is created for each user so ensure that all types of users (Managers, HR, Staff, Customer) can use the functionality to order the pizza from the website.
'''


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=64)
    phone_no = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.username}({self.customer_id})"


'''
Menu model used to create the basic pizza item and establishing it's name and price
'''


class Menu(models.Model):
    item_id = models.PositiveIntegerField(primary_key=True)
    item_name = models.CharField(max_length=64)
    item_price = models.FloatField()

    def __str__(self):
        return f"{self.item_name} - {self.item_price} zł"


'''
PizzaIngredient - all toppings or items that go on pizza, that are listed on the menu. Relation makes sure that an item is assigned to a given pizza.
'''


class PizzaIngredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


'''
All details related to a pizza, such as it's image, ingredients, price, size, name etc.
'''

class PizzaMenuItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=60, default="Pizza")
    image = models.ImageField(upload_to='products/', default="temp")
    ingredients = models.ManyToManyField(
        'PizzaIngredient',
        related_name='ingredients'
    )
    img = models.CharField(max_length=300, default=None, null=True)
    price = models.FloatField()
    size = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return str(self.name)


'''
The total order a Customer can make - the confirmation shown to user is created based on this model.
The Model item is created when a customer proceeeds to the "checkout'
'''


class Order(models.Model):
    customer = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    timestamp = models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    in_cart = models.BooleanField(default=True)
    completed = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=50)
    address = models.CharField(max_length=250)


'''
OrderItems is a model that makes it easy to assing each pizza to an order made by a customer.
'''

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=True,
        related_name='items'
    )
    pizza_name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=5, blank=True)
    toppings = models.ManyToManyField(
        PizzaIngredient,
        blank=True,
        related_name='pizza'
    )


'''
Booking model - related with many to one to User.
Used in the table booking functionality.
'''


class Booking(models.Model):
    booking_status = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_name = models.CharField(max_length=200)
    booking_date = models.DateField(default=timezone.now)
    booking_time = models.TimeField()
    booking_no_of_people = models.IntegerField()
    status = models.CharField(max_length=30, choices=booking_status, default="Pending")


