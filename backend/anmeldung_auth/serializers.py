from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from .models import UserExtended
from rest_framework import serializers, status, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime as dt


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = '__all__'


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'email': {'required': True},
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        attrs['email'] = attrs['email'].lower()
        attrs['username'] = attrs['email']

        if 'first_name' not in attrs:
            attrs['first_name'] = ''
        if 'last_name' not in attrs:
            attrs['last_name'] = ''
        if 'password' not in attrs:
            attrs['password'] = User.objects.make_random_password()
        return attrs

    def create(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user is None:
            user = User.objects.create_user(data['email'],
                                            email=data['email'],
                                            password=data['password'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'])

            data['newly_registered'] = True
            data['username'] = data['email'].split('@', 1)[0]
            data['user'] = user.email
        else:
            user.set_password(data['password'])
            data['username'] = user.userextended.scout_name
            data['user'] = user.email
            data['newly_registered'] = False
            user.save()

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
