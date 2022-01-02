from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from event.models import Event, EventLocation
from event.serializers import EventSerializer, EventPlanerSerializer, EventLocationSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class EventViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        if request.data.get('name', None) is None:
            request.data['name'] = 'Dummy'
        if request.data.get('responsible_person', None) is None:
            request.data['responsible_person'] = request.user.id
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class EventPlanerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventPlanerSerializer

    def get_queryset(self):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return Event.objects.filter(Q(keycloak_path__in=user_groups) | Q(responsible_person=self.request.user))
