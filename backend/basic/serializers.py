from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer

from .models import ScoutHierarchy, ZipCode, ScoutOrgaLevel, Tag, TagType, AbstractAttribute, BooleanAttribute, \
    TimeAttribute, IntegerAttribute, FloatAttribute, TravelAttribute


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


class BooleanAttributeSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = BooleanAttribute
        fields = '__all__'


class TimeAttributeSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = TimeAttribute
        fields = '__all__'


class IntegerAttributeSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = IntegerAttribute
        fields = '__all__'


class FloatAttributeSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = FloatAttribute
        fields = '__all__'


class TravelAttributeSerializer(serializers.ModelSerializer):
    type = TagTypeShortSerializer(many=False)

    class Meta:
        model = TravelAttribute
        fields = '__all__'


class AbstractAttributePolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        FloatAttribute: FloatAttributeSerializer,
        IntegerAttribute: IntegerAttributeSerializer,
        TimeAttribute: TimeAttributeSerializer,
        BooleanAttribute: BooleanAttributeSerializer,
        TravelAttribute: TravelAttributeSerializer,
    }
