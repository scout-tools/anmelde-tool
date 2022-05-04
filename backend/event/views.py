from copy import deepcopy
from datetime import datetime

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basic import models as basic_models
from basic import serializers as basic_serializers
from event import serializers as event_serializers
from event import api_exceptions as event_api_exceptions
from event import models as event_models
from event import choices as event_choices
from event.permissions import IsEventResponsiblePersonOrReadOnly, IsSubEventResponsiblePersonOrReadOnly, \
    IsRegistrationResponsiblePerson, \
    IsSubRegistrationResponsiblePerson, IsEventSuperResponsiblePerson, IsSubEventSuperResponsiblePerson, \
    IsSubEventResponsiblePerson


def add_event_module(module: event_models.EventModuleMapper,
                     event: event_models.Event) -> event_models.EventModuleMapper:
    new_module: event_models.EventModuleMapper = deepcopy(module)
    new_module.pk = None
    new_module.standard = False
    new_module.event = event
    new_module.save()
    new_module.attributes.add(*module.attributes.all())
    return new_module


def add_event_attribute(attribute: basic_models.AbstractAttribute) -> basic_models.AbstractAttribute:
    new_attribute: basic_models.AbstractAttribute = deepcopy(attribute)
    new_attribute.pk = None
    new_attribute.id = None
    new_attribute.template = False
    new_attribute.template_id = attribute.id
    new_attribute.save()
    return new_attribute


def create_missing_eat_habits(request) -> None:
    eat_habits = request.data.get('eat_habit', [])
    for habit in eat_habits:
        if len(habit) > 100:
            raise event_api_exceptions.EatHabitTooLong
        if not basic_models.EatHabit.objects.filter(name__exact=habit).exists():
            basic_models.EatHabit.objects.create(name=habit)


class EventLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    queryset = event_models.EventLocation.objects.all()
    serializer_class = event_serializers.EventLocationSerializer


class EventRegistrationViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = event_models.Event.objects.all()
    serializer_class = event_serializers.EventRegistrationSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEventSuperResponsiblePerson]
    queryset = event_models.Event.objects.all()
    serializer_class = event_serializers.EventCompleteSerializer

    def get_formatted_date(self, date: str, request) -> datetime | None:
        if request.data.get(date):
            for fmt in ('%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S%Z'):
                try:
                    return datetime.strptime(request.data.get(date), fmt)
                except ValueError:
                    pass

        return None

    def check_event_dates(self, request, event: event_models.Event) -> bool:
        edited = False
        start_date = self.get_formatted_date('start_date', request)
        if start_date is None:
            start_date = event.start_date
        else:
            edited = True


        end_date = self.get_formatted_date('end_date', request)
        if end_date is None:
            end_date = event.end_date
        else:
            edited = True

        registration_deadline = self.get_formatted_date('registration_deadline', request)
        if registration_deadline is None:
            registration_deadline = event.registration_deadline
        else:
            edited = True

        registration_start = self.get_formatted_date('registration_start', request)
        if registration_start is None:
            registration_start = event.registration_start
        else:
            edited = True

        last_possible_update = self.get_formatted_date('last_possible_update', request)
        if last_possible_update is None:
            last_possible_update = event.last_possible_update
        else:
            edited = True

        if not edited:
            return True

        if end_date < start_date:
            raise event_api_exceptions.EndBeforeStart
        if start_date <= last_possible_update:
            raise event_api_exceptions.StartBeforeLastChange
        if last_possible_update <= registration_deadline:
            raise event_api_exceptions.LastChangeBeforeRegistrationDeadline
        if registration_deadline < registration_start:
            raise event_api_exceptions.RegistrationDeadlineBeforeRegistrationStart
        return True

    def create(self, request, *args, **kwargs) -> Response:
        if request.data.get('name', None) is None:
            request.data['name'] = 'Dummy'
        if request.data.get('responsible_persons', None) is None:
            request.data['responsible_persons'] = [request.user.email, ]
        serializer: event_serializers.EventCompleteSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event: event_models.Event = serializer.save()
        event.responsible_persons.add(request.user)
        standard_event = get_object_or_404(event_models.StandardEventTemplate, pk=1)

        add_event_module(standard_event.introduction, event)

        if event.personal_data_required:
            add_event_module(standard_event.personal_registration, event)
        else:
            add_event_module(standard_event.registration, event)

        add_event_module(standard_event.summary, event)

        for mapper in standard_event.other_required_modules.all():
            add_event_module(mapper, event)

        # TODO: When event_planer_modules does not contain all necessary modules, they wont be added
        if request.data.get('event_planer_modules', None) is None:
            for planer_module in standard_event.planer_modules.all():
                event.event_planer_modules.add(planer_module)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        event: event_models.Event = self.get_object()
        # standard_event = get_object_or_404(event_models.StandardEventTemplate, pk=1)

        self.check_event_dates(request, event)

        # TODO: Check personal data required changed and if so exchange data

        return super().update(request, *args, **kwargs)


class BookingOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSubEventResponsiblePersonOrReadOnly]
    serializer_class = event_serializers.BookingOptionSerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.BookingOption.objects.filter(event=event_id)

    def create(self, request, *args, **kwargs) -> Response:
        if request.data.get('name', None) is None:
            request.data['name'] = 'Standard'
        event_id = self.kwargs.get("event_pk", None)

        if event_id is None:
            raise NotFound()

        event = get_object_or_404(event_models.Event.objects, pk=event_id)

        request.data['event'] = event_id

        if request.data.get('bookable_till', None) is None:
            request.data['bookable_till'] = event.start_date

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        if request.data.get('name', None) is None:
            request.data['name'] = self.get_object().name
        request.data['event'] = self.get_object().event.id
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs) -> Response:
        if self.get_queryset().count() > 1:
            return super().destroy(request, *args, **kwargs)
        else:
            raise MethodNotAllowed(method='delete',
                                   detail=f'delete not allowed, because there must be at least one booking option')


class EventPlanerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = event_serializers.EventPlanerSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_superuser:
            return event_models.Event.objects.all()
        else:
            return event_models.Event.objects.filter(Q(keycloak_admin_path__in=self.request.user.groups.all())
                                                     | Q(responsible_persons=self.request.user)).distinct()


class EventStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = event_serializers.EventPlanerSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_superuser:
            return event_models.Event.objects.filter(is_public=True)
        else:
            return event_models.Event.objects.filter(Q(keycloak_path__in=self.request.user.groups.all())
                                                     | Q(responsible_persons=self.request.user)).distinct()


class RegistrationTypeGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.RegistrationTypeGroup.choices, status=status.HTTP_200_OK)


class RegistrationTypeSingleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.RegistrationTypeSingle.choices, status=status.HTTP_200_OK)


class EventModulesMapperViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [IsSubEventResponsiblePersonOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return event_serializers.EventModuleMapperPostSerializer
        elif self.request.method == 'PUT':
            return event_serializers.EventModuleMapperPutSerializer
        else:
            return event_serializers.EventModuleMapperSerializer

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_id = kwargs.get("event_pk", None)
        module_id = request.data.get("module")

        event = get_object_or_404(event_models.Event, pk=event_id)
        standard_event = get_object_or_404(event_models.StandardEventTemplate, pk=1)

        module_mapper_template = standard_event.other_optional_modules.filter(module__id=module_id).first()
        if module_mapper_template is None:
            module_type = basic_models.TagType.objects.get(id=10)
            module_template = event_models.EventModule.objects.create(name="Custom", custom=True, type=module_type,
                                                                      header="Custom")
            module_mapper_template = event_models.EventModuleMapper.objects.create(module=module_template, event=event)

        new_module = add_event_module(module_mapper_template, event)
        json = event_serializers.EventModuleMapperSerializer(new_module)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        super().update(request, *args, **kwargs)
        json = event_serializers.EventModuleMapperSerializer(self.get_object())
        return Response(json.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        mapper: event_models.EventModuleMapper = self.get_object()
        if mapper.required:
            raise event_api_exceptions.ModuleRequired
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        return event_models.EventModuleMapper.objects.filter(event=event_id)


class EventModulesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsEventResponsiblePersonOrReadOnly]
    serializer_class = event_serializers.EventModuleSerializer
    queryset = event_models.EventModule.objects.all()


class AvailableEventModulesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsSubEventSuperResponsiblePerson]
    serializer_class = event_serializers.EventModuleSerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        mapper = event_models.EventModuleMapper.objects.filter(event=event_id).values_list('module_id', flat=True)
        return event_models.EventModule.objects.exclude(id__in=mapper).exclude(type__in=[7, 4]).exclude(custom=True)


class EventModuleAttributeMapperViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsSubEventResponsiblePersonOrReadOnly]

    def create(self, request, *args, **kwargs) -> Response:
        serializer: event_serializers.AttributeEventModuleMapperSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mapper_id = self.kwargs.get("eventmodulemapper_pk", None)
        mapper = get_object_or_404(event_models.EventModuleMapper, id=mapper_id)

        attribute = serializer.data.get('attribute')
        attribute['type'] = basic_models.TagType.objects.get(name=attribute['type']['name'])
        test = basic_serializers.AbstractAttributePostPolymorphicSerializer().create(attribute)
        request.data['attribute'] = test

        attribute_mapper = serializer.create(request.data)

        mapper.attributes.add(attribute_mapper)

        json = self.get_serializer(attribute_mapper)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def get_queryset(self) -> QuerySet:
        mapper_id = self.kwargs.get("eventmodulemapper_pk", None)
        mapper = get_object_or_404(event_models.EventModuleMapper, id=mapper_id)
        return mapper.attributes.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return event_serializers.AttributeEventModuleMapperPostSerializer
        else:
            return event_serializers.AttributeEventModuleMapperSerializer


class AssignedEventModulesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSubEventResponsiblePersonOrReadOnly]
    serializer_class = event_serializers.EventModuleMapperGetSerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.EventModuleMapper.objects.filter(event=event_id).order_by('ordering')


class EventOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = event_serializers.EventOverviewSerializer

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_superuser:
            return event_models.Event.objects.filter(is_public=True)
        else:
            list_parent_organistations = []
            iterator: basic_models.ScoutHierarchy = self.request.user.userextended.scout_organisation
            while iterator is not None:
                list_parent_organistations.append(iterator)
                iterator = iterator.parent
            return event_models.Event.objects.filter(is_public=True, end_date__gte=timezone.now(),
                                                     limited_registration_hierarchy__in=list_parent_organistations)


class RegistrationViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [IsRegistrationResponsiblePerson]
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

        json = event_serializers.RegistrationGetSerializer(registration)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tmp: event_models.Registration = serializer.save()

        tmp.responsible_persons.add(request.user)

        serializer = event_serializers.RegistrationGetSerializer(tmp)
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
            return event_serializers.RegistrationPostSerializer
        elif self.request.method == 'GET':
            return event_serializers.RegistrationGetSerializer
        elif self.request.method == 'PUT':
            return event_serializers.RegistrationPutSerializer
        elif self.request.method == 'DESTROY':
            return event_serializers.RegistrationPutSerializer


class GenderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.Gender.choices, status=status.HTTP_200_OK)


class LeaderTypesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.LeaderTypes.choices, status=status.HTTP_200_OK)


class RegistrationSingleParticipantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSubRegistrationResponsiblePerson]

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        return event_models.RegistrationParticipant.objects.filter(registration=registration_id)

    def create(self, request, *args, **kwargs) -> Response:
        create_missing_eat_habits(request)
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
        create_missing_eat_habits(request)
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
            'create': event_serializers.RegistrationParticipantSerializer,
            'retrieve': event_serializers.RegistrationParticipantSerializer,
            'list': event_serializers.RegistrationParticipantShortSerializer,
            'update': event_serializers.RegistrationParticipantSerializer,
            'destroy': event_serializers.RegistrationParticipantSerializer
        }
        return serializer.get(self.action, event_serializers.RegistrationParticipantPutSerializer)

    def participant_initialization(self, request) -> event_models.Registration:
        input_serializer = event_serializers.RegistrationParticipantPutSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=registration_id)

        if registration.event.registration_start > timezone.now():
            raise event_api_exceptions.TooEarly
        elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
            raise event_api_exceptions.TooLate

        return registration


class RegistrationGroupParticipantViewSet(viewsets.ViewSet):
    permission_classes = [IsSubRegistrationResponsiblePerson]
    serializer_class = event_serializers.RegistrationParticipantShortSerializer

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
                participant = event_models.RegistrationParticipant(first_name='Teilnehmer',
                                                                   last_name=i,
                                                                   registration=registration,
                                                                   generated=True,
                                                                   needs_confirmation=confirm,
                                                                   booking_option=booking)
                new_participants.append(participant)
            event_models.RegistrationParticipant.objects.bulk_create(new_participants)

        return Response({'activated': activate, 'created': create}, status=status.HTTP_201_CREATED)

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
        input_serializer = event_serializers.RegistrationParticipantGroupSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: event_models.Registration = get_object_or_404(event_models.Registration, id=registration_id)

        if registration.event.registration_start > timezone.now():
            raise event_api_exceptions.TooEarly
        elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
            raise event_api_exceptions.TooLate

        return registration


class RegistrationAttributeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSubRegistrationResponsiblePerson]

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


class RegistrationSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsSubRegistrationResponsiblePerson]
    serializer_class = event_serializers.RegistrationSummarySerializer

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        return event_models.Registration.objects.filter(id=registration_id)


class EventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsSubEventResponsiblePerson]
    serializer_class = event_serializers.EventSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Event.objects.filter(id=event_id)


class EventDetailedSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsSubEventSuperResponsiblePerson]
    serializer_class = event_serializers.EventDetailedSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Event.objects.filter(id=event_id)


class EventAttributeSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsSubEventResponsiblePerson]
    serializer_class = event_serializers.EventAttributeSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        mapper_ids = event_models.EventModuleMapper.objects.filter(event=event_id).values_list('attributes', flat=True)
        return event_models.AttributeEventModuleMapper.objects.filter(id__in=mapper_ids)


class WorkshopEventSummaryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsSubEventResponsiblePerson]
    serializer_class = event_serializers.WorkshopEventSummarySerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.Workshop.objects.filter(registration__event__id=event_id)


class WorkshopViewSet(viewsets.ModelViewSet):
    serializer_class = event_serializers.WorkshopSerializer
    permission_classes = [IsSubRegistrationResponsiblePerson]

    def create(self, request, *args, **kwargs) -> Response:
        if not request.data.get('supervisor'):
            request.data['supervisor'] = request.user.id

        request.data['registration'] = self.kwargs.get("registration_pk", None)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs) -> Response:
        request.data['registration'] = self.kwargs.get("registration_pk", None)
        return super().update(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        return event_models.Workshop.objects.filter(registration__id=registration_id)
