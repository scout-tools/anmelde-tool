from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
from rest_framework.request import Request

from event.api_exceptions import RequiredGroupNotFound
from event.helper import custom_get_or_404, get_registration
from event.helper import get_event
from event.models import Registration, Event

CREATE_METHOD = 'POST'
UPDATE_METHODS = ('UPDATE', 'PATCH')

User = get_user_model()


def get_keycloak_permission(user: User, keycloak_role: Group) -> bool:
    has_role = user.groups.filter(name=keycloak_role).exists()

    return has_role


def get_responsible_person_permission(user: User, event: Event) -> bool:
    return event.responsible_persons.contains(user) if event.responsible_persons else False


def check_event_permission(event_id: [str, Event], user: User) -> bool:
    event = get_event(event_id)
    if user.is_superuser:
        return True
    if get_keycloak_permission(user, event.keycloak_path):
        return True
    if get_keycloak_permission(user, event.keycloak_admin_path):
        return True
    if get_responsible_person_permission(user, event):
        return True
    return False


def check_leader_permission(event_id: [str, Event], user: User) -> bool:
    event = get_event(event_id)
    if event.limited_registration_hierarchy.id == 493:
        perm_name = 'dpv_bundesfuehrungen'
        bufu_group = custom_get_or_404(RequiredGroupNotFound(perm_name), Group, name=perm_name)
        return get_keycloak_permission(user, bufu_group)
    else:
        return False


def check_event_permission_admin(event_id: [str, Event], user: User) -> bool:
    event = get_event(event_id)
    if user.is_superuser:
        return True
    if get_keycloak_permission(user, event.keycloak_admin_path):
        return True
    if get_responsible_person_permission(user, event):
        return True
    return False


def check_event_super_permission(event_id: [str, Event], user: User) -> bool:
    event = get_event(event_id)
    if get_keycloak_permission(user, event.keycloak_admin_path):
        return True
    if get_responsible_person_permission(user, event):
        return True
    return False


def check_registration_permission(registration_id: str, user: User) -> bool:
    registration: Registration = get_registration(registration_id)
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


class IsLeaderPerson(permissions.BasePermission):
    message = 'Du darfst die Statistik dieses Events nicht ansehen'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        event_id: str = view.kwargs.get('event_pk', None)
        return check_leader_permission(event_id, request.user)


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
        if request.user.is_superuser:
            return True
        registration_id: str = view.kwargs.get('pk', None)
        return check_registration_permission(registration_id, request.user)


class IsSubRegistrationResponsiblePerson(permissions.BasePermission):
    message = 'Du darfst diese Registrierung nicht bearbeiten'

    def has_permission(self, request: Request, view) -> bool:
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        registration_id: str = view.kwargs.get('registration_pk', None)
        return check_registration_permission(registration_id, request.user)
