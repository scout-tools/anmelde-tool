# views.py
from itertools import chain
from rest_framework.response import Response
from django.db.models.functions import ExtractWeek, ExtractYear
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets, mixins, generics, filters


from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration,\
        ZipCode, Participant, ParticipantRole, Role, MethodOfTravel, Tent,\
        ScoutOrgaLevel, ParticipantExtended, EatHabitType, EatHabit, TravelType, TentType
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer,\
    ScoutHierarchySerializer, RegistrationSerializer, ZipCodeSerializer, ParticipantSerializer,\
    ParticipantRoleSerializer, RoleSerializer, MethodOfTravelSerializer, TentSerializer,\
    ParticipantSerializer2, ScoutOrgaLevelSerializer, ParticipantExtendedSerializer,\
    EatHabitTypeSerializer, EatHabitSerializer, TravelTypeSerializer, TentTypeSerializer


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['zip_code']


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ParticipantRoleViewSet(viewsets.ModelViewSet):
    queryset = ParticipantRole.objects.all()
    serializer_class = ParticipantRoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class MethodOfTravelViewSet(viewsets.ModelViewSet):
    queryset = MethodOfTravel.objects.all()
    serializer_class = MethodOfTravelSerializer


class TentViewSet(viewsets.ModelViewSet):
    queryset = Tent.objects.all()
    serializer_class = TentSerializer


class ParticipantViewSet2(viewsets.ModelViewSet):
    serializer_class = ParticipantSerializer2

    def get_queryset(self):
        event_id = self.kwargs.get("event_pk", None)
        if event_id is not None:
            queryset = Participant.objects.filter(registration__event_id=event_id)
        else:
            queryset = Participant.objects.all()
        return queryset


class ScoutOrgaLevelViewSet(viewsets.ModelViewSet):
    queryset = ScoutOrgaLevel.objects.all()
    serializer_class = ScoutOrgaLevelSerializer


class ParticipantExtendedViewSet(viewsets.ModelViewSet):
    queryset = ParticipantExtended.objects.all()
    serializer_class = ParticipantExtendedSerializer


class EatHabitTypeViewSet(viewsets.ModelViewSet):
    queryset = EatHabitType.objects.all()
    serializer_class = EatHabitTypeSerializer


class EatHabitViewSet(viewsets.ModelViewSet):
    queryset = EatHabit.objects.all()
    serializer_class = EatHabitSerializer


class TravelTypeViewSet(viewsets.ModelViewSet):
    queryset = TravelType.objects.all()
    serializer_class = TravelTypeSerializer


class TentTypeViewSet(viewsets.ModelViewSet):
    queryset = TentType.objects.all()
    serializer_class = TentTypeSerializer
