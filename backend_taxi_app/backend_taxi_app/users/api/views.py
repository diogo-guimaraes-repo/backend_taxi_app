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

from ..models import Client
from .serializers import UserSerializer, ClientSerializer, CustomUserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "email"
    lookup_value_regex = '[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ClientViewSet(UserViewSet):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
    lookup_field = "client__email"
    lookup_value_regex = '[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(client=self.request.user)

    @action(detail=False)
    def me(self, request):
        current_client = self.queryset.filter(client=self.request.user)
        client = get_object_or_404(current_client)
        serializer = ClientSerializer(client, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


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
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def list(self, request):
        serializer = self.get_serializer(self.get_object())
        return Response(status=status.HTTP_200_OK, data=serializer.data)
