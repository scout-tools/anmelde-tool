from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserExtended, EmailNotificationType
from .serializers import UserExtendedGetSerializer, UserExtendedPostSerializer, GroupSerializer, EmailSettingsSerializer


class PersonalData(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedGetSerializer(queryset, many=False)
        return Response(serializer.data)

    def create(self, request, pk=None):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedPostSerializer(queryset, data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_200_OK)


class PersonalDataCheck(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = UserExtended.objects.get(user=request.user)
        serializer = UserExtendedGetSerializer(queryset, many=False)
        if not serializer.data['scout_organisation'] or not serializer.data['dsgvo_confirmed']:
            return Response({'status': "init required"}, status=status.HTTP_426_UPGRADE_REQUIRED)
        else:
            return Response({'status': "user ok"}, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def get_queryset(self):
        return self.request.user.groups.all()


class EmailSettingsViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = EmailSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserExtended.objects.filter(id=self.request.user.userextended.id)


class EmailNotificationTypeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(EmailNotificationType.choices, status=status.HTTP_200_OK)
