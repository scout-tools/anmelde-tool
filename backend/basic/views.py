# views.py
from django.db.models.functions import ExtractWeek, ExtractYear
from rest_framework import pagination, viewsets, mixins, generics, filters

from .models import Event, AgeGroup
from .serializers import EventSerializer, AgeGroupSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class AgeGroupViewSet(viewsets.ModelViewSet):
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer
