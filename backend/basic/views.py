from django.db.models import Q, QuerySet
from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import basic.choices
from basic import models as basic_models
from basic import serializers as basic_serializers
from basic.permissions import IsStaffOrReadOnly


class ScoutHierarchyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = basic_models.ScoutHierarchy.objects.all().exclude(level=6)
    serializer_class = basic_serializers.ScoutHierarchySerializer


class ZipCodeSearchFilter(FilterSet):
    zip_city = CharFilter(field_name='zip_city', method='get_zip_city')

    class Meta:
        model = basic_models.ZipCode
        fields = ['zip_code', 'city', 'id']

    def get_zip_city(self, queryset, field_name, value) -> QuerySet[basic_models.ZipCode]:
        cities = queryset.filter(Q(zip_code__contains=value) | Q(city__contains=value))
        if cities.count() > 250:
            raise PermissionDenied('Too many results!!!')
        return cities


class ZipCodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = basic_models.ZipCode.objects.all()
    serializer_class = basic_serializers.ZipCodeSerializer
    filterset_class = ZipCodeSearchFilter


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsStaffOrReadOnly]
    queryset = basic_models.Tag.objects.all()
    serializer_class = basic_serializers.TagShortSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type', 'type__name']
    search_fields = ['type__name', 'name']


class TagTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    queryset = basic_models.TagType.objects.all()
    serializer_class = basic_serializers.TagTypeShortSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['name', ]
    ordering_fields = ['id', ]


class AttributeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = basic_models.AbstractAttribute.objects.all()

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return basic_serializers.AbstractAttributePostPolymorphicSerializer
        else:
            return basic_serializers.AbstractAttributeGetPolymorphicSerializer


class DescriptionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = basic_serializers.DescriptionSerializer

    def get_queryset(self) -> QuerySet:
        if self.basename == 'faq':
            return basic_models.Description.objects.filter(public=True, type=basic.choices.DescriptionType.FAQ)
        elif self.basename == 'privacy':
            return basic_models.Description.objects.filter(public=True, type=basic.choices.DescriptionType.Privacy)
        else:
            raise NotFound


class TravelTypeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(basic.choices.TravelType.choices, status=status.HTTP_200_OK)


class TravelSlotsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        return Response(basic.choices.TravelSlots.choices, status=status.HTTP_200_OK)


class AttributeTypeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def inheritors(self, klass) -> [str]:
        subclasses = set()
        work = [klass]
        while work:
            parent = work.pop()
            for child in parent.__subclasses__():
                if child not in subclasses:
                    subclasses.add(child.__name__)
                    work.append(child)
        return subclasses

    def list(self, request) -> Response:
        choices = self.inheritors(basic_models.AbstractAttribute)
        return Response(choices, status=status.HTTP_200_OK)


class EatHabitViewSet(viewsets.ModelViewSet):
    queryset = basic_models.EatHabit.objects.all()
    serializer_class = basic_serializers.EatHabitSerializer
    permission_classes = [IsAuthenticated]


class FrontendThemeViewSet(viewsets.ModelViewSet):
    queryset = basic_models.FrontendTheme.objects.all()
    serializer_class = basic_serializers.FrontendThemeSerializer
    permission_classes = [IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = basic_models.Message.objects.all().order_by('created_at')
    serializer_class = basic_serializers.MessageSerializer

class MessageTypeViewSet(viewsets.ModelViewSet):
    queryset = basic_models.MessageType.objects.all()
    serializer_class = basic_serializers.MessageTypeSerializer