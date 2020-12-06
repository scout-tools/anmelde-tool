from rest_framework import generics, permissions, mixins
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer, OneClickLoginSerializer
from django.contrib.auth.models import User
from rest_framework import mixins, viewsets
from .email import send_register_mail, send_login_mail


# Register API
class RegisterView(generics.UpdateAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_register_mail(user)
        return Response({
            "message": "User Created Successfully.",
        })


class OneClickView(generics.UpdateAPIView):
    serializer_class = OneClickLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_login_mail(user)
        return Response({
            "message": "Login email sent",
        })
