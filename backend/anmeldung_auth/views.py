from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .email import send_register_mail, send_login_mail
from .serializers import RegisterSerializer, OneClickLoginSerializer, MyTokenObtainPairSerializer, UserExtendedSerializer
from .models import UserExtended


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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserExtendedViewSet(viewsets.ModelViewSet):
    queryset = UserExtended.objects.all()
    serializer_class = UserExtendedSerializer
