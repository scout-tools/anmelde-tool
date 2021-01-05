# views.py
from itertools import chain
from rest_framework.response import Response
from django.db.models.functions import ExtractWeek, ExtractYear
from rest_framework import pagination, viewsets, mixins, generics, filters
from rest_framework.response import Response

from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, Participants
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, ScoutHierarchySerializer, \
    RegistrationSerializer, ZipCodeSerializer, ParticipantsSerializer, ParticipantsSerializer2


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AgeGroupViewSet(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class ScoutHierarchyViewSet(viewsets.ModelViewSet):
    queryset = ScoutHierarchy.objects.all()
    serializer_class = ScoutHierarchySerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


class ZipCodeViewSet(viewsets.ModelViewSet):
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer

class TravelMethodViewSet(viewsets.ModelViewSet):
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer

    def list(self, request, *args, **kwargs):
        return Response(["Auto (doof)", "Flugzeug (sehr doof)", "Bahn (gut)", "Fahrrad (sehr gut)"])

class ParticipantsViewSet(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer2


class ParticipantsViewSet2(viewsets.ModelViewSet):
    serializer_class = ParticipantsSerializer2

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        if event_id is not None:
            queryset = Participants.objects.filter(registration__event_id=event_id)
        else:
            queryset = Participants.objects.all()
        return queryset
