from rest_framework import serializers
from event.cash import models as cash_models


class CashIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = cash_models.CashIncome
        fields = '__all__'
