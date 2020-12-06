# serializers.py
from rest_framework import serializers
from .models import Event, AgeGroup, EventLocation, Person, ScoutHerarchy, Registration


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'location',
            'ageGroups',
            'contact',
            'startTime',
            'endTime',
            'registrationDeadline',
            'participationFee',
        )


class AgeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = AgeGroup
        fields = (
            'id',
            'name',
            'description',
        )


class EventLocationSerializer(serializers.ModelSerializer):

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


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = (
            'id',
            'name',
            'emailAddress',
            'scoutOrganisation',
            'mobileNumber'
        )


class ScoutHerarchySerializer(serializers.ModelSerializer):

    class Meta:
        model = ScoutHerarchy
        fields = (
            'id',
            'level',
            'name',
            'city',
            'zipCode',
            'parent'
        )


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Registration
        fields = (
            'id',
            'scoutOrganisation',
            'numberOfParticipants',
            'responsiblePerson'
        )
