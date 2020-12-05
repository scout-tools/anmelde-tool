# serializers.py
from rest_framework import serializers
from .models import Event, AgeGroup, EventLocation, EventContact


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'location',
            'ageGroups',
            'contact',
            'startTime,'
            'endTime',
            'registrationDeadline',
            'participationFee',
        )


class AgeGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AgeGroup
        fields = (
            'id',
            'name',
            'description',
        )


class EventLocationSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = EventLocation
        fields = (
            'id',
            'name',
            'description',
            'city',
            'zipCode',
            'address',
        )


class EventContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = EventContact
        fields = (
            'id',
            'name',
            'emailAddress',
        )
