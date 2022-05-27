from django.db.models import QuerySet, Sum, Count, F
from datetime import datetime
import pytz
from rest_framework import serializers
from django.contrib.auth.models import User

from basic import serializers as basic_serializers
from basic.models import EatHabit
from event import models as event_models
from event import serializers as event_serializer
from event.registration import serializers as registration_serializers
from event.cash import serializers as cash_serializers
from event.summary import serializers as summary_serializers


class WorkshopEventSummarySerializer(serializers.ModelSerializer):
    supervisor = registration_serializers.CurrentUserSerializer(
        many=False, read_only=True)

    class Meta:
        model = event_models.Workshop
        fields = '__all__'


class RegistrationEventSummarySerializer(serializers.ModelSerializer):
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )
    participant_count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    scout_organisation = basic_serializers.ScoutHierarchyDetailedSerializer(
        many=False, read_only=True)
    booking_options = serializers.SerializerMethodField()

    class Meta:
        model = event_models.Registration
        fields = (
            'id',
            'is_confirmed',
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
        booking_option_list = self.context['request'].query_params.getlist(
            'booking-option')
        queryset = registration.registrationparticipant_set

        if booking_option_list:
            queryset = queryset.filter(booking_option__in=booking_option_list)

        return queryset.count()

    def get_price(self, registration: event_models.Registration) -> float:
        return registration.registrationparticipant_set.aggregate(
            sum=Sum('booking_option__price'))['sum']

    def get_tags(self, registration: event_models.Registration) -> []:
        queryset = registration.tags.filter(in_summary=True)
        serializer = basic_serializers.AbstractAttributeGetPolymorphicSerializer(
            queryset, many=True)
        return serializer.data

    def get_booking_options(self, registration: event_models.Registration) -> dict:
        return registration.registrationparticipant_set \
            .values(booking_options=F('booking_option__name')) \
            .annotate(sum=Count('booking_option__name')) \
            .annotate(price=Sum('booking_option__price'))


class RegistrationParticipantEventDetailedSummarySerializer(serializers.ModelSerializer):
    booking_option = registration_serializers.RegistrationSummaryBookingOptionSerializer(
        many=False, read_only=True)
    registration = summary_serializers.RegistrationEventSummarySerializer(
        many=False, read_only=True)
    gender = serializers.CharField(source='get_gender_display')
    leader = serializers.CharField(source='get_leader_display')
    zip_code = basic_serializers.ZipCodeSerializer(many=False, read_only=True)
    eat_habit = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=EatHabit.objects.all(),
        required=False
    )
    needs_confirmation = serializers.CharField(
        source='get_needs_confirmation_display')

    class Meta:
        model = event_models.RegistrationParticipant
        exclude = ('deactivated', 'generated')


class RegistrationEventDetailedSummarySerializer(RegistrationEventSummarySerializer):
    registrationparticipant_set = RegistrationParticipantEventDetailedSummarySerializer(
        read_only=True, many=True)

    class Meta:
        model = RegistrationEventSummarySerializer.Meta.model
        fields = RegistrationEventSummarySerializer.Meta.fields + \
                 ('registrationparticipant_set',)


