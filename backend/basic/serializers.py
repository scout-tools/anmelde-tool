# serializers.py
from rest_framework import serializers
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, \
    ParticipantGroup, ParticipantRole, Role, MethodOfTravel, Tent, ScoutOrgaLevel, ParticipantPersonal, \
    EatHabitType, EatHabit, TravelType, TentType
from rest_framework.fields import Field
from django.contrib.auth.models import User


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventOverviewSerializer(serializers.ModelSerializer):
    participant_role = serializers.SerializerMethodField('get_event_role')

    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'description',
            'event_tags',
            'start_time',
            'end_time',
            'participant_role'
        )

    def get_event_role(self, obj):
        roles = obj.eventrolemapping_set.filter(user=self.context['request'].user).values_list('event_role_id',
                                                                                               flat=True)
        if roles:
            return roles
        else:
            return []


class AgeGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroup
        fields = '__all__'


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = '__all__'


class ScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutHierarchy
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    responsible_persons = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Registration
        fields = '__all__'


class ZipCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = '__all__'


class ParticipantGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantGroup
        fields = '__all__'


class ParticipantSerializer2(serializers.ModelSerializer):
    lon = serializers.SerializerMethodField('get_lon')
    lat = serializers.SerializerMethodField('get_lat')
    name = serializers.SerializerMethodField('get_name')
    bund = serializers.SerializerMethodField('get_bund')

    def get_bund_name(self, scout_organisation):
        if scout_organisation.level_id > 3:
            return self.get_bund_name(scout_organisation.parent)
        elif scout_organisation.level_id < 3:
            raise Exception("To low value")
        else:
            return scout_organisation.name

    def get_lon(self, par: ParticipantGroup):
        if par.registration.scout_organisation.zip_code is not None:
            lon = par.registration.scout_organisation.zip_code.lon
        else:
            lon = 10.451526
        return lon

    def get_lat(self, par: ParticipantGroup):
        if par.registration.scout_organisation.zip_code is not None:
            lat = par.registration.scout_organisation.zip_code.lat
        else:
            lat = 51.165691
        return lat

    def get_bund(self, par: ParticipantGroup):
        return self.get_bund_name(par.registration.scout_organisation)

    def get_name(self, par: ParticipantGroup):
        return par.registration.scout_organisation.name

    class Meta:
        model = ParticipantGroup
        fields = '__all__'


class ParticipantRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantRole
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class MethodOfTravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MethodOfTravel
        fields = '__all__'


class TentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tent
        fields = '__all__'


class ScoutOrgaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutOrgaLevel
        fields = '__all__'


class ParticipantPersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantPersonal
        fields = '__all__'


class EatHabitTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EatHabitType
        fields = '__all__'


class EatHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EatHabit
        fields = '__all__'


class EatHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = EatHabit
        fields = '__all__'


class TravelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelType
        fields = '__all__'


class TentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TentType
        fields = '__all__'