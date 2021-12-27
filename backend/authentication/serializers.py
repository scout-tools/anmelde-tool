from basic.models import ScoutHierarchy
from rest_framework import serializers
from .models import UserExtended


class UserExtendedScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutHierarchy
        fields = ('id', 'name', 'parent', 'zip_code')


class UserExtendedGetSerializer(serializers.ModelSerializer):
    scout_organisation = UserExtendedScoutHierarchySerializer()

    class Meta:
        model = UserExtended
        fields = (
            'mobile_number',
            'scout_name',
            'scout_organisation',
            'dsgvo_confirmed'
        )


class UserExtendedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = (
            'mobile_number',
            'scout_name',
            'scout_organisation',
            'dsgvo_confirmed'
        )
