from rest_framework import serializers

from basic import serializers as basic_serializers
from event import models as event_models


class RegistrationEventKPISerializer(serializers.ModelSerializer):
    scout_organisation = basic_serializers.ScoutHierarchyDetailedSerializer(many=False, read_only=True)
    count = serializers.IntegerField()

    class Meta:
        model = event_models.Registration
        fields = (
            'is_confirmed',
            'is_accepted',
            'single',
            'scout_organisation',
            'created_at',
            'updated_at',
            'count'
        )
