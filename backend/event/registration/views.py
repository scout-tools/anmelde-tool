import re
from copy import deepcopy
from datetime import timezone

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from basic import models as basic_models
from basic import serializers as basic_serializers
from event import api_exceptions as event_api_exceptions
from event import models as event_models
from event import permissions as event_permissions
from event.choices import choices as event_choices
from event.helper import get_registration
from event.registration import serializers as registration_serializers


def create_missing_eat_habits(request) -> [str]:
    eat_habits = request.data.get('eat_habit', [])
    result = []
    for habit in eat_habits:
        if len(habit) > 100:
            raise event_api_exceptions.EatHabitTooLong
        splitted = re.split(',|;', habit)
        for split in splitted:
            split = split.strip().title()
            result.append(split)
            if not basic_models.EatHabit.objects.filter(name__exact=split).exists():
                basic_models.EatHabit.objects.create(name=split)
    return result


def add_event_attribute(attribute: basic_models.AbstractAttribute) -> basic_models.AbstractAttribute:
    new_attribute: basic_models.AbstractAttribute = deepcopy(attribute)
    new_attribute.pk = None
    new_attribute.id = None
    new_attribute.template = False
    new_attribute.template_id = attribute.id
    new_attribute.save()
    return new_attribute


class RegistrationSingleParticipantViewSet(viewsets.ModelViewSet):
    permission_classes = [event_permissions.IsSubRegistrationResponsiblePerson]

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        return event_models.RegistrationParticipant.objects.filter(registration=registration_id)

    def create(self, request, *args, **kwargs) -> Response:
        eat_habits_formatted = create_missing_eat_habits(request)

        if eat_habits_formatted and len(eat_habits_formatted) > 0:
            request.data['eat_habit'] = eat_habits_formatted

        registration: event_models.Registration = self.participant_initialization(request)

        if request.data.get('age'):
            request.data['birthday'] = timezone.now() - relativedelta(years=int(request.data.get('age')))

        request.data['registration'] = registration.id
        if request.data.get('first_name') is None and request.data.get('last_name') is None:
            max_num = self.get_queryset().count()
            request.data['first_name'] = 'Teilnehmer'
            request.data['last_name'] = max_num + 1
        if request.data.get('booking_option') is None:
            request.data['booking_option'] = registration.event.bookingoption_set.first().id
        if registration.event.registration_deadline < timezone.now():
            request.data['needs_confirmation'] = event_choices.ParticipantActionConfirmation.AddCompletyNew

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:

        eat_habits_formatted = create_missing_eat_habits(request)

        if eat_habits_formatted and len(eat_habits_formatted) > 0:
            request.data['eat_habit'] = eat_habits_formatted

        registration: event_models.Registration = self.participant_initialization(request)
        participant: event_models.RegistrationParticipant = self.get_object()

        if participant.deactivated:
            if request.data.get('activate') and registration.event.registration_deadline >= timezone.now():
                request.data['deactivated'] = False
                request.data['needs_confirmation'] = event_choices.ParticipantActionConfirmation.Nothing
            elif registration.event.last_possible_update >= timezone.now():
                request.data['deactivated'] = False
                request.data['needs_confirmation'] = event_choices.ParticipantActionConfirmation.AddFromExisting

        request.data['generated'] = False
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        registration: event_models.Registration = self.participant_initialization(request)

        if registration.event.last_possible_update < timezone.now():
            request.data['deactivated'] = True
            request.data['needs_confirmation'] = event_choices.ParticipantActionConfirmation.Nothing
            return super().update(request, *args, **kwargs)
        elif registration.event.registration_deadline < timezone.now():
            request.data['deactivated'] = True
            if not request.data.get('avoid_manual_check'):
                request.data['needs_confirmation'] = event_choices.ParticipantActionConfirmation.Delete
            return super().update(request, *args, **kwargs)

        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        serializer = {
            'create': registration_serializers.RegistrationParticipantSerializer,
            'retrieve': registration_serializers.RegistrationParticipantSerializer,
            'list': registration_serializers.RegistrationParticipantShortSerializer,
            'update': registration_serializers.RegistrationParticipantSerializer,
            'destroy': registration_serializers.RegistrationParticipantSerializer
        }
        return serializer.get(self.action, registration_serializers.RegistrationParticipantPutSerializer)

    def participant_initialization(self, request) -> event_models.Registration:
        input_serializer = registration_serializers.RegistrationParticipantPutSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_registration(registration_id)

        if not event_permissions.IsEventSuperResponsiblePerson:
            if registration.event.registration_start > timezone.now():
                raise event_api_exceptions.TooEarly
            elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
                raise event_api_exceptions.TooLate

        return registration

