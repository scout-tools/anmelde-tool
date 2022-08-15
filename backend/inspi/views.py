from datetime import date

from django.db.models.functions import ExtractMonth, ExtractYear
from django_filters import FilterSet, BooleanFilter, ModelMultipleChoiceFilter, NumberFilter, BaseInFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets, mixins, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from inspi import models as inspi_models
from inspi import serializers as inspi_serializers


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = inspi_models.Tag.objects.all().order_by('sorting', 'name')
    serializer_class = inspi_serializers.TagSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.filter(is_public=True)
        else:
            return self.queryset

    def create(self, request, pk=None, partial=False):
        return super().create(request, pk, partial=partial)

    def update(self, request, pk=None, partial=False):
        return super().update(request, pk, partial=partial)


class TagCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = inspi_models.TagCategory.objects.all().order_by('sorting', 'name')
    serializer_class = inspi_serializers.TagCategorySerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.filter(is_public=True)
        else:
            return self.queryset

    def create(self, request, pk=None, partial=False):
        return super().create(request, pk, partial=partial)

    def update(self, request, pk=None, partial=False):
        return super().update(request, pk, partial=partial)


class EventPagination(pagination.PageNumberPagination):
    page_size = 3
    page_size_query_param = 'limit'
    max_page_size = 1000


class _NumberInFilter(BaseInFilter, NumberFilter):
    pass


class EventFilter(FilterSet):
    preparationTime__gt = NumberFilter(field_name='preparation_time', lookup_expr='gt')
    preparationTime__lt = NumberFilter(field_name='preparation_time', lookup_expr='lt')
    preparationTime = NumberFilter(field_name='preparation_time')
    preparationTime__in = _NumberInFilter(field_name='preparation_time', lookup_expr='in')

    costsRating__gt = NumberFilter(field_name='costs_rating', lookup_expr='gt')
    costsRating__lt = NumberFilter(field_name='costs_rating', lookup_expr='lt')
    costsRating = NumberFilter(field_name='costs_rating')
    costsRating__in = _NumberInFilter(field_name='costs_rating', lookup_expr='in')

    executionTime__gt = NumberFilter(field_name='execution_time', lookup_expr='gt')
    executionTime__lt = NumberFilter(field_name='execution_time', lookup_expr='lt')
    executionTime = NumberFilter(field_name='execution_time')
    executionTime__in = _NumberInFilter(field_name='execution_time', lookup_expr='in')

    difficulty__gt = NumberFilter(field_name='difficulty', lookup_expr='gt')
    difficulty__lt = NumberFilter(field_name='difficulty', lookup_expr='lt')
    difficulty = NumberFilter(field_name='difficulty')
    difficulty__in = _NumberInFilter(field_name='difficulty', lookup_expr='in')

    is_public = BooleanFilter(field_name='is_public', method='get_is_public')
    withoutCosts = BooleanFilter(method='get_cost_rating', field_name='costs_rating')

    filterTags = ModelMultipleChoiceFilter(field_name='tags__id',
                                           to_field_name='id',
                                           queryset=inspi_models.Tag.objects.all(),
                                           method='get_tags')

    class Meta:
        model = inspi_models.Activity
        fields = [
            'is_public',
            'withoutCosts',
            'filterTags',
            'executionTime__gt',
            'executionTime__lt',
            'executionTime',
            'executionTime__in',
            'preparationTime__gt',
            'preparationTime__lt',
            'preparationTime',
            'preparationTime__in',
            'costsRating__gt',
            'costsRating__lt',
            'costsRating',
            'costsRating__in',
            'difficulty__gt',
            'difficulty__lt',
            'difficulty',
            'difficulty__in',
        ]

    def get_CostRating(self, queryset, field_name, value):
        if value:
            return queryset.filter(costs_rating=0)
        return queryset

    def get_is_public(self, queryset, field_name, value):
        if not value:
            if self.request.user.is_authenticated:
                return queryset.filter(is_public=value)
        return queryset.filter(is_public=True)

    def get_tags(self, queryset, field_name, value):
        tags_category = dict()

        for val in value:
            tags_category.setdefault(str(val.category.id), []).append(val.id)

        for filter_elements in tags_category:
            queryset = queryset.filter(tags__id__in=tags_category[filter_elements]).distinct()

        return queryset


class EventOfTheWeekFilter(FilterSet):
    past = BooleanFilter(field_name='release_date', method='get_past')

    class Meta:
        model = inspi_models.EventOfTheWeek
        fields = ['release_date']

    def get_past(self, queryset, field_name, value):
        if value:
            return queryset.filter(release_date__lte=date.today())
        return queryset


class EventViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Activity.objects.all()
    serializer_class = inspi_serializers.EventItemSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_class = EventFilter
    ordering = ['-created_at']
    ordering_fields = ['-created_at', 'created_at', 'title', '-like_score', '?']
    search_fields = ['title', 'description', 'tags__name', 'created_by']
    pagination_class = EventPagination

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.filter(is_public=True)
        else:
            return self.queryset


class LikeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = inspi_models.Like.objects.all()
    serializer_class = inspi_serializers.LikeSerializer


class HighscoreViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = inspi_models.Activity.objects.values('created_by').distinct()
    serializer_class = inspi_serializers.HighscoreSerializer


class StatisticViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = inspi_models.Activity.objects.values(
        month=ExtractMonth('created_at')).annotate(
        year=ExtractYear('created_at')).values('month', 'year').distinct().order_by('year', 'month')
    serializer_class = inspi_serializers.StatisticSerializer


class TopViewsViewSet(viewsets.ViewSet):
    queryset = inspi_models.Activity.objects.all()

    def list(self, data):
        serializer = inspi_serializers.TopViewsSerializer(self.queryset, many=True)
        serializer_data = sorted(serializer.data, key=lambda k: k['view_count'], reverse=True)[:10]

        return Response(serializer_data)


class ImageMetaViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.ImageMeta.objects.all()
    serializer_class = inspi_serializers.ImageMetaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event',)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Image.objects.all()
    serializer_class = inspi_serializers.ImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = inspi_serializers.ImageSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialItemViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.MaterialItem.objects.all()
    serializer_class = inspi_serializers.MaterialItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event',)


class MaterialUnitViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.MaterialUnit.objects.all()
    serializer_class = inspi_serializers.MaterialUnitSerializer


class MaterialNameViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.MaterialName.objects.order_by('name').all()
    serializer_class = inspi_serializers.MaterialNameSerializer


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Experiment.objects.all()
    serializer_class = inspi_serializers.ExperimentSerializer


class ExperimentOverviewViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Experiment.objects.all()
    serializer_class = inspi_serializers.ExperimentOverviewSerializer


class ExperimentItemViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.ExperimentItem.objects.all()
    serializer_class = inspi_serializers.ExperimentItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = inspi_serializers.ExperimentItemSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            event = data['event']
            score = data['score']
            if score == 0:
                total_ratings = inspi_models.ExperimentItem.objects.filter(event=event).count()
                unclear_ratings = inspi_models.ExperimentItem.objects.filter(event=event).filter(score=0).count()
                if total_ratings >= 1:
                    unclear_rate = unclear_ratings / total_ratings
                    if unclear_rate >= 0.3:
                        event = inspi_models.Activity.objects.filter(id=event)
                        event.update(is_public=False)
                        inspi_models.Activity.objects.get(id=event).tags.add(inspi_models.Tag.objects.get(id=70))

        return super().create(request, *args, **kwargs)


class RandomEventViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Activity.objects.filter(is_public=True).order_by("?")[:10]
    serializer_class = inspi_serializers.EventSerializer


class AdminEventViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Activity.objects.order_by('-created_at').all()
    serializer_class = inspi_serializers.EventAdminSerializer


class EventSitemapViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Activity.objects.all()
    serializer_class = inspi_serializers.EventSitemapSerializer


class EventTimestampViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.Activity.objects.filter(is_public=True).order_by('created_at')
    serializer_class = inspi_serializers.EventTimestampSerializer


class ChangePublishStatusViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        worked = False
        set_active = self.request.data.get('set_active', False)
        event_id = self.request.data.get('event', None)

        if event_id:
            event: inspi_models.Activity = get_object_or_404(inspi_models.Activity, id=event_id)
            event.is_public = set_active
            event.save()
            worked = True

        return Response({"worked": worked}, status=status.HTTP_200_OK)


class NextBestHeimabendViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.NextBestHeimabend.objects.order_by("score").all()
    serializer_class = inspi_serializers.NextBestHeimabendSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event',)


class EventOfTheWeekViewSet(viewsets.ModelViewSet):
    queryset = inspi_models.EventOfTheWeek.objects.order_by("release_date").all()
    serializer_class = inspi_serializers.EventOfTheWeekSerializer
    filterset_class = EventOfTheWeekFilter
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    ordering = ['release_date']
    ordering_fields = ['-release_date', 'release_date']


class MaterialItemsViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    def create(self, request, *args, **kwargs):
        posted_data = self.request.data
        return_array = []
        for item in posted_data:
            material_name_count = inspi_models.MaterialName.objects.filter(name=item['name']).count()

            if material_name_count == 0:
                material_name_new = inspi_models.MaterialName.objects.create(name=item['name'])
                material_name_new.save()

            material_name_obj = inspi_models.MaterialName.objects.filter(name=item['name']).first()

            if item['id'] > 0:
                material_item = inspi_models.MaterialItem.objects.filter(id=item['id'])
                material_item.update(
                    quantity=item['quantity'],
                    material_name_id=material_name_obj.id,
                    event_id=item['event_id'],
                    material_unit_id=item['unit_id']
                )
                return_array.append(item['id'])
            else:
                new_obj = inspi_models.MaterialItem.objects.create(
                    quantity=item['quantity'],
                    material_name_id=material_name_obj.id,
                    material_unit_id=item['unit_id'],
                    event_id=item['event_id']
                )
                new_obj.save()
                return_array.append(new_obj.id)

        return Response({"material_event_ids": return_array}, status=status.HTTP_200_OK)
