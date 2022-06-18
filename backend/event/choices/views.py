from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from event.choices import choices as event_choices


class RegistrationTypeGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.RegistrationTypeGroup.choices, status=status.HTTP_200_OK)


class RegistrationTypeSingleViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.RegistrationTypeSingle.choices, status=status.HTTP_200_OK)


class GenderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.Gender.choices, status=status.HTTP_200_OK)


class LeaderTypesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.LeaderTypes.choices, status=status.HTTP_200_OK)

class ScoutLevelTypesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.ScoutLevelTypes.choices, status=status.HTTP_200_OK)


class FileTypeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.FileType.choices, status=status.HTTP_200_OK)


class FileExtensionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.FileExtension.choices, status=status.HTTP_200_OK)