class RegistrationAddGroupParticipantViewSet(viewsets.ViewSet):
    permission_classes = [event_permissions.IsSubRegistrationResponsiblePerson]
    serializer_class = registration_serializers.RegistrationParticipantShortSerializer

    def create(self, request, *args, **kwargs) -> Response:
        registration: event_models.Registration = self.participant_group_initialization(request)
        number: int = request.data.get('number', 0)
        scout_level: int = request.data.get('scout_level', 'N')
        # eat_habit_id: int = request.data.get('eat_habit', None)

        new_participants = []

        confirm = event_choices.ParticipantActionConfirmation.Nothing

        booking: event_models.BookingOption = registration.event.bookingoption_set.first()
        # eat_habit: basic_models.EatHabit = get_object_or_404(basic_models.EatHabit, id=eat_habit_id)
        for i in range(1, int(number) + 1):
            participant = event_models.RegistrationParticipant(first_name='Pfadi',
                                                                scout_name='Namenlos',
                                                                last_name=i,
                                                                scout_level=scout_level,
                                                                # eat_habit=eat_habit,
                                                                registration=registration,
                                                                generated=True,
                                                                needs_confirmation=confirm,
                                                                booking_option=booking)
            new_participants.append(participant)
        event_models.RegistrationParticipant.objects.bulk_create(new_participants)

        return Response({ 'created  persons' }, status=status.HTTP_201_CREATED)

    def participant_group_initialization(self, request) -> event_models.Registration:
        input_serializer = registration_serializers.RegistrationParticipantGroupSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=registration_id)

        if registration.event.registration_start > timezone.now():
            raise event_api_exceptions.TooEarly
        elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
            raise event_api_exceptions.TooLate

        return registration

class RegistrationGroupParticipantViewSet(viewsets.ViewSet):
    permission_classes = [event_permissions.IsSubRegistrationResponsiblePerson]
    serializer_class = registration_serializers.RegistrationParticipantShortSerializer

    def create(self, request, *args, **kwargs) -> Response:
        registration: event_models.Registration = self.participant_group_initialization(request)
        number: int = request.data.get('number', 0)
        existing_participants: QuerySet = event_models.RegistrationParticipant.objects.filter(
            registration=registration.id)
        active_participants: QuerySet = existing_participants.filter(deactivated=False)
        inactive_participants: QuerySet = existing_participants.filter(deactivated=True)
        active_participant_count: int = active_participants.count()
        inactive_participant_count: int = inactive_participants.count()
        total_participant_count: int = active_participant_count + inactive_participant_count
        activate = min(inactive_participant_count, number)
        create: int = max(number - total_participant_count, 0)
        confirm_needed: bool = registration.event.registration_deadline < timezone.now()

        if activate > 0:

            if confirm_needed:
                confirm = event_choices.ParticipantActionConfirmation.AddFromExisting
            else:
                confirm = event_choices.ParticipantActionConfirmation.Nothing

            event_models.RegistrationParticipant.objects \
                .filter(pk__in=inactive_participants.order_by('created_at').values_list('pk', flat=True)[:activate]) \
                .update(deactivated=False, needs_confirmation=confirm)

        if create > 0:
            new_participants = []

            if confirm_needed:
                confirm = event_choices.ParticipantActionConfirmation.AddCompletyNew
            else:
                confirm = event_choices.ParticipantActionConfirmation.Nothing

            booking: event_models.BookingOption = registration.event.bookingoption_set.first().id

            for i in range(total_participant_count + 1, number + 1):
                participant = event_models.RegistrationParticipant(first_name='Pfadi',
                                                                   last_name=i,
                                                                   registration=registration,
                                                                   generated=True,
                                                                   needs_confirmation=confirm,
                                                                   booking_option=booking)
                new_participants.append(participant)
            event_models.RegistrationParticipant.objects.bulk_create(new_participants)

        return Response({'activated': activate, 'created': create}, status=status.HTTP_201_CREATED)

    def participant_group_initialization(self, request) -> event_models.Registration:
        input_serializer = registration_serializers.RegistrationParticipantGroupSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=registration_id)

        if registration.event.registration_start > timezone.now():
            raise event_api_exceptions.TooEarly
        elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
            raise event_api_exceptions.TooLate

        return registration

    def delete(self, request, *args, **kwargs) -> Response:
        registration: event_models.Registration = self.participant_group_initialization(request)
        number: int = request.data.get('number', 9999)
        all_participants: QuerySet = event_models.RegistrationParticipant.objects.filter(registration=registration.id)
        participant_count = all_participants.count()

        if number <= participant_count:
            num_delete: int = max(participant_count - number, 0)
            deletable_participants: QuerySet = all_participants.filter(generated=True)
            deletable_participants_count: int = deletable_participants.count()

            if num_delete < deletable_participants_count:
                selected_deletable_participants = event_models.RegistrationParticipant.objects.filter(
                    pk__in=deletable_participants.order_by('-created_at').values_list('pk', flat=True)[:num_delete])
            else:
                selected_deletable_participants = deletable_participants

            if registration.event.registration_deadline >= timezone.now():
                selected_deletable_participants.delete()
                return Response({'deleted': num_delete}, status=status.HTTP_204_NO_CONTENT)
            else:
                if registration.event.last_possible_update >= timezone.now() \
                        and not request.data.get('avoid_manual_check'):
                    confirm = event_choices.ParticipantActionConfirmation.Delete
                else:
                    confirm = event_choices.ParticipantActionConfirmation.Nothing

                selected_deletable_participants.update(deactivated=True, needs_confirmation=confirm)
                return Response({'deactivated': num_delete}, status=status.HTTP_200_OK)

        else:
            return Response(f'number: {number} is higher or equal than current participantc count {participant_count}',
                            status=status.HTTP_400_BAD_REQUEST)

    def participant_group_initialization(self, request) -> event_models.Registration:
        input_serializer = registration_serializers.RegistrationParticipantGroupSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=registration_id)

        if registration.event.registration_start > timezone.now():
            raise event_api_exceptions.TooEarly
        elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
            raise event_api_exceptions.TooLate

        return registration


