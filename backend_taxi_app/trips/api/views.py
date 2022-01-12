from django.db.models import query_utils
from rest_framework.decorators import permission_classes
from .serializers import PaymentSerializer, TripSerializer, TripDetailSerializer, TripDetailUpdateSerializer
from ..models import Trip, Payment, User
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import permissions, viewsets


class TripsViewSet(viewsets.ReadOnlyModelViewSet):
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
            return Trip.objects.filter(client=user)
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
