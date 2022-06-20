from django import forms

from PizzeriaManager.models import Customer, Shift, User, Booking


class UpdateUserDetails(forms.ModelForm):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=50)
    phone_no = forms.CharField(max_length=20, min_length=6)

    class Meta:
        model = Customer
        fields = ["username", "first_name", "last_name", "email", "phone_no"]


class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shift
        fields = ["user", "shift", "date"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ShiftForm, self).__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(profile__function="Staff")


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"