class RegistrationAttributeViewSet(viewsets.ModelViewSet):
    permission_classes = [event_permissions.IsSubRegistrationResponsiblePerson]

    def create(self, request, *args, **kwargs) -> Response:
        serializer: basic_serializers.AbstractAttributePutPolymorphicSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=registration_id)

        template_attribute: basic_models.AbstractAttribute = \
            get_object_or_404(basic_models.AbstractAttribute, pk=serializer.data.get('template_id', -1))

        new_attribute = add_event_attribute(template_attribute)

        serializer.update(new_attribute, serializer.validated_data)

        registration.tags.add(new_attribute.id)

        json = basic_serializers.AbstractAttributeGetPolymorphicSerializer(new_attribute)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        super().update(request, *args, **kwargs)
        json = basic_serializers.AbstractAttributeGetPolymorphicSerializer(self.get_object())
        return Response(json.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return basic_serializers.AbstractAttributePostPolymorphicSerializer
        elif self.request.method == 'GET':
            return basic_serializers.AbstractAttributeGetPolymorphicSerializer
        elif self.request.method == 'PUT':
            return basic_serializers.AbstractAttributePutPolymorphicSerializer
        else:
            return basic_serializers.AbstractAttributePutPolymorphicSerializer

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=registration_id)
        return registration.tags


class AddResponsablePersonRegistrationViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsRegistrationResponsiblePerson]
    queryset = event_models.Registration.objects.all()
    serializer_class = registration_serializers.RegistrationPutSerializer

    def update(self, request, *args, **kwargs):
        new_responsable_person = request.data.get('responsable_person')

        # get user-id
        new_responsable_person_id = User.objects.filter(email=new_responsable_person).first().id

        instance = self.get_object()

        # prepair the return list with new user
        responseable_person_ids = [new_responsable_person_id]

        # add all exsisting users-id to list
        for x in instance.responsible_persons.all():
            responseable_person_ids.append(x.id)

        request.data['responsible_persons'] = responseable_person_ids

        return super().update(request, *args, **kwargs)


class RegistrationSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubRegistrationResponsiblePerson]
    serializer_class = registration_serializers.RegistrationSummarySerializer

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        return event_models.Registration.objects.filter(id=registration_id)


