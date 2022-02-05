from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.utils.translation import gettext_lazy as _
from .models import Client, Driver, User, Admin
from django.db import transaction
from django import forms as d_forms
from crispy_forms.helper import FormHelper

# User = get_user_model()

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
from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm
from allauth.account.utils import user_pk_to_url_str


class CustomResetPasswordForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator')
        template = kwargs.get("email_template_name")
        for user in self.users:
            uid = user_pk_to_url_str(user)
            token = token_generator.make_token(user)
            reset_url = f"https://taxi-app-two.vercel.app/password/reset/confirm/{uid}/{token}"
            context = {"user": user, "request": request, "email": email, "reset_url": reset_url}
            get_adapter(request).send_mail(template, email, context)
        return email


class ClientCreationForm(admin_forms.UserCreationForm):
    email = d_forms.EmailField(required=True)
    first_name = d_forms.CharField(required=True)
    last_name = d_forms.CharField(required=True)
    password1 = d_forms.PasswordInput()
    password2 = d_forms.PasswordInput()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    @transaction.atomic
    def save(self):
        # Set the user's type from the form reponse
        user = super().save(commit=False)
        user.type = User.Types.DRIVER
        user.save()
        driver = Driver.objects.create(driver=user)
        driver.save()
        return user


class AdminCreationForm(admin_forms.UserCreationForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    @transaction.atomic
    def save(self):
        # Set the user's type from the form reponse
        user = super().save(commit=False)
        user.type = User.Types.ADMIN
        user.save()
        return user
