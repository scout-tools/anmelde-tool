from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotFound, MethodNotAllowed
from rest_framework.permissions import IsAuthenticated

from event.models import Event, EventLocation, SleepingLocation
from event.serializers import EventPlanerSerializer, EventLocationGetSerializer, EventLocationPostSerializer, \
    EventCompleteSerializer, SleepingLocationSerializer


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
    # permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventCompleteSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = 'Dummy'
        if request.data.get('responsible_persons', None) is None:
            request.data['responsible_persons'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = self.get_object().name
        return super().update(request, *args, **kwargs)


class SleepingLocationViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = SleepingLocationSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        return SleepingLocation.objects.filter(event=event_id)

    def create(self, request, *args, **kwargs):
        if request.data.get('name', None) is None:
            request.data['name'] = 'Standard'
        event_id = self.kwargs.get("event_pk", None)
        if event_id is not None:
            event = Event.objects.get(id=event_id)
            request.data['event'] = event_id
        else:
            raise NotFound()
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
