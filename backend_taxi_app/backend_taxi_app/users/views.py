from django.contrib.auth import get_user_model
from .models import Client, Driver
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView, CreateView

from .forms import ClientCreationForm, DriverCreationForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "email"
    slug_url_kwarg = "email"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["first_name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:email", kwargs={"email": self.request.user.email})


user_redirect_view = UserRedirectView.as_view()


class ClientSignUpView(CreateView):
    model = Client
    form_class = ClientCreationForm
    template_name = '../templates/account/signup.html'


client_signup_view = ClientSignUpView.as_view()


class DriverSignUpView(CreateView):
    model = Driver
    form_class = DriverCreationForm
    template_name = '../templates/account/signup.html'


driver_signup_view = DriverSignUpView.as_view()
