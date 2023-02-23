![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
# PizzeriaManager

This is a Django-bassed application that is responsible for both ordering pizza online, as well as a whole employee management system. There are 4 types of users defined. When a user registers, he/she is automatically assigned a "Customer" type, however all users can be changed into "Staff", "Manager" or "HR. Depending on the user type, different views are accessible to the user.

Customer users have the following functionalities:
* Order pizzas online
* View order history
* Update user details in the system
* Request table booking in a restaurant
* View their own booking hisotry & status

Staff users have the following functionalities:
* All of the Customer functionalities are available
* Can view shifts assigned to them
* Can request days off
* Can view history and status of all requested days off

Manager/HR users have the following functionalities:
* Customer + Staff functionalities are available
* View and edit users and their types
* View and approve leaves
* Edit placed order (update to "completed")
* Edit the menu
* Add new toppings and assign them to pizzas
* Approve/Decline table booking requests

The app has an authentication and authorization system.


## Technology used

Python 3, Django, Bootstrap, Django-cart, SQL, HTML, Black, iSort, JavaScript

## Tests

App has a set of tests to verify that all functionalities are running. The tests are divided into 2 separate files:
* tests.py - tests all functionalities/views

* tests_models_signin.py - tests the authorization/authentication as well as all models and it's option to create/update/delete

Example tests:
```python

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
```
```python
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
```
## Running the project

* clone the repository from GitHub

Using the console naviagte to the cloned repository and run the following commands:

* pip install virtualenv
* virtualenv “name as you like”
* source env/bin/activate
* pip install -r requirements.txt
* python manage.py runserver

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
