from urllib import request
from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from ..forms import CustomResetPasswordForm
from dj_rest_auth.serializers import PasswordResetSerializer
from ..models import Admin, Client, User, Driver

# User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "birth_date", "picture", "type"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "email"}
        }


class CustomUserRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=User.Types.choices, required=True)

    @transaction.atomic
    def save(self, request):
        # Set the user's type from the form reponse
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.type = self.data.get('type')
        user.phone_number = self.data.get('phone_number')
        user.save()
        if user.type == User.Types.CLIENT:
            client = Client.objects.create(client=user)
            client.save()
        elif user.type == User.Types.DRIVER:
            driver = Driver.objects.create(driver=user)
            driver.save()
        else:
            pass

        return user


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomResetPasswordForm

    def get_email_options(self):
        return {
            "email_template_name": "account/email/password_reset_key",
        }


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["credit"]


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ["rating"]
        read_only_fields = ["rating"]


class CustomUserSerializer(serializers.ModelSerializer):
    client_details = serializers.SerializerMethodField()
    driver_details = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "birth_date",
                  "picture", "type", "address", "driver_details", "client_details"]

    def get_client_details(self, obj):
        if obj.type == User.Types.CLIENT and hasattr(obj, 'client'):
            return ClientSerializer(obj.client).data
        return None

    def get_driver_details(self, obj):
        if obj.type == User.Types.DRIVER and hasattr(obj, 'driver'):
            return DriverSerializer(obj.driver).data
        return None


class ClientUpdateSerializer(serializers.ModelSerializer):
    client = ClientSerializer()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "birth_date",
                  "picture", "type", "address", "client"]

    def update(self, instance, validated_data):
        client_details = validated_data.pop("client")
        if client_details:
            client_details["credit"] = instance.client.update_credit(client_details["credit"])
            client_serializer = ClientSerializer(instance.client, data=client_details)
            if client_serializer.is_valid():
                client_serializer.save()
        return instance
