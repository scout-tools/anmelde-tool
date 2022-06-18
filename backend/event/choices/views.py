from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from event.choices import choices as event_choices


class RegistrationTypeGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(event_choices.RegistrationTypeGroup.choices, status=status.HTTP_200_OK)


class RegistrationTypeSingleViewSet(RegistrationTypeGroupViewSet):

    def list(self, request) -> Response:
        return Response(event_choices.RegistrationTypeSingle.choices, status=status.HTTP_200_OK)


class GenderViewSet(RegistrationTypeGroupViewSet):

    def list(self, request) -> Response:
        return Response(event_choices.Gender.choices, status=status.HTTP_200_OK)


class LeaderTypesViewSet(RegistrationTypeGroupViewSet):

    def list(self, request) -> Response:
        return Response(event_choices.LeaderTypes.choices, status=status.HTTP_200_OK)


class FileTypeViewSet(RegistrationTypeGroupViewSet):

    def list(self, request) -> Response:
        return Response(event_choices.FileType.choices, status=status.HTTP_200_OK)


class FileExtensionViewSet(RegistrationTypeGroupViewSet):

    def list(self, request) -> Response:
        return Response(event_choices.FileExtension.choices, status=status.HTTP_200_OK)


class WorkshopTypeViewSet(RegistrationTypeGroupViewSet):

    def list(self, request) -> Response:
        return Response(event_choices.WorkshopType.choices, status=status.HTTP_200_OK)
