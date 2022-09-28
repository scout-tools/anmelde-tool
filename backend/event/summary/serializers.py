from django.contrib.auth.models import User
from django.db.models import QuerySet, Sum, Count, F
from rest_framework import serializers

from basic import serializers as basic_serializers
from basic.models import EatHabit
from event import models as event_models
from event import serializers as event_serializer
from event.cash import serializers as cash_serializers
from event.registration import serializers as registration_serializers


class WorkshopEventSummarySerializer(serializers.ModelSerializer):
    supervisor = registration_serializers.CurrentUserSerializer(many=False, read_only=True)
    type = serializers.CharField(source='get_type_display')

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
    scout_organisation = basic_serializers.ScoutHierarchyDetailedSerializer(many=False, read_only=True)
    booking_options = serializers.SerializerMethodField()
    responsible_persons_extended = serializers.SerializerMethodField()

    class Meta:
        model = event_models.Registration
        fields = (
            'id',
            'is_confirmed',
            'is_accepted',
            'single',
            'scout_organisation',
            'responsible_persons',
            'responsible_persons_extended',
            'participant_count',
            'price',
            'created_at',
            'updated_at',
            'booking_options',)

    def get_participant_count(self, registration: event_models.Registration) -> int:
        booking_option_list = self.context['request'].query_params.getlist('booking-option')
        queryset = registration.registrationparticipant_set

        if booking_option_list:
            queryset = queryset.filter(booking_option__in=booking_option_list)

        return queryset.count()

    def get_price(self, registration: event_models.Registration) -> float:
        booking_option_list = self.context['request'].query_params.getlist('booking-option')
        queryset = registration.registrationparticipant_set

        if booking_option_list:
            queryset = queryset.filter(booking_option__in=booking_option_list)

        return queryset.aggregate(sum=Sum('booking_option__price'))['sum']

    def get_booking_options(self, registration: event_models.Registration) -> dict:
        return registration.registrationparticipant_set \
            .values(booking_options=F('booking_option__name')) \
            .annotate(sum=Count('booking_option__name')) \
            .annotate(price=Sum('booking_option__price'))

    def get_responsible_persons_extended(self, registration: event_models.Registration) -> str:
        return_string = ''
        for person in registration.responsible_persons.all():
            return_string = return_string + f'{person.userextended.scout_name} (Tel:{person.userextended.mobile_number}) '
        return return_string


class RegistrationParticipantEventDetailedSummarySerializer(serializers.ModelSerializer):
    booking_option = registration_serializers.RegistrationSummaryBookingOptionSerializer(many=False, read_only=True)
    scout_group = basic_serializers.ScoutHierarchyDetailedSerializer(many=False, read_only=True)
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
    scout_organisation = serializers.SerializerMethodField()

    class Meta:
        model = event_models.RegistrationParticipant
        exclude = (
            'deactivated',
            'generated',
            'registration',
            'id',
            'tags'
        )

    def get_scout_organisation(self, participant: event_models.RegistrationParticipant) -> str:
        return participant.registration.scout_organisation.name


class RegistrationLocationSerializer(serializers.ModelSerializer):
    participant_count = serializers.SerializerMethodField()
    scout_organisation = basic_serializers.ScoutHierarchyDetailedSerializer(many=False, read_only=True)

    class Meta:
        model = event_models.Registration
        fields = (
            'scout_organisation',
            'participant_count',
            'created_at',
            'updated_at',)

    def get_participant_count(self, registration: event_models.Registration) -> int:
        booking_option_list = self.context['request'].query_params.getlist('booking-option')
        queryset = registration.registrationparticipant_set

        if booking_option_list:
            queryset = queryset.filter(booking_option__in=booking_option_list)

        return queryset.count()


class EventLocationSummarySerializer(serializers.ModelSerializer):
    location = event_serializer.EventLocationSummarySerializer(many=False, read_only=True)

    class Meta:
        model = event_models.Event
        fields = (
            'location',
        )


class RegistrationAttributeGetSerializer(serializers.ModelSerializer):
    scout_organisation = basic_serializers.NamyOnlyScoutHierarchySerializer(
        many=False, read_only=True)
    responsible_persons = registration_serializers.CurrentUserSerializer(
        many=True, read_only=True)

    class Meta:
        model = event_models.Registration
        fields = (
            'scout_organisation',
            'is_confirmed',
            'is_accepted',
            'responsible_persons'
        )


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
    responsible_persons = registration_serializers.CurrentUserSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    payement = serializers.SerializerMethodField()
    scout_organisation = basic_serializers.ScoutHierarchyDetailedSerializer(many=False, read_only=True)
    booking_options = serializers.SerializerMethodField()
    cashincome_set = cash_serializers.CashIncomeSerializer(many=True, read_only=True)
    ref_id = serializers.SerializerMethodField()

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
                  'cashincome_set',
                  'ref_id')

    def get_participant_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.count()

    def get_payement(self, registration: event_models.Registration) -> dict:
        total_price = registration.registrationparticipant_set.aggregate(
            sum=Sum('booking_option__price'))['sum'] or 0
        paid = registration.cashincome_set.aggregate(sum=Sum('amount'))[
                   'sum'] or 0.0
        difference = float(total_price) - paid

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

    def get_ref_id(self, registration: event_models.Registration) -> str:
        return f'{registration.event.name.replace(" ", "")[:10]}' \
               f'-{registration.scout_organisation.name.replace(" ", "")[:10]}' \
               f'-{str(registration.created_at.timestamp())[:10]}'


class CashSummarySerializer(serializers.ModelSerializer):
    registration_set = RegistrationCashSummarySerializer(many=True, read_only=True)
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
