from django.contrib.auth.models import User
from django.db.models import Sum, Count
from rest_framework import serializers

from authentication.serializers import UserExtendedGetSerializer
from basic import serializers as basic_serializers
from basic.models import EatHabit
from event import models as event_models


class CurrentUserSerializer(serializers.ModelSerializer):
    userextended = UserExtendedGetSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'userextended', 'first_name', 'last_name')


class RegistrationPostSerializer(serializers.Serializer):  # noqa
    event_code = serializers.CharField(required=True)
    single = serializers.BooleanField(required=True)
    event = serializers.UUIDField(required=True)


class RegistrationPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.Registration
        fields = ('responsible_persons', 'is_confirmed', 'tags')
        extra_kwargs = {"responsible_persons": {"required": False, "allow_null": True}}


class RegistrationGetSerializer(serializers.ModelSerializer):
    responsible_persons = CurrentUserSerializer(many=True, read_only=True)
    tags = basic_serializers.TagShortSerializer(many=True, read_only=True)

    class Meta:
        model = event_models.Registration
        fields = '__all__'


class RegistrationParticipantShortSerializer(serializers.ModelSerializer):
    scout_level = serializers.CharField(source='get_scout_level_display')
    eat_habit = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        queryset=EatHabit.objects.all(),
        required=False
    )
    class Meta: 
        model = event_models.RegistrationParticipant
        fields = ('id', 'scout_name', 'first_name', 'last_name', 'scout_level', 'eat_habit', 'age')


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
        fields = ('first_name', 'last_name', 'scout_name', 'deactivated', 'booking_option', 'eat_habit', 'scout_level')


class RegistrationSummarySerializer(serializers.ModelSerializer):
    registrationparticipant_set = RegistrationSummaryParticipantSerializer(many=True, read_only=True)
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='email'
    )
    vegan_count = serializers.SerializerMethodField()
    veggi_count = serializers.SerializerMethodField()
    veggi_count = serializers.SerializerMethodField()
    wolf_count = serializers.SerializerMethodField()
    sippling_count = serializers.SerializerMethodField()
    rover_count = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta: # here age
        model = event_models.Registration
        fields = ('is_confirmed',
                  'is_accepted',
                  'responsible_persons',
                  'participant_count',
                  'price',
                  'registrationparticipant_set',
                  'tags',
                  'vegan_count',
                  'veggi_count',
                  'wolf_count',
                  'sippling_count',
                  'rover_count',
                  )

    def get_participant_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.count()

    def get_vegan_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.filter(eat_habit__id__contains=2).count()

    def get_veggi_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.filter(eat_habit__id__contains=1).count()

    def get_wolf_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.filter(scout_level='W').count()

    def get_sippling_count(self, registration: event_models.Registration) -> int:
        return registration.registrationparticipant_set.filter(scout_level='S').count()

    def get_rover_count(self, registration: event_models.Registration) -> float:
        return registration.registrationparticipant_set.filter(scout_level='R').count()

    def get_price(self, registration: event_models.Registration) -> float:
        return registration.registrationparticipant_set.aggregate(
            sum=Sum('booking_option__price'))['sum']

    def get_tags(self, registration: event_models.Registration) -> []:
        queryset = registration.tags.filter(in_summary=True)
        serializer = basic_serializers.AbstractAttributeGetPolymorphicSerializer(queryset, many=True)
        return serializer.data


class WorkshopSerializer(serializers.ModelSerializer):
    class Meta:
        model = event_models.Workshop
        fields = '__all__'
