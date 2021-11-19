from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, generics, mixins, status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, UserExtendedSerializer, AuthSerializer, User
from .models import UserExtended
from rest_framework.permissions import IsAuthenticated


# Register API
class AuthenticateView(generics.UpdateAPIView):
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

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


class UserExtendedViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedSerializer(queryset, many=False)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedSerializer(queryset, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
