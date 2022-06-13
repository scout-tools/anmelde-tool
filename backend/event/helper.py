from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from basic import models as basic_models
from event import models as event_models
from event import permissions as event_permissions

User = get_user_model()


def get_bund(obj: basic_models.ScoutHierarchy) -> basic_models.ScoutHierarchy | None:
    iterator: basic_models.ScoutHierarchy = obj
    while iterator is not None:
        if iterator.level.id == 3:
            return iterator
        iterator = iterator.parent

    return None


def filter_registration_by_leadership(user: User, event_id: str, registrations: QuerySet[event_models.Registration]) \
        -> QuerySet[event_models.Registration]:
    event: event_models.Event = get_object_or_404(event_models.Event, id=event_id)
    if not event_permissions.check_event_permission(event, user) \
            and event_permissions.check_leader_permission(event, user):
        bund = get_bund(user.userextended.scout_organisation)
        sub_hierachies = get_object_or_404(basic_models.ScoutHierarchyChildModel, head=bund)
        registrations = registrations.filter(scout_organisation__in=sub_hierachies.childs.all())
    return registrations
