from django.contrib.auth import get_user_model
from django.db.models import fields
from rest_framework import serializers
from ..models import Client, User, Driver

#User = get_user_model()


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
