from functools import partial
from django.contrib.auth import get_user_model
from django.db.models import query
from rest_framework import status
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from ..models import User
from .serializers import UserSerializer, CustomUserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "email"
    lookup_value_regex = '[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)


class DriversViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    serializer_class = CustomUserSerializer
    queryset = User.objects.filter(is_active=True, type=User.Types.DRIVER)


class ClientsViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    serializer_class = CustomUserSerializer
    queryset = User.objects.filter(is_active=True, type=User.Types.CLIENT)


class CurrentUserViewSet(GenericViewSet):
    serializer_class = CustomUserSerializer
    queryset = User.objects.filter(is_active=True)

    def get_object(self):
        return self.request.user

    def partial_update(self, request):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED, data=serializer.data)

    def list(self, request):
        serializer = self.get_serializer(self.get_object())
        return Response(status=status.HTTP_200_OK, data=serializer.data)