class WorkshopViewSet(viewsets.ModelViewSet):
    serializer_class = registration_serializers.WorkshopSerializer
    permission_classes = [event_permissions.IsSubRegistrationResponsiblePerson]

    def create(self, request, *args, **kwargs) -> Response:
        if not request.data.get('supervisor'):
            request.data['supervisor'] = request.user.id

        request.data['registration'] = self.kwargs.get("registration_pk", None)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        request.data['registration'] = self.get_object().registration.id
        return super().update(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        return event_models.Workshop.objects.filter(registration__id=registration_id)


class RegistrationViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsRegistrationResponsiblePerson]
    queryset = event_models.Registration.objects.all()

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event: event_models.Event = get_object_or_404(event_models.Event, pk=serializer.data['event'])

        general_code_check = False
        single_code_check = False
        group_code_check = False
        if serializer.data['event_code'] == event.invitation_code:
            general_code_check = True
        elif event.invitation_code_single and serializer.data['event_code'] == event.invitation_code_single:
            single_code_check = True
        elif event.invitation_code_group and serializer.data['event_code'] == event.invitation_code_group:
            group_code_check = True

        if not general_code_check and not single_code_check and not group_code_check:
            raise event_api_exceptions.WrongEventCode()

        if not general_code_check and single_code_check and not serializer.data['single']:
            raise event_api_exceptions.WrongEventCodeForGroup()

        if not general_code_check and group_code_check and serializer.data['single']:
            raise event_api_exceptions.WrongEventCodeForSingle()

        #  Check registration type permissions
        if event.group_registration == event_choices.RegistrationTypeGroup.No and not serializer.data['single']:
            raise event_api_exceptions.WrongRegistrationFormatGroup
        if event.single_registration == event_choices.RegistrationTypeSingle.No and serializer.data['single']:
            raise event_api_exceptions.WrongRegistrationFormatSingle
        if event.single_registration == event_choices.RegistrationTypeSingle.Attached:
            raise event_api_exceptions.RegistrationNotSupported

        # Check registration type permissions based on existing registrations
        existing_registration = event_models.Registration.objects.filter(event=event.id)

        if existing_registration.exists():
            single_registration = existing_registration.filter(responsible_persons__in=[request.user.id], single=True)
            existing_group_registration = existing_registration. \
                filter(scout_organisation=request.user.userextended.scout_organisation, single=False)
            group_registration = existing_group_registration.filter(responsible_persons__in=[request.user.id])

            if single_registration.exists() and serializer.data['single']:
                raise event_api_exceptions.SingleAlreadyRegistered()
            elif existing_group_registration.exists() and not group_registration.exists() \
                    and not serializer.data['single']:
                raise event_api_exceptions.NotResponsible()
            elif existing_group_registration.exists() and not serializer.data['single']:
                raise event_api_exceptions.GroupAlreadyRegistered
            elif group_registration.exists() and serializer.data['single']:
                raise event_api_exceptions.SingleGroupNotAllowed
            elif event.group_registration == event_choices.RegistrationTypeGroup.Required and \
                    not group_registration.exists() and serializer.data['single']:
                raise event_api_exceptions.WrongRegistrationFormat

        single = serializer.data['single'] if general_code_check else single_code_check
        registration: event_models.Registration = event_models.Registration(
            scout_organisation=request.user.userextended.scout_organisation,
            event=event,
            single=single
        )

        registration.save()
        registration.responsible_persons.add(request.user)

        event_module: QuerySet = event_models.EventModuleMapper.objects.filter(event=event.id, required=True)
        for mapper in event_module:
            for attribute_mapper in mapper.attributes.all():
                attribute = attribute_mapper.attribute
                new_attribute = add_event_attribute(attribute)
                registration.tags.add(new_attribute.id)

        json = registration_serializers.RegistrationGetSerializer(registration)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tmp: event_models.Registration = serializer.save()

        # tmp.responsible_persons.add(request.user)

        serializer = registration_serializers.RegistrationGetSerializer(tmp)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        registration: event_models.Registration = self.get_object()
        participants_count = event_models.RegistrationParticipant.objects.filter(registration=registration.id).count()
        if participants_count == 0:
            return super().destroy(request, *args, **kwargs)

        if registration.event.last_possible_update < timezone.now():
            raise event_api_exceptions.TooLate
        elif registration.event.registration_deadline < timezone.now():
            raise event_api_exceptions.TooManyParticipants

        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return registration_serializers.RegistrationPostSerializer
        elif self.request.method == 'GET':
            return registration_serializers.RegistrationGetSerializer
        elif self.request.method == 'PUT':
            return registration_serializers.RegistrationPutSerializer
        elif self.request.method == 'DESTROY':
            return registration_serializers.RegistrationPutSerializer
