# serializers.py
from rest_framework import serializers
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

    class Meta:
        model = Participants
        fields = '__all__'
