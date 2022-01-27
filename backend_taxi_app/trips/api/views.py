from lib2to3.pgen2 import driver
from rest_framework import filters
from django.db.models import Q
from rest_framework.decorators import permission_classes
from .serializers import TripSerializer, TripDetailSerializer, TripDetailUpdateSerializer, TripPaymentSerializer
from ..models import Trip, User
from django.utils import timezone
from rest_framework import permissions, viewsets


class TripsViewSet(viewsets.ReadOnlyModelViewSet):
    search_fields = ['trip_status', 'driver__email']
    filter_backends = (filters.SearchFilter,)
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MyTripsViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.type == User.Types.CLIENT:
            return Trip.objects.filter(client=user).order_by('-request_time')[:4]
        if user.type == User.Types.DRIVER:
            return Trip.objects.filter(~Q(trip_status=Trip.Status.COMPLETE) & Q(driver=user))
        return Trip.objects.none()

    def perform_create(self, serializer):
        return serializer.save(client=self.request.user, request_time=timezone.now())


class TripView(viewsets.ModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TripDetailSerializer

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return TripDetailUpdateSerializer
        return TripDetailSerializer

    def get_queryset(self):
        return Trip.objects.all()


class PayView(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TripPaymentSerializer
