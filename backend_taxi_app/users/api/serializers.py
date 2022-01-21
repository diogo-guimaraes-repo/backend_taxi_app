from django.contrib.auth import get_user_model
from django.db.models import fields
from rest_framework import serializers
from ..models import Client, User, Driver

#User = get_user_model()


class WritableSerializerMethodField(serializers.SerializerMethodField):

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        self.setter_method_name = kwargs.pop('setter_method_name', None)
        self.deserializer_field = kwargs.pop('deserializer_field')

        kwargs['source'] = '*'
        super(serializers.SerializerMethodField, self).__init__(**kwargs)

    def bind(self, field_name, parent):
        retval = super().bind(field_name, parent)
        if not self.setter_method_name:
            self.setter_method_name = f'set_{field_name}'

        return retval

    def to_internal_value(self, data):
        value = self.deserializer_field.to_internal_value(data)
        method = getattr(self.parent, self.setter_method_name)
        method(value)
        return {}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "phone_number", "birth_date", "picture", "type"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "email"}
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
                  "picture", "type", "driver_details", "client_details"]

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
                  "picture", "type", "client"]

    def update(self, instance, validated_data):
        client_details = validated_data.pop("client")
        if client_details:
            client_details["credit"] = instance.client.update_credit(client_details["credit"])
            client_serializer = ClientSerializer(instance.client, data=client_details)
            if client_serializer.is_valid():
                client_serializer.save()
        return instance
