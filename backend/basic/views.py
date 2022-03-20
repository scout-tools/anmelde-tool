from django.db.models import Q
from django_filters import CharFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import ScoutHierarchy, ZipCode, Tag, TagType, AbstractAttribute, Description, DescriptionType
from .serializers import ScoutHierarchySerializer, ZipCodeSerializer, TagShortSerializer, TagTypeShortSerializer, \
    AbstractAttributeGetPolymorphicSerializer, DescriptionSerializer


class ScoutHierarchyViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ScoutHierarchy.objects.all().exclude(level=6)
    serializer_class = ScoutHierarchySerializer


class ZipCodeSearchFilter(FilterSet):
    zip_city = CharFilter(field_name='zip_city', method='get_zip_city')

    class Meta:
        model = ZipCode
        fields = ['zip_code', 'city', 'id']

    def get_zip_city(self, queryset, field_name, value):
        cities = queryset.filter(Q(zip_code__contains=value) | Q(city__contains=value))
        if cities.count() > 250:
            raise PermissionDenied('Too many results!!!')
        return cities


class ZipCodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ZipCode.objects.all()
    serializer_class = ZipCodeSerializer
    filterset_class = ZipCodeSearchFilter


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagShortSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['type', 'type__name']
    search_fields = ['type__name', 'name']


class TagTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = TagType.objects.all()
    serializer_class = TagTypeShortSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['name', ]
    ordering_fields = ['id', ]


class AttributeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = AbstractAttribute.objects.all()
    serializer_class = AbstractAttributeGetPolymorphicSerializer


class DescriptionViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = DescriptionSerializer

    def get_queryset(self):
        if self.basename == 'faq':
            return Description.objects.filter(public=True, type=DescriptionType.FAQ)
        elif self.basename == 'legal':
            return Description.objects.filter(public=True, type=DescriptionType.LegalNotice)
        elif self.basename == 'privacy':
            return Description.objects.filter(public=True, type=DescriptionType.Privacy)
        else:
            raise NotFound
