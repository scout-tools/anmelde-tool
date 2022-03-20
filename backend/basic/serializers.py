from rest_framework import serializers
from .models import ScoutHierarchy, ZipCode, ScoutOrgaLevel, Tag, TagType, AbstractAttribute, BooleanAttribute, \
    TimeAttribute, IntegerAttribute, FloatAttribute, TravelAttribute, StringAttribute, TravelType, TravelSlots, \
    Description
from .polymorphic_serializer import PolymorphicSerializer

"""
# noqa turn off pycharm warnings about missing abstract methods, which is a bug of pycharm
"""


class ScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutHierarchy
        fields = '__all__'


class ZipCodeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = ('zip_code', 'city')


class ZipCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZipCode
        fields = '__all__'


class ScoutOrgaLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutOrgaLevel
        fields = '__all__'


class TagTypeLongSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagType
        fields = ('id',
                  'name',
                  'description',
                  'color')


class TagTypeShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagType
        fields = ('name',
                  'color')


class TagShortSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'type')


class TagLongSerializer(serializers.ModelSerializer):
    type = TagTypeLongSerializer(many=False)

    class Meta:
        model = Tag
        fields = ('name',
                  'type',
                  'is_custom',
                  'is_visible',
                  'description')


class AbstractAttributeSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = AbstractAttribute
        exclude = ('template', 'polymorphic_ctype')


class BooleanAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = BooleanAttribute
        exclude = ('template', 'polymorphic_ctype')


class TimeAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = TimeAttribute
        exclude = ('template', 'polymorphic_ctype')


class IntegerAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = IntegerAttribute
        exclude = ('template', 'polymorphic_ctype')


class FloatAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = FloatAttribute
        exclude = ('template', 'polymorphic_ctype')


class TravelAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = TravelAttribute
        exclude = ('template', 'polymorphic_ctype')


class StringAttributeGetSerializer(serializers.ModelSerializer):  # noqa
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = StringAttribute
        exclude = ('template', 'polymorphic_ctype')


class AbstractAttributeGetPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        FloatAttribute: FloatAttributeGetSerializer,
        IntegerAttribute: IntegerAttributeGetSerializer,
        TimeAttribute: TimeAttributeGetSerializer,
        BooleanAttribute: BooleanAttributeGetSerializer,
        TravelAttribute: TravelAttributeGetSerializer,
        StringAttribute: StringAttributeGetSerializer
    }


class BooleanAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanAttribute
        fields = ('boolean_field',)


class TimeAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeAttribute
        fields = ('date_field',)


class IntegerAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegerAttribute
        fields = ('integer_field',)


class FloatAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatAttribute
        fields = ('float_field',)


class TravelAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelAttribute
        fields = ('type_field', 'time_field')


class StringAttributePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringAttribute
        fields = ('string_field',)


class AbstractAttributePutPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        FloatAttribute: FloatAttributePutSerializer,
        IntegerAttribute: IntegerAttributePutSerializer,
        TimeAttribute: TimeAttributePutSerializer,
        BooleanAttribute: BooleanAttributePutSerializer,
        TravelAttribute: TravelAttributePutSerializer,
        StringAttribute: StringAttributePutSerializer
    }


class BooleanAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = BooleanAttribute
        fields = ('boolean_field', 'resourcetype', 'template_id')


class TimeAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = TimeAttribute
        fields = ('date_field', 'resourcetype', 'template_id')


class IntegerAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = IntegerAttribute
        fields = ('integer_field', 'resourcetype', 'template_id')


class FloatAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = FloatAttribute
        fields = ('float_field', 'resourcetype', 'template_id')


class TravelAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = TravelAttribute
        fields = ('type_field', 'time_field', 'resourcetype', 'template_id')


class StringAttributeTemplatePostSerializer(serializers.ModelSerializer):
    resourcetype = serializers.CharField()

    class Meta:
        model = StringAttribute
        fields = ('string_field', 'resourcetype', 'template_id')


class AbstractAttributeTemplatePostPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        FloatAttribute: FloatAttributeTemplatePostSerializer,
        IntegerAttribute: IntegerAttributeTemplatePostSerializer,
        TimeAttribute: TimeAttributeTemplatePostSerializer,
        BooleanAttribute: BooleanAttributeTemplatePostSerializer,
        TravelAttribute: TravelAttributeTemplatePostSerializer,
        StringAttribute: StringAttributeTemplatePostSerializer
    }


class DescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Description
        exclude = ('public', 'type')


class BooleanAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BooleanAttribute
        fields = '__all__'


class TimeAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeAttribute
        fields = '__all__'


class IntegerAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegerAttribute
        fields = '__all__'


class FloatAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FloatAttribute
        fields = '__all__'


class TravelAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelAttribute
        fields = '__all__'


class StringAttributePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = StringAttribute
        fields = '__all__'


class AbstractAttributePostPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        FloatAttribute: FloatAttributePostSerializer,
        IntegerAttribute: IntegerAttributePostSerializer,
        TimeAttribute: TimeAttributePostSerializer,
        BooleanAttribute: BooleanAttributePostSerializer,
        TravelAttribute: TravelAttributePostSerializer,
        StringAttribute: StringAttributePostSerializer
    }
