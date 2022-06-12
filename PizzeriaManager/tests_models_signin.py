from datetime import datetime, date
from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from PizzeriaManager.models import Customer, User, DaysOff, Menu, Order, PizzaIngredient, OrderItem, PizzaMenuItem, Profile\
    , Shift, Booking

'''
Tests written for sign-in functionality, testing model fields + relations and generic Create/Update/Delete model items.
'''

class SigninTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='12test12', email='test@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='12test12')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)


class BaseUserModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseUserModelTestCase, cls).setUpClass()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com")
        cls.user.save()


class UserModelTestCase(BaseUserModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.user.first_name, 'jan')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)

    def test_it_has_timestamps(self):
        self.assertIsInstance(self.user.date_joined, datetime)


class BaseCustomerModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseCustomerModelTestCase, cls).setUpClass()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com", date_joined="2022-03-17 23:04:38.691991")
        cls.user.save()
        cls.customer = Customer(user_id=1, customer_id=1, first_name="jan", last_name="kowalski", username='jankowalski', password='asd', email="asd@asd.com", phone_no="124234234")
        cls.customer.save()


class CustomerModelTestCase(BaseCustomerModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.customer.first_name, 'jan')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.customer.first_name, str)
        self.assertIsInstance(self.customer.last_name, str)

    def test_its_string_representation_is_its_username_and_id(self):
        string = f"{self.customer.username}({self.customer.customer_id})"
        self.assertEquals(str(self.customer), string)


class BaseDaysoffModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseDaysoffModelTestCase, cls).setUpClass()
        cls.daysoff = DaysOff(start_date=datetime.today(), end_date=datetime.today(), reason="On demand", status="Pending", user_id=1)
        cls.daysoff.save()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com")
        cls.user.save()


class DaysoffModelTestCase(BaseDaysoffModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.daysoff.reason, 'On demand')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.daysoff.reason, str)
        self.assertIsInstance(self.daysoff.status, str)

    def test_it_has_date_fields(self):
        self.assertIsInstance(self.daysoff.start_date, datetime)


class BaseMenuModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseMenuModelTestCase, cls).setUpClass()
        cls.menu = Menu(item_id=1, item_name="Goat Cheese Pizza", item_price=15.0)
        cls.menu.save()


class MenuModelTestCase(BaseMenuModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.menu.item_name, 'Goat Cheese Pizza')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.menu.item_id, int)
        self.assertIsInstance(self.menu.item_price, float)

    def test_its_string_representation_is_its_name_and_price(self):
        string = f"{self.menu.item_name} - {self.menu.item_price} zł"
        self.assertEquals(str(self.menu), string)


class BaseOrderModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseOrderModelTestCase, cls).setUpClass()
        cls.customer = Customer(user_id=1, customer_id=1, first_name="jan", last_name="kowalski",
                                username='jankowalski', password='asd', email="asd@asd.com", phone_no="124234234")
        cls.customer.save()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com",
                        date_joined="2022-03-17 23:04:38.691991")
        cls.user.save()
        cls.order = Order(timestamp=datetime.now(), total=60.50, payment_method="cash", customer_id=1, address="asd")
        cls.order.save()


class OrderModelTestCase(BaseOrderModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.order.payment_method, 'cash')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.order.customer_id, int)
        self.assertIsInstance(self.order.total, float)


class BasePizzaIngredientModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BasePizzaIngredientModelTestCase, cls).setUpClass()
        cls.topping = PizzaIngredient(id=1, name="test_ingredient")
        cls.topping.save()


class PizzaIngredientModelTestCase(BasePizzaIngredientModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.topping.name, 'test_ingredient')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.topping.id, int)
        self.assertIsInstance(self.topping.name, str)

    def test_its_string_representation_is_its_name(self):
        string = f"{self.topping.name}"
        self.assertEquals(str(self.topping), string)


class BaseOrderItemModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseOrderItemModelTestCase, cls).setUpClass()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com",
                        date_joined="2022-03-17 23:04:38.691991")
        cls.user.save()
        cls.order = Order(id=1, timestamp=datetime.now(), total=60.50, payment_method="cash", customer_id=1, address="asd")
        cls.order.save()
        cls.order_item = OrderItem(price=15.50, size=30, order_id=1, pizza_name="WhatevsPizza", quantity=4)
        cls.order_item.save()
        cls.customer = Customer(user_id=1, customer_id=1, first_name="jan", last_name="kowalski",
                                username='jankowalski', password='asd', email="asd@asd.com", phone_no="124234234")
        cls.customer.save()


