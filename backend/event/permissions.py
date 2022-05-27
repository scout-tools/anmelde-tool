from django.contrib.auth.models import User, Group
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request
from event import models as event_models

from event.models import Registration, Event

CREATE_METHOD = 'POST'
UPDATE_METHODS = ('UPDATE', 'PATCH')


def get_event(event_id: [str, Event]) -> Event:
    if isinstance(event_id, str):
        return get_object_or_404(event_models.Event, id=event_id)
    else:
        return event_id


def get_keycloak_permission(user: User, keycloak_role: Group) -> bool:
    return user.groups.contains(keycloak_role) if keycloak_role else False


def get_responsible_person_permission(user: User, event: Event) -> bool:
    return event.responsible_persons.contains(user) if event.responsible_persons else False


def check_event_permission(event_id: [str, Event], user: User) -> bool:
    event = get_event(event_id)
    if user.is_superuser: return True
    if get_keycloak_permission(user, event.keycloak_path): return True
    if get_responsible_person_permission(user, event): return True
    return False


def check_event_super_permission(event_id: [str, Event], user: User) -> bool:
    event = get_event(event_id)
    if get_keycloak_permission(user, event.keycloak_admin_path): return True
    if get_responsible_person_permission(user, event): return True
    return False


def check_registration_permission(registration_id: str, user: User) -> bool:
    registration: Registration = get_object_or_404(Registration, id=registration_id)
    return registration.responsible_persons.contains(user) or check_event_super_permission(registration.event, user)


class IsStaffOrReadOnly(permissions.BasePermission):
    message = 'Kann nur von den Admins bearbeitet werden'

    def has_permission(self, request: Request, view) -> bool:
        return bool(
            request.method in SAFE_METHODS or
            (request.user and request.user.is_authenticated and request.user.is_staff)
        )


class IsEventSuperResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst dieses Event nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.method == CREATE_METHOD:
            return True
        event_id: str = view.kwargs.get("pk", None)
        return check_event_super_permission(event_id, request.user)


class IsSubEventSuperResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst dieses Event nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.method == CREATE_METHOD:
            return True
        event_id: str = view.kwargs.get('event_pk', None)
        return check_event_super_permission(event_id, request.user)


class IsEventResponsiblePersonOrReadOnly(permissions.BasePermission):
    message = 'Du darfst dieses Event nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        event_id: str = view.kwargs.get("pk", None)
        return check_event_permission(event_id, request.user)


class IsSubEventResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst dieses Event nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        event_id: str = view.kwargs.get('event_pk', None)
        return check_event_permission(event_id, request.user)


class IsSubEventResponsiblePersonOrReadOnly(permissions.BasePermission):
    message = 'Du darfst dieses Event nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if request.method in SAFE_METHODS:
            return True
        event_id: str = view.kwargs.get('event_pk', None)
        return check_event_permission(event_id, request.user)


class IsRegistrationResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst diese Registrierung nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method == CREATE_METHOD:
            return True
        registration_id: str = view.kwargs.get('pk', None)
        return check_registration_permission(registration_id, request.user)


class IsSubRegistrationResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst diese Registrierung nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        registration_id: str = view.kwargs.get('registration_pk', None)
        return check_registration_permission(registration_id, request.user)
