# serializers.py
from rest_framework import serializers
from .models import Tag, Event, Message, Like, TagCategory, \
    Image, MaterialItem, \
    ExperimentItem, Experiment, MaterialUnit, MaterialName, MessageType, \
    Faq, FaqRating, NextBestHeimabend, ImageMeta, EventOfTheWeek
from rest_framework.serializers import Serializer, FileField
from django.core.cache import cache
from django.db.models import Sum
from datetime import date, timedelta
from django.utils import timezone


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'description',
            'color',
            'icon',
            'category',
            'is_public',
            'sorting'
        )


class TagCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TagCategory
        fields = (
            'id',
            'name',
            'description',
            'sorting',
            'icon',
            'is_public',
            'is_header',
            'is_mandatory',
            'is_event_overview'
        )


class MaterialItemSerializer(serializers.ModelSerializer):
    material_unit_str = serializers.ReadOnlyField(source='material_unit.name')
    material_name_str = serializers.ReadOnlyField(source='material_name.name')

    class Meta:
        model = MaterialItem
        fields = (
            'id',
            'quantity',
            'material_unit_str',
            'material_name_str',
            'material_name',
            'material_unit',
            'event'
        )


class LikeSerializer(serializers.ModelSerializer):
    current_median = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = (
            'event',
            'opinion_type_id',
            'like_created',
            'current_median'
        )

    def get_current_median(self, obj):
        # return getmedian()
        return 0


def getmedian():
    median = cache.get('median')
    if median is None:
        query = Like.objects.values("event__id").annotate(
            sum=Sum('opinion_type_id')).order_by('sum')
        median = query[int(query.count() / 2)]['sum']
        cache.set('median', median, timeout=12 * 60 * 60)
    return median


class EventSerializer(serializers.ModelSerializer):
    header_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'tags',
            'header_image',
            'costs_rating',
            'execution_time',
            'prepairation_time',
            'created_by',
            'created_at',
            'is_public')

    def get_header_image(self, obj):
        qs = ImageMeta.objects.filter(event_id=obj.id).first()
        serializer = ImageMetaSerializer(instance=qs)
        if ('id' in serializer.data):
            return serializer.data
        return None


class ImageMetaSerializer(serializers.ModelSerializer):
    image_uuid = serializers.SerializerMethodField(read_only=True)
    image_id = serializers.SerializerMethodField(read_only=True)
    event_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ImageMeta
        fields = (
            'image_uuid',
            'id',
            'description',
            'is_open_source',
            'privacy_consent',
            'photographer_name',
            'uploaded_at',
            'image',
            'image_id',
            'event',
            'event_id'
        )

    def get_image_uuid(self, obj):
        qs = Image.objects.filter(id=obj.image_id).first()
        serializer = ImageSerializer(instance=qs)
        return serializer.data

    def get_event_id(self, obj):
        if (obj.event):
            if (obj.event.id):
                return obj.event.id
        return None

    def get_image_id(self, obj):
        if (obj.image):
            if (obj.image.id):
                return obj.image.id
        return None


class EventItemSerializer(serializers.ModelSerializer):
    header_image = serializers.SerializerMethodField(read_only=True)
    material_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'tags',
            'material_list',
            'header_image',
            'costs_rating',
            'execution_time',
            'prepairation_time',
            'difficulty',
            'created_by',
            'created_by_email',
            'updated_by',
            'created_at',
            'updated_at',
            'is_public',
            'like_score')

    def get_header_image(self, obj):
        qs = ImageMeta.objects.filter(event_id=obj.id).first()
        serializer = ImageMetaSerializer(instance=qs)
        if ('id' in serializer.data):
            return serializer.data
        return None

    def get_material_list(self, obj):
        qs = MaterialItem.objects.filter(event_id=obj.id)
        serializer = MaterialItemSerializer(instance=qs, many=True)
        return serializer.data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class HighscoreSerializer(serializers.ModelSerializer):
    highscore = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'created_by',
            'highscore',
        )

    def get_highscore(self, obj):
        score = Event.objects.filter(created_by=obj['created_by']).count()
        return score


class StatisticSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    score_cumulative = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'score',
            'score_cumulative',
            'month',
            'year'
        )

    def get_score(self, obj):
        score = Event.objects.filter(
            created_at__year__exact=obj['year'],
            created_at__month__exact=obj['month']).count()
        return score

    def get_score_cumulative(self, obj):
        score = Event.objects.filter(
            created_at__year__lte=obj['year'],
            created_at__month__lte=obj['month']).count()
        return score

    def get_month(self, obj):
        return obj['month']

    def get_year(self, obj):
        return obj['year']


