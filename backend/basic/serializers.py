# serializers.py
from rest_framework import serializers
from rest_framework.fields import Field

from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, Participants


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'


class AgeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = '__all__'


class EventLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = EventLocation
        fields = '__all__'


class ScoutHierarchySerializer(serializers.ModelSerializer):

    class Meta:
        model = ScoutHierarchy
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = '__all__'


class ZipCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ZipCode
        fields = '__all__'


class ParticipantsSerializer(serializers.ModelSerializer):
    lon = serializers.SerializerMethodField('get_lon')
    lat = serializers.SerializerMethodField('get_lat')
    name = serializers.SerializerMethodField('get_name')
    bund = serializers.SerializerMethodField('get_bund')

    def get_bund_name(self, scout_organisation):
        if scout_organisation.level_id > 3:
            return self.get_bund_name(scout_organisation.parent)
        elif scout_organisation.level_id < 3:
            raise Exception("To low value")
        else:
            return scout_organisation.name

    def get_lon(self, par: Participants):
        if par.registration.scout_organisation.zip_code is not None:
            lon = par.registration.scout_organisation.zip_code.lon
        else:
            lon = 10.451526
        return lon

    def get_lat(self, par: Participants):
        if par.registration.scout_organisation.zip_code is not None:
            lat = par.registration.scout_organisation.zip_code.lat
        else:
            lat = 51.165691
        return lat

    def get_bund(self, par: Participants):
        return self.get_bund_name(par.registration.scout_organisation)

    def get_name(self, par: Participants):
        return par.registration.scout_organisation.name

    class Meta:
        model = Participants
        fields = '__all__'
