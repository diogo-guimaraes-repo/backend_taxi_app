from rest_framework import permissions
from .models import User


class AdminAccessOnly(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.type == User.Types.ADMIN:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False


class ClientNotAllowed(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated and (request.user.type == User.Types.ADMIN or request.user.type == User.Types.DRIVER):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.user.type == User.Types.ADMIN or request.user.type == User.Types.DRIVER:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        return False
