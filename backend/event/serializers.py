from rest_framework import serializers
from rest_framework.authtoken.admin import User

from basic.serializers import TagShortSerializer, ZipCodeSerializer, AbstractAttributePolymorphicSerializer
from .models import Event, EventLocation, SleepingLocation, EventModuleMapper, EventModule, AttributeEventModuleMapper


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
                  'tags',
                  'registration_model')


class SleepingLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SleepingLocation
        fields = '__all__'


class EventModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModule
        fields = '__all__'


class EventModuleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModule
        fields = ('header', 'name')


class EventModuleMapperShortSerializer(serializers.ModelSerializer):
    module = EventModuleShortSerializer(read_only=True)

    class Meta:
        model = EventModuleMapper
        fields = ('ordering', 'module', 'required')


class EventModuleMapperGetSerializer(serializers.ModelSerializer):
    module = EventModuleSerializer(read_only=True)

    class Meta:
        model = EventModuleMapper
        fields = '__all__'


class EventModuleMapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModuleMapper
        fields = '__all__'


class EventCompleteSerializer(serializers.ModelSerializer):
    eventmodulemapper_set = EventModuleMapperGetSerializer(many=True, read_only=True)
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )

    # tags = TagShortSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class EventPlanerSerializer(serializers.ModelSerializer):
    tags = TagShortSerializer(many=True)
    eventmodulemapper_set = EventModuleMapperShortSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = '__all__'


class AttributeEventModuleMapperSerializer(serializers.ModelSerializer):
    attribute = AbstractAttributePolymorphicSerializer(many=False, read_only=True)

    class Meta:
        model = AttributeEventModuleMapper
        fields = '__all__'
