from rest_framework import serializers
from basic import models as basic_models
from .polymorphic_serializer import PolymorphicSerializer

"""
# noqa turn off pycharm warnings about missing abstract methods, which is a bug of pycharm
"""


class ScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.ScoutHierarchy
        fields = '__all__'


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
        exclude = ('template', 'polymorphic_ctype')


class TimeAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.TimeAttribute
        exclude = ('template', 'polymorphic_ctype')


class IntegerAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.IntegerAttribute
        exclude = ('template', 'polymorphic_ctype')


class FloatAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.FloatAttribute
        exclude = ('template', 'polymorphic_ctype')


class TravelAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.TravelAttribute
        exclude = ('template', 'polymorphic_ctype')


class StringAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = basic_models.StringAttribute
        exclude = ('template', 'polymorphic_ctype')


class AbstractAttributeGetPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        basic_models.FloatAttribute: FloatAttributeGetSerializer,
        basic_models.IntegerAttribute: IntegerAttributeGetSerializer,
        basic_models.TimeAttribute: TimeAttributeGetSerializer,
        basic_models.BooleanAttribute: BooleanAttributeGetSerializer,
        basic_models.TravelAttribute: TravelAttributeGetSerializer,
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
        fields = ('type_field', 'time_field', 'resourcetype', 'template_id')


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
        basic_models.StringAttribute: StringAttributePostSerializer
    }


class EatHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = basic_models.EatHabit
        fields = '__all__'
