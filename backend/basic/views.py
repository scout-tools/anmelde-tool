# views.py
from django.db.models.functions import ExtractWeek, ExtractYear
from rest_framework import pagination, viewsets, mixins, generics, filters

from .models import Event, AgeGroup, EventLocation, EventContact, ScoutHerarchy
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, EventContactSerializer, ScoutHerarchySerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AgeGroupViewSet(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class EventContactViewSet(viewsets.ModelViewSet):
    queryset = EventContact.objects.all()
    serializer_class = EventContactSerializer


class ScoutHerarchyViewSet(viewsets.ModelViewSet):
    queryset = ScoutHerarchy.objects.all()
    serializer_class = ScoutHerarchySerializer
