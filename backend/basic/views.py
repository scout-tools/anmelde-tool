# views.py
from rest_framework import viewsets
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, Participants
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, ScoutHierarchySerializer, \
    RegistrationSerializer, ZipCodeSerializer, ParticipantsSerializer2
from django.contrib.auth.models import User
from Helper.user_creation import CreateUserExternally


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

    def create(self, request, *args, **kwargs):
        emails = request.data['responsible_persons']
        for user_email in emails:
            user = User.objects.filter(username=user_email).first()
            if user is None:
                CreateUserExternally(user_email)
        # TODO: Add email notification for adding a helper
        return super().create(request, *args, **kwargs)


class ZipCodeViewSet(viewsets.ModelViewSet):
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer


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
