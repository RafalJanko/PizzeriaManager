from django.db import models
from django.contrib.auth.models import User

# Create your models here.

'''
Basic profile model related to :model:`auth.User`.
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


"""
Stores a single Shift entry, related to :model:`auth.User`.
"""

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


"""
Stores a single Day-off entry, related to :model:`auth.User`.
"""


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


"""
Stores a single profile entry for each registered user, related to :model:`auth.User`.
"""


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=64)
    phone_no = models.CharField(max_length=12)

    def __str__(self):
        return f"{self.username}({self.customer_id})"


"""
Stores a single Menu entry.
"""


class Menu(models.Model):
    item_id = models.PositiveIntegerField(primary_key=True)
    item_name = models.CharField(max_length=64)
    item_price = models.FloatField()

    def __str__(self):
        return f"{self.item_name} - {self.item_price} zł"


"""
Stores a single Pizza ingredient entry.
"""


class PizzaIngredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


"""
Stores a single Pizza Menu Item entry, related to :model:`PizzaIngredient`.
"""


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


"""
Stores an Order entry, related to :model:`user.Customer`.
"""


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


"""
Stores a single ordered item entry, related to :model:`PizzaIngredient` and model:`Order`.
"""


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
