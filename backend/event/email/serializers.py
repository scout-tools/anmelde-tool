from rest_framework import serializers

class CustomMailSerializer(serializers.Serializer): # noqa
    subject = serializers.CharField()
    header = serializers.CharField()
    body = serializers.CharField()
    send_confirmed = serializers.BooleanField(default=True)
    send_unconfirmed = serializers.BooleanField(default=True)