class OrderItemModelTestCase(BaseOrderItemModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.order_item.pizza_name, 'WhatevsPizza')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.order_item.order_id, int)
        self.assertIsInstance(self.order_item.quantity, int)


class BaseMenuItemModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseMenuItemModelTestCase, cls).setUpClass()
        cls.menu_item = PizzaMenuItem(id=1, name="test_MenuPizza", image="temp", img="test.png", price=15.0, size=30)
        cls.menu_item.save()


class MenuItemModelTestCase(BaseMenuItemModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.menu_item.name, 'test_MenuPizza')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.menu_item.img, str)
        self.assertIsInstance(self.menu_item.price, float)

    def test_its_string_representation_is_its_name(self):
        string = f"{self.menu_item.name}"
        self.assertEquals(str(self.menu_item), string)


class BaseProfileModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseProfileModelTestCase, cls).setUpClass()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com",
                        date_joined="2022-03-17 23:04:38.691991")
        cls.user.save()
        cls.profile = Profile(function="Staff", user_id=1)
        cls.profile.save()


class ProfileTestCase(BaseProfileModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.profile.function, 'Staff')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.profile.function, str)
        self.assertIsInstance(self.profile.user_id, int)


class BaseShiftModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseShiftModelTestCase, cls).setUpClass()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com")
        cls.user.save()
        cls.shift = Shift(date=date.today(), user_id=1, shift="12:00 - 20:00")
        cls.shift.save()


class ShiftModelTestCase(BaseShiftModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.shift.shift, "12:00 - 20:00")

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.shift.shift, str)
        self.assertIsInstance(self.shift.user_id, int)

    def test_it_has_date_fields(self):
        self.assertIsInstance(self.shift.date, date)


