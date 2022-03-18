from datetime import datetime

from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import ScoutHierarchy, ZipCode, ScoutOrgaLevel, Tag, TagType, AbstractAttribute, BooleanAttribute, \
    TimeAttribute, IntegerAttribute, FloatAttribute, TravelAttribute, StringAttribute, TravelType, TravelSlots

"""
# noqa turn off pycharm warnings about missing abstract methods, which is a bug of pycharm
"""


def assign_value_attribute(attribute: AbstractAttribute, value) -> AbstractAttribute:
    if isinstance(attribute, BooleanAttribute):
        attribute.boolean_field = bool(value)
    elif isinstance(attribute, TimeAttribute):
        attribute.date_field = datetime(value)
    elif isinstance(attribute, IntegerAttribute):
        attribute.integer_field = int(value)
    elif isinstance(attribute, FloatAttribute):
        attribute.float_field = float(value)
    elif isinstance(attribute, StringAttribute):
        attribute.string_field = str(value)
    elif isinstance(attribute, TravelAttribute):
        attribute.type_field = TravelType(value[:1])
        attribute.time_field = TravelSlots(value[1:])
    else:
        raise Exception('attribute type not found')
    attribute.save()
    return attribute


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


class AbstractAttributeSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = AbstractAttribute
        fields = '__all__'


class BooleanAttributeGetSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = BooleanAttribute
        fields = '__all__'


class TimeAttributeGetSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = TimeAttribute
        fields = '__all__'


class IntegerAttributeGetSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = IntegerAttribute
        fields = '__all__'


class FloatAttributeGetSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = FloatAttribute
        fields = '__all__'


class TravelAttributeGetSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = TravelAttribute
        fields = '__all__'


class StringAttributeGetSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = StringAttribute
        fields = '__all__'


class AbstractAttributeGetPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        FloatAttribute: FloatAttributeGetSerializer,
        IntegerAttribute: IntegerAttributeGetSerializer,
        TimeAttribute: TimeAttributeGetSerializer,
        BooleanAttribute: BooleanAttributeGetSerializer,
        TravelAttribute: TravelAttributeGetSerializer,
        StringAttribute: StringAttributeGetSerializer
    }


class BooleanAttributePostSerializer(serializers.Serializer):  # noqa
    template_id = serializers.IntegerField(required=True)
    boolean_field = serializers.BooleanField(required=False)


class TimeAttributePostSerializer(serializers.Serializer):  # noqa
    template_id = serializers.IntegerField(required=True)
    date_field = serializers.DateTimeField(required=False)


class IntegerAttributePostSerializer(serializers.Serializer):  # noqa
    template_id = serializers.IntegerField(required=True)
    integer_field = serializers.IntegerField(required=False)


class FloatAttributePostSerializer(serializers.Serializer):  # noqa
    template_id = serializers.IntegerField(required=True)
    float_field = serializers.FloatField(required=False)


class TravelAttributePostSerializer(serializers.Serializer):  # noqa
    template_id = serializers.IntegerField(required=True)
    time_field = serializers.CharField(required=False, max_length=2)
    type_field = serializers.CharField(required=False, max_length=2)


class StringAttributePostSerializer(serializers.Serializer):  # noqa
    template_id = serializers.IntegerField(required=True)
    string_field = serializers.CharField(required=False, max_length=9999)


class AbstractAttributePostPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = 'template_id'
    model_serializer_mapping = {
        FloatAttribute: FloatAttributePostSerializer,
        IntegerAttribute: IntegerAttributePostSerializer,
        TimeAttribute: TimeAttributePostSerializer,
        BooleanAttribute: BooleanAttributePostSerializer,
        TravelAttribute: TravelAttributePostSerializer,
        StringAttribute: StringAttributePostSerializer
    }


class AbstractAttributePostSerializer(serializers.Serializer):
    template_id = serializers.IntegerField(required=True)
