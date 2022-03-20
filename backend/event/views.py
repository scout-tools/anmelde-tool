from copy import deepcopy

from django.db.models import Q, QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basic.models import ScoutHierarchy, AbstractAttribute
from basic.serializers import AbstractAttributeGetPolymorphicSerializer, AbstractAttributePutPolymorphicSerializer, \
    AbstractAttributePostPolymorphicSerializer
from event.api_exceptions import GroupAlreadyRegistered, NotResponsible, SingleAlreadyRegistered, \
    SingleGroupNotAllowed, WrongRegistrationFormat, RegistrationNotSupported, WrongEventCode, TooEarly, TooLate, \
    TooManyParticipants
from event.models import Event, EventLocation, BookingOption, RegistrationTypeGroup, RegistrationTypeSingle, \
    StandardEventTemplate, Registration, RegistrationParticipant, Gender, ParticipantActionConfirmation
from event.serializers import EventPlanerSerializer, EventLocationGetSerializer, EventLocationPostSerializer, \
    EventCompleteSerializer, BookingOptionSerializer, EventModuleMapper, EventModule, EventModuleMapperSerializer, \
    EventModuleSerializer, AttributeEventModuleMapperSerializer, EventOverviewSerializer, \
    EventModuleMapperPostSerializer, EventModuleMapperGetSerializer, RegistrationPostSerializer, \
    RegistrationGetSerializer, RegistrationPutSerializer, RegistrationParticipantSerializer, \
    RegistrationParticipantShortSerializer, RegistrationParticipantPutSerializer, \
    RegistrationParticipantGroupSerializer, EventRegistrationSerializer, EventModuleMapperPutSerializer


def add_event_module(module: EventModuleMapper, event: Event) -> EventModuleMapper:
    new_module: EventModuleMapper = deepcopy(module)
    new_module.pk = None
    new_module.standard = False
    new_module.event = event
    new_module.save()
    new_module.attributes.add(*module.attributes.all())
    return new_module


def add_event_attribute(attribute: AbstractAttribute) -> AbstractAttribute:
    new_attribute: AbstractAttribute = deepcopy(attribute)
    new_attribute.pk = None
    new_attribute.id = None
    new_attribute.template = False
    new_attribute.template_id = attribute.id
    new_attribute.save()
    return new_attribute


class EventLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationGetSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventLocationPostSerializer
        return EventLocationGetSerializer


class EventRegistrationViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventRegistrationSerializer


class EventViewSet(viewsets.ModelViewSet):
    # TODO: Limit complete event to creators
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventCompleteSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = 'Dummy'
        if request.data.get('responsible_persons', None) is None:
            request.data['responsible_persons'] = [request.user.id, ]
        serializer: EventCompleteSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event = serializer.save()
        event.responsible_persons.add(request.user)
        standard_event = get_object_or_404(StandardEventTemplate, pk=1)

        add_event_module(standard_event.introduction, event)

        if event.personal_data_required:
            add_event_module(standard_event.personal_registration, event)
        else:
            add_event_module(standard_event.registration, event)

        add_event_module(standard_event.summary, event)

        for mapper in standard_event.other_required_modules.all():
            add_event_module(mapper, event)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = self.get_object().name
        return super().update(request, *args, **kwargs)


class BookingOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingOptionSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        return BookingOption.objects.filter(event=event_id)

    def create(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = 'Standard'
        event_id = self.kwargs.get("event_pk", None)

        if event_id is None:
            raise NotFound()

        event = get_object_or_404(Event.objects, pk=event_id)

        request.data['event'] = event_id

        if request.data.get('bookable_till', None) is None:
            request.data['bookable_till'] = event.start_date

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = self.get_object().name
        request.data['event'] = self.get_object().event.id
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if self.get_queryset().count() > 1:
            return super().destroy(request, *args, **kwargs)
        else:
            raise MethodNotAllowed(method='delete',
                                   detail=f'delete not allowed, because there must be at least one booking option')


class EventPlanerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventPlanerSerializer

    def get_queryset(self):
        return Event.objects.filter(
            Q(keycloak_path__in=self.request.user.groups.all()) | Q(responsible_persons=self.request.user))


class RegistrationTypeGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, pk=None):
        return Response(RegistrationTypeGroup.choices, status=status.HTTP_200_OK)


class RegistrationTypeSingleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, pk=None):
        return Response(RegistrationTypeSingle.choices, status=status.HTTP_200_OK)


class EventModulesMapperViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = EventModuleMapper.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventModuleMapperPostSerializer
        elif self.request.method == 'PUT':
            return EventModuleMapperPutSerializer
        else:
            return EventModuleMapperSerializer

    def create(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        module_id = request.data.get("module")

        event = get_object_or_404(Event, pk=event_id)
        standard_event = get_object_or_404(StandardEventTemplate, pk=1)

        module_template = standard_event.other_optional_modules.filter(module__id=module_id).first()
        if module_template is None:
            return super().create(request, *args, **kwargs)

        new_module = add_event_module(module_template, event)
        json = EventModuleMapperSerializer(new_module)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        json = EventModuleMapperSerializer(self.get_object())
        return Response(json.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs) -> Response:
        mapper: EventModuleMapper = self.get_object()
        if mapper.required:
            raise MethodNotAllowed('module is required')
        return super().destroy(request, *args, **kwargs)


class EventModulesViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = EventModuleSerializer
    queryset = EventModule.objects.all()


class AvailableEventModulesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventModuleSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        mapper = EventModuleMapper.objects.filter(event=event_id).values_list('module_id', flat=True)
        return EventModule.objects.exclude(id__in=mapper).exclude(type__in=[7, 4]).exclude(custom=True)


class EventModuleAttributeMapperViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = AttributeEventModuleMapperSerializer

    def get_queryset(self):
        mapper_id = self.kwargs.get("eventmodulemapper_pk", None)
        mapper = get_object_or_404(EventModuleMapper, id=mapper_id)
        return mapper.attributes.all()


class AssignedEventModulesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventModuleMapperGetSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        return EventModuleMapper.objects.filter(event=event_id).order_by('ordering')


class EventOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventOverviewSerializer

    def get_queryset(self):
        list_parent_organistations = []
        iterator: ScoutHierarchy = self.request.user.userextended.scout_organisation
        while iterator is not None:
            list_parent_organistations.append(iterator)
            iterator = iterator.parent
        return Event.objects.filter(is_public=True, end_date__gte=timezone.now(),
                                    limited_registration_hierarchy__in=list_parent_organistations)


class RegistrationViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Registration.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event: Event = get_object_or_404(Event, pk=serializer.data['event'])
        if serializer.data['event_code'] != event.invitation_code:
            raise WrongEventCode()

        #  Check registration type permissions
        # if event.group_registration == RegistrationTypeSingle.External and not serializer.data['single']:
        #      raise WrongRegistrationFormat
        if event.single_registration == RegistrationTypeSingle.Attached:
            raise RegistrationNotSupported

        # Check registration type permissions based on existing registrations
        existing_registration = Registration.objects.filter(event=event.id)

        if existing_registration.exists():
            single_registration = existing_registration.filter(responsible_persons__in=[request.user.id], single=True)
            existing_group_registration = existing_registration. \
                filter(scout_organisation=request.user.userextended.scout_organisation, single=False)
            group_registration = existing_group_registration.filter(responsible_persons__in=[request.user.id])

            if single_registration.exists() and serializer.data['single']:
                raise SingleAlreadyRegistered()
            elif existing_group_registration.exists() and not group_registration.exists():
                raise NotResponsible()
            elif existing_group_registration.exists() and not serializer.data['single']:
                raise GroupAlreadyRegistered
            elif group_registration.exists() and serializer.data['single']:
                raise SingleGroupNotAllowed
            elif event.group_registration == RegistrationTypeGroup.Required and \
                    not group_registration.exists() and serializer.data['single']:
                raise WrongRegistrationFormat

        registration: Registration = Registration(
            scout_organisation=request.user.userextended.scout_organisation,
            event=event,
            single=serializer.data['single']
        )

        registration.save()
        registration.responsible_persons.add(request.user)

        event_module: QuerySet[EventModuleMapper] = EventModuleMapper.objects.filter(event=event.id, required=True)
        for mapper in event_module:
            for attribute_mapper in mapper.attributes.all():
                attribute = attribute_mapper.attribute
                new_attribute = add_event_attribute(attribute)
                registration.tags.add(new_attribute.id)

        json = RegistrationGetSerializer(registration)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tmp: Registration = serializer.save()

        tmp.responsible_persons.add(request.user)

        serializer = RegistrationGetSerializer(tmp)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        registration: Registration = self.get_object()
        participants_count = RegistrationParticipant.objects.filter(registration=registration.id).count()
        if participants_count == 0:
            return super().destroy(request, *args, **kwargs)

        if registration.event.last_possible_update < timezone.now():
            raise TooLate
        elif registration.event.registration_deadline < timezone.now():
            raise TooManyParticipants

        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegistrationPostSerializer
        elif self.request.method == 'GET':
            return RegistrationGetSerializer
        elif self.request.method == 'PUT':
            return RegistrationPutSerializer
        elif self.request.method == 'DESTROY':
            return RegistrationPutSerializer


class GenderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, pk=None):
        return Response(Gender.choices, status=status.HTTP_200_OK)


class RegistrationSingleParticipantViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        registration_id = self.kwargs.get("registration_pk", None)
        return RegistrationParticipant.objects.filter(registration=registration_id)

    def create(self, request, *args, **kwargs):

        registration: Registration = self.participant_initialization(request)

        request.data['registration'] = registration.id
        if request.data.get('first_name') or request.data.get('last_name') is None:
            max_num = self.get_queryset().count()
            request.data['first_name'] = 'Teilnehmer'
            request.data['last_name'] = max_num + 1
        if request.data.get('booking_option') is None:
            request.data['booking_option'] = registration.event.bookingoption_set.first().id

        if registration.event.registration_deadline < timezone.now():
            request.data['needs_confirmation'] = ParticipantActionConfirmation.AddCompletyNew

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        registration: Registration = self.participant_initialization(request)
        participant: RegistrationParticipant = self.get_object()
        if participant.deactivated:
            if request.data.get('activate') and registration.event.registration_deadline >= timezone.now():
                request.data['deactivated'] = False
                request.data['needs_confirmation'] = ParticipantActionConfirmation.Nothing
            elif registration.event.last_possible_update >= timezone.now():
                request.data['deactivated'] = False
                request.data['needs_confirmation'] = ParticipantActionConfirmation.AddFromExisting

        request.data['generated'] = False

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        registration: Registration = self.participant_initialization(request)

        if registration.event.last_possible_update < timezone.now():
            request.data['deactivated'] = True
            request.data['needs_confirmation'] = ParticipantActionConfirmation.Nothing
            return super().update(request, *args, **kwargs)
        elif registration.event.registration_deadline < timezone.now():
            request.data['deactivated'] = True
            if not request.data.get('avoid_manual_check'):
                request.data['needs_confirmation'] = ParticipantActionConfirmation.Delete
            return super().update(request, *args, **kwargs)

        return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        serializer = {
            'create': RegistrationParticipantSerializer,
            'retrieve': RegistrationParticipantSerializer,
            'list': RegistrationParticipantShortSerializer,
            'update': RegistrationParticipantSerializer,
            'destroy': RegistrationParticipantSerializer
        }
        return serializer.get(self.action, RegistrationParticipantPutSerializer)

    def participant_initialization(self, request):
        input_serializer = RegistrationParticipantPutSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: Registration = get_object_or_404(Registration, id=registration_id)

        if registration.event.registration_start > timezone.now():
            raise TooEarly
        elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
            raise TooLate

        return registration


