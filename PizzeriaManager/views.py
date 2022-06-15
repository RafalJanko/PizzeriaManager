import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import UpdateView, ListView, DeleteView, CreateView
from PizzeriaManager.models import PizzaMenuItem, Customer, Order, OrderItem, Profile, Shift, DaysOff, PizzaIngredient, Booking
from django.shortcuts import render, redirect
from cart.cart import Cart
from PizzeriaManager.forms import ShiftForm
from django.forms import inlineformset_factory

# Create your views here.


'''
function that calculates the number all items in a customer's cart, it's total and is able to show how many pizzas of the same type are ordered in the cart section.
This has to be used in a view in order to see the current number of items in a cart, while using different views.
'''

def calculate_costam(session):
    total = []
    total_items = []
    number = 0
    number_items = 0
    cart = session["cart"]

    for car in cart:
        a = (float(cart[car]['quantity']) * float(cart[car]['price']))
        b = (cart[car]['quantity'])
        total.append(a)
        total_items.append(b)
    for item in range(0, len(total)):
        number = number + total[item]
        number_items = number_items + total_items[item]
    return number, number_items, total

'''
APART FROM THE LOGIN/REGISTER VIEW, ALL VIEWS REQUIRE TO BE LOGGED IN.
EACH VIEW IS COMMENTED WITH A TYPE OF A USER THAT CAN VIEW/USE IT.
'''

'''
Django login functionality
'''


@csrf_exempt
def login_view(request):
    username = request.POST.get("uname")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("menu"))
    else:
        return render(request, "PizzeriaManager/login.html", {"message": ""})


'''
Django register functionality - for the use of this project, it was joined with login on the same page
'''


