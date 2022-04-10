from django.contrib.auth.models import Group

from basic.models import ScoutHierarchy
from rest_framework import serializers
from .models import UserExtended


class UserExtendedScoutHierarchySerializer(serializers.ModelSerializer): #

    bund = serializers.SerializerMethodField()

    class Meta:
        model = ScoutHierarchy
        fields = ('id', 'name', 'parent', 'zip_code', 'bund')

    def get_bund(self, obj: ScoutHierarchy) -> str:
        iterator: ScoutHierarchy = obj
        while iterator is not None:
            if iterator.level.name == 'Bund':
                return iterator.name
            iterator = iterator.parent

    


class UserExtendedShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = (
            'mobile_number',
            'scout_name',
        )


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


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name',)


class EmailSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = ('email_notifaction', 'sms_notifcation')
