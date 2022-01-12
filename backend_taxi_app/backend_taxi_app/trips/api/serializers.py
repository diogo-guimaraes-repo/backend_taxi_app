from rest_framework import fields, serializers
from backend_taxi_app.users.models import User

from backend_taxi_app.users.api.serializers import CustomUserSerializer
from ..models import Payment, Trip


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('value', 'payment_time')


class TripSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'client', 'origin', 'destination', 'trip_status')
        read_only_fields = ('id', 'trip_status')


class TripDetailSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer(read_only=True)
    driver = CustomUserSerializer()
    payment = PaymentSerializer
    waiting_time = serializers.DurationField(max_value=None, min_value=None)

    class Meta:
        model = Trip
        fields = ('client', 'driver', 'origin', 'destination',
                  'request_time', 'waiting_time', 'payment', 'price', 'trip_status')
        read_only_fields = ('id', 'request_time')


class TripDetailUpdateSerializer(TripDetailSerializer):
    driver = CustomUserSerializer
