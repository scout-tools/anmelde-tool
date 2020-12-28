# views.py
from itertools import chain
from rest_framework.response import Response
from django.db.models.functions import ExtractWeek, ExtractYear
from rest_framework import pagination, viewsets, mixins, generics, filters

from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, Participants
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, ScoutHierarchySerializer, \
    RegistrationSerializer, ZipCodeSerializer, ParticipantsSerializer


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


def get_bund_name(scout_organisation):
    if scout_organisation.level_id > 3:
        return get_bund_name(scout_organisation.parent)
    elif scout_organisation.level_id < 3:
        raise Exception("To low value")
    else:
        return scout_organisation.name


class ParticipantsViewSet(viewsets.ModelViewSet):
    queryset = Participants.objects.all()
    serializer_class = ParticipantsSerializer

    def list(self, request, event_pk=None):
        registrations = Registration.objects.all().filter(event_id=event_pk)
        data = []
        for reg in registrations:
            participants = reg.participants_set.all()
            for participant in participants:
                participant_data = self.serializer_class(participant).data
                bund_name = get_bund_name(reg.scout_organisation)
                participant_data["bund"] = bund_name
                participant_data["name"] = reg.scout_organisation.name
                if reg.scout_organisation.zip_code is not None:
                    participant_data["lat"] = reg.scout_organisation.zip_code.lat
                    participant_data["lon"] = reg.scout_organisation.zip_code.lon
                else:
                    participant_data["lat"] = 51.165691
                    participant_data["lon"] = 10.451526
                data.append(participant_data)
        return Response(data)
