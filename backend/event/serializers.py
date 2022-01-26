from rest_framework import serializers

from basic.serializers import TagShortSerializer, ZipCodeSerializer
from .models import Event, EventLocation, SleepingLocation


class EventLocationGetSerializer(serializers.ModelSerializer):
    zip_code = ZipCodeSerializer(many=False, read_only=True)

    class Meta:
        model = EventLocation
        fields = '__all__'


class EventLocationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id',
                  'name',
                  'description',
                  'location',
                  'start_time',
                  'end_time',
                  'registration_deadline',
                  'registration_start',
                  'last_possible_update',
                  'price',
                  'tags',
                  'registration_model')


class SleepingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepingLocation
        fields = '__all__'


class EventCompleteSerializer(serializers.ModelSerializer):
    # sleepinglocation_set = SleepingLocationSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventPlanerSerializer(serializers.ModelSerializer):
    tags = TagShortSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
