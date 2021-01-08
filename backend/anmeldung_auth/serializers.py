from django.contrib.auth.models import User
from .models import UserExtended
from rest_framework import serializers, status, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime as dt
from helper.user_creation import login_or_create_user


# User serializer
class UserExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = (
            'mobileMumber',
            'scoutName',
            'scoutOrganisation',
        )


# Authentication serialzer
class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        attrs['username'] = attrs['email']
        attrs['password'] = User.objects.make_random_password()

        if 'first_name' not in attrs:
            attrs['first_name'] = ''
        if 'last_name' not in attrs:
            attrs['last_name'] = ''
        return attrs

    def create(self, data):
        data = login_or_create_user(data)
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'email': '',
            'password': attrs.get("password")
        }

        user_obj = User.objects.filter(
            email=attrs.get("username")).first() or User.objects.filter(username=attrs.get("username")).first()

        if user_obj:
            credentials['username'] = user_obj.username

            if not user_obj.is_superuser and not user_obj.is_staff:
                now = dt.datetime.now(dt.timezone.utc)
                password_date = user_obj.userextended.password_date
                if now - password_date > dt.timedelta(days=1):
                    raise ServiceUnavailableError()

        return super().validate(credentials)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['userId'] = user.id  # transforded to camelCase for frontend
        token['email'] = user.username  # transforded to camelCase for frontend
        token['groups'] = [x.as_dict() for x in user.groups.all()]
        token['isStaff'] = user.is_staff  # transforded to camelCase for frontend

        return token


class ServiceUnavailableError(exceptions.APIException):
    status_code = status.HTTP_418_IM_A_TEAPOT
    default_detail = "Password expired, please get a new one"
