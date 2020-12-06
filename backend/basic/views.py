# views.py
from django.db.models.functions import ExtractWeek, ExtractYear
from rest_framework import pagination, viewsets, mixins, generics, filters

from .models import Event, AgeGroup, EventLocation, Person, ScoutHerarchy, Registration
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, PersonSerializer, ScoutHerarchySerializer, RegistrationSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AgeGroupViewSet(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ScoutHerarchyViewSet(viewsets.ModelViewSet):
    queryset = ScoutHerarchy.objects.all()
    serializer_class = ScoutHerarchySerializer


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
