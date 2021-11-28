from rest_framework import serializers

from .models import UserExtended


class UserExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = (
            'mobile_number',
            'scout_name',
            'scout_organisation',
            'dsgvo_confirmed'
        )
