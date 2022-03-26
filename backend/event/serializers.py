from django.db.models import QuerySet, Sum, Count
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.serializers import UserExtendedShortSerializer
from basic.models import EatHabit

from basic import serializers as basic_serializers
from event import models as event_models
from event import choices as event_choices


class EventLocationGetSerializer(serializers.ModelSerializer):
    zip_code = basic_serializers.ZipCodeSerializer(many=False, read_only=True)

    class Meta:
        model = event_models.EventLocation
        fields = '__all__'


class EventLocationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.EventLocation
        fields = '__all__'


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.Event
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
        model = event_models.BookingOption
        fields = '__all__'


class EventModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.EventModule
        fields = '__all__'


class EventModuleShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.EventModule
        fields = ('header', 'name')


class EventModuleMapperShortSerializer(serializers.ModelSerializer):
    module = EventModuleShortSerializer(read_only=True)

    class Meta:
        model = event_models.EventModuleMapper
        fields = ('ordering', 'module', 'required')


class EventModuleMapperGetSerializer(serializers.ModelSerializer):
    module = EventModuleSerializer(read_only=True)

    class Meta:
        model = event_models.EventModuleMapper
        fields = '__all__'


class EventModuleMapperSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.EventModuleMapper
        fields = '__all__'


class EventModuleMapperPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.EventModuleMapper
        fields = (
            'attributes',
            'event',
            'overwrite_description',
            'ordering'
        )
        optional_fields = ('module',)


class EventModuleMapperPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.EventModuleMapper
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
        model = event_models.Event
        fields = '__all__'


class EventPlanerSerializer(serializers.ModelSerializer):
    tags = basic_serializers.TagShortSerializer(many=True)
    eventmodulemapper_set = EventModuleMapperShortSerializer(many=True, read_only=True)

    class Meta:
        model = event_models.Event
        fields = '__all__'


class AttributeEventModuleMapperSerializer(serializers.ModelSerializer):
    attribute = basic_serializers.AbstractAttributeGetPolymorphicSerializer(many=False, read_only=False)

    class Meta:
        model = event_models.AttributeEventModuleMapper
        fields = '__all__'


class AttributeEventModuleMapperPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.AttributeEventModuleMapper
        fields = '__all__'


class EventLocationShortSerializer(serializers.ModelSerializer):
    zip_code = basic_serializers.ZipCodeShortSerializer(many=False, read_only=True)

    class Meta:
        model = event_models.EventLocation
        fields = ('name', 'zip_code', 'address')


class EventOverviewSerializer(serializers.ModelSerializer):
    can_register = serializers.SerializerMethodField('get_can_register')
    can_edit = serializers.SerializerMethodField('get_can_edit')
    registration = serializers.SerializerMethodField('get_registration')
    location = EventLocationShortSerializer(read_only=True, many=False)

    class Meta:
        model = event_models.Event
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

    def get_can_register(self, obj: event_models.Event) -> bool:
        return obj.registration_deadline >= timezone.now() >= obj.registration_start

    def get_can_edit(self, obj: event_models.Event) -> bool:
        return obj.last_possible_update >= timezone.now()

    def get_registration(self, obj: event_models.Event) -> dict:
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

        if obj.group_registration != event_choices.RegistrationTypeGroup.No:
            if group_id:
                group_possible = group.exists() and existing_group.exists() \
                    if group is not None and existing_group is not None else False
            elif single_id is None:
                group_possible = True

        if obj.single_registration != event_choices.RegistrationTypeSingle.No:
            if obj.group_registration == event_choices.RegistrationTypeGroup.Required:
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
        model = event_models.Registration
        fields = ('responsible_persons', 'is_confirmed', 'tags')
        extra_kwargs = {"responsible_persons": {"required": False, "allow_null": True}}


class CurrentUserSerializer(serializers.ModelSerializer):
    userextended = UserExtendedShortSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'userextended')


class RegistrationGetSerializer(serializers.ModelSerializer):
    responsible_persons = CurrentUserSerializer(many=True, read_only=True)
    tags = basic_serializers.TagShortSerializer(many=True, read_only=True)

    class Meta:
        model = event_models.Registration
        fields = '__all__'


class RegistrationParticipantShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.RegistrationParticipant
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
        model = event_models.RegistrationParticipant
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
        model = event_models.RegistrationParticipant
        exclude = ('deactivated', 'generated', 'registration', 'needs_confirmation')


class RegistrationParticipantGroupSerializer(serializers.Serializer):
    number = serializers.CharField(required=True)
    avoid_manual_check = serializers.BooleanField(required=False, default=False)


class RegistrationSummaryBookingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.BookingOption
        fields = ('name', 'price')


class RegistrationSummaryParticipantSerializer(serializers.ModelSerializer):
    booking_option = RegistrationSummaryBookingOptionSerializer(many=False, read_only=True)

    class Meta:
        model = event_models.RegistrationParticipant
        fields = ('first_name', 'last_name', 'scout_name', 'deactivated', 'booking_option')


class RegistrationSummarySerializer(serializers.ModelSerializer):
    registrationparticipant_set = RegistrationSummaryParticipantSerializer(many=True, read_only=True)
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )
    participant_count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = event_models.Registration
        fields = ('is_confirmed',
                  'is_accepted',
                  'responsible_persons',
                  'participant_count',
                  'price',
                  'registrationparticipant_set',
                  'tags'
                  )

    def get_participant_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.count()

    def get_price(self, registration: event_models.Registration) -> float:
        return registration.registrationparticipant_set.aggregate(
            sum=Sum('booking_option__price'))['sum']

    def get_tags(self, registration: event_models.Registration) -> []:
        queryset = registration.tags.filter(in_summary=True)
        serializer = basic_serializers.AbstractAttributeGetPolymorphicSerializer(queryset, many=True)
        return serializer.data


class RegistrationEventSummarySerializer(serializers.ModelSerializer):
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )
    participant_count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    scout_organisation = basic_serializers.ScoutHierarchyDetailedSerializer(many=False, read_only=True)

    class Meta:
        model = event_models.Registration
        fields = ('is_confirmed',
                  'is_accepted',
                  'single',
                  'scout_organisation',
                  'responsible_persons',
                  'tags',
                  'participant_count',
                  'price',
                  'created_at',
                  'updated_at')

    def get_participant_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.count()

    def get_price(self, registration: event_models.Registration) -> float:
        return registration.registrationparticipant_set.aggregate(
            sum=Sum('booking_option__price'))['sum']

    def get_tags(self, registration: event_models.Registration) -> []:
        queryset = registration.tags.filter(in_summary=True)
        serializer = basic_serializers.AbstractAttributeGetPolymorphicSerializer(queryset, many=True)
        return serializer.data


class EventSummarySerializer(serializers.ModelSerializer):
    registration_set = RegistrationEventSummarySerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = event_models.Event
        fields = ('participant_count', 'price', 'registration_set')

    def get_participant_count(self, event: event_models.Event) -> int:
        return event.registration_set.aggregate(count=Count('registrationparticipant'))['count']

    def get_price(self, event: event_models.Event) -> float:
        return event.registration_set.aggregate(sum=Sum('registrationparticipant__booking_option__price'))['sum']
