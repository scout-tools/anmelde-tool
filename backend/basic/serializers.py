from rest_framework import serializers
from basic import models as basic_models
from .polymorphic_serializer import PolymorphicSerializer
from django.contrib.auth.models import User

"""
# noqa turn off pycharm warnings about missing abstract methods, which is a bug of pycharm
"""


class ScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.ScoutHierarchy
        fields = '__all__'


class NamyOnlyScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.ScoutHierarchy
        fields = ('name',)


class ZipCodeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.ZipCode
        fields = ('zip_code', 'city')


class ZipCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.ZipCode
        fields = '__all__'


class ScoutOrgaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.ScoutOrgaLevel
        fields = '__all__'


class TagTypeLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TagType
        fields = ('id',
                  'name',
                  'description',
                  'color')


class TagTypeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TagType
        fields = ('name',
                  'color')


class TagShortSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.Tag
        fields = ('id', 'name', 'type')


class TagLongSerializer(serializers.ModelSerializer):
    type = TagTypeLongSerializer(many=False)

    class Meta:
        model = basic_models.Tag
        fields = ('name',
                  'type',
                  'is_custom',
                  'is_visible',
                  'description')


class AbstractAttributeSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.AbstractAttribute
        exclude = ('template', 'polymorphic_ctype')


class BooleanAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.BooleanAttribute
        exclude = ('template', 'polymorphic_ctype', 'in_summary')


class TimeAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.TimeAttribute
        exclude = ('template', 'polymorphic_ctype', 'in_summary')


class IntegerAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.IntegerAttribute
        exclude = ('template', 'polymorphic_ctype', 'in_summary')


class FloatAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.FloatAttribute
        exclude = ('template', 'polymorphic_ctype', 'in_summary')


class TravelAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)
    type_field = serializers.CharField(source='get_type_field_display')
    time_field = serializers.CharField(source='get_time_field_display')

    class Meta:
        model = basic_models.TravelAttribute
        exclude = ('template', 'polymorphic_ctype', 'in_summary')


class TravelAttributeV2GetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)
    type_field = serializers.CharField(source='get_type_field_display')
    class Meta:
        model = basic_models.TravelAttributeV2
        exclude = ('template', 'polymorphic_ctype', 'in_summary')


class StringAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.StringAttribute
        exclude = ('template', 'polymorphic_ctype', 'in_summary')


class AbstractAttributeGetPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        basic_models.FloatAttribute: FloatAttributeGetSerializer,
        basic_models.IntegerAttribute: IntegerAttributeGetSerializer,
        basic_models.TimeAttribute: TimeAttributeGetSerializer,
        basic_models.BooleanAttribute: BooleanAttributeGetSerializer,
        basic_models.TravelAttribute: TravelAttributeGetSerializer,
        basic_models.TravelAttributeV2: TravelAttributeV2GetSerializer,
        basic_models.StringAttribute: StringAttributeGetSerializer
    }


class BooleanAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.BooleanAttribute
        fields = ('boolean_field',)


class TimeAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TimeAttribute
        fields = ('date_field',)


class IntegerAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.IntegerAttribute
        fields = ('integer_field',)


class FloatAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.FloatAttribute
        fields = ('float_field',)


class TravelAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TravelAttribute
        fields = ('type_field', 'time_field')

class TravelAttributeV2PutSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TravelAttributeV2
        fields = ('type_field', 'date_time_field', 'number_persons', 'description')


class StringAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.StringAttribute
        fields = ('string_field',)


class AbstractAttributePutPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        basic_models.FloatAttribute: FloatAttributePutSerializer,
        basic_models.IntegerAttribute: IntegerAttributePutSerializer,
        basic_models.TimeAttribute: TimeAttributePutSerializer,
        basic_models.BooleanAttribute: BooleanAttributePutSerializer,
        basic_models.TravelAttribute: TravelAttributePutSerializer,
        basic_models.TravelAttributeV2: TravelAttributeV2PutSerializer,
        basic_models.StringAttribute: StringAttributePutSerializer
    }


class BooleanAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = basic_models.BooleanAttribute
        fields = ('boolean_field', 'resourcetype', 'template_id')


class TimeAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = basic_models.TimeAttribute
        fields = ('date_field', 'resourcetype', 'template_id')


class IntegerAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = basic_models.IntegerAttribute
        fields = ('integer_field', 'resourcetype', 'template_id')


class FloatAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = basic_models.FloatAttribute
        fields = ('float_field', 'resourcetype', 'template_id')


class TravelAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = basic_models.TravelAttribute
        fields = ('type_field', 'time_field' , 'resourcetype', 'template_id')


class TravelAttributeV2TemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = basic_models.TravelAttributeV2
        fields = ('type_field', 'date_time_field' ,'persons', 'description', 'resourcetype', 'template_id')


class StringAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = basic_models.StringAttribute
        fields = ('string_field', 'resourcetype', 'template_id')


class AbstractAttributeTemplatePostPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        basic_models.FloatAttribute: FloatAttributeTemplatePostSerializer,
        basic_models.IntegerAttribute: IntegerAttributeTemplatePostSerializer,
        basic_models.TimeAttribute: TimeAttributeTemplatePostSerializer,
        basic_models.BooleanAttribute: BooleanAttributeTemplatePostSerializer,
        basic_models.TravelAttribute: TravelAttributeTemplatePostSerializer,
        basic_models.TravelAttributeV2: TravelAttributeV2TemplatePostSerializer,
        basic_models.StringAttribute: StringAttributeTemplatePostSerializer
    }


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.Description
        exclude = ('public', 'type')


class BooleanAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.BooleanAttribute
        fields = '__all__'


class TimeAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TimeAttribute
        fields = '__all__'


class IntegerAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.IntegerAttribute
        fields = '__all__'


class FloatAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.FloatAttribute
        fields = '__all__'


class TravelAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TravelAttribute
        fields = '__all__'


class TravelAttributeV2PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.TravelAttributeV2
        fields = '__all__'


class StringAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.StringAttribute
        fields = '__all__'


class AbstractAttributePostPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        basic_models.FloatAttribute: FloatAttributePostSerializer,
        basic_models.IntegerAttribute: IntegerAttributePostSerializer,
        basic_models.TimeAttribute: TimeAttributePostSerializer,
        basic_models.BooleanAttribute: BooleanAttributePostSerializer,
        basic_models.TravelAttribute: TravelAttributePostSerializer,
        basic_models.TravelAttributeV2: TravelAttributeV2PostSerializer,
        basic_models.StringAttribute: StringAttributePostSerializer
    }


class EatHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.EatHabit
        fields = '__all__'


class FrontendThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.FrontendTheme
        fields = '__all__'


class ZipCodeDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.ZipCode
        fields = ('zip_code', 'city', 'lat', 'lon')


class ScoutHierarchyDetailedSerializer(serializers.ModelSerializer):
    level = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='name'
    )
    zip_code = ZipCodeDetailedSerializer(many=False, read_only=True)
    ring = serializers.SerializerMethodField()
    bund = serializers.SerializerMethodField()

    class Meta:
        model = basic_models.ScoutHierarchy
        fields = ('name', 'abbreviation', 'level', 'zip_code', 'ring', 'bund')

    def get_ring(self, obj: basic_models.ScoutHierarchy) -> str:
        iterator: basic_models.ScoutHierarchy = obj
        while iterator is not None:
            if iterator.level.name == 'Ring/Regional':
                return iterator.name
            iterator = iterator.parent

        return ''

    def get_bund(self, obj: basic_models.ScoutHierarchy) -> str:
        iterator: basic_models.ScoutHierarchy = obj
        while iterator is not None:
            if iterator.level.name == 'Bund':
                return iterator.name
            iterator = iterator.parent

        return ''


class MessageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = basic_models.MessageType
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):

    supervisor = serializers.SlugRelatedField(
        many=False,
        required=False,
        read_only=False,
        slug_field='email',
        queryset=User.objects.all()
    )
    class Meta:
        model = basic_models.Message
        fields = '__all__'

