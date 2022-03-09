from copy import deepcopy

from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.exceptions import NotFound, MethodNotAllowed, PermissionDenied, APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basic.models import ScoutHierarchy
from event.models import Event, EventLocation, SleepingLocation, RegistrationTypeGroup, RegistrationTypeSingle, \
    StandardEventTemplate, Registration
from event.serializers import EventPlanerSerializer, EventLocationGetSerializer, EventLocationPostSerializer, \
    EventCompleteSerializer, SleepingLocationSerializer, EventModuleMapper, EventModule, EventModuleMapperSerializer, \
    EventModuleSerializer, AttributeEventModuleMapperSerializer, EventOverviewSerializer, \
    EventModuleMapperPostSerializer, EventModuleMapperGetSerializer, RegistrationPostSerializer, \
    RegistrationGetSerializer, RegistrationPutSerializer


def add_event_module(module: EventModuleMapper, event: Event) -> EventModuleMapper:
    new_module: EventModuleMapper = deepcopy(module)
    new_module.pk = None
    new_module.standard = False
    new_module.event = event
    new_module.save()
    new_module.attributes.add(*module.attributes.all())
    return new_module


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


class EventViewSet(viewsets.ModelViewSet):
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


class SleepingLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SleepingLocationSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        return SleepingLocation.objects.filter(event=event_id)

    def create(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = 'Standard'
        event_id = self.kwargs.get("event_pk", None)

        if event_id is None:
            raise NotFound()

        event = get_object_or_404(Event.objects, pk=event_id)

        request.data['event'] = event_id

        if request.data.get('bookable_till', None) is None:
            request.data['bookable_till'] = event.start_time

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
                                   detail=f'delete not allowed, because there must be at least one sleeping location')


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
    permission_classes = [IsAuthenticated]
    queryset = EventModuleMapper.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventModuleMapperPostSerializer
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
        json = model_to_dict(new_module)
        return Response(json, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs) -> Response:
        mapper: EventModuleMapper = self.get_object()
        if mapper.required:
            raise MethodNotAllowed('module is required')
        return super().destroy(request, *args, **kwargs)


class EventModulesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    serializer_class = AttributeEventModuleMapperSerializer

    def get_queryset(self):
        mapper_id = self.kwargs.get("eventmodulemapper_pk", None)
        mapper = EventModuleMapper.objects.get(id=mapper_id)
        return mapper.attributes.all()


class AssignedEventModulesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventModuleMapperGetSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        return EventModuleMapper.objects.filter(event=event_id)


class EventOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventOverviewSerializer

    def get_queryset(self):
        list_parent_organistations = []
        iterator: ScoutHierarchy = self.request.user.userextended.scout_organisation
        while iterator is not None:
            list_parent_organistations.append(iterator)
            iterator = iterator.parent
        return Event.objects.filter(is_public=True, end_time__gte=timezone.now(),
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
            raise PermissionDenied()

        # Check registration type permissions
        if event.single_registration == RegistrationTypeSingle.External and \
                not serializer.data['single']:
            raise WrongRegistrationFormat
        elif event.single_registration == RegistrationTypeSingle.Attached:
            raise RegistrationNotSupported

        # Check registration type permissions based on existing registrations
        existing_registration = Registration.objects.filter(scout_hierachy=request.user.userextended.scout_organisation)
        if existing_registration.exists():
            single_registration = existing_registration.filter(responsible_persons__in=[request.user.id], single=True)
            existing_group_registration = existing_registration.filter(single=False)
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
                    not group_registration.exists() and \
                    serializer.data['single']:
                raise WrongRegistrationFormat

        registration: Registration = Registration(
            scout_hierachy=request.user.userextended.scout_organisation,
            event=event,
            single=serializer.data['single']
        )

        registration.save()
        registration.responsible_persons.add(request.user)

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
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegistrationPostSerializer
        elif self.request.method == 'GET':
            return RegistrationGetSerializer
        elif self.request.method == 'PUT':
            return RegistrationPutSerializer
        elif self.request.method == 'DESTROY':
            return RegistrationPutSerializer


class GroupAlreadyRegistered(APIException):
    status_code = 403
    default_detail = 'Your group is already registered'
    default_code = 'already_registered'


class NotResponsible(APIException):
    status_code = 403
    default_detail = 'An registration already exists, but you are not responsible'
    default_code = 'already_registered'


class SingleAlreadyRegistered(APIException):
    status_code = 403
    default_detail = "You're already registed"
    default_code = 'already_registered'


class SingleGroupNotAllowed(APIException):
    status_code = 403
    default_detail = "You already have a registation, please edit this one"
    default_code = 'already_registered'


class WrongRegistrationFormat(APIException):
    status_code = 405
    default_detail = "You're regisration contains information which does not fit to the event"
    default_code = 'misleading_information'


class RegistrationNotSupported(APIException):
    status_code = 501
    default_detail = "Attached registrations are currently not implemented"
    default_code = 'no_attached_registrations'
