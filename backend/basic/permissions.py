from rest_framework import permissions, status, exceptions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request


class IsStaffOrReadOnly(permissions.BasePermission):
    message = 'Kann nur von den Admins bearbeitet werden'

    def has_permission(self, request: Request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_authenticated and request.user.is_staff)
        )
