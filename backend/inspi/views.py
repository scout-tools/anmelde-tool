# views.py
import json

from django.db.models.functions import ExtractMonth, ExtractYear
from django.http import HttpResponse
from django_filters import FilterSet, BooleanFilter, OrderingFilter, \
    ModelMultipleChoiceFilter, NumberFilter, BaseInFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, viewsets, mixins, generics, \
    filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from datetime import date

from .models import Tag, Event, Message, Like, TagCategory, Image, \
    MaterialItem, ExperimentItem, Experiment, MaterialUnit, \
    MaterialName, MessageType, Faq, FaqRating, NextBestHeimabend, \
    ImageMeta, EventOfTheWeek
from .serializers import TagSerializer, EventSerializer, MessageSerializer, \
    LikeSerializer, HighscoreSerializer, EventItemSerializer, \
    TagCategorySerializer, StatisticSerializer, ImageSerializer, \
    MaterialItemSerializer, ExperimentItemSerializer, ExperimentSerializer, \
    TopViewsSerializer, EventAdminSerializer, EventTimestampSerializer, \
    MaterialUnitSerializer, MaterialNameSerializer, MessageTypeSerializer, \
    FaqSerializer, FaqRatingSerializer, ExperimentOverviewSerializer, \
    NextBestHeimabendSerializer, ImageMetaSerializer, EventOfTheWeekSerializer, \
    EventSitemapSerializer


class TagViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Tag.objects.all().order_by('sorting', 'name')
    serializer_class = TagSerializer

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
    queryset = TagCategory.objects.all().order_by('sorting', 'name')
    serializer_class = TagCategorySerializer

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
    prepairationTime__gt = NumberFilter(
        field_name='prepairation_time', lookup_expr='gt')
    prepairationTime__lt = NumberFilter(
        field_name='prepairation_time', lookup_expr='lt')
    prepairationTime = NumberFilter(field_name='prepairation_time')
    prepairationTime__in = _NumberInFilter(
        field_name='prepairation_time', lookup_expr='in')

    costsRating__gt = NumberFilter(
        field_name='costs_rating', lookup_expr='gt')
    costsRating__lt = NumberFilter(
        field_name='costs_rating', lookup_expr='lt')
    costsRating = NumberFilter(field_name='costs_rating')
    costsRating__in = _NumberInFilter(
        field_name='costs_rating', lookup_expr='in')

    executionTime__gt = NumberFilter(
        field_name='execution_time', lookup_expr='gt')
    executionTime__lt = NumberFilter(
        field_name='execution_time', lookup_expr='lt')
    executionTime = NumberFilter(field_name='execution_time')
    executionTime__in = _NumberInFilter(
        field_name='execution_time', lookup_expr='in')

    difficulty__gt = NumberFilter(
        field_name='difficulty', lookup_expr='gt')
    difficulty__lt = NumberFilter(
        field_name='difficulty', lookup_expr='lt')
    difficulty = NumberFilter(field_name='difficulty')
    difficulty__in = _NumberInFilter(
        field_name='difficulty', lookup_expr='in')

    is_public = BooleanFilter(field_name='is_public', method='get_is_public')
    withoutCosts = BooleanFilter(
        method='get_cost_rating', field_name='costs_rating')

    filterTags = ModelMultipleChoiceFilter(field_name='tags__id',
                                           to_field_name='id',
                                           queryset=Tag.objects.all(),
                                           method='get_tags')

    class Meta:
        model = Event
        fields = [
            'is_public',
            'withoutCosts',
            'filterTags',
            'executionTime__gt',
            'executionTime__lt',
            'executionTime',
            'executionTime__in',
            'prepairationTime__gt',
            'prepairationTime__lt',
            'prepairationTime',
            'prepairationTime__in',
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
            queryset = queryset.filter(
                tags__id__in=tags_category[filter_elements]).distinct()

        return queryset


class EventOfTheWeekFilter(FilterSet):
    past = BooleanFilter(field_name='release_date', method='get_past')

    class Meta:
        model = EventOfTheWeek
        fields = ['release_date']

    def get_past(self, queryset, field_name, value):
        if value:
            return queryset.filter(release_date__lte=date.today())
        return queryset


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventItemSerializer
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    filterset_class = EventFilter
    ordering = ['-created_at']
    ordering_fields = ['-created_at',
                       'created_at', 'title', '-like_score', '?']
    search_fields = ['title', 'description', 'tags__name', 'created_by']
    pagination_class = EventPagination

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return self.queryset.filter(is_public=True)
        else:
            return self.queryset


class EventItem(viewsets.ModelViewSet):
    serializer_class = EventItemSerializer

    def get_queryset(self):
        queryset = Event.objects.filter(pk=self.kwargs['event_id'])
        if not self.request.user.is_authenticated:
            return queryset.filter(is_public=True)
        else:
            return queryset


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('created_at')
    serializer_class = MessageSerializer


class LikeViewSet(mixins.CreateModelMixin, viewsets.ViewSetMixin,
                  generics.GenericAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class HighscoreView(mixins.ListModelMixin, viewsets.ViewSetMixin,
                    generics.GenericAPIView):
    queryset = Event.objects.values('created_by').distinct()
    serializer_class = HighscoreSerializer


class StatisticView(mixins.ListModelMixin, viewsets.ViewSetMixin,
                    generics.GenericAPIView):
    queryset = Event.objects.values(
        month=ExtractMonth('created_at')).annotate(
            year=ExtractYear('created_at')).values(
                'month', 'year').distinct().order_by(
                    'year', 'month')
    serializer_class = StatisticSerializer


class TopViewsView(viewsets.ViewSet):
    queryset = Event.objects.all()

    def list(self, data):
        serializer = TopViewsSerializer(self.queryset, many=True)
        serializer_data = sorted(
            serializer.data, key=lambda k: k['view_count'], reverse=True)[:10]

        return Response(serializer_data)


class ImageMetaView(viewsets.ModelViewSet,
                    generics.GenericAPIView):
    queryset = ImageMeta.objects.all()
    serializer_class = ImageMetaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event',)


class ImageView(viewsets.ModelViewSet, generics.GenericAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = ImageSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class MaterialItemViewSet(viewsets.ModelViewSet):
    queryset = MaterialItem.objects.all()
    serializer_class = MaterialItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event',)


class MaterialUnitViewSet(viewsets.ModelViewSet):
    queryset = MaterialUnit.objects.all()
    serializer_class = MaterialUnitSerializer


class MaterialNameViewSet(viewsets.ModelViewSet):
    queryset = MaterialName.objects.order_by('name').all()
    serializer_class = MaterialNameSerializer


class MessageTypeViewSet(viewsets.ModelViewSet):
    queryset = MessageType.objects.all()
    serializer_class = MessageTypeSerializer


class ExperimentViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer


class ExperimentOverviewViewSet(viewsets.ModelViewSet):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentOverviewSerializer


class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer


class FaqRatingViewSet(viewsets.ModelViewSet):
    queryset = FaqRating.objects.all()
    serializer_class = FaqRatingSerializer


class ExperimentItemViewSet(viewsets.ModelViewSet):
    queryset = ExperimentItem.objects.all()
    serializer_class = ExperimentItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = ExperimentItemSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            event = data['event']
            score = data['score']
            if (score == 0):
                total_ratings = ExperimentItem.objects.filter(
                    event=event).count()
                unclear_ratings = ExperimentItem.objects.filter(
                    event=event).filter(
                        score=0).count()
                if (total_ratings >= 1):
                    unclear_rate = unclear_ratings / total_ratings
                    if (unclear_rate >= 0.3):
                        event = Event.objects.filter(id=event)
                        event.update(is_public=False)
                        Event.objects.get(id=event).tags.add(
                            Tag.objects.get(id=70))

        return super().create(request, *args, **kwargs)


class RandomEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_public=True).order_by("?")[:10]
    serializer_class = EventSerializer


class AdminEventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.order_by('-created_at').all()
    serializer_class = EventAdminSerializer


class EventSitemapViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSitemapSerializer


class EventTimestampViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_public=True).order_by('created_at')
    serializer_class = EventTimestampSerializer


class ChangePublishStatus(APIView):
    def post(self, request, *args, **kwargs):
        posted_data = self.request.data
        set_active = posted_data['set_active']
        event_id = posted_data['event']

        event = Event.objects.filter(id=event_id)
        event.update(is_public=set_active)

        return_data = [
            {"worked": True}
        ]
        return Response(status=200, data=return_data)


class NextBestHeimabendViewSet(viewsets.ModelViewSet):
    queryset = NextBestHeimabend.objects.order_by("score").all()
    serializer_class = NextBestHeimabendSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('event',)


class EventOfTheWeekViewSet(viewsets.ModelViewSet):
    queryset = EventOfTheWeek.objects.order_by("release_date").all()
    serializer_class = EventOfTheWeekSerializer
    filterset_class = EventOfTheWeekFilter
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    ordering = ['release_date']
    ordering_fields = ['-release_date',
                       'release_date']


class MaterialItems(APIView):
    def post(self, request, *args, **kwargs):
        posted_data = self.request.data
        return_array = []
        for item in posted_data:

            material_name_count = MaterialName.objects.filter(
                name=item['name']
            ).count()

            if (material_name_count == 0):
                material_name_new = MaterialName.objects.create(
                    name=item['name']
                )
                material_name_new.save()

            material_name_obj = MaterialName.objects.filter(
                name=item['name']
            ).first()

            if (item['id'] > 0):
                material_item = MaterialItem.objects.filter(
                    id=item['id']
                )

                material_item.update(
                    quantity=item['quantity'],
                    material_name_id=material_name_obj.id,
                    event_id=item['event_id'],
                    material_unit_id=item['unit_id']
                )
                return_array.append(item['id'])
            else:
                new_obj = MaterialItem.objects.create(
                    quantity=item['quantity'],
                    material_name_id=material_name_obj.id,
                    material_unit_id=item['unit_id'],
                    event_id=item['event_id']
                )
                new_obj.save()

                return_array.append(new_obj.id)

        return_data = [
            {"material_event_ids": return_array}
        ]
        return Response(status=200, data=return_data)
