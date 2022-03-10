from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.models import UserExtended
from authentication.serializers import UserExtendedShortSerializer
from basic.serializers import TagShortSerializer, ZipCodeSerializer, AbstractAttributePolymorphicSerializer, \
    ZipCodeShortSerializer
from .models import Event, EventLocation, BookingOption, EventModuleMapper, EventModule, AttributeEventModuleMapper, \
    RegistrationTypeGroup, RegistrationTypeSingle, Registration, RegistrationParticipant


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
                  'short_description',
                  'long_description',
                  'location',
                  'start_time',
                  'end_time',
                  'registration_deadline',
                  'registration_start',
                  'last_possible_update',
                  'tags',
                  'registration_model',
                  'cloud_link')


class BookingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingOption
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


class EventLocationShortSerializer(serializers.ModelSerializer):
    zip_code = ZipCodeShortSerializer(many=False, read_only=True)

    class Meta:
        model = EventLocation
        fields = ('name', 'zip_code', 'address')


class EventOverviewSerializer(serializers.ModelSerializer):
    can_register = serializers.SerializerMethodField('get_can_register')
    can_edit = serializers.SerializerMethodField('get_can_edit')
    registration = serializers.SerializerMethodField('get_registration')
    location = EventLocationShortSerializer(read_only=True, many=False)

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'short_description',
            'long_description',
            'location',
            'start_time',
            'end_time',
            'registration_deadline',
            'registration_start',
            'last_possible_update',
            'tags',
            'can_register',
            'can_edit',
            'registration'
        )

    def get_can_register(self, obj: Event):
        return obj.registration_deadline >= timezone.now() >= obj.registration_start

    def get_can_edit(self, obj: Event):
        return obj.last_possible_update >= timezone.now()

    def get_registration(self, obj: Event):
        group_id = None
        single_id = None
        group_possible = False
        single_possible = False

        registration = obj.registration_set.filter(
            scout_organisation=self.context['request'].user.userextended.scout_organisation)
        if registration.exists() > 0:
            existing_group: QuerySet = registration.filter(single=False)
            group: QuerySet = existing_group.filter(responsible_persons__in=[self.context['request'].user.id])
            single: QuerySet = registration.filter(responsible_persons__in=[self.context['request'].user.id],
                                                   single=True)

            if existing_group.exists():
                group_id = existing_group.first().id

            if single.exists():
                single_id = single.first().id

        if obj.group_registration != RegistrationTypeGroup.No:
            if group_id:
                group_possible = group.exists() and existing_group.exists() \
                    if group is not None and existing_group is not None else False
            else:
                group_possible = True
        if obj.single_registration != RegistrationTypeSingle.No:
            if obj.group_registration == RegistrationTypeGroup.Required:
                if group_id is None:
                    single_possible = True
            else:
                single_possible = True
        return {
            'group_id': group_id,
            'single_id': single_id,
            'group_possible': group_possible,
            'single_possible': single_possible
        }


class RegistrationPostSerializer(serializers.Serializer):
    event_code = serializers.CharField(required=True)
    single = serializers.BooleanField(required=True)
    event = serializers.IntegerField(required=True)


class RegistrationPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('responsible_persons', 'is_confirmed', 'tags')
        extra_kwargs = {"responsible_persons": {"required": False, "allow_null": True}}


class CurrentUserSerializer(serializers.ModelSerializer):
    userextended = UserExtendedShortSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'userextended')


class RegistrationGetSerializer(serializers.ModelSerializer):
    responsible_persons = CurrentUserSerializer(many=True, read_only=True)
    tags = TagShortSerializer(many=True, read_only=True)

    class Meta:
        model = Registration
        fields = '__all__'


class RegistrationParticipantShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationParticipant
        fields = ('scout_name', 'first_name', 'last_name')
