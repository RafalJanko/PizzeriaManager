import pytest
from datetime import date

from django.contrib.auth.models import User

from PizzeriaManager.models import User, Customer, PizzaMenuItem, PizzaIngredient, Profile, Order, OrderItem, DaysOff, Shift

'''
Fixtures for PyTest - used in the tests.py file to create "dummy" data.
Most of the fixtures compose of a single object and list of multiple objects, for testing purposes
'''

@pytest.fixture
def user():
    return User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski", email="jankowalski@gmail.com", is_superuser=1)

@pytest.fixture
def users():
    lst = []
    for i in range(10):
        x = User.objects.create(
            id=f'{i+123123}',
            username=f"user{i+10}",
            first_name=f"fnuser{i}",
            last_name=f"lsuser{i}",
            email=f"email{i}@test.com",
            password={i},
        )
        lst.append(x)
    return lst

@pytest.fixture
def profile(user):
    return Profile.objects.create(user_id=1, function="Manager")

@pytest.fixture
def profiles(user):
    lst = []
    for i in range(5):
        x = Profile.objects.create(user_id=i, function="Manager")
        lst.append(x)
    return Profile.objects.create()

@pytest.fixture
def customer():
    return Customer.objects.create(customer_id=1 ,username="Janek", first_name="Jan", last_name="Kowalski", email="jankowalski@gmail.com", phone_no="12323345", user_id=1)

@pytest.fixture
def shift():
    return Shift.objects.create(date=date(2022,3,12), user_id=1, shift='12:00 - 20:00')

@pytest.fixture
def shifts(user):
    lst = []
    for i in range(10):
        x = Shift.objects.create(
            user_id=i,
            date=2022-10-12,
            shift="12:00 - 20:00"
        )
        lst.append(x)
    return lst

@pytest.fixture
def ingredient():
    return PizzaIngredient.objects.create(id=1, name="test")

@pytest.fixture
def ingredients():
    lst = []
    for i in range(3):
        x = PizzaIngredient.objects.create(name=f"test{i}")
        lst.append(x)
    return lst

@pytest.fixture
def pizza(ingredient):
    PizzaMenuItem.objects.create(name="test", category="Pizza", img="test", image="temp", price=15, size="30")

@pytest.fixture
def pizzas():
    lst = []
    for i in range(3):
        x = PizzaMenuItem.objects.create(id=i, name=f"test{i}", category="Pizza", img="test", image="temp", price=15, size="30")
        lst.append(x)
    return lst

@pytest.fixture
def dayoff():
    return DaysOff.objects.create(user_id=1, start_date="2022-03-28", end_date="2022-03-28", status="Pending", reason="On demand")


@pytest.fixture
def daysoff():
    lst = []
    for i in range(5):
        x = DaysOff.objects.create(id=i, user_id=1, start_date="2022-03-28", end_date="2022-03-28", status="Pending", reason="On demand")
        lst.append(x)
    return lst

@pytest.fixture
def orders():
    lst=[]
    for i in range(5):
        x = Order.objects.create(id=i, timestamp="2022-03-18 10:37:57.782908", total=60, payment_method="cash", customer_id=1, address="testaddress")
        lst.append(x)
    return lst

@pytest.fixture
def order():
    return Order.objects.create(id=1, timestamp="2022-03-18 10:37:57.782908", total=60, payment_method="cash", customer_id=1, address="testaddress")

@pytest.fixture
def orderitem(order):
    lst = []
    for i in range(5):
        x = OrderItem.objects.create(category="Pizza", price=15, size=30, order_id=i, pizza_name=f"pizza{i}", quantity=i)
        lst.append(x)
    return lst