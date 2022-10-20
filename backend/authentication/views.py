import re
from datetime import timedelta

from django.db.models import Q, QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from event import api_exceptions as event_api_exceptions
from basic import models as basic_models

from datetime import datetime, time
import pytz

from basic.api_exceptions import TooManySearchResults, NoSearchResults
from basic.permissions import IsStaffOrReadOnly
from .models import Person, UserExtended, EmailNotificationType
from .serializers import UserExtendedGetSerializer, UserExtendedPostSerializer, GroupSerializer, \
    EmailSettingsSerializer, ResponsablePersonSerializer, PersonSerializer, PersonPostSerializer


def create_missing_eat_habits(request) -> [str]:
    eat_habits = request.data.get('eat_habits', [])
    result = []
    for habit in eat_habits:
        if len(habit) > 100:
            raise event_api_exceptions.EatHabitTooLong
        splitted = re.split(',|;', habit)
        for split in splitted:
            split = split.strip().title()
            result.append(split)
            if not basic_models.EatHabit.objects.filter(name__exact=split).exists():
                basic_models.EatHabit.objects.create(name=split)
    return result


class PersonalData(viewsets.ViewSet):
    """
    Viewset for handling personal data, contained in the UserExtended model
    """
    permission_classes = [IsAuthenticated]

    # pylint: disable=no-self-use
    def list(self, request) -> Response:
        """
        @param request: request information
        @return: Response with serialized UserExtended instance of the user requesting the personal data
        """
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedGetSerializer(queryset, many=False)
        return Response(serializer.data)

    # pylint: disable=no-self-use
    def create(self, request) -> Response:
        """
        Create UserExtended instance
        @param request: standard django request information
                        containg the UserExtendedPostSerializer values in the data field
        @return: new userextended instance
        """
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedPostSerializer(queryset, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # pylint: disable=no-self-use
    def delete(self, request) -> Response:
        """
        @param request: standard django request information
        @return: Statuscode 200 after the user is successfully deleted
        """
        user = request.user
        user.delete()
        return Response(status=status.HTTP_200_OK)


class PersonalDataCheck(viewsets.ViewSet):
    """
    Viewset if the personal data is set up correctly, when yes return 200
    else return 426 so that the frontend can notify the user about missing information
    """
    permission_classes = [IsAuthenticated]

    # pylint: disable=no-self-use
    def list(self, request) -> Response:
        """
        @param request: standard django request information
        @return: Reponse wether user data is complete or not
        """
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedGetSerializer(queryset, many=False)
        if not serializer.data['scout_organisation'] or not serializer.data['dsgvo_confirmed']:
            return Response({'status': "init required"}, status=status.HTTP_426_UPGRADE_REQUIRED)

        return Response({'status': "user ok"}, status=status.HTTP_200_OK)


class PersonConnect(viewsets.ViewSet):
    """
    Viewset if the personal data is set up correctly, when yes return 200
    else return 426 so that the frontend can notify the user about missing information
    """
    permission_classes = [IsAuthenticated]

    # pylint: disable=no-self-use
    def create(self, request) -> Response:
        """
        @param request: standard django request information
        @return: Reponse wether user data is complete or not
        """
        user = UserExtended.objects.get(user=request.user)
        person = Person.objects.get(id=request.data.get('person'))
        user.person = person
        user.save()

        return Response({'status': "ok"}, status=status.HTTP_200_OK)

    def delete(self, request) -> Response:
        user = UserExtended.objects.get(user=request.user)
        user.person = None
        user.save()

        return Response({'status': "ok"}, status=status.HTTP_200_OK)


class ResponsablePersonViewSet(viewsets.ModelViewSet):
    """
    Viewset for filtering responsable persons
    """
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = ResponsablePersonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__email', 'scout_name', ]

    def list(self, request, *args, **kwargs) -> Response:
        queryset = UserExtended.objects.all()
        search_param = request.GET.get('search')
        queryset = queryset.filter(Q(scout_name__icontains=search_param)
                                   | Q(user__email__icontains=search_param)
                                   | Q(scout_organisation__name__icontains=search_param))
        serializer = ResponsablePersonSerializer(queryset, many=True)
        response_len = len(serializer.data)
        if response_len > 10:
            raise TooManySearchResults
        if response_len == 0:
            raise NoSearchResults
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Viewset for retrieving groups
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def get_queryset(self):
        """
        @return: all groups which a user has
        """
        return self.request.user.groups.all()


class EmailSettingsViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for retrieving and updating notification settings of a user
    """
    serializer_class = EmailSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        @return: UserExtended instance of the user requesting the email settings
        """
        return UserExtended.objects.filter(id=self.request.user.userextended.id)


class EmailNotificationTypeViewSet(viewsets.ViewSet):
    """
    Viewset for retrieving the choices of notifications
    """
    permission_classes = [IsAuthenticated]

    # pylint: disable=no-self-use
    def list(self, request) -> Response:
        """
        @param request: standard django request
        @return: Response which EmailNotificationType choices
        """
        return Response(EmailNotificationType.choices, status=status.HTTP_200_OK)


class PersonsViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling person data, contained in the UserExtended model
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PersonSerializer

    def get_queryset(self) -> QuerySet:
        return Person.objects.filter(owned_by__in=[self.request.user.id])

    # pylint: disable=no-self-use

    def create(self, request, *args, **kwargs) -> Response:

        birthday = datetime.strptime(request.data['birthday'][:10], '%Y-%m-%d')
        request.data['birthday'] = birthday.date() + timedelta(days=1)

        request.data['created_by'] = request.user.id

        eat_habits_formatted = create_missing_eat_habits(request)

        if eat_habits_formatted and len(eat_habits_formatted) > 0:
            request.data['eat_habits'] = eat_habits_formatted

        return super().create(request, *args, **kwargs)

    # pylint: disable=no-self-use
    def update(self, request, *args, **kwargs) -> Response:
        birthday = datetime.strptime(request.data['birthday'][:10], '%Y-%m-%d')
        request.data['birthday'] = birthday.date() + timedelta(days=1)

        eat_habits_formatted = create_missing_eat_habits(request)

        if eat_habits_formatted and len(eat_habits_formatted) > 0:
            request.data['eat_habits'] = eat_habits_formatted

        return super().update(request, *args, **kwargs)
