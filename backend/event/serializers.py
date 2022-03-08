from django.utils import timezone
from rest_framework import serializers

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
                  'start_date',
                  'end_date',
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


class EventModuleMapperPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModuleMapper
        fields = (
            'module',
            'attributes',
            'event',
            'overwrite_description',
            'ordering'
        )


class EventCompleteSerializer(serializers.ModelSerializer):
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )

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


class EventOverviewSerializer(serializers.ModelSerializer):
    can_register = serializers.SerializerMethodField('get_can_register')
    can_edit = serializers.SerializerMethodField('get_can_edit')
    registration_modes = serializers.SerializerMethodField('get_registration_modes')

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'location',
            'start_date',
            'end_date',
            'registration_deadline',
            'registration_start',
            'last_possible_update',
            'tags',
            'single_registration',
            'group_registration',
            'personal_data_required',
            'can_register',
            'can_edit',
            'registration_modes'
        )

    def get_can_register(self, obj: Event):
        return obj.registration_deadline >= timezone.now()

    def get_can_edit(self, obj: Event):
        return obj.last_possible_update >= timezone.now()

    def get_registration_modes(self, obj: Event):
        registration = obj.registration_set.filter(
            scout_hierachy=self.context['request'].user.userextended.scout_organisation)
        if len(registration) > 0:
            group_registration = registration.filter(responsible_persons__in=[self.context['request'].user.id],
                                                     personal=False)
            single_registration = registration.filter(responsible_persons__in=[self.context['request'].user.id],
                                                      personal=True)

            return {
                'group': group_registration,
                'single': single_registration,
            }
        else:
            return {
                'group': None,
                'single': None
            }