class RegistrationGroupParticipantViewSet(viewsets.ViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = RegistrationParticipantShortSerializer

    def create(self, request, *args, **kwargs) -> Response:
        registration: Registration = self.participant_group_initialization(request)
        number: int = request.data.get('number', 0)
        existing_participants: QuerySet = RegistrationParticipant.objects.filter(registration=registration.id)
        active_participants: QuerySet = existing_participants.filter(deactivated=False)
        inactive_participants: QuerySet = existing_participants.filter(deactivated=True)
        active_participant_count: int = active_participants.count()
        inactive_participant_count: int = inactive_participants.count()
        total_participant_count: int = active_participant_count + inactive_participant_count
        activate = min(inactive_participant_count, number)
        create: int = max(number - total_participant_count, 0)
        confirm_needed: bool = registration.event.registration_deadline < timezone.now()

        if activate > 0:
            confirm = ParticipantActionConfirmation.AddFromExisting if confirm_needed else ParticipantActionConfirmation.Nothing
            RegistrationParticipant.objects \
                .filter(pk__in=inactive_participants.order_by('created_at').values_list('pk', flat=True)[:activate]) \
                .update(deactivated=False, needs_confirmation=confirm)

        if create > 0:
            new_participants = []
            confirm = ParticipantActionConfirmation.AddCompletyNew if confirm_needed else ParticipantActionConfirmation.Nothing
            for i in range(total_participant_count + 1, number + 1):
                participant = RegistrationParticipant(first_name='Teilnehmer',
                                                      last_name=i,
                                                      registration=registration,
                                                      generated=True,
                                                      needs_confirmation=confirm)
                new_participants.append(participant)
            RegistrationParticipant.objects.bulk_create(new_participants)

        return Response({'activated': activate, 'created': create}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs) -> Response:
        registration: Registration = self.participant_group_initialization(request)
        number: int = request.data.get('number', 9999)
        all_participants: QuerySet = RegistrationParticipant.objects.filter(registration=registration.id)
        participant_count = all_participants.count()

        if number <= participant_count:
            num_delete: int = max(participant_count - number, 0)
            deletable_participants: QuerySet[RegistrationParticipant] = all_participants.filter(generated=True)
            deletable_participants_count: int = deletable_participants.count()

            if num_delete < deletable_participants_count:
                selected_deletable_participants = RegistrationParticipant.objects.filter(
                    pk__in=deletable_participants.order_by('-created_at').values_list('pk', flat=True)[:num_delete])
            else:
                selected_deletable_participants = deletable_participants

            if registration.event.registration_deadline >= timezone.now():
                selected_deletable_participants.delete()
                return Response({'deleted': num_delete}, status=status.HTTP_204_NO_CONTENT)
            else:
                if registration.event.last_possible_update >= timezone.now() \
                        and not request.data.get('avoid_manual_check'):
                    confirm = ParticipantActionConfirmation.Delete
                else:
                    confirm = ParticipantActionConfirmation.Nothing

                selected_deletable_participants.update(deactivated=True, needs_confirmation=confirm)
                return Response({'deactivated': num_delete}, status=status.HTTP_200_OK)

        else:
            return Response(f'number: {number} is higher or equal than current participantc count {participant_count}',
                            status=status.HTTP_400_BAD_REQUEST)

    def participant_group_initialization(self, request) -> Registration:
        input_serializer = RegistrationParticipantGroupSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: Registration = get_object_or_404(Registration, id=registration_id)

        if registration.event.registration_start > timezone.now():
            raise TooEarly
        elif self.action != 'destroy' and registration.event.last_possible_update < timezone.now():
            raise TooLate

        return registration


class RegistrationAttributeViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs) -> Response:
        serializer: AbstractAttributePutPolymorphicSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        registration_id = self.kwargs.get("registration_pk", None)
        registration: Registration = get_object_or_404(Registration, id=registration_id)

        template_attribute: AbstractAttribute = get_object_or_404(AbstractAttribute,
                                                                  pk=serializer.data.get('template_id', -1))

        new_attribute = add_event_attribute(template_attribute)

        serializer.update(new_attribute, serializer.validated_data)

        registration.tags.add(new_attribute.id)

        json = AbstractAttributeGetPolymorphicSerializer(new_attribute)
        return Response(json.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        json = AbstractAttributeGetPolymorphicSerializer(self.get_object())
        return Response(json.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AbstractAttributePostPolymorphicSerializer
        elif self.request.method == 'GET':
            return AbstractAttributeGetPolymorphicSerializer
        elif self.request.method == 'PUT':
            return AbstractAttributePutPolymorphicSerializer
        else:
            return AbstractAttributePutPolymorphicSerializer

    def get_queryset(self) -> QuerySet:
        registration_id = self.kwargs.get("registration_pk", None)
        registration: Registration = get_object_or_404(Registration, id=registration_id)
        return registration.tags