@csrf_exempt
def register_view(request):
    username = request.POST["uname"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        return render(request, "PizzeriaManager/login.html", {"message": "User already registered"})
    else:
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pnumber = request.POST["pnumber"]

        user = User.objects.create_user(username=username, email=email, password=password, first_name=fname, last_name=lname)
        user.first_name = fname
        user.last_name = lname
        id = user.id
        c = Customer.objects.create(first_name=fname, last_name=lname, username=username, password=password, email=email, phone_no=pnumber, user_id=id)
        login(request, user)
        prof = Profile.objects.create(function="Customer", user_id=id)
        permission = 3
        user.user_permissions.add(permission)
        user.save()

        return render(request, "PizzeriaManager/login.html", {"message": "User registered successfully"})


'''
Functionality accessible only to all logged in users.
Simple logout functionality
'''


def logout_view(request):
    Session.objects.all().delete()
    return render(request, "PizzeriaManager/login.html", {"message": "Logged out."})


'''
Functionality accessible only to all logged in users.
Base view, used after a user logs in. It lists all the pizzas, together with their details.
Navbar functionalities change, depending on the user type.
Customers cas see: Menu button, Edit profile button, Orders button (view order history and clear cart button and log out button.
Staff users can see Customers options + Staff tab - request leave and View leave history
Managers/HR can see Staff options + manager tab - managing users (update profile and details), managing leaves (update/delete leaves), managing shifts (create/update/delete for staff members) and manage orders (complete/delete orders)
'''


@login_required(login_url="/login")
def index(request):
    if request.method == 'GET':
        total = []
        total_items = []
        number = 0
        number_items = 0

        if "cart" not in request.session:
            pass
        else:
            cart = request.session["cart"]

            for car in cart:
                a = (float(cart[car]['quantity']) * float(cart[car]['price']))
                b = (cart[car]['quantity'])
                total.append(a)
                total_items.append(b)
            for item in range(0, len(total)):
                number = number + total[item]
                number_items = number_items + total_items[item]
        pizzas = PizzaMenuItem.objects.all()

        return render(request, 'PizzeriaManager/menu.html', {'pizzas': pizzas, 'number':number, 'number_items':number_items})
    return HttpResponse(status=405)


'''
Functionality accessible only to all logged in users.
Functionality from the django-cart package that allows to add to cart and in the Cart details view
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_menu')
def cart_add(request, id):
    cart = Cart(request)
    product = PizzaMenuItem.objects.get(id=id)
    cart.add(product=product)
    return redirect("menu")


'''
Functionality accessible only to all logged in users.
Django-cart functionality that allows a user to remove an item from a cart
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_menu')
def item_clear(request, id):
    cart = Cart(request)
    product = PizzaMenuItem.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


'''
Functionality accessible only to all logged in users.
Django-cart functionality that allows to add more items of the same sort in the cart details view
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_menu')
def item_increment(request, id):
    cart = Cart(request)
    product = PizzaMenuItem.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


'''
Functionality accessible only to all logged in users.
Django-cart functionality that allows to remove items of the same sort in the cart details view
I've programmed the functionality to change button's functionality to "remove item from cart" if the quantity of an item = 1
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_menu')
def item_decrement(request, id):
    cart = Cart(request)
    product = PizzaMenuItem.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


'''
Functionality accessible only to all logged in users.
Django-cart functionality that allows a user to clear all items from the cart in 1 click
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_menu')
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("menu")


'''
Functionality accessible only to all logged in users.
Django-cart functionality that allows a user to view all items in their cart, together with the details of the cart
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_menu')
def cart_detail(request):
    number, number_items, total = calculate_costam(request.session)
    return render(request, 'PizzeriaManager/cart.html', {'number': number, 'number_items':number_items})


'''
Functionality accessible only to all logged in users.
A functionality that redirects user to a form that allows them to fill in the details of their order, such as:
- summary of the order and user details
- delivery address
- payment type
'''


@csrf_exempt
@login_required(redirect_field_name='index')
@permission_required('PizzeriaManager.view_menu')
def checkout(request):
    if request.method == "POST":

        number, number_items, total = calculate_costam(request.session)

        return render(request, 'PizzeriaManager/checkout.html', {'number': number, 'number_items':number_items, 'total':total})


'''
Functionality accessible only to all logged in users.
A summary of a placed order with unique order id assigned to it.
This view creates all respective model items that are assigned to user id.
'''


@csrf_exempt
@login_required(redirect_field_name='/login')
def thanks(request):
    if request.method == "POST":

        cart = request.session["cart"]
        user = request.user.id
        payment_method = request.POST.get("paymenttype")
        address = request.POST.get("address")

        number, number_items, total = calculate_costam(request.session)

        o = Order.objects.create(customer_id=user, total=number, payment_method=payment_method, address=address)
        order_id = o.id

        for item in cart:
            category = "Pizza"
            price = cart[item]['price']
            size = 30
            order_id = order_id
            pizza_name = cart[item]['name']
            quantity = cart[item]['quantity']
            oi = OrderItem.objects.create(category=category, price=price, size=size, order_id=order_id, pizza_name=pizza_name, quantity=quantity)

        cart_clear(request)
        return render(request, "PizzeriaManager/thanks.html", {'number': number, 'number_items':number_items,
                                                               'total':total, "cart":cart, "order_id":order_id})


'''
Functionality accessible only to all logged in users.
A functionality to view currently logged in's user past orders
'''


@login_required(redirect_field_name='/login')
def ListOrderView(request):

    number, number_items, total = calculate_costam(request.session)
    orders = Order.objects.filter(customer_id=request.user.id)

    return render(request, 'PizzeriaManager/orderlist.html',
                      {'number': number, 'number_items': number_items, 'total': total, "orders":orders})


'''
Functionality accessible only to HR and Manager users.
It allows them to update users roles, update their details and delete respective users
'''


class ViewUsersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('PizzeriaManager.change_daysoff')
    model = User
    queryset = User.objects.all()
    fields = '__all__'
    template_name = 'PizzeriaManager/userlist.html'
    context_object_name = "users"


'''
Functionality accessible only to HR and Manager users.
Functionality to update details - related to the functionality above (listing all users).
'''


class UpdateUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('PizzeriaManager.change_user')
    model = User
    fields = '__all__'
    success_url = reverse_lazy('ViewUsers')
    template_name = 'PizzeriaManager/form.html'


'''
Functionality accessible only to HR and Manager users.
Functionality to delete a user - related to the functionality above (listing all users).
'''


class DeleteUserView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('PizzeriaManager.delete_user')
    model = User
    success_url = reverse_lazy('ViewUsers')


'''
Functionality accessible only to HR and Manager users.
Functionality to list all orders, created by all user
'''


class ListOrdersView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('PizzeriaManager.view_order')
    model = Order
    queryset = Order.objects.all()
    fields = '__all__'
    template_name = 'PizzeriaManager/managerorderlist.html'
    context_object_name = 'orders'


'''
Functionality accessible only to HR and Manager users.
Functionality to update orders. Linked to the functionality above - listing all orders from all users.
'''


class UpdateOrderView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('PizzeriaManager.change_order')
    model = Order
    fields = ('completed', )
    success_url = reverse_lazy('list_orders_managers')
    template_name = 'PizzeriaManager/form.html'


'''
Functionality accessible only to HR and Manager users.
Functionality to delete orders. Linked to the functionality above - listing all orders from all users.
'''


class DeleteOrderView (LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('PizzeriaManager.delete_order')
    model = Order
    success_url = reverse_lazy('list_orders_managers')


'''
Functionality accessible only to HR and Manager users.
Functionality to user profiles. Linked to the functionality above - listing all orders from all users.
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.change_daysoff')
def manage_users(request, user_id):
    user = User.objects.get(pk=user_id)
    ProfileUserSet = inlineformset_factory(User, Profile, fields=('function',))
    if request.method == "POST":
        formset = ProfileUserSet(request.POST, request.FILES, instance=user)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(str(user.id))
    else:
        formset = ProfileUserSet(instance=user)
    return render(request, "PizzeriaManager/manage_users.html", {'formset':formset})


'''
Functionality accessible only to HR and Manager users.
Functionality to view all user whose role is changed to "staff. On this page, one can find also the list of shifts, together with an option to create new ones and deleteing existing ones
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.change_daysoff')
def view_staff(request):
    if request.method == "GET":
        staff = User.objects.filter(profile__function="Staff")
        return render(request, "PizzeriaManager/list_staff.html", {"staff":staff})


'''
Functionality accessible only to HR and Manager users.
Functionality to create shifts for users whose profile is changed to Staff. Linked to the functionality above - listing all staff members and their shifts.
'''


class ShiftCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('PizzeriaManager.add_shift')
    template_name = 'PizzeriaManager/shift_form.html'
    form_class = ShiftForm
    success_url = reverse_lazy('view_staff')

    def get_form_kwargs(self):
        kwargs = super(ShiftCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


'''
Functionality accessible only to HR and Manager users.
Functionality to update shifts for users whose role is changed to Staff. Linked to the functionality above - listing all staff members and their shifts.
'''


class UpdateShiftView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('PizzeriaManager.change_shift')
    model = Shift
    fields = ('date', 'shift', )
    success_url = reverse_lazy('view_staff')
    template_name = 'PizzeriaManager/form.html'


'''
Functionality accessible only to HR and Manager users.
Functionality to delete shifts for users whose role is changed to Staff. Linked to the functionality above - listing all staff members and their shifts.
'''


class DeleteShiftView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('PizzeriaManager.delete_shift')
    model = Shift
    success_url = reverse_lazy('view_staff')


'''
Functionality accessible only to Staff, HR and Manager users.
Functionality to create a leave request for users whose role is changed to Staff, HR or Managers.
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_shift')
def RequestLeave(request):
    if request.method == "GET":
        return render(request, "PizzeriaManager/request_leave.html")


'''
Functionality accessible only to HR and Manager users.
Functionality to update (accept) a leave request for users whose role is changed to Staff, HR or Managers.
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_shift')
def ConfirmLeave(request):
    if request.method == "POST":
        user_id = request.user.id
        start_date = request.POST.get("start")
        end_date = request.POST.get("end")
        reason = request.POST.get("reason")

        leave = DaysOff.objects.create(start_date=start_date, end_date=end_date, reason=reason, user_id=user_id)

        return render(request, "PizzeriaManager/confirm_leave_request.html")


'''
Functionality accessible only to Staff, HR and Manager users.
Functionality to list all leaves for a currently logged in user, whose role is changed to Staff, HR or Managers.
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.view_shift')
def ListLeaves(request):
    if request.method == "GET":
        leaves = DaysOff.objects.filter(user_id=request.user.id)
        return render(request, "PizzeriaManager/listuserleaves.html", {"leaves":leaves})


'''
Functionality accessible only to HR and Manager users.
Functionality to create all leave request for users whose role is changed to Staff, HR or Managers. (and update the status - accept/delete them)
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.change_daysoff')
def ListAllLeaves(request):
    if request.method == "GET":
        leaves = DaysOff.objects.all()
        return render(request, "PizzeriaManager/listallleaves.html", {"leaves": leaves})


'''
Functionality accessible only to HR and Manager users.
Functionality to delete a leave request for users whose role is changed to Staff, HR or Managers. Linked to the functionality above to view all leave requests.
'''


class DeleteLeaveView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('PizzeriaManager.delete_daysoff')
    model = DaysOff
    success_url = reverse_lazy('list_all_leaves')


'''
Functionality accessible only to HR and Manager users.
Functionality to update a leave request for users whose role is changed to Staff, HR or Managers. Linked to the functionality above to view all leave requests.
'''


class UpdateLeaveView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('PizzeriaManager.change_daysoff')
    model = DaysOff
    fields = ('start_date', 'end_date', 'status', )
    success_url = reverse_lazy('list_all_leaves')
    template_name = 'PizzeriaManager/form.html'


'''
Functionality accessible only to all users.
Functionality to edit currently logged in user details.
'''


class UpdateUserDetails(LoginRequiredMixin, UpdateView):
    model = Customer
    fields = ['username', 'first_name', 'last_name', 'email', "phone_no"]
    success_url = reverse_lazy('menu')

    def get_object(self, queryset=None):
        return self.request.user.customer


'''
Functionality accessible only to HR and Manager users.
Functionality to create a topping that can be assigned to a pizza
'''


class ToppingCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('PizzeriaManager.add_pizzaingredient')
    model = PizzaIngredient
    fields = '__all__'
    success_url = reverse_lazy('list_pizzas')


'''
Functionality accessible only to HR and Manager users.
Functionality to create a topping that can be assigned to a pizza
'''


class ToppingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('PizzeriaManager.delete_pizzaingredient')
    model = PizzaIngredient
    success_url = reverse_lazy('list_pizzas')


'''
Functionality accessible only to HR and Manager users.
Functionality that lists all topping, allows to edit/create/delete them, as well as lists all pizzas (allows to create/edit/delete them) together with the toppings, related to them
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.change_daysoff')
def listPizzas(request):
    if request.method == 'GET':
        pizzas = PizzaMenuItem.objects.all()
        toppings = PizzaIngredient.objects.all()
        return render(request, 'PizzeriaManager/list_pizzas_for_edit.html', {"pizzas":pizzas, "toppings":toppings})


'''
Functionality accessible only to HR and Manager users.
Functionality to update a topping that can be assigned to a pizza - used in the view above (listing all currently created pizzas and toppings)
'''


class UpdateToppingView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('PizzeriaManager.change_pizzaingredient')
    model = PizzaIngredient
    fields = 'name',
    success_url = reverse_lazy('list_pizzas')


'''
Functionality accessible only to HR and Manager users.
Functionality to create a pizza - used in the view above (listing all currently created pizzas and toppings)
'''


class CreatePizzaView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('PizzeriaManager.create_pizzamenuitem')
    model = PizzaMenuItem
    fields = '__all__'
    success_url = reverse_lazy('list_pizzas')


'''
Functionality accessible only to HR and Manager users.
Functionality to delete a pizza - used in the view above (listing all currently created pizzas and toppings)
'''


class DeletePizzaView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('PizzeriaManager.delete_pizzamenuitem')
    model = PizzaMenuItem
    success_url = reverse_lazy('list_pizzas')


'''
Functionality accessible only to HR and Manager users.
Functionality to update a pizza - used in the view above (listing all currently created pizzas and toppings)
'''


class UpdatPizzaDetails(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('PizzeriaManager.change_pizzamenuitem')
    model = PizzaMenuItem
    fields = '__all__'
    success_url = reverse_lazy('list_pizzas')


'''
Functionality accessible only to HR and Manager users.
Functionality to list all table bookings, with links to change and delete them.
'''


@login_required(login_url="/login")
@permission_required('PizzeriaManager.change_daysoff')
def ListAllBookings(request):
    if request.method == "GET":
        bookings = Booking.objects.all()
        return render(request, "PizzeriaManager/listallbookings.html", {"bookings": bookings})


'''
Functionality accessible to everyone
Functionality to request a table booking.
'''

@login_required(login_url="/login")
def CreateBookingView(request):
    if request.method == "GET":
        return render(request, "PizzeriaManager/request_booking.html")


'''
Functionality accessible to everyone.
Functionality to view the confirmation of a requested booking. This view creates a db entry of the booking.
'''

@login_required(login_url="/login")
def ConfirmBookingView(request):
    if request.method == "POST":
        user = request.user
        booking_name = request.POST.get("booking_name")
        booking_time = request.POST.get("booking_time")
        booking_no_of_people = request.POST.get("booking_no_of_people")

        booking = Booking.objects.create(user=user, booking_name=booking_name, booking_time=booking_time, booking_no_of_people=booking_no_of_people)

        def send_email_fct(filename, filepath, fromaddr, mdpfrom, toaddr):
            """" filename: file name to be sent with extension
                 filepath: file path of the file to be sent
                 fromaddr: sender email address
                 mdpfrom: password of sender email address
                 toaddr: receiver email address"""

        msg = MIMEMultipart()  # instance of MIMEMultipart
        msg['From'] = "YOUR EMAIL ADDRESS"
        msg['To'] = user.email
        msg['Subject'] = "Booking request confirmation"

        body_email = "Thank you for sending a request to book a table. We will let you know once the booking is confirmed"
        msg.attach(MIMEText(body_email, 'plain'))

        s = smtplib.SMTP('smtp.gmail.com', 587)  # SMTP
        s.starttls()
        s.login("YOUR EMAIL ADDRESS", "YOUR APP PASSWORD")

        text = msg.as_string()

        s.sendmail("YOUR EMAIL ADDRESS", user.email, text)  # sending the email
        s.quit()  # terminating the session

        return render(request, "PizzeriaManager/confirm_booking.html")


'''
Functionality accessible only to HR and Manager users.
Functionality to delete bookings (booking model instances), from the "list all bookings view".
'''


class DeleteBookingView(LoginRequiredMixin, DeleteView):
    model = Booking
    success_url = reverse_lazy('list_all_bookings')


'''
Functionality accessible only to HR and Manager users.
Functionality to update bookings (booking model instances), from the "list all bookings view".
'''


class UpdateBookingView(LoginRequiredMixin, UpdateView):
    model = Booking
    fields = '__all__'
    success_url = reverse_lazy('list_all_bookings')
    template_name = 'PizzeriaManager/form.html'


""" Simple contact page"""

def ContactView(request):
    return render(request, "PizzeriaManager/contact.html")