from rest_framework import mixins, viewsets

from event.cash import permissions as cash_permissions
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
