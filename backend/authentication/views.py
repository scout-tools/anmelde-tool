from rest_framework import status, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, QuerySet
from django_filters import CharFilter

from .models import UserExtended, EmailNotificationType
from .serializers import UserExtendedGetSerializer, UserExtendedPostSerializer, GroupSerializer, EmailSettingsSerializer, ResponseablePersontSerializer
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.filters import SearchFilter
from basic.api_exceptions import TooManySearchResults, NoSearchResults, NoSearchValue

from basic.permissions import IsStaffOrReadOnly

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


class ResponseablePersonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = ResponseablePersontSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__email', 'scout_name',]

    def list(self, request):
        queryset = UserExtended.objects.all()
        search_param = request.GET.get('search')
        queryset = queryset.filter(Q(scout_name__contains=search_param) | Q(user__email__contains=search_param) | Q(scout_organisation__name__contains=search_param))
        serializer = ResponseablePersontSerializer(queryset, many=True)
        response_len = len(serializer.data)
        if response_len > 10:
            raise TooManySearchResults
        elif response_len == 0:
            raise NoSearchResults
        return Response(serializer.data)

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
