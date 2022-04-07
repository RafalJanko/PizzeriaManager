from datetime import date
from django.test import Client
import pytest
from django.urls import reverse

# Create your tests here.

'''
Tests written in PyTests. Some of the tests include checking:
- landing on a page while not being logged in
- landing on  a page while being logged in
- creation of model items
- update of model items
- deletion of model item
'''

@pytest.mark.django_db
def test_menu_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    url = reverse('menu')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_menu_not_logged_in():
    client = Client()
    url = reverse('menu')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_update_user_view_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    response = client.get('/user_detail_update/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_user_view_not_logged_in():
    client = Client()
    url = '/UpdateUser/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_user_update(user, users):
    test_user = users[1]
    client = Client()
    client.force_login(user)
    url = reverse('UpdateUser', kwargs={'pk':test_user.id})
    data = {
        'username': 'update',
        'first_name': "?",
        'last_name': "????",
        'email': 'moze@moze.pl',
        'password': 'asdsdfsagdf'

    }

    client.post((url, data))
    test_user.refresh_from_db()
    assert (test_user.username, 'update')


@pytest.mark.django_db
def test_checkout_get_not_logged_in():
    client = Client()
    url = reverse('checkout')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_checkout_post_not_logged_in():
    client = Client()
    url = reverse('checkout')
    response = client.post(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_users_list_not_logged_in(user):
    client = Client()
    url = reverse('ViewUsers')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_user_list_logged_in(user, users, customer):
    client = Client()
    client.force_login(user)
    url = reverse('ViewUsers')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['users'].count() == int(len(users)) + 1


@pytest.mark.django_db
def test_delete_user_view_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    response = client.get('/DeleteUser/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_user_view_not_logged_in():
    client = Client()
    url = '/DeleteUser/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_list_orders_view_logged_in(user, orders, customer):
    client = Client()
    client.force_login(user)
    response = client.get('/listorder')
    assert response.status_code == 200
    assert response.context['orders'].count() == int(len(orders))


@pytest.mark.django_db
def test_list_orders_view_not_logged_in():
    client = Client()
    url = '/listorder'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_order_logged_in(user, order, customer):
    client = Client()
    client.force_login(user)
    response = client.get('/order_update/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_order_not_logged_in():
    client = Client()
    url = '/order_update/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_order_update(user, orders):
    test_order = orders[1]
    client = Client()
    client.force_login(user)
    url = reverse('update_orders_manager', kwargs={'pk': test_order.id})
    data = {
        'timestamp': "2022-03-18 10:37:57.782908",
        'total': 60,
        'payment_method': "cash",
        'customer_id': 158,
        'address': 'testaddress'
    }

    client.post((url, data))
    test_order.refresh_from_db()
    assert (test_order.customer_id, 158)


@pytest.mark.django_db
def test_delete_order_logged_in(user, customer, order):
    client = Client()
    client.force_login(user)
    response = client.get('/order_delete/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_order_not_logged_in():
    client = Client()
    url = '/order_delete/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_view_staff_logged_in(user, customer, users):
    client = Client()
    client.force_login(user)
    url = reverse('view_staff')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_staff_not_logged_in():
    client = Client()
    url = reverse('view_staff')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_create_shift(user):
    client = Client()
    url = reverse('create_shift')
    date = {
        'date': '2022-10-12',
        'user_id': 1,
        'shift': '12:00 - 20:00',

    }
    response = client.post(url, date)
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_shift_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    url = reverse('create_shift')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_shift_not_logged_in():
    client = Client()
    url = '/create_shift'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_shift_logged_in(user, order, customer, shift):
    client = Client()
    client.force_login(user)
    response = client.get('/shift_update/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_shift_not_logged_in():
    client = Client()
    url = '/shift_update/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_shift_update(user, shift):
    client = Client()
    client.force_login(user)
    url = reverse('update_shift_manager', kwargs={'pk': shift.id})
    data = {
        'date': date(2022,3,12),
        'user_id': 155,
        'shift': '12:00 - 20:00',
    }

    client.post((url, data))
    shift.refresh_from_db()
    assert (shift.user_id, 155)


@pytest.mark.django_db
def test_delete_shift_logged_in(user, customer, shift):
    client = Client()
    client.force_login(user)
    response = client.get('/shift_delete/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_shift_not_logged_in():
    client = Client()
    url = '/shift_delete/1'
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_request_leave_logged_in(user, customer, dayoff):
    client = Client()
    client.force_login(user)
    response = client.get('/request_leave')
    assert response.status_code == 200


@pytest.mark.django_db
def test_request_leave_not_logged_in():
    client = Client()
    url = '/request_leave'
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_list_user_leaves_logged_in(user, customer, dayoff):
    client = Client()
    client.force_login(user)
    url = reverse('list_user_leaves')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_user_leaves_not_logged_in():
    client = Client()
    url = reverse('list_user_leaves')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_list_all_user_leaves_logged_in(user, customer, dayoff):
    client = Client()
    client.force_login(user)
    url = reverse('list_all_leaves')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_list_all_leaves_not_logged_in():
    client = Client()
    url = reverse('list_all_leaves')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)

@pytest.mark.django_db
def test_delete_shift_logged_in(user, customer, dayoff):
    client = Client()
    client.force_login(user)
    response = client.get('/leave_delete/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_shift_not_logged_in():
    client = Client()
    url = '/leave_delete/1'
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_leave_logged_in(user, customer, dayoff):
    client = Client()
    client.force_login(user)
    response = client.get('/leave_update/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_leave_not_logged_in():
    client = Client()
    url = '/leave_update/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_leave_update(user, daysoff):
    dayoff_test = daysoff[1]
    client = Client()
    client.force_login(user)
    url = reverse('update_leave', kwargs={'pk': dayoff_test.id})
    data = {
        'user_id': 1,
        'start_date': date(2022,3,28),
        'end_date': date(2022,3,29),
        'status': 'Accepted',
        'reason': 'On demand'
    }

    client.post((url, data))
    dayoff_test.refresh_from_db()
    assert (dayoff_test.status, 'Accepted')

@pytest.mark.django_db
def test_update_leave_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    response = client.get('/user_detail_update/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_leave_not_logged_in():
    client = Client()
    url = '/user_detail_update/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_leave_update(users, user):
    user_test = users[1]
    client = Client()
    client.force_login(user)
    url = reverse('update_leave', kwargs={'pk': user.id})
    data = {
        'user_id': 1,
        'username': 'Janekupdate',
        'first_name': "Jan",
        'last_name': 'Kowalski',
        'email': "jankowalski@gmail.com",

    }

    client.post((url, data))
    user_test.refresh_from_db()
    assert (user_test.username, 'Janekupdate')


@pytest.mark.django_db
def test_create_ingredient(user):
    client = Client()
    url = reverse('create_topping')
    date = {
        'id': 122,
        'name': 'test1',
    }

    response = client.post(url, date)
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_ingredient_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    url = reverse('create_topping')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_ingredient_not_logged_in():
    client = Client()
    url = '/create_Ingredient'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_ingredient_logged_in(user, customer, ingredient):
    client = Client()
    client.force_login(user)
    response = client.get('/delete_Ingredient/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_ingredient_not_logged_in():
    client = Client()
    url = '/delete_Ingredient/1'
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_ingredient_logged_in(user, customer, ingredient):
    client = Client()
    client.force_login(user)
    response = client.get('/update_Ingredient/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_ingredient_not_logged_in():
    client = Client()
    url = '/update_Ingredient/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_ingredient_update(users, user, ingredients):
    test_ingredient = ingredients[1]
    client = Client()
    client.force_login(user)
    url = reverse('update_topping', kwargs={'pk': test_ingredient.id})
    data = {
        'id': 1,
        'name': 'ingredienttest',
    }

    client.post((url, data))
    test_ingredient.refresh_from_db()
    assert (test_ingredient.name, 'ingredienttest')

@pytest.mark.django_db
def test_list_pizzas_for_edit_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    url = reverse('list_pizzas')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_menu_not_logged_in():
    client = Client()
    url = reverse('list_pizzas')
    response = client.get(url)
    assert response.status_code == 302
    url = reverse('index')
    assert response.url.startswith(url)


@pytest.mark.django_db
def test_delete_pizza_logged_in(user, customer, pizza):
    client = Client()
    client.force_login(user)
    response = client.get('/delete_pizza/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_pizza_not_logged_in():
    client = Client()
    url = '/delete_pizza/1'
    response = client.get(url)
    assert response.status_code == 302

@pytest.mark.django_db
def test_update_pizza_detail_logged_in(user, customer, pizza):
    client = Client()
    client.force_login(user)
    response = client.get('/pizza_detail_update/1')
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_pizza_detail_not_logged_in():
    client = Client()
    url = '/pizza_detail_update/1'
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_pizza_detail_update(user, customer, pizzas):
    test_pizza = pizzas[1]
    client = Client()
    client.force_login(user)
    url = reverse('update_pizza_details', kwargs={'pk': test_pizza.id})
    data = {
        'id': 1,
        'name': 'pizzaupdate',
        'category': 'Pizza',
        'img': 'test',
        'image': 'temp',
        'price': 15,
        'size': 30,
    }

    client.post((url, data))
    test_pizza.refresh_from_db()
    assert (test_pizza.name, 'ingredienttest')

@pytest.mark.django_db
def test_create_pizza(user, customer):
    client = Client()
    url = reverse('create_pizza')
    date = {
        'id': 1,
        'name': 'pizzaupdate',
        'category': 'Pizza',
        'img': 'test',
        'image': 'temp',
        'price': 15,
        'size': 30,
    }
    response = client.post(url, date)
    assert response.status_code == 302


@pytest.mark.django_db
def test_create_pizza_logged_in(user, customer):
    client = Client()
    client.force_login(user)
    url = reverse('create_pizza')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_pizza_not_logged_in():
    client = Client()
    url = '/create_pizza'
    response = client.get(url)
    assert response.status_code == 302


