from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework import status

from backend_taxi_app.users.api.serializers import CustomUserSerializer
from ..models import Payment, Trip


class InsufficientFundsExcpetion(PermissionDenied):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Insufficient credit."
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class BadTripStatusExcpetion(PermissionDenied):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Not allowed"
    default_code = 'invalid'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('value', 'payment_time', 'payment_method')


class TripSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer(read_only=True)

    class Meta:
        model = Trip
        fields = ('id', 'client', 'origin', 'destination', 'trip_status')
        read_only_fields = ('id', 'trip_status')


class TripDetailSerializer(serializers.ModelSerializer):
    client = CustomUserSerializer(read_only=True)
    driver = CustomUserSerializer()
    payment = PaymentSerializer()
    waiting_time = serializers.DurationField(max_value=None, min_value=None)

    class Meta:
        model = Trip
        fields = ('client', 'driver', 'origin', 'destination',
                  'request_time', 'waiting_time', 'payment', 'price', 'trip_status')
        read_only_fields = ('id', 'request_time')


class TripDetailUpdateSerializer(TripDetailSerializer):
    driver = CustomUserSerializer


class TripPaymentSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer()

    class Meta:
        model = Trip
        fields = ('payment',)

    def update(self, instance, validated_data):
        payment_data = validated_data.pop('payment')
        if instance.pay_trip(payment_data) == "INSUFFICIENT_FUNDS":
            raise InsufficientFundsExcpetion(detail={"message": "Not enough credit."},
                                             status_code=status.HTTP_406_NOT_ACCEPTABLE)
        return instance


class TripCancelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('trip_status',)

    def update(self, instance, validated_data):
        status = validated_data.pop('trip_status')
        if status != Trip.Status.CANCELLED:
            raise BadTripStatusExcpetion(detail={"message": "Not allowed."})
        instance.cancel_trip()
        return instance
