from django.contrib.auth.models import User
from rest_framework import permissions, status, exceptions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request
from event import models as event_models

from time import process_time

CREATE_METHOD = 'POST'
UPDATE_METHOD = 'UPDATE'


def check_event_permission(event_id: str, user: User) -> bool:
    t1_start = process_time()
    event = get_object_or_404(event_models.Event, id=event_id)
    group_match: bool = user.groups.contains(event.keycloak_path) if event.keycloak_path else False
    responsible_person_match: bool = event.responsible_persons.contains(user) if event.responsible_persons else False
    t1_stop = process_time()
    print(f"Elapsed time: {(t1_stop - t1_start) * 1000}")
    return bool(group_match or responsible_person_match)


class IsStaffOrReadOnly(permissions.BasePermission):
    message = 'Kann nur von den Admins bearbeitet werden'

    def has_permission(self, request: Request, view):
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_authenticated and request.user.is_staff)
        )


class IsEventResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst dieses Event nicht bearbeiten'

    def has_permission(self, request: Request, view):
        if not request.user and not request.user.is_authenticated:
            return False
        if request.method == CREATE_METHOD:
            return True
        event_id = view.kwargs.get("pk", None)
        return check_event_permission(event_id, request.user)


class IsSubEventResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst dieses Event nicht bearbeiten'

    def has_permission(self, request: Request, view):
        if not request.user and not request.user.is_authenticated:
            return False
        event_id = view.kwargs.get('event_pk', None)
        return check_event_permission(event_id, request.user)