class ImageSerializer(serializers.ModelSerializer):
    image_uuid = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = (
            'id',
            'image_uuid',
            'image',
        )

    def get_image_uuid(self, obj):
        xx = obj.image.name.split('/')[1]
        xxx = xx.split('.')[0]
        return xxx


class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = '__all__'


class ExperimentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperimentItem
        fields = '__all__'


class ExperimentOverviewSerializer(serializers.ModelSerializer):
    event_counter = serializers.SerializerMethodField()
    experiment_item = serializers.SerializerMethodField()

    class Meta:
        model = Experiment
        fields = (
            'id',
            'created_at',
            'age_level',
            'group_type',
            'group_leader',
            'event_counter',
            'experiment_item',
        )

    def get_event_counter(self, obj):
        return ExperimentItem.objects.filter(experiment__id=obj.id).count()

    def get_experiment_item(self, obj):
        return ExperimentItem.objects.filter(
            experiment__id=obj.id
        ).values('score', 'event__title')


class TopViewsSerializer(serializers.ModelSerializer):
    view_count = serializers.SerializerMethodField()
    header_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'view_count',
            'title',
            'tags',
            'created_by',
            'header_image',
            'description')

    def get_header_image(self, obj):
        qs = ImageMeta.objects.filter(event_id=obj.id).first()
        serializer = ImageMetaSerializer(instance=qs)
        if ('id' in serializer.data):
            return serializer.data
        return None

    def get_view_count(self, obj):
        ## some_day_last_week = timezone.now().date() - timedelta(days=90)
        view_count = 6  # TODO: Implement

        return view_count


class EventAdminSerializer(serializers.ModelSerializer):
    view_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'tags',
            'created_by',
            'created_by_email',
            'updated_by',
            'created_at',
            'updated_at',
            'is_public',
            'like_score',
            'view_count')

    def get_view_count(self, obj):
        ## some_day_last_week = timezone.now().date() - timedelta(days=90)
        view_count = 5  # ToDO: Implement

        return view_count


class EventSitemapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'title')


class EventTimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            'created_at')


class MaterialUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialUnit
        fields = '__all__'


class MaterialNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialName
        fields = '__all__'


class MessageTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageType
        fields = '__all__'


class FaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faq
        fields = '__all__'


class FaqRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaqRating
        fields = '__all__'


class NextBestHeimabendSerializer(serializers.ModelSerializer):
    header_image = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    class Meta:
        model = NextBestHeimabend
        fields = (
            'event',
            'event_score',
            'score',
            'header_image',
            'title',
            'description',
            'tags',
            'id',
        )

    def get_id(self, obj):
        id = Event.objects.filter(id=obj.event_score.id).values('id').first()
        return id['id']

    def get_title(self, obj):
        title = Event.objects.filter(
            id=obj.event_score.id).values('title').first()
        return title['title']

    def get_description(self, obj):
        title = Event.objects.filter(
            id=obj.event_score.id).values('description').first()
        return title['description']

    def get_header_image(self, obj):
        qs = ImageMeta.objects.filter(event_id=obj.event_score.id).first()
        serializer = ImageMetaSerializer(instance=qs)
        if ('id' in serializer.data):
            return serializer.data
        return None

    def get_tags(self, obj):
        return_tags = []
        tags = Event.objects.filter(id=obj.event_score.id).values('tags')
        for tag in tags:
            return_tags.append(tag['tags'])
        return return_tags


class EventOfTheWeekSerializer(serializers.ModelSerializer):
    event_obj = serializers.SerializerMethodField()
    history = serializers.SerializerMethodField()
    header_image = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = EventOfTheWeek
        fields = (
            'id',
            'release_date',
            'event',
            'event_obj',
            'history',
            'comment',
            'header_image',
            'title',
            'description',
            'tags',
        )

    def get_event_obj(self, obj):
        event = []
        if obj.event.id:
            event = Event.objects.filter(id=obj.event.id).values(
                'title',
                'created_by',
            )
        return event[0]

    def get_history(self, obj):
        return date.today() >= obj.release_date

    def get_title(self, obj):
        title = Event.objects.filter(
            id=obj.event.id).values('title').first()
        return title['title']

    def get_description(self, obj):
        title = Event.objects.filter(
            id=obj.event.id).values('description').first()
        return title['description']

    def get_header_image(self, obj):
        qs = ImageMeta.objects.filter(event_id=obj.event.id).first()
        serializer = ImageMetaSerializer(instance=qs)
        if ('id' in serializer.data):
            return serializer.data
        return None

    def get_tags(self, obj):
        return_tags = []
        tags = Event.objects.filter(id=obj.event.id).values('tags')
        for tag in tags:
            return_tags.append(tag['tags'])
        return return_tags
