from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.serializers import UserExtendedShortSerializer
from basic.models import EatHabit
from basic.serializers import TagShortSerializer, ZipCodeSerializer, AbstractAttributeGetPolymorphicSerializer, \
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
                  'start_date',
                  'end_date',
                  'registration_deadline',
                  'registration_start',
                  'last_possible_update',
                  'tags',
                  'cloud_link',
                  'personal_data_required')


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
            'attributes',
            'event',
            'overwrite_description',
            'ordering'
        )
        optional_fields = ('module',)


class EventModuleMapperPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventModuleMapper
        fields = (
            'attributes',
            'overwrite_description',
            'ordering'
        )


class EventCompleteSerializer(serializers.ModelSerializer):
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )

    event_planer_modules = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
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
    attribute = AbstractAttributeGetPolymorphicSerializer(many=False, read_only=False)

    class Meta:
        model = AttributeEventModuleMapper
        fields = '__all__'


class AttributeEventModuleMapperPostSerializer(serializers.ModelSerializer):
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
            'start_date',
            'end_date',
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

        existing_group: QuerySet = obj.registration_set. \
            filter(single=False, scout_organisation=self.context['request'].user.userextended.scout_organisation)
        group: QuerySet = existing_group.filter(responsible_persons__in=[self.context['request'].user.id])
        single: QuerySet = obj.registration_set.filter(responsible_persons__in=[self.context['request'].user.id],
                                                       single=True)

        if existing_group.exists():
            group_id = existing_group.first().id

        if single.exists():
            single_id = single.first().id

        if obj.group_registration != RegistrationTypeGroup.No:
            if group_id:
                group_possible = group.exists() and existing_group.exists() \
                    if group is not None and existing_group is not None else False
            elif single_id is None:
                group_possible = True

        if obj.single_registration != RegistrationTypeSingle.No:
            if obj.group_registration == RegistrationTypeGroup.Required:
                if group_id is not None:
                    single_possible = True
            elif group_id is None:
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
    event = serializers.UUIDField(required=True)


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
        fields = ('id', 'scout_name', 'first_name', 'last_name')


class RegistrationParticipantSerializer(serializers.ModelSerializer):
    eat_habit = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=EatHabit.objects.all(),
        required=False
    )

    class Meta:
        model = RegistrationParticipant
        fields = '__all__'


class RegistrationParticipantPutSerializer(serializers.ModelSerializer):
    avoid_manual_check = serializers.BooleanField(required=False, default=False)
    activate = serializers.BooleanField(required=False, default=False)
    eat_habit = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=EatHabit.objects.all(),
        required=False
    )

    class Meta:
        model = RegistrationParticipant
        exclude = ('deactivated', 'generated', 'registration', 'needs_confirmation')


class RegistrationParticipantGroupSerializer(serializers.Serializer):
    number = serializers.CharField(required=True)
    avoid_manual_check = serializers.BooleanField(required=False, default=False)
