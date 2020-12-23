from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from .models import UserExtended
from rest_framework import serializers, status, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import datetime as dt


class RegisterSerializer(serializers.ModelSerializer):
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
        if 'username' not in attrs:
            attrs['username'] = attrs['email'].split('@', 1)[0]
        if 'first_name' not in attrs:
            attrs['first_name'] = ''
        if 'last_name' not in attrs:
            attrs['last_name'] = ''
        if 'password' not in attrs:
            attrs['password'] = "HagiIstDerCoolste"
        return attrs

    def create(self, data):
        if not User.objects.filter(email=data['email']).exists():
            user = User.objects.create_user(data['username'],
                                            email=data['email'],
                                            password=data['password'],
                                            first_name=data['first_name'],
                                            last_name=data['last_name'])
            return user
        else:
            raise serializers.ValidationError(
                u'User "%s" is already in use.' % data['email'])


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
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
            raise serializers.ValidationError(
                u'User "%s" does not exist.' % validated_data['email'])


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }

        user_obj = User.objects.filter(
            email=attrs.get("username")).first() or User.objects.filter(
                username=attrs.get("username")).first()

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
        token['email'] = user.email
        token['groups'] = [x.as_dict() for x in user.groups.all()]

        token['isStaff'] = user.is_staff  # transforded to camelCase for frontend

        return token


class ServiceUnavailableError(exceptions.APIException):
    status_code = status.HTTP_418_IM_A_TEAPOT
    default_detail = "Password expired, please get a new one"
