from __future__ import annotations # we use a python 3.10 Feature in line 14

from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q

from basic import models as basic_models
from event import api_exceptions as event_exceptions
from event import models as event_models
from event import permissions as event_permissions

User = get_user_model()


def get_bund(obj: basic_models.ScoutHierarchy) -> [basic_models.ScoutHierarchy | None]:
    iterator: basic_models.ScoutHierarchy = obj
    while iterator is not None:
        if iterator.level.id == 3:
            return iterator
        iterator = iterator.parent

    return None


def filter_registration_by_leadership(user: User, event_id: str, registrations: QuerySet[event_models.Registration]) \
        -> QuerySet[event_models.Registration]:
    event: event_models.Event = get_event(event_id)
    if not event_permissions.check_event_permission(event, user) \
            and event_permissions.check_leader_permission(event, user):
        bund = get_bund(user.userextended.scout_organisation)

        registrations = registrations.filter(
            Q(scout_organisation=bund)
            | Q(scout_organisation__parent=bund)
            | Q(scout_organisation__parent__parent=bund)
            | Q(scout_organisation__parent__parent__parent=bund))
    return registrations


def get_event(event_id: [str, event_models.Event], ex=event_exceptions.EventNotFound) -> event_models.Event:
    if isinstance(event_id, str):
        return custom_get_or_404(ex, event_models.Event, id=event_id)
    else:
        return event_id


def custom_get_or_404(ex, model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        raise ex
