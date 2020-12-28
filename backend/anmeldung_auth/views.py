from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .email import send_auth_mail
from .serializers import MyTokenObtainPairSerializer, UserExtendedSerializer, AuthSerializer
from .models import UserExtended


# Register API
class AuthenticateView(generics.UpdateAPIView):
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_auth_mail(user)

        if user['newly_registered']:
            return Response({
                "message": "User Created Successfully and login email sent.",
            })
        else:
            return Response({
                "message": "Login email sent",
            })

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserExtendedViewSet(viewsets.ModelViewSet):
    queryset = UserExtended.objects.all()
    serializer_class = UserExtendedSerializer
