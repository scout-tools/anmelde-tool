# serializers.py
from rest_framework import serializers
from .models import Event, AgeGroup, EventLocation, ScoutHerarchy, Registration, ZipCode


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


class ScoutHerarchySerializer(serializers.ModelSerializer):

    class Meta:
        model = ScoutHerarchy
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = '__all__'


class ZipCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ZipCode
        fields = '__all__'
