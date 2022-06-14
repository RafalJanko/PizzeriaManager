"""Pizza URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from PizzeriaManager.views import index, login_view, register_view, cart_add, item_clear, item_increment, item_decrement, \
    cart_clear, cart_detail, checkout, thanks, ListOrderView, ViewUsersView, UpdateUserView, manage_users, ListOrdersView, \
    UpdateOrderView, DeleteOrderView, view_staff, ShiftCreateView, UpdateShiftView, DeleteShiftView, DeleteUserView, RequestLeave,\
    ConfirmLeave, ListLeaves, ListAllLeaves, DeleteLeaveView, UpdateLeaveView, UpdateUserDetails, ToppingCreateView, listPizzas,\
    ToppingDeleteView, UpdateToppingView, DeletePizzaView, UpdatPizzaDetails, CreatePizzaView, CreateBookingView, ConfirmBookingView, \
    ListAllBookings, DeleteBookingView, UpdateBookingView, ContactView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login_view, name="index"),
    path("login/", login_view, name="login"),
    path("logout/", login_view, name="logout"),
    path('register', register_view, name='register'),
    path('menu/', index, name='menu'),
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail,name='cart_detail'),
    path('checkout', checkout, name='checkout'),
    path('thanks/', thanks, name='thanks'),
    path('orderlist/', ListOrderView, name='orderlist'),
    path('ViewUsers/', ViewUsersView.as_view(), name='ViewUsers'),
    path('UpdateUser/<int:pk>', UpdateUserView.as_view(), name='UpdateUser'),
    path('DeleteUser/<int:pk>', DeleteUserView.as_view(), name='DeleteUser'),
    path('manage_users/<int:user_id>', manage_users, name='manage_users'),
    path('listorder', ListOrdersView.as_view(), name='list_orders_managers'),
    path('order_update/<int:pk>', UpdateOrderView.as_view(), name='update_orders_manager'),
    path('order_delete/<int:pk>', DeleteOrderView.as_view(), name='delete_orders_manager'),
    path('view_staff', view_staff, name='view_staff'),
    path('create_shift', ShiftCreateView.as_view(), name='create_shift'),
    path('shift_update/<int:pk>', UpdateShiftView.as_view(), name='update_shift_manager'),
    path('shift_delete/<int:pk>', DeleteShiftView.as_view(), name='delete_shift_manager'),
    path('request_leave', RequestLeave, name='request_leave'),
    path('confirm_leave', ConfirmLeave, name='confirm_leave'),
    path('list_user_leaves', ListLeaves, name='list_user_leaves'),
    path('list_all_leaves', ListAllLeaves, name='list_all_leaves'),
    path('leave_delete/<int:pk>', DeleteLeaveView.as_view(), name='delete_leave'),
    path('leave_update/<int:pk>', UpdateLeaveView.as_view(), name='update_leave'),
    path('user_detail_update/<int:pk>', UpdateUserDetails.as_view(), name='update_details'),
    path('create_Ingredient', ToppingCreateView.as_view(), name='create_topping'),
    path('delete_Ingredient/<int:pk>', ToppingDeleteView.as_view(), name='delete_topping'),
    path('update_Ingredient/<int:pk>', UpdateToppingView.as_view(), name='update_topping'),
    path('list_pizzas_for_edit', listPizzas , name='list_pizzas'),
    path('delete_pizza/<int:pk>', DeletePizzaView.as_view(), name='delete_pizza'),
    path('pizza_detail_update/<int:pk>', UpdatPizzaDetails.as_view(), name='update_pizza_details'),
    path('create_pizza', CreatePizzaView.as_view(), name='create_pizza'),
    path('create_booking', CreateBookingView, name='create_booking'),
    path('confirm_booking', ConfirmBookingView, name='confirm_booking'),
    path('list_all_bookings', ListAllBookings, name='list_all_bookings'),
    path('booking_delete/<int:pk>', DeleteBookingView.as_view(), name='delete_booking'),
    path('booking_update/<int:pk>', UpdateBookingView.as_view(), name='update_booking'),
    path('contact', ContactView, name="contact"),
]
