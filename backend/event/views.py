from copy import deepcopy
from datetime import datetime

from celery.result import AsyncResult
from django.db.models import Q, QuerySet
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basic import models as basic_models
from basic import serializers as basic_serializers
from event import api_exceptions as event_api_exceptions
from event import helper as event_helper
from event import models as event_models
from event import permissions as event_permissions
from event import serializers as event_serializers

from .sample_task import create_task


def add_event_module(module: event_models.EventModuleMapper,
                     event: event_models.Event) -> event_models.EventModuleMapper:
    new_module: event_models.EventModuleMapper = deepcopy(module)
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
    queryset = event_models.EventLocation.objects.all()
    serializer_class = event_serializers.EventLocationSerializer


class EventRegistrationViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = event_models.Event.objects.all()
    serializer_class = event_serializers.EventRegistrationSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [event_permissions.IsEventSuperResponsiblePerson]
    queryset = event_models.Event.objects.all()
    serializer_class = event_serializers.EventCompleteSerializer

    def get_formatted_date(self, date: str, request) -> datetime:
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
        if (request.data.get('responsible_persons') is None) | (request.data.get('responsible_persons', []) is []):
            request.data['responsible_persons'] = [request.user.email, ]
        serializer: event_serializers.EventCompleteSerializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        event: event_models.Event = serializer.save()
        event.responsible_persons.add(request.user)
        standard_event = event_helper.custom_get_or_404(event_api_exceptions.SomethingNotFound('Standard Event 1'),
                                                        event_models.StandardEventTemplate,
                                                        pk=1)

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
    permission_classes = [event_permissions.IsSubEventResponsiblePersonOrReadOnly]
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

        event = event_helper.get_event(event_id)

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
                                                     | Q(keycloak_admin_path__in=self.request.user.groups.all())
                                                     | Q(responsible_persons=self.request.user)).distinct()


class EventModulesMapperViewSet(mixins.CreateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                mixins.DestroyModelMixin,
                                viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePersonOrReadOnly]

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

        event = event_helper.get_event(event_id)
        standard_event = event_helper.custom_get_or_404(event_api_exceptions.SomethingNotFound('Standard Event 1'),
                                                        event_models.StandardEventTemplate,
                                                        pk=1)

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
    permission_classes = [event_permissions.IsEventResponsiblePersonOrReadOnly]
    serializer_class = event_serializers.EventModuleSerializer
    queryset = event_models.EventModule.objects.all()


class AvailableEventModulesViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [event_permissions.IsSubEventSuperResponsiblePerson]
    serializer_class = event_serializers.EventModuleSerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        mapper = event_models.EventModuleMapper.objects.filter(event=event_id).values_list('module_id', flat=True)
        return event_models.EventModule.objects.exclude(id__in=mapper).exclude(type__in=[7, 4]).exclude(custom=True)


class EventModuleAttributeMapperViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePersonOrReadOnly]

    def create(self, request, *args, **kwargs) -> Response:
        serializer: event_serializers.AttributeEventModuleMapperSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mapper_id = self.kwargs.get("eventmodulemapper_pk", None)
        mapper = event_helper.custom_get_or_404(event_api_exceptions.SomethingNotFound(f'Modul {mapper_id}'),
                                                event_models.EventModuleMapper,
                                                id=mapper_id)

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
        mapper = event_helper.custom_get_or_404(event_api_exceptions.SomethingNotFound(f'Modul {mapper_id}'),
                                                event_models.EventModuleMapper,
                                                id=mapper_id)
        return mapper.attributes.all()

    def get_serializer_class(self):
        if self.action == 'update':
            return event_serializers.AttributeEventModuleMapperPostSerializer
        else:
            return event_serializers.AttributeEventModuleMapperSerializer


class AssignedEventModulesViewSet(viewsets.ModelViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePersonOrReadOnly]
    serializer_class = event_serializers.EventModuleMapperGetSerializer

    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("event_pk", None)
        return event_models.EventModuleMapper.objects.filter(event=event_id).order_by('ordering')


class EventOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = event_serializers.EventOverviewSerializer
    def get_queryset(self) -> QuerySet:
        event_id = self.kwargs.get("pk", None)
        if (event_id):
            return event_models.Event.objects.filter(id=event_id).all()

        if self.request.user.is_superuser:
            return event_models.Event.objects.filter(is_public=True, end_date__gte=timezone.now())
        else:
            list_parent_organistations = []
            iterator: basic_models.ScoutHierarchy = self.request.user.userextended.scout_organisation
            while iterator is not None:
                list_parent_organistations.append(iterator)
                iterator = iterator.parent
            return event_models.Event.objects.filter(is_public=True, end_date__gte=timezone.now(),
                                                     limited_registration_hierarchy__in=list_parent_organistations)


class ScoutHierarchyViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = basic_serializers.ScoutHierarchySerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.userextended.scout_organisation.level.id < 5:
            raise event_api_exceptions.ScoutHierarchyAtThisLevelNotPossible

        if self.request.user.userextended.scout_organisation.level == 6:
            scout_organisation = self.request.user.userextended.scout_organisation.parent
        else:
            scout_organisation = self.request.user.userextended.scout_organisation

        name = request.data.get('name', None)
        if name:
            exists = basic_models.ScoutHierarchy \
                .objects.filter(level=6, parent_id=scout_organisation.id, name__iexact=name).exists()
            if exists:
                raise event_api_exceptions.ScoutHierarchyAlreadyExist

        request.data['level'] = 6
        request.data['zip_code'] = scout_organisation.zip_code.id
        request.data['parent'] = scout_organisation.id

        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        level = int(self.request.query_params.get('level', 5))
        if level == 5:
            return basic_models.ScoutHierarchy.objects.filter(
                id=self.request.user.userextended.scout_organisation.id,
                level=5)
        elif level in {2, 3, 4}:
            user_orga = self.request.user.userextended.scout_organisation
            orga_filter = Q(id=user_orga.id)

            if user_orga.parent:
                orga_filter |= Q(id=user_orga.parent.id)
                if user_orga.parent.parent:
                    orga_filter |= Q(id=user_orga.parent.parent.id)

            return basic_models.ScoutHierarchy.objects.filter(orga_filter, level=level)
        elif level == 6:
            return basic_models.ScoutHierarchy.objects.filter(
                level=6,
                parent_id=self.request.user.userextended.scout_organisation.id)
        else:
            return []


class TestViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        task_type = request.data.get("type", 1)
        task = create_task.delay(int(task_type))
        return Response({"task_id": task.id}, status=202)

    def retrieve(self, request, *args, **kwargs):
        task_id = kwargs.get("pk", None)
        print(task_id)
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result
        }
        return Response(result, status=200)
