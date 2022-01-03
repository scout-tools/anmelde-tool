from rest_framework import serializers
from .models import ScoutHierarchy, ZipCode, ScoutOrgaLevel, Tag, TagType


class ScoutHierarchySerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutHierarchy
        fields = '__all__'


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
        fields = ('name', 'type')


class TagLongSerializer(serializers.ModelSerializer):
    type = TagTypeLongSerializer(many=False)

    class Meta:
        model = Tag
        fields = ('name',
                  'type',
                  'is_custom',
                  'is_visible',
                  'description')
