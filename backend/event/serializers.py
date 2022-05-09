from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.utils import timezone
from rest_framework import serializers

from basic import serializers as basic_serializers
from event import models as event_models
from event import permissions as event_permissions
from event.choices import choices as event_choices


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
        read_only=False,
        slug_field='email',
        queryset=User.objects.all()
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
        user: User = self.context['request'].user

        group_id = None
        single_id = None
        allow_edit_group_reg = False
        allow_edit_single_reg = False

        existing_group: QuerySet = obj.registration_set. \
            filter(single=False, scout_organisation=user.userextended.scout_organisation)
        group: QuerySet[event_models.Registration] = existing_group. \
            filter(responsible_persons__in=[user.id])
        single: QuerySet[event_models.Registration] = obj.registration_set. \
            filter(responsible_persons__in=[user.id], single=True)

        if existing_group.exists():
            group_id = existing_group.first().id
            allow_edit_group_reg = group.exists() and existing_group.exists() and self.get_can_edit(obj)

        if single.exists():
            single_id = single.first().id
            allow_edit_single_reg = self.get_can_edit(obj) and not allow_edit_group_reg

        allow_new_group_reg = not group_id \
                              and not single_id \
                              and user.userextended.scout_organisation.level.id == 5 \
                              and self.get_can_register(obj) \
                              and obj.group_registration != event_choices.RegistrationTypeGroup.No
        allow_new_single_reg = not single_id \
                               and not allow_edit_group_reg \
                               and self.get_can_register(obj) \
                               and obj.single_registration != event_choices.RegistrationTypeGroup.No

        return {
            'group_id': group_id,
            'allow_new_group_reg': allow_new_group_reg,
            'allow_edit_group_reg': allow_edit_group_reg,
            'single_id': single_id,
            'allow_new_single_reg': allow_new_single_reg,
            'allow_edit_single_reg': allow_edit_single_reg
        }
