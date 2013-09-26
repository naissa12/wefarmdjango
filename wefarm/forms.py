from django import forms
from models import Farmer
from django.contrib.auth.models import User
from registration.forms import RegistrationForm
from registration.signals import user_registered


class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        exclude = ['user', 'wepay_access_token', 'wepay_account_id']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class CustomRegistrationForm(RegistrationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    farm = forms.CharField(required=True)
    produce = forms.CharField(required=True)
    produce_price = forms.DecimalField(
        required=True, min_value=0)


def user_created(sender, user, request, **kwargs):
    form = FarmerForm(request.POST)
    item, c = Farmer.objects.get_or_create(user=user)
    item.farm = form.data["farm"]
    item.produce = form.data["produce"]
    item.produce_price = form.data["produce_price"]
    item.save()

    user.first_name = form.data["first_name"]
    user.last_name = form.data["last_name"]
    user.is_active = True
    user.save()

user_registered.connect(user_created)
