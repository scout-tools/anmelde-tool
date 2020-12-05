# serializers.py
from rest_framework import serializers
from .models import Event, AgeGroup


class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
        )


class AgeGroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AgeGroup
        fields = (
            'id',
            'name',
            'description',
        )
