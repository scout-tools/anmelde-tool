from datetime import datetime

import pytz
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from event import models as event_models
from event import permissions as event_permissions
from event.summary import serializers as summary_serializers


class WorkshopEventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.WorkshopEventSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Workshop.objects.filter(registration__event__id=event_id)


class EventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.RegistrationEventSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        registrations = event_models.Registration.objects.filter(event=event_id)

        confirmed: bool = self.request.query_params.get('confirmed', 'true') == 'true'

        if confirmed:
            registrations = registrations.filter(is_confirmed=confirmed)

        return registrations


class RegistrationLocationViewSet(EventSummaryViewSet):
    serializer_class = summary_serializers.RegistrationLocationSerializer


class EventLocationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.EventLocationSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Event.objects.filter(id=event_id)


class EventDetailedSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventSuperResponsiblePerson]
    serializer_class = summary_serializers.RegistrationParticipantEventDetailedSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)

        booking_option_list: list = self.request.query_params.getlist('booking-option')
        confirmed: bool = self.request.query_params.get('confirmed', 'true') == 'true'

        registrations: QuerySet = event_models.Registration.objects.filter(event=event_id)

        if confirmed:
            registrations.filter(is_confirmed=True)

        reg_ids = registrations.values('id')
        participants = event_models.RegistrationParticipant.objects.filter(registration__in=reg_ids)

        if booking_option_list:
            participants = participants.filter(booking_option__in=booking_option_list)

        return participants


class EventAttributeSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.EventAttributeSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        mapper_ids = event_models.EventModuleMapper.objects.filter(event=event_id).values_list('attributes', flat=True)
        return event_models.AttributeEventModuleMapper.objects.filter(id__in=mapper_ids)


class EventFoodSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]

    def list(self, request, *args, **kwargs) -> Response:
        participants: QuerySet[event_models.RegistrationParticipant] = self.get_queryset()

        eat_habits_sum = {}
        eat_habits = {}
        for participant in participants.all():
            key = tuple(participant.eat_habit.values_list('id', flat=True))
            if key in eat_habits_sum:
                eat_habits_sum[key] += 1
            else:
                eat_habits_sum[key] = 1
                eat_habits[key] = participant.eat_habit.all()

        formatted_eat_habits = []
        for key in eat_habits:
            food = ', '.join(eat_habits[key].values_list('name', flat=True))
            if food is None or food == '':
                food = 'Normal'
            result = {
                'sum': eat_habits_sum[key],
                'food': food,
            }
            formatted_eat_habits.append(result)

        return Response(formatted_eat_habits, status=status.HTTP_200_OK)

    def get_queryset(self) -> QuerySet[event_models.RegistrationParticipant]:
        event_id = self.kwargs.get("event_pk", None)

        booking_option_list = self.request.query_params.getlist('booking-option')
        confirmed: bool = self.request.query_params.get('confirmed', 'true') == 'true'

        registrations = event_models.Registration.objects.filter(event=event_id)

        if confirmed:
            registrations = registrations.filter(is_confirmed=confirmed)

        registration_ids = registrations.values_list('id', flat=True)
        queryset = event_models.RegistrationParticipant.objects.filter(registration__id__in=registration_ids)

        if booking_option_list:
            queryset = queryset.filter(booking_option__in=booking_option_list)

        return queryset


class EventAgeGroupsSummaryViewSet(EventFoodSummaryViewSet):

    def list(self, request, *args, **kwargs) -> Response:
        """
        0-10 Wölfling
        11-16 Pfadfinder
        17-23 Rover
        23+ Altrover
        """
        event_id = self.kwargs.get("event_pk", None)
        event = get_object_or_404(event_models.Event, pk=event_id)
        all_participants: QuerySet[event_models.RegistrationParticipant] = self.get_queryset()

        woelfling = self.age_range(0, 12, all_participants, event)
        pfadfinder = self.age_range(12, 17, all_participants, event)
        rover = self.age_range(17, 24, all_participants, event)
        alt_rover = self.age_range(24, 999, all_participants, event)

        result = {
            'woelfling': woelfling,
            'pfadfinder': pfadfinder,
            'rover': rover,
            'alt_rover': alt_rover
        }

        return Response(result, status=status.HTTP_200_OK)

    def age_range(self, min_age, max_age, participants: QuerySet[event_models.RegistrationParticipant],
                  event: event_models.Event) -> int:
        min_date = datetime(event.start_date.year - min_age, event.start_date.month, event.start_date.day,
                            tzinfo=pytz.timezone('Europe/Berlin'))
        max_date = datetime(event.start_date.year - max_age, event.start_date.month, event.start_date.day,
                            tzinfo=pytz.timezone('Europe/Berlin'))

        return participants.filter(birthday__gte=max_date, birthday__lte=min_date).count()


class CashSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.CashSummarySerializer

    def get_queryset(self) -> QuerySet[event_models.Event]:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Event.objects.filter(id=event_id)


class EmailResponsiblePersonsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.UserEmailSerializer

    def get_queryset(self) -> QuerySet[User]:
        event_id = self.kwargs.get("event_pk", None)
        only_admin = self.request.query_params.get('only-admins', False)
        event: event_models.Event = event_models.Event.objects.filter(id=event_id).first()

        admin_groups: QuerySet[User] = event.keycloak_admin_path.user_set.exclude(email__exact='')
        internal: QuerySet[User] = event.responsible_persons.exclude(email__exact='')

        all_users = admin_groups | internal

        if not only_admin:
            normal_groups: QuerySet[User] = event.keycloak_path.user_set.exclude(email__exact='')
            all_users = all_users | normal_groups

        return all_users.distinct()


class EmailRegistrationResponsiblePersonsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]
    serializer_class = summary_serializers.UserEmailSerializer

    def get_queryset(self) -> QuerySet[User]:
        event_id = self.kwargs.get("event_pk", None)

        confirmed: bool = self.request.query_params.get('confirmed', 'true') == 'true'
        unconfirmed: bool = self.request.query_params.get('unconfirmed', 'true') == 'true'
        # all_participants: bool = self.request.query_params.get('all-participants', False)

        all_registrations: QuerySet[event_models.Registration] = event_models.Registration.objects. \
            filter(event=event_id)
        registrations: QuerySet[event_models.Registration] = event_models.Registration.objects.none()

        if confirmed:
            confirmed_registrations = all_registrations.filter(is_confirmed=True)
            registrations = registrations | confirmed_registrations

        if unconfirmed:
            unconfirmed_registrations = all_registrations.filter(is_confirmed=False)
            registrations = registrations | unconfirmed_registrations

        registrations_ids: QuerySet[int] = registrations.all().distinct() \
            .values_list('responsible_persons__id', flat=True)
        all_users = User.objects.filter(id__in=registrations_ids).distinct().exclude(email__exact='')

        return all_users
