from django.db.models import QuerySet, Sum, Count, F
from django.utils import timezone
from datetime import datetime
import pytz
from rest_framework import serializers
from django.contrib.auth.models import User
from authentication.serializers import UserExtendedGetSerializer
from basic.models import EatHabit

from basic import models as basic_models
from basic import serializers as basic_serializers
from event import models as event_models
from event import choices as event_choices
from event import permissions as event_permissions


class EventLocationSummarySerializer(serializers.ModelSerializer):
    zip_code = basic_serializers.ZipCodeSerializer(many=False, read_only=True)

    class Meta:
        model = event_models.EventLocation
        fields = '__all__'


class EventLocationSerializer(serializers.ModelSerializer):
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
        read_only=False,
        slug_field='name',
        queryset=event_models.EventPlanerModule.objects.all()
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
    registration_options = serializers.SerializerMethodField()
    location = EventLocationShortSerializer(read_only=True, many=False)
    allow_statistic = serializers.SerializerMethodField()

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
            'registration_options',
            'allow_statistic',
            'icon',
            'theme',
        )

    def get_allow_statistic(self, obj: event_models.Event) -> bool:
        return event_permissions.check_event_permission(obj, self.context['request'].user)

    def get_can_register(self, obj: event_models.Event) -> bool:
        return obj.registration_deadline > timezone.now() >= obj.registration_start

    def get_can_edit(self, obj: event_models.Event) -> bool:
        return obj.last_possible_update >= timezone.now()

    def get_registration_options(self, obj: event_models.Event) -> dict:
        group_id = None
        single_id = None
        allow_new_group_reg = False
        allow_edit_group_reg = False
        allow_new_single_reg = False
        allow_edit_single_reg = False

        existing_group: QuerySet = obj.registration_set. \
            filter(single=False, scout_organisation=self.context['request'].user.userextended.scout_organisation)
        group: QuerySet[event_models.Registration] = existing_group. \
            filter(responsible_persons__in=[self.context['request'].user.id])
        single: QuerySet[event_models.Registration] = obj.registration_set. \
            filter(responsible_persons__in=[self.context['request'].user.id], single=True)

        if existing_group.exists():
            group_id = existing_group.first().id
            allow_edit_group_reg = group.exists() and existing_group.exists() and self.get_can_edit(obj)

        if single.exists():
            single_id = single.first().id
            allow_edit_single_reg = self.get_can_edit(obj) and not allow_edit_group_reg

        no_registration_exists = not group_id and not single_id

        allow_new_group_reg = no_registration_exists and self.get_can_register(
            obj) and obj.group_registration != event_choices.RegistrationTypeGroup.No
        allow_new_single_reg = no_registration_exists and self.get_can_register(
            obj) and obj.single_registration != event_choices.RegistrationTypeGroup.No

        return {
            'group_id': group_id,
            'allow_new_group_reg': allow_new_group_reg,
            'allow_edit_group_reg': allow_edit_group_reg,
            'single_id': single_id,
            'allow_new_single_reg': allow_new_single_reg,
            'allow_edit_single_reg': allow_edit_single_reg
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
    userextended = UserExtendedGetSerializer(many=False, read_only=True)

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
    booking_options = serializers.SerializerMethodField()

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
                  'updated_at',
                  'booking_options',)

    def get_participant_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.count()

    def get_price(self, registration: event_models.Registration) -> float:
        return registration.registrationparticipant_set.aggregate(
            sum=Sum('booking_option__price'))['sum']

    def get_tags(self, registration: event_models.Registration) -> []:
        queryset = registration.tags.filter(in_summary=True)
        serializer = basic_serializers.AbstractAttributeGetPolymorphicSerializer(queryset, many=True)
        return serializer.data

    def get_booking_options(self, registration: event_models.Registration) -> dict:
        return registration.registrationparticipant_set \
            .values(booking_options=F('booking_option__name')) \
            .annotate(sum=Count('booking_option__name')) \
            .annotate(price=Sum('booking_option__price'))


class RegistrationParticipantEventDetailedSummarySerializer(serializers.ModelSerializer):
    booking_option = RegistrationSummaryBookingOptionSerializer(many=False, read_only=True)
    gender = serializers.CharField(source='get_gender_display')
    leader = serializers.CharField(source='get_leader_display')
    needs_confirmation = serializers.CharField(source='get_needs_confirmation_display')

    class Meta:
        model = event_models.RegistrationParticipant
        exclude = ('deactivated', 'generated', 'registration')


