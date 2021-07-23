# views.py
import io
import time

import xlsxwriter
from django.contrib.auth.models import User
from django.db.models import Q, Case, When, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import FilterSet, CharFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from django.core.exceptions import PermissionDenied
from helper.user_creation import CreateUserExternally
from rest_framework.response import Response
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, \
    ZipCode, ParticipantGroup, Role, MethodOfTravel, Tent, \
    ScoutOrgaLevel, ParticipantPersonal, EatHabitType, EatHabit, TravelType, \
    TentType, EatHabit, TravelTag, PostalAddress, EventRoleMapping, RegistrationMatching, \
    Workshop
from .serializers import EventSerializer, AgeGroupSerializer, EventLocationSerializer, \
    ScoutHierarchySerializer, RegistrationSerializer, ZipCodeSerializer, ParticipantGroupSerializer, \
    RoleSerializer, MethodOfTravelSerializer, TentSerializer, \
    EventParticipantsSerializer, ScoutOrgaLevelSerializer, ParticipantPersonalSerializer, \
    EatHabitTypeSerializer, EatHabitSerializer, TravelTypeSerializer, \
    TentTypeSerializer, EventOverviewSerializer, EatHabitSerializer, EventCashMasterSerializer, \
    EventKitchenMasterSerializer, EventProgramMasterSerializer, RegistrationParticipantsSerializer, \
    RegistrationSummarySerializer, TravelTagSerializer, PostalAddressSerializer, RegistrationStatSerializer, \
    WorkshopSerializer, WorkshopStatsSerializer

from .permissions import IsEventMaster, IsKitchenMaster, IsEventCashMaster, IsProgramMaster, \
    IsLogisticMaster, IsSocialMediaPermission, IsResponsiblePersonPermission, IsTeamMemberPermission, \
    IsOrganisationLeader, IsResponsiblePersonParticipantPersonalPermission

from helper.registration_summary import registration_responsible_person, create_registration_summary, \
    create_reminder_registration
from helper.registration_matching_mail import create_matching_mail


def get_dataset(kwargs, pk, dataset):
    dataset_id = kwargs.get(pk, None)
    if dataset_id is not None:
        return dataset.objects.filter(id=dataset_id)
    else:
        return Response('No dataset selected', status=status.HTTP_400_BAD_REQUEST)


def get_event(kwargs):
    event_id = kwargs.get("event_pk", None)
    if event_id is not None:
        return Event.objects.get(id=event_id)
    else:
        return Response('No event selected', status=status.HTTP_400_BAD_REQUEST)


def filter_data(user, kwargs, data):
    event_id = kwargs.get("event_pk", None)
    role = EventRoleMapping.objects.filter(event_id=event_id, user=user)
    # parent_level =
    # queryset = data.objects.filter()
    return


def get_registrations_from_event(kwargs):
    event_id = kwargs.get("event_pk", None)
    if event_id is not None:
        return Registration.objects.filter(event=event_id)
    else:
        return Response('No event selected', status=status.HTTP_400_BAD_REQUEST)


def create_missing_eat_habit(request):
    # Check whether habit type exists
    if 'eat_habit_type' in request.data:
        habit_types = request.data['eat_habit_type']
        for food_type in habit_types:
            if not EatHabitType.objects.filter(name__exact=food_type).exists():
                new_type = EatHabitType.objects.create(name=food_type)
                new_type.save()


def create_missing_scout_group(request):
    # Check whether group name exits
    if 'scout_group' in request.data:
        scout_group = request.data['scout_group']
        if not ScoutHierarchy.objects.filter(name__exact=scout_group, level__id=6).exists():
            new_group = ScoutHierarchy.objects.create(name=scout_group, level=ScoutOrgaLevel.objects.get(pk=6),
                                                      parent=request.user.userextended.scout_organisation)
            new_group.save()


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventOverviewViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()
    serializer_class = EventOverviewSerializer


class AgeGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AgeGroup.objects.all()
    serializer_class = AgeGroupSerializer


class EventLocationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)
    queryset = EventLocation.objects.all()
    serializer_class = EventLocationSerializer


class ScoutHierarchyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScoutHierarchy.objects.all().exclude(level=6)
    serializer_class = ScoutHierarchySerializer


class ScoutHierachyGroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ScoutHierarchySerializer

    def get_queryset(self):
        return ScoutHierarchy.objects.filter(level=6, parent=self.request.user.userextended.scout_organisation)


class RegistrationViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [IsAuthenticated],
                                    'default': [IsAuthenticated, IsResponsiblePersonPermission]}
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)

    def create(self, request, *args, **kwargs):
        if 'event' not in request.data:
            return Response('Event not selected', status=status.HTTP_400_BAD_REQUEST)
        # Check invitation code
        queryset_event = Event.objects.all()
        event = get_object_or_404(queryset_event, pk=request.data['event'])

        if request.user.userextended.scout_organisation.id != request.data['scout_organisation']:
            return Response({'forbidden': 'scout organisation from user and request does not match'},
                            status=status.HTTP_403_FORBIDDEN)
        if event.registration_set.filter(scout_organisation=request.user.userextended.scout_organisation.id).exists():
            return Response({'forbidden': 'already registered'}, status=status.HTTP_403_FORBIDDEN)

        if 'code' in self.request.query_params:
            code = self.request.query_params.get('code', None)
        else:
            return Response({'code': 'missing query param'}, status=status.HTTP_400_BAD_REQUEST)

        if event.invitation_code != code:
            raise PermissionDenied('wrong invitation code')

        self.add_responsible_person(event, request)

        return super().create(request, *args, **kwargs)

    def update(self, request, pk=None, partial=False):
        queryset_registration = Registration.objects.all()
        registration = get_object_or_404(queryset_registration, pk=pk)

        if "responsible_persons" in request.data or not partial:
            queryset_event = Event.objects.all()
            event = get_object_or_404(queryset_event, pk=request.data['event'])
            self.add_responsible_person(event, request, registration)

        response = super().update(request, pk, partial=partial)

        if registration is not None and not registration.is_confirmed and 'is_confirmed' in response.data and \
                response.data['is_confirmed']:
            create_registration_summary(response.data)
        return response

    def add_responsible_person(self, event, request, registration=None):
        event_data = {'event': event.name,
                      'event_id': event.id,
                      'foreign_email': request.user.username,
                      'foreign_name': request.user.userextended.scout_name
                      }

        # Check responsible person
        emails = request.data['responsible_persons']

        # Check if responsible person already exists
        new_responsible_persons = []
        if registration is not None:
            existing_responsible_persons = registration.responsible_persons.values_list('username', flat=True)

            for email in emails:
                if email not in existing_responsible_persons:
                    new_responsible_persons.append(email)
        else:
            new_responsible_persons = emails

        # send to each new responsible person a notification
        for user_email in new_responsible_persons:
            if user_email != request.user.username:
                data = event_data
                user = User.objects.filter(username=user_email).first()
                if user is None:
                    data.update(CreateUserExternally(user_email, event_data))
                else:
                    user_data = {'username': user.userextended.scout_name if user.userextended is not None else
                    user.username.split('@', 1)[0],
                                 'user': user.username,
                                 'email': user.username,
                                 }
                    data.update(user_data)
                registration_responsible_person(data)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes_by_action['default']]


class ZipCodeSearchFilter(FilterSet):
    zip_city = CharFilter(field_name='zip_city', method='get_zip_city')

    class Meta:
        model = ZipCode
        fields = ['zip_code', 'city', 'id']

    def get_zip_city(self, queryset, field_name, value):
        cities = queryset.filter(Q(zip_code__contains=value) | Q(city__contains=value))
        if cities.count() > 250:
            raise PermissionDenied('Too many results!!!')
        return cities


class ZipCodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer
    filterset_class = ZipCodeSearchFilter


class ParticipantGroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ParticipantGroup.objects.all().order_by('-updated_at')
    serializer_class = ParticipantGroupSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)


class RoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class MethodOfTravelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = MethodOfTravel.objects.all()
    serializer_class = MethodOfTravelSerializer


class TentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tent.objects.all()
    serializer_class = TentSerializer


class ScoutOrgaLevelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScoutOrgaLevel.objects.all()
    serializer_class = ScoutOrgaLevelSerializer


class ParticipantPersonalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonParticipantPersonalPermission]
    queryset = ParticipantPersonal.objects.all()
    serializer_class = ParticipantPersonalSerializer

    def create(self, request, *args, **kwargs):
        create_missing_scout_group(request)
        create_missing_eat_habit(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        create_missing_scout_group(request)
        create_missing_eat_habit(request)
        return super().update(request, *args, **kwargs)


class EatHabitTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EatHabitType.objects.all()
    serializer_class = EatHabitTypeSerializer


class EatHabitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EatHabit.objects.all()
    serializer_class = EatHabitSerializer

    def create(self, request, *args, **kwargs):
        create_missing_eat_habit(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class TravelTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TravelType.objects.all()
    serializer_class = TravelTypeSerializer


class TentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TentType.objects.all()
    serializer_class = TentTypeSerializer


class PostalAddressViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PostalAddress.objects.all()
    serializer_class = PostalAddressSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)


class TravelTagViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TravelTag.objects.all()
    serializer_class = TravelTagSerializer


class EventCodeCheckerViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        event = get_object_or_404(queryset, pk=pk)

        if 'code' in self.request.query_params:
            code = self.request.query_params.get('code', None)
        else:
            return Response({'code': 'missing query param'}, status=status.HTTP_400_BAD_REQUEST)

        if event.invitation_code == code:
            return Response({'status': 'Code correct'}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied('wrong invitation code')


class EventMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]
    serializer_class = EventCashMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventCashMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsEventCashMaster]
    serializer_class = EventCashMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventKitchenMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsKitchenMaster]
    serializer_class = EventKitchenMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventProgramMasterViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsProgramMaster]
    serializer_class = EventProgramMasterSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class EventParticipantsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EventParticipantsSerializer

    def get_queryset(self):
        return get_event(self.kwargs)


class RegistrationParticipantsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonPermission]
    serializer_class = RegistrationParticipantsSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("registration_pk", None)
        if event_id is not None:
            return Registration.objects.filter(id=event_id)
        else:
            return Response('No registration selected', status=status.HTTP_400_BAD_REQUEST)


class RegistrationSummaryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsResponsiblePersonPermission]
    serializer_class = RegistrationSummarySerializer

    def get_queryset(self):
        return get_dataset(self.kwargs, 'registration_pk', Registration)


class RegistrationStatViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTeamMemberPermission]  # IsOrganisationLeader
    serializer_class = RegistrationStatSerializer

    def get_queryset(self):
        queryset = get_registrations_from_event(self.kwargs)
        # queryset = filter_data(self.request.user, self.kwargs, queryset)
        return queryset


class TravelPreferenceXlsxViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]
    queryset = ParticipantGroup.objects.all().order_by('-updated_at')

    def list(self, request, event_pk):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        groups = Registration.objects.filter(event_id=event_pk).values(
            "scout_organisation__name",
            "scout_organisation__zip_code__zip_code",
            "scout_organisation__zip_code__city",
            "custom_choice",
            "eventlocation").annotate(
            bund=Case(When(scout_organisation__parent__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__parent__name')),
                      When(scout_organisation__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__name')),
                      When(scout_organisation__parent__level=3,
                           then=F('scout_organisation__parent__name')),
                      When(scout_organisation__level=3,
                           then=F('scout_organisation__name')))
        )

        options = {1: 'Heim, Zuhause',
                   4: 'Heim, auswärts, nah',
                   5: 'Heim, auswärts, weit weg',
                   6: 'Heim, auswärts, Distanz egal',
                   7: 'Heim, egal wo, lieber nah',
                   8: 'Heim, egal wo, lieber weit',
                   9: 'Heim, egal wo, Distanz egal',
                   10: 'Kein Heim, lieber nah',
                   11: 'Kein Heim, lieber weit',
                   12: 'Kein Heim, Distanz egal',
                   }

        worksheet.set_column(0, 2, 25)

        worksheet.write(0, 0, "Export-Timestamp")
        worksheet.write(0, 1, time.ctime())

        worksheet.write(1, 0, "Stamm")
        worksheet.write(1, 1, "Bund")
        worksheet.write(1, 2, "Plz")
        worksheet.write(1, 3, "Ort")
        worksheet.write(1, 4, "Präferenz")
        worksheet.write(1, 5, "Hat Heim")

        for row_num, group in enumerate(groups.iterator()):
            worksheet.write(row_num + 2, 0, group['scout_organisation__name'])
            worksheet.write(row_num + 2, 1, group['bund'])
            worksheet.write(row_num + 2, 2, group['scout_organisation__zip_code__zip_code'])
            worksheet.write(row_num + 2, 3, group['scout_organisation__zip_code__city'])
            worksheet.write(row_num + 2, 4, options.get(group['custom_choice']))

            if group['eventlocation']:
                worksheet.write(row_num + 2, 5, 'x')

        workbook.close()
        output.seek(0)

        filename = f"group_custom_choice_{int(time.time())}.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class TextAndPackageAddressXlsxViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]
    queryset = ParticipantGroup.objects.all().order_by('-updated_at')

    def list(self, request, event_pk):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        groups = Registration.objects.filter(event_id=event_pk).values(
            "scout_organisation__name",
            "postaladdress__street",
            "postaladdress__first_name",
            "postaladdress__last_name",
            "postaladdress__address_addition",
            "postaladdress__zip_code__zip_code",
            "postaladdress__zip_code__city",
            "free_text").annotate(
            bund=Case(When(scout_organisation__parent__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__parent__name')),
                      When(scout_organisation__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__name')),
                      When(scout_organisation__parent__level=3,
                           then=F('scout_organisation__parent__name')),
                      When(scout_organisation__level=3,
                           then=F('scout_organisation__name')))
        )

        worksheet.set_column(0, 1, 25)
        worksheet.set_column(2, 3, 10)
        worksheet.set_column(4, 7, 20)
        worksheet.set_column(6, 6, 8)
        worksheet.set_column(8, 8, 40)

        worksheet.write(0, 0, "Export-Timestamp")
        worksheet.write(0, 1, time.ctime())

        worksheet.write(1, 0, "Stamm")
        worksheet.write(1, 1, "Bund")
        worksheet.write(1, 2, "First")
        worksheet.write(1, 3, "Last")
        worksheet.write(1, 4, "Street")
        worksheet.write(1, 5, "Add.")
        worksheet.write(1, 6, "Plz")
        worksheet.write(1, 7, "Stadt")
        worksheet.write(1, 8, "Text")
        for row_num, group in enumerate(groups.iterator()):
            worksheet.write(row_num + 2, 0, group['scout_organisation__name'])
            worksheet.write(row_num + 2, 1, group['bund'])
            worksheet.write(row_num + 2, 2, group['postaladdress__first_name'])
            worksheet.write(row_num + 2, 3, group['postaladdress__last_name'])
            worksheet.write(row_num + 2, 4, group['postaladdress__street'])
            worksheet.write(row_num + 2, 5, group['postaladdress__address_addition'])
            worksheet.write(row_num + 2, 6, group['postaladdress__zip_code__zip_code'])
            worksheet.write(row_num + 2, 7, group['postaladdress__zip_code__city'])
            worksheet.write(row_num + 2, 8, group['free_text'])

        workbook.close()
        output.seek(0)

        filename = f"text_package_address{int(time.time())}.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class EventLocationFeeXlsxViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]
    queryset = ParticipantGroup.objects.all().order_by('-updated_at')

    def list(self, request, event_pk):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        locations = EventLocation.objects.filter(registration__event_id=event_pk).values(
            "name",
            "address",
            "zip_code__zip_code",
            "zip_code__city",
            "contact_name",
            "contact_email",
            "contact_phone",
            "fix_fee",
            "per_person_fee",
            "capacity_corona",
            "capacity",
            "location_type__name",
            "registration__scout_organisation__name") \
            .annotate(bund=Case(When(registration__scout_organisation__parent__parent__parent__level=3,
                                     then=F('registration__scout_organisation__parent__parent__parent__name')),
                                When(registration__scout_organisation__parent__parent__level=3,
                                     then=F('registration__scout_organisation__parent__parent__name')),
                                When(registration__scout_organisation__parent__level=3,
                                     then=F('registration__scout_organisation__parent__name')),
                                When(registration__scout_organisation__level=3,
                                     then=F('registration__scout_organisation__name'))))

        worksheet.set_column(0, 13, 25)

        worksheet.write(0, 0, "Export-Timestamp")
        worksheet.write(0, 1, time.ctime())

        worksheet.write(1, 0, "Stamm")
        worksheet.write(1, 1, "Bund")
        worksheet.write(1, 2, "Kontakt")
        worksheet.write(1, 3, "Email")
        worksheet.write(1, 4, "Telefon")
        worksheet.write(1, 5, "Name")
        worksheet.write(1, 6, "Adresse")
        worksheet.write(1, 7, "Postleitzahl")
        worksheet.write(1, 8, "Stadt")
        worksheet.write(1, 9, "Typ")
        worksheet.write(1, 10, "Fixkosten")
        worksheet.write(1, 11, "Kosten p.P.")
        worksheet.write(1, 12, "Schlafplatz")
        worksheet.write(1, 13, "Schlafplatz unter Corona Bedinungen")

        for row_num, location in enumerate(locations.iterator()):
            worksheet.write(row_num + 2, 0, location['registration__scout_organisation__name'])
            worksheet.write(row_num + 2, 1, location['bund'])
            worksheet.write(row_num + 2, 2, location['contact_name'])
            worksheet.write(row_num + 2, 3, location['contact_email'])
            worksheet.write(row_num + 2, 4, location['contact_phone'])
            worksheet.write(row_num + 2, 5, location['name'])
            worksheet.write(row_num + 2, 6, location['address'])
            worksheet.write(row_num + 2, 7, location['zip_code__zip_code'])
            worksheet.write(row_num + 2, 8, location['zip_code__city'])
            worksheet.write(row_num + 2, 9, location['location_type__name'])
            worksheet.write(row_num + 2, 10, location['fix_fee'])
            worksheet.write(row_num + 2, 11, location['per_person_fee'])
            worksheet.write(row_num + 2, 12, location['capacity'])
            worksheet.write(row_num + 2, 13, location['capacity_corona'])

        workbook.close()
        output.seek(0)

        filename = f"event_location_fee{int(time.time())}.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class RegistrationGroupsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]
    queryset = ParticipantGroup.objects.all().order_by('-updated_at')

    def list(self, request, event_pk):
        output = io.BytesIO()

        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()

        groups = Registration.objects.filter(event_id=event_pk).values(
            'id',
            "scout_organisation__name",
            "responsible_persons__userextended__scout_name",
            "responsible_persons__username",
            "scout_organisation__zip_code__zip_code",
            "scout_organisation__zip_code__city",
            "custom_choice", ).annotate(
            bund=Case(When(scout_organisation__parent__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__parent__name')),
                      When(scout_organisation__parent__parent__level=3,
                           then=F('scout_organisation__parent__parent__name')),
                      When(scout_organisation__parent__level=3,
                           then=F('scout_organisation__parent__name')),
                      When(scout_organisation__level=3,
                           then=F('scout_organisation__name')))
        )

        options = {1: 'Heim, Zuhause',
                   4: 'Heim, auswärts, nah',
                   5: 'Heim, auswärts, weit weg',
                   6: 'Heim, auswärts, Distanz egal',
                   7: 'Heim, egal wo, lieber nah',
                   8: 'Heim, egal wo, lieber weit',
                   9: 'Heim, egal wo, Distanz egal',
                   10: 'Kein Heim, lieber nah',
                   11: 'Kein Heim, lieber weit',
                   12: 'Kein Heim, Distanz egal',
                   }

        worksheet.write(0, 0, "Export-Timestamp")
        worksheet.write(0, 1, time.ctime())

        worksheet.set_column(0, 25, 25)

        worksheet.write(1, 0, "Stamm")
        worksheet.write(1, 1, "Bund")
        worksheet.write(1, 2, "Veranwortliche Person")
        worksheet.write(1, 3, "Email")
        worksheet.write(1, 4, "Plz")
        worksheet.write(1, 5, "Ort")
        worksheet.write(1, 6, "Präferenz")
        worksheet.write(1, 7, "Stammesvertretung")
        worksheet.write(1, 8, "Helferlein")
        worksheet.write(1, 9, "Teilnehmende")
        worksheet.write(1, 10, "Gruppenleitung")
        worksheet.write(1, 11, "Name Des Schlafplatzes 1")
        worksheet.write(1, 12, "Typ")
        worksheet.write(1, 13, "Fixkosten")
        worksheet.write(1, 14, "Kosten p.P.")
        worksheet.write(1, 15, "Schlafplätze")
        worksheet.write(1, 16, "Schlafplätze unter Corona Bedinungen")
        worksheet.write(1, 17, "Name Des Schlafplatzes 2")
        worksheet.write(1, 18, "Typ")
        worksheet.write(1, 19, "Fixkosten")
        worksheet.write(1, 20, "Kosten p.P.")
        worksheet.write(1, 21, "Schlafplätze")
        worksheet.write(1, 22, "Schlafplätze unter Corona Bedinungen")

        for row_num, group in enumerate(groups.iterator()):
            participant_group = ParticipantGroup.objects.filter(registration__id=group['id']).values(
                "participant_role__name",
                "number_of_persons", )

            stammesvertretung = 0
            helferlein = 0
            teilnehmende = 0
            gruppenleitung = 0
            for participants in participant_group:
                if participants['participant_role__name'] == 'Gruppenleitung':
                    gruppenleitung = participants['number_of_persons']
                elif participants['participant_role__name'] == 'Stammesvertretung':
                    stammesvertretung = participants['number_of_persons']
                elif participants['participant_role__name'] == 'Helferlein':
                    helferlein = participants['number_of_persons']
                elif participants['participant_role__name'] == 'Teilnehmende':
                    teilnehmende = participants['number_of_persons']

            locations = EventLocation.objects.filter(registration__id=group['id']).values(
                "name",
                "fix_fee",
                "per_person_fee",
                "capacity_corona",
                "capacity",
                "location_type__name")

            worksheet.write(row_num + 2, 0, group['scout_organisation__name'])
            worksheet.write(row_num + 2, 1, group['bund'])
            worksheet.write(row_num + 2, 2, group['responsible_persons__userextended__scout_name'])
            worksheet.write(row_num + 2, 3, group['responsible_persons__username'])
            worksheet.write(row_num + 2, 4, group['scout_organisation__zip_code__zip_code'])
            worksheet.write(row_num + 2, 5, group['scout_organisation__zip_code__city'])
            worksheet.write(row_num + 2, 6, options.get(group['custom_choice']))
            worksheet.write(row_num + 2, 7, stammesvertretung)
            worksheet.write(row_num + 2, 8, helferlein)
            worksheet.write(row_num + 2, 9, teilnehmende)
            worksheet.write(row_num + 2, 10, gruppenleitung)

            for col_num, loc in enumerate(locations.iterator()):
                worksheet.write(row_num + 2, 11 + col_num * 6, loc['name'])
                worksheet.write(row_num + 2, 12 + col_num * 6, loc['location_type__name'])
                worksheet.write(row_num + 2, 13 + col_num * 6, loc['fix_fee'])
                worksheet.write(row_num + 2, 14 + col_num * 6, loc['per_person_fee'])
                worksheet.write(row_num + 2, 15 + col_num * 6, loc['capacity'])
                worksheet.write(row_num + 2, 16 + col_num * 6, loc['capacity_corona'])

        workbook.close()
        output.seek(0)

        filename = f"registration_groups_{int(time.time())}.xlsx"
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


class ReminderMailViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsEventMaster]

    def create(self, request, *args, **kwargs):
        registrations = get_registrations_from_event(kwargs)
        event = get_event(kwargs)

        if 'code' in request.query_params:
            code = request.query_params.get('code', None)
        else:
            return Response({'code': 'missing query param'}, status=status.HTTP_400_BAD_REQUEST)

        if code != 'A1B2C3D4':
            raise PermissionDenied('wrong code for reminder mails')

        email_receiver = 'all'
        email_type = 'reminder'
        if 'type' in request.query_params:
            email_type = request.query_params.get('type', None)

        if 'receiver' in request.query_params:
            email_receiver = request.query_params.get('receiver', None)

        if email_type == 'reminder':
            if email_type == 'reminder':
                if email_receiver == 'unconfirmed':
                    registrations = registrations.filter(is_confirmed=False)
                elif email_receiver == 'confirmed':
                    registrations = registrations.filter(is_confirmed=True)
                elif email_receiver == 'all':
                    registrations = registrations
                else:
                    return Response({'type': f'no valid receiver "{email_receiver}" given'},
                                    status=status.HTTP_400_BAD_REQUEST)

                for registration in registrations:
                    create_reminder_registration(registration)

        elif email_type == 'matching':
            matchings = RegistrationMatching.objects.filter(event=event)
            registation_of_matching = []
            for i in matchings.all():
                for x in i.registrations.all():
                    registation_of_matching.append(x)

            if email_receiver == 'matched':
                registrations = registation_of_matching
            elif email_receiver == 'unmatched':
                registrations = [x for x in registrations if x not in registation_of_matching]
            elif email_receiver == 'all':
                registrations = registrations
            else:
                return Response({'type': f'no valid receiver "{email_receiver}" given'},
                                status=status.HTTP_400_BAD_REQUEST)

            for registration in registrations:
                matching = matchings.filter(registrations__in=[registration]).first()
                create_matching_mail(matching, registration, email_receiver)

        else:
            return Response({'receiver': f'no valid type "{email_type}" given'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'emails sent'}, status=status.HTTP_200_OK)


class WorkshopViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('registration',)


class WorkshopStatsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WorkshopStatsSerializer
    queryset = Workshop.objects.all()
