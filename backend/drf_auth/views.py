from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics, views, exceptions

from rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_settings
from allauth.account.models import EmailAddress, EmailConfirmationHMAC

from rest_auth.app_settings import (UserDetailsSerializer, PasswordResetConfirmSerializer, create_token)
from rest_auth.utils import jwt_encode
from rest_auth.registration.views import VerifyEmailView
from rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetConfirmView

from .email import send_register_mail, send_reset_password_email

User = get_user_model()

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2')
)


class RegisterUserView(RegisterView):
    def __init__(self):
        # self.token = ''
        # self.request = None
        # self.serializer = None
        pass

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        if getattr(settings, 'REST_USE_JWT', False):
            self.token = jwt_encode(user)
        else:
            create_token(self.token_model, user, serializer)
        email = EmailAddress.objects.get(user=user, email=user.email)
        confirmation = EmailConfirmationHMAC(email)
        send_register_mail(user, confirmation.key)
        return user


class LoginUserView(LoginView):
    queryset = ''

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        self.serializer.is_valid(raise_exception=True)

        self.login()
        return self.get_response()


class VerifyUserEmailView(VerifyEmailView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


class PasswordResetUserView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.NotAcceptable(_("please enter correct email."))
        send_reset_password_email(user)
        return Response({"detail": _("Password reset has been sent.")},
                        status=status.HTTP_200_OK)


class PasswordResetConfirmUserView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(PasswordResetConfirmUserView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Password has been reset with the new password.")})


class PasswordUserChangeView(PasswordChangeView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password has been Changed.")})


class UserDetailsAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return get_user_model().objects.none()
