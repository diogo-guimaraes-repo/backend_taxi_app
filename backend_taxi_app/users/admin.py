from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import User, Client, Driver
#from backend_taxi_app.users.forms import UserChangeForm, UserCreationForm

User = get_user_model()


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Driver)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    #form = UserChangeForm
    #add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "type", "phone_number", "birth_date", "picture")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "first_name", "last_name", "is_superuser"]
    search_fields = ["email"]
    ordering = ('email',)
