from rest_framework import serializers

from basic.serializers import TagShortSerializer, ZipCodeSerializer
from .models import Event, EventLocation


class EventLocationSerializer(serializers.ModelSerializer):
    zip_code = ZipCodeSerializer(many=False)

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


class EventCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventPlanerSerializer(serializers.ModelSerializer):
    tags = TagShortSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
