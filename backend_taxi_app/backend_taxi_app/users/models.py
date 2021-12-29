from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Default user for Taxi App Backend."""

    class Types(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        DRIVER = "DRIVER", "Driver"
        ADMIN = "ADMIN", "Admin"

    base_type = Types.CLIENT
    email = models.EmailField(unique=True,
                              blank=False, max_length=254, verbose_name="email address")
    birth_date = models.DateField(_("Birth Date"), null=True, blank=True)
    user_type = models.CharField(
        max_length=50, choices=Types.choices, default=base_type)
    picture = models.ImageField(_("Profile Picture"), upload_to='uploads/% Y/% m/% d/', blank=True)
    type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"email": self.email})


class Client(models.Model):
    client = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    credit = models.FloatField(default=0.00)
    base_type = User.Types.CLIENT
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=False, unique=True, default="")

    def __str__(self):
        return self.client.email


class Driver(models.Model):
    driver = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.FloatField(default=0.00)
    base_type = User.Types.DRIVER
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=False, unique=True, default="")

    def __str__(self):
        return self.driver.email


class Admin(models.Model):
    admin = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    base_type = User.Types.ADMIN
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=False, unique=True, default="")

    def __str__(self):
        return self.admin.email