class RegistrationEventDetailedSummarySerializer(RegistrationEventSummarySerializer):
    registrationparticipant_set = RegistrationParticipantEventDetailedSummarySerializer(read_only=True, many=True)

    class Meta:
        model = RegistrationEventSummarySerializer.Meta.model
        fields = RegistrationEventSummarySerializer.Meta.fields + ('registrationparticipant_set',)


class EventSummarySerializer(serializers.ModelSerializer):
    registration_set = RegistrationEventSummarySerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    booking_options = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    age_groups = serializers.SerializerMethodField()
    location = EventLocationSummarySerializer(many=False, read_only=True)

    class Meta:
        model = event_models.Event
        fields = (
            'participant_count',
            'price',
            'registration_set',
            'booking_options',
            'age_groups',
            'location'
        )

    def get_participant_count(self, event: event_models.Event) -> int:
        return event.registration_set.filter(is_confirmed=True).aggregate(count=Count('registrationparticipant'))[
            'count']

    def get_booking_options(self, event: event_models.Event) -> dict:
        return event.registration_set.filter(is_confirmed=True) \
            .values(booking_option=F('registrationparticipant__booking_option__name')) \
            .annotate(count=Count('registrationparticipant')) \
            .annotate(price=Sum('registrationparticipant__booking_option__price'))

    def get_price(self, event: event_models.Event) -> float:
        return event.registration_set.filter(is_confirmed=True) \
            .aggregate(sum=Sum('registrationparticipant__booking_option__price'))['sum']

    def get_age_groups(self, event: event_models.Event) -> dict:
        """
            0-10 Wölfling
            11-16 Pfadfinder
            17-23 Rover
            23+ Altrover
        """
        participant_ids = event.registration_set.filter(is_confirmed=True).values('registrationparticipant')
        all_participants = event_models.RegistrationParticipant.objects.filter(id__in=participant_ids)
        woelfling = self.age_range(0, 10, all_participants)
        pfadfinder = self.age_range(11, 16, all_participants)
        rover = self.age_range(17, 23, all_participants)
        alt_rover = self.age_range(24, 999, all_participants)

        return {
            'woelfling': woelfling,
            'pfadfinder': pfadfinder,
            'rover': rover,
            'alt_rover': alt_rover
        }

    def age_range(self, min_age, max_age, participants: QuerySet[event_models.RegistrationParticipant]) -> int:
        current = timezone.now().date()
        min_date = datetime(current.year - min_age, current.month, current.day, tzinfo=pytz.timezone('Europe/Berlin'))
        max_date = datetime(current.year - max_age, current.month, current.day, tzinfo=pytz.timezone('Europe/Berlin'))

        return participants.filter(birthday__gte=max_date, birthday__lte=min_date).count()


class EventDetailedSummarySerializer(EventSummarySerializer):
    registration_set = RegistrationEventDetailedSummarySerializer(many=True, read_only=True)


class EventAttributeSummarySerializer(serializers.ModelSerializer):
    attribute = basic_serializers.AbstractAttributeGetPolymorphicSerializer(many=False, read_only=False)
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = event_models.AttributeEventModuleMapper
        fields = '__all__'

    def get_attributes(self, mapper: event_models.AttributeEventModuleMapper) -> dict:
        event_id = self.context['view'].kwargs.get("event_pk", None)
        registration_tag_ids: QuerySet[int] = event_models.Registration.objects.filter(event=event_id) \
            .values_list('tags', flat=True)
        tags: QuerySet[basic_models.AbstractAttribute] = basic_models.AbstractAttribute.objects \
            .filter(id__in=registration_tag_ids, in_summary=True, template=False, template_id=mapper.attribute.id)

        attribute_sum = 0
        if mapper.attribute.polymorphic_ctype.app_labeled_name == 'basic | integer attribute':
            attribute_sum = tags.aggregate(sum=Sum('integerattribute__integer_field'))['sum']
        elif mapper.attribute.polymorphic_ctype.app_labeled_name == 'basic | float attribute':
            attribute_sum = tags.aggregate(sum=Sum('floatattribute__integer_field'))['sum']

        serializer = basic_serializers.AbstractAttributeGetPolymorphicSerializer(tags, many=True)
        return {
            'data': serializer.data,
            'sum': attribute_sum
        }


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.Workshop
        fields = '__all__'


class WorkshopEventSummarySerializer(serializers.ModelSerializer):
    supervisor = CurrentUserSerializer(many=False, read_only=True)

    class Meta:
        model = event_models.Workshop
        fields = '__all__'
