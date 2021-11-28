# serializers.py

from rest_framework import serializers

from .models import EventLocation, ScoutHierarchy, ZipCode, ScoutOrgaLevel


class EventLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocation
        fields = '__all__'


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
