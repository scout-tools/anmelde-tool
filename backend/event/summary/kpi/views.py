from django.db.models import QuerySet, Count
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from event import models as event_models
from event import permissions as event_permissions
from event.summary.kpi import serializers as kpi_serializers


class TotalParticipantsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsSubEventResponsiblePerson]

    def list(self, request, *args, **kwargs) -> Response:
        registrations: QuerySet[event_models.Registration] = self.get_queryset()
        num = registrations.aggregate(count=Count('registrationparticipant'))['count'] or 0

        return Response(num, status=status.HTTP_200_OK)

    def get_queryset(self) -> QuerySet[event_models.Registration]:
        event_id = self.kwargs.get("event_pk", None)

        registrations = event_models.Registration.objects.filter(event=event_id, is_confirmed=True)

        return registrations


class TotalRegistrationsViewSet(TotalParticipantsViewSet):
    def list(self, request, *args, **kwargs) -> Response:
        registrations: QuerySet[event_models.Registration] = self.get_queryset()
        num = registrations.count() or 0

        return Response(num, status=status.HTTP_200_OK)


class LastRegistrationsViewSet(TotalParticipantsViewSet):
    def list(self, request, *args, **kwargs) -> Response:
        registrations: QuerySet[event_models.Registration] = self.get_queryset()
        registrations = registrations.annotate(count=Count('registrationparticipant')).order_by('-created_at')
        result = registrations[:5]

        serializer = kpi_serializers.RegistrationEventKPISerializer(result, many=True, read_only=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LargestRegistrationsViewSet(TotalParticipantsViewSet):
    def list(self, request, *args, **kwargs) -> Response:
        registrations: QuerySet[event_models.Registration] = self.get_queryset()
        registrations = registrations.annotate(count=Count('registrationparticipant')).order_by('-count')
        result = registrations[:5]

        serializer = kpi_serializers.RegistrationEventKPISerializer(result, many=True, read_only=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingOptionViewSet(TotalParticipantsViewSet):
    def list(self, request, *args, **kwargs) -> Response:
        registrations: QuerySet[event_models.Registration] = self.get_queryset()
        booking_option = self.request.query_params.get('booking-option')

        reg_ids = registrations.values('id')
        result = event_models.RegistrationParticipant.objects.filter(registration__in=reg_ids,
                                                                     booking_option=booking_option).count()

        return Response(result, status=status.HTTP_200_OK)
