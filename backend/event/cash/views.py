from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from email_services.services import send_payment_reminder_mail
from event.cash import permissions as cash_permissions
from event import permissions as event_permissions
from event.cash import serializers as cash_serializers
from event.cash import models as cash_models


class CashIncomeViewSet(mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [cash_permissions.IsCashResponsiblePerson]
    serializer_class = cash_serializers.CashIncomeSerializer
    queryset = cash_models.CashIncome.objects.all()


class MailReminderViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [event_permissions.IsStaffOrReadOnly]
    serializer_class = cash_serializers.MailReminderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event_id = serializer.data['event_id']
        send_payment_reminder_mail(event_id)
        return Response(serializer.data, status=status.HTTP_200_OK)
