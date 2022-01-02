from rest_framework import serializers
from .models import Event, EventLocation


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventPlanerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
