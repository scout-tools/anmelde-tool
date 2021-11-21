from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserExtended
from .serializers import UserExtendedSerializer


class PersonalData(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedSerializer(queryset, many=False)
        return Response(serializer.data)
        # auth = OIDCAuthenticationBackend()
        # user = auth.get_userinfo(request.auth, None, None)
        # return Response({'status': 'passt',
        #                  'user-email': request.user.email,
        #                  'user-username': request.user.username,
        #                  'auth': user}, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedSerializer(queryset, many=False)
        return Response(serializer.data)

    def create(self, request, pk=None):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedSerializer(queryset, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        return Response('test', status=status.HTTP_400_BAD_REQUEST)
