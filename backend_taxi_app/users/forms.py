from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.utils.translation import gettext_lazy as _
from .models import Client, Driver, User
from django.db import transaction
from django import forms as d_forms


#User = get_user_model()

'''
class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        error_messages = {
            "email": {"unique": _("This email already exists.")}
        }
'''


class ClientCreationForm(admin_forms.UserCreationForm):
    email = d_forms.EmailField(required=True)
    first_name = d_forms.CharField(required=True)
    last_name = d_forms.CharField(required=True)
    phone_number = d_forms.CharField(required=True)

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone_number',
        ]
        error_messages = {
            "email": {"unique": _("This email already exists.")}
        }

    @transaction.atomic
    def save(self):
        # Set the user's type from the form reponse
        user = super().save(commit=False)
        user.type = User.Types.CLIENT
        user.save()
        client = Client.objects.create(client=user)
        client.save()
        return user


class DriverCreationForm(admin_forms.UserCreationForm):
    email = d_forms.EmailField(required=True)
    first_name = d_forms.CharField(required=True)
    last_name = d_forms.CharField(required=True)
    phone_number = d_forms.CharField(required=True)

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            'phone_number',
        ]
        error_messages = {
            "email": {"unique": _("This email already exists.")}
        }

    @transaction.atomic
    def save(self):
        # Set the user's type from the form reponse
        user = super().save(commit=False)
        user.type = User.Types.DRIVER
        user.save()
        driver = Driver.objects.create(driver=user)
        driver.save()
        return user
