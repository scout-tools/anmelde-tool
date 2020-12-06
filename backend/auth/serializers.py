from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password  # Register serializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True,'required':False},
            'email': {'required': True},
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if 'username' not in attrs:
            attrs['username'] = attrs['email'].split('@', 1)[0]
        if 'first_name' not in attrs:
            attrs['first_name'] = ''
        if 'last_name' not in attrs:
            attrs['last_name'] = ''
        if 'password' not in attrs:
            attrs['password'] = "HagiIstDerCoolste"
        return attrs

    def create(self, validated_data):
        if not User.objects.filter(email=validated_data['email']).exists():
            user = User.objects.create_user(validated_data['username'],
                                            email=validated_data['email'],
                                            password=validated_data['password'],
                                            first_name=validated_data['first_name'],
                                            last_name=validated_data['last_name'])
            return user
        else:
            raise serializers.ValidationError(u'User "%s" is already in use.' % validated_data['email'])


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OneClickLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

    def validate(self, attrs):
        attrs['password'] = User.objects.make_random_password()
        return attrs

    def create(self, validated_data):

        user = User.objects.get(email=validated_data['email'])
        if user is not None:
            user.set_password(validated_data['password'])
            user.save()
            validated_data['username'] = user.username
            return validated_data
        else:
            raise serializers.ValidationError(u'User "%s" does not exist.' % validated_data['email'])