class ToppingViewsTests(TestCase):

    def test_topping_update_view(self):
        topping = PizzaIngredient.objects.create(id=1, name='test')
        response = self.client.post(
            reverse('update_topping', kwargs={'pk': topping.pk}),
                          {'name':'test'})

        self.assertEqual(response.status_code, 302)

    def test_topping_delete_view(self):
        topping = PizzaIngredient.objects.create(id=1, name='test')
        resp = self.client.post(reverse('delete_topping', kwargs={'pk': topping.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_topping_add_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski", email="jankowalski@gmail.com")
        profile = Profile.objects.create(user_id=1, function="Manager")
        client = Client()
        client.force_login(user)
        url = reverse('create_topping')
        dct = {
            'name': "test"
        }

        response = self.client.post(url, dct)
        self.assertEqual(response.status_code, 302)

class PizzaViewsTests(TestCase):

    def test_pizza_update_view(self):
        pizza = PizzaMenuItem.objects.create(id=1, name='test', image='temp', img="temp", price=15.0, size=30)
        response = self.client.post(
            reverse('update_pizza_details', kwargs={'pk': pizza.pk}),
                          {'name':'test'})

        self.assertEqual(response.status_code, 302)

    def test_pizza_delete_view(self):
        pizza = PizzaMenuItem.objects.create(id=1, name='test', image='temp', img="temp", price=15.0, size=30)
        resp = self.client.post(reverse('delete_pizza', kwargs={'pk': pizza.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_pizza_add_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski", email="jankowalski@gmail.com")
        profile = Profile.objects.create(user_id=1, function="Manager")
        client = Client()
        client.force_login(user)
        url = reverse('create_pizza')
        dct = {
            'id':1,
            'name': "test",
            'image':'image',
            'img':'img',
            'price':15.0,
            'size':15

        }

        response = self.client.post(url, dct)
        self.assertEqual(response.status_code, 302)


class ShiftViewsTests(TestCase):

    def test_shift_update_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        shift = Shift.objects.create(id=1, date=date(2022, 10, 15), user_id=1, shift='12:00 - 20:00')
        response = self.client.post(
            reverse('update_shift_manager', kwargs={'pk': shift.pk}),
                          {'shift':'18:00 - 2:00'})

        self.assertEqual(response.status_code, 302)

    def test_shift_delete_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        shift = Shift.objects.create(id=1, date=date(2022, 10, 15), user_id=1, shift='12:00 - 20:00')
        resp = self.client.post(reverse('delete_shift_manager', kwargs={'pk': shift.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_shift_add_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        client = Client()
        client.force_login(user)
        url = reverse('create_shift')
        dct = {
            'id':1,
            'date': date(2022, 10, 15),
            'user_id':1,
            'shift':'12:00 - 20:00'
        }

        response = self.client.post(url, dct)
        self.assertEqual(response.status_code, 302)


class OrderViewsTests(TestCase):

    def test_order_update_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        profile = Profile.objects.create(user_id=1, function="Manager")
        order = Order.objects.create(id=1, total=60.0, payment_method="cash", customer_id=1, address="asd")
        response = self.client.post(
            reverse('update_orders_manager', kwargs={'pk': order.id}),
                          {'payment_method':'card'})

        self.assertEqual(response.status_code, 302)

    def test_order_delete_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        profile = Profile.objects.create(user_id=1, function="Manager")
        order = Order.objects.create(id=1, total=60.0, payment_method="cash", customer_id=1, address="asd")
        resp = self.client.post(reverse('delete_orders_manager', kwargs={'pk': order.id}))
        self.assertEqual(resp.status_code, 302)

class DaysOffViewsTests(TestCase):

    def test_daysoff_update_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        dayoff = DaysOff.objects.create(id=1, start_date=date(2022, 7, 13), end_date=date(2022, 7, 15) , reason="On demand", status="Pending", user_id=1)
        response = self.client.post(
            reverse('update_leave', kwargs={'pk': dayoff.id}),
                          {'status':'Accepted'})

        self.assertEqual(response.status_code, 302)

    def test_daysoff_delete_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        dayoff = DaysOff.objects.create(id=1, start_date=date(2022, 7, 13), end_date=date(2022, 7, 15) , reason="On demand", status="Pending", user_id=1)
        resp = self.client.post(reverse('delete_leave', kwargs={'pk': dayoff.id}))
        self.assertEqual(resp.status_code, 302)


class UserViewsTests(TestCase):

    def test_user_update_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        response = self.client.post(
            reverse('UpdateUser', kwargs={'pk': user.id}),
                          {'email':'test@test.com'})

        self.assertEqual(response.status_code, 302)

    def test_user_delete_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        resp = self.client.post(reverse('DeleteUser', kwargs={'pk': user.id}))
        self.assertEqual(resp.status_code, 302)


class BaseBookingModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseBookingModelTestCase, cls).setUpClass()
        cls.user = User(first_name="jan", last_name="kowalski", password="asd", email="asd@asd.com",
                        date_joined="2022-03-17 23:04:38.691991")
        cls.user.save()
        cls.booking = Booking(booking_name="Jankowski", booking_no_of_people=3, user_id=1, booking_time="12:30:00")
        cls.booking.save()


class BookingModelTestCase(BaseBookingModelTestCase):

    def test_created_properly(self):
        self.assertEqual(self.booking.booking_name, 'Jankowski')

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.booking.booking_no_of_people, int)
        self.assertIsInstance(self.booking.booking_date, datetime)


class BookingViewsTests(TestCase):

    def test_shift_update_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        booking = Booking.objects.create(booking_name="Jankowski", booking_no_of_people=3, user_id=1, booking_time="12:30:00")
        response = self.client.post(
            reverse('update_booking', kwargs={'pk': booking.pk}),
                          {'booking_no_of_people':4})

        self.assertEqual(response.status_code, 302)

    def test_shift_delete_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        booking = Booking.objects.create(booking_name="Jankowski", booking_no_of_people=3, user_id=1, booking_time="12:30:00")
        resp = self.client.post(reverse('delete_booking', kwargs={'pk': booking.pk}))
        self.assertEqual(resp.status_code, 302)

    def test_shift_add_view(self):
        user = User.objects.create_user(id=1, username="Janek", first_name="Jan", last_name="Kowalski",
                                        email="jankowalski@gmail.com")
        client = Client()
        client.force_login(user)
        url = reverse('create_booking')
        dct = {
            'id':1,
            'booking_name': 'Jankowski',
            'user_id':1,
            'booking_no_of_people': 4,
            'booking_time': "12:30:00"
        }

        response = self.client.post(url, dct)
        self.assertEqual(response.status_code, 302)