class EventSummarySerializer(serializers.ModelSerializer):
    registration_set = RegistrationEventSummarySerializer(
        many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    booking_options = serializers.SerializerMethodField()
    age_groups = serializers.SerializerMethodField()
    location = event_serializer.EventLocationSummarySerializer(
        many=False, read_only=True)

    class Meta:
        model = event_models.Event
        fields = (
            'id',
            'participant_count',
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

    def get_age_groups(self, event: event_models.Event) -> dict:
        """
            0-10 Wölfling
            11-16 Pfadfinder
            17-23 Rover
            23+ Altrover
        """
        participant_ids = event.registration_set.filter(
            is_confirmed=True).values('registrationparticipant')
        all_participants = event_models.RegistrationParticipant.objects.filter(
            id__in=participant_ids)
        booking_option_list = self.context['request'].query_params.getlist(
            'booking-option')

        if booking_option_list:
            all_participants = all_participants.filter(
                booking_option__in=booking_option_list)

        woelfling = self.age_range(0, 12, all_participants, event)
        pfadfinder = self.age_range(12, 17, all_participants, event)
        rover = self.age_range(17, 24, all_participants, event)
        alt_rover = self.age_range(24, 999, all_participants, event)

        return {
            'woelfling': woelfling,
            'pfadfinder': pfadfinder,
            'rover': rover,
            'alt_rover': alt_rover
        }

    def age_range(self, min_age, max_age, participants: QuerySet[event_models.RegistrationParticipant],
                  event: event_models.Event) -> int:
        min_date = datetime(event.start_date.year - min_age, event.start_date.month, event.start_date.day,
                            tzinfo=pytz.timezone('Europe/Berlin'))
        max_date = datetime(event.start_date.year - max_age, event.start_date.month, event.start_date.day,
                            tzinfo=pytz.timezone('Europe/Berlin'))

        return participants.filter(birthday__gte=max_date, birthday__lte=min_date).count()


class EventDetailedSummarySerializer(EventSummarySerializer):
    registration_set = RegistrationEventDetailedSummarySerializer(
        many=True, read_only=True)


class RegistrationAttributeGetSerializer(serializers.ModelSerializer):
    scout_organisation = basic_serializers.NamyOnlyScoutHierarchySerializer(
        many=False, read_only=True)
    responsible_persons = registration_serializers.CurrentUserSerializer(
        many=True, read_only=True)

    class Meta:
        model = event_models.Registration
        fields = ('scout_organisation', 'is_confirmed',
                  'is_accepted', 'responsible_persons')


class EventAttributeSummarySerializer(serializers.ModelSerializer):
    attribute = basic_serializers.AbstractAttributeGetPolymorphicSerializer(
        many=False, read_only=False)
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = event_models.AttributeEventModuleMapper
        fields = '__all__'

    def get_attributes(self, mapper: event_models.AttributeEventModuleMapper) -> dict:
        event_id = self.context['view'].kwargs.get("event_pk", None)
        registrations: QuerySet[event_models.Registration] = event_models.Registration.objects.filter(
            event=event_id)

        registration_tags = []
        attribute_sum = 0
        for registration in registrations.all():
            tags = registration.tags.filter(
                template=False, template_id=mapper.attribute.id)

            if mapper.attribute.polymorphic_ctype.app_labeled_name == 'basic | integer attribute':
                attribute_sum += tags.aggregate(
                    sum=Sum('integerattribute__integer_field'))['sum'] or 0
            elif mapper.attribute.polymorphic_ctype.app_labeled_name == 'basic | float attribute':
                attribute_sum += tags.aggregate(
                    sum=Sum('floatattribute__integer_field'))['sum'] or 0

            serialized_registration = RegistrationAttributeGetSerializer(
                registration, many=False).data
            for tag in tags.all():
                serialized_tag = basic_serializers.AbstractAttributeGetPolymorphicSerializer(
                    tag, many=False).data
                result = {
                    'registration': serialized_registration,
                    'tag': serialized_tag,
                }
                registration_tags.append(result)

        return {
            'data': registration_tags,
            'sum': attribute_sum
        }


class RegistrationCashSummarySerializer(serializers.ModelSerializer):
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )
    participant_count = serializers.SerializerMethodField()
    payement = serializers.SerializerMethodField()
    scout_organisation = basic_serializers.ScoutHierarchyDetailedSerializer(
        many=False, read_only=True)
    booking_options = serializers.SerializerMethodField()
    cashincome_set = cash_serializers.CashIncomeSerializer(
        many=True, read_only=True)

    class Meta:
        model = event_models.Registration
        fields = ('id',
                  'is_confirmed',
                  'is_accepted',
                  'single',
                  'scout_organisation',
                  'responsible_persons',
                  'participant_count',
                  'payement',
                  'created_at',
                  'updated_at',
                  'booking_options',
                  'cashincome_set')

    def get_participant_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.count()

    def get_payement(self, registration: event_models.Registration) -> dict:
        total_price = registration.registrationparticipant_set.aggregate(
            sum=Sum('booking_option__price'))['sum'] or 0
        paid = registration.cashincome_set.aggregate(sum=Sum('amount'))[
                   'sum'] or 0
        difference = total_price - paid

        return {
            'price': total_price,
            'paid': paid,
            'open': difference,
        }

    def get_booking_options(self, registration: event_models.Registration) -> dict:
        return registration.registrationparticipant_set \
            .values(booking_options=F('booking_option__name')) \
            .annotate(sum=Count('booking_option__name')) \
            .annotate(price=Sum('booking_option__price'))


class CashSummarySerializer(serializers.ModelSerializer):
    registration_set = RegistrationCashSummarySerializer(
        many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    booking_options = serializers.SerializerMethodField()

    class Meta:
        model = event_models.Event
        fields = (
            'participant_count',
            'registration_set',
            'booking_options',
        )

    def get_participant_count(self, event: event_models.Event) -> int:
        return event.registration_set.filter(is_confirmed=True).aggregate(count=Count('registrationparticipant'))[
            'count']

    def get_booking_options(self, event: event_models.Event) -> dict:
        return event.registration_set.filter(is_confirmed=True) \
            .values(booking_option=F('registrationparticipant__booking_option__name')) \
            .annotate(count=Count('registrationparticipant')) \
            .annotate(price=Sum('registrationparticipant__booking_option__price'))


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
