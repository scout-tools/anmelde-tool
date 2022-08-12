import uuid

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, \
    MinValueValidator, MinLengthValidator, MaxLengthValidator

from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _
from stdimage import JPEGField


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    updated_by = models.CharField(max_length=20, blank=True, null=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        abstract = True


class TagCategory(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    sorting = models.IntegerField(blank=False, unique=True)
    icon = models.CharField(max_length=20, blank=True, null=True)
    is_header = models.BooleanField(default=False)
    is_mandatory = models.BooleanField(default=False)
    is_event_overview = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class MaterialUnit(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class MaterialName(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100, blank=True)
    unit_detaults = models.ForeignKey(MaterialUnit, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Tag(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=7)
    icon = models.CharField(max_length=20, blank=True, null=True)
    category = models.ForeignKey(
        TagCategory, on_delete=models.PROTECT, blank=True, null=True)
    sorting = models.IntegerField(blank=False, unique=False, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


def nameFile(instance, filename):
    return 'images/' + str(uuid.uuid1()) + '.jpeg'


class Image(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    image = JPEGField(upload_to=nameFile, blank=True, variations={
        'big': (800, 600),
        'default': (400, 266),
        'small': (200, 133)
    }, delete_orphans=True)

    def __str__(self):
        return '{}'.format(self.id)

    def __repr__(self):
        return self.__str__()


class Event(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=40, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(40)])
    description = models.CharField(
        max_length=8000,
        default='',
        validators=[MaxLengthValidator(8000)])
    description_detail = models.CharField(max_length=1, default='')
    tags = models.ManyToManyField(Tag, default='')
    costs_rating = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    execution_time = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    prepairation_time = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    difficulty = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_by_email = models.CharField(max_length=60, blank=True)
    like_score = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.__str__()


class ImageMeta(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    description = models.CharField(max_length=255)
    is_open_source = models.BooleanField(default=False)
    privacy_consent = models.BooleanField(default=False)
    photographer_name = models.CharField(max_length=100, default='', blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, blank=True, null=True)
    event = models.ForeignKey(
        Event,
        related_name='event_id',
        on_delete=models.CASCADE,
        blank=True,
        null=True)


class MaterialItem(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    quantity = models.IntegerField(default=0)
    number_of_participants = models.IntegerField(default=0, blank=True)
    material_name = models.ForeignKey(MaterialName, on_delete=models.PROTECT)
    material_unit = models.ForeignKey(MaterialUnit, on_delete=models.PROTECT)
    event = models.ForeignKey(Event, related_name='material_list', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.material_name

    def __repr__(self):
        return self.__str__()


class MessageType(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30)
    is_comment = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True)
    sorting = models.IntegerField(blank=False, auto_created=True, unique=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Message(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    created_by_email = models.CharField(max_length=60, blank=True, null=True)
    message_type = models.ForeignKey(
        MessageType, on_delete=models.CASCADE, blank=True, null=True)
    message_body = models.CharField(max_length=1000)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, blank=True, null=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return self.message_body

    def __repr__(self):
        return self.__str__()


class Like(TimeStampMixin):
    class OptionType(models.IntegerChoices):
        LIKE = 1, _('Like'),
        DISLIKE = -1, _('Dislike'),

    id = models.AutoField(auto_created=True, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    opinion_type_id = models.IntegerField(choices=OptionType.choices, default=OptionType.LIKE)
    like_created = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        super(Like, self).save(*args, **kwargs)
        if self.id:
            query = Like.objects.filter(event=self.event).all().aggregate(sum=Sum('opinion_type_id'))
            likes = query['sum']

            if likes is None:
                likes = 0

            if likes < 3:
                likescore = 0
            elif likes < 10:
                likescore = 1
            elif likes < 20:
                likescore = 2
            elif likes >= 20:
                likescore = 3
            else:
                likescore = 0

            event = Event.objects.filter(id=self.event.id).first()
            event.like_score = likescore
            event.save()


class Experiment(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    age_level = models.IntegerField(blank=False, unique=False, null=True)
    group_type = models.IntegerField(blank=False, unique=False, null=True)
    group_leader = models.IntegerField(blank=False, unique=False, null=True)

    def __str__(self):
        return f'{self.id} {self.age_level} {self.group_type} {self.group_leader}'

    def __repr__(self):
        return self.__str__()


class ExperimentItem(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    score = models.IntegerField(blank=False, unique=False, null=True)

    def __str__(self):
        return f'{self.event} {self.experiment} {self.score}'

    def __repr__(self):
        return self.__str__()


class Faq(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    question = models.CharField(max_length=1000, blank=True, null=True)
    answer = models.CharField(max_length=2000, blank=True, null=True)
    sorting = models.IntegerField(blank=False, auto_created=True, unique=True, null=True)

    def __str__(self):
        return self.question

    def __repr__(self):
        return self.__str__()


class FaqRating(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    faq = models.ForeignKey(Faq, on_delete=models.CASCADE)
    useful_score = models.SmallIntegerField(default=1, validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return self.faq

    def __repr__(self):
        return self.__str__()


class NextBestHeimabend(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    event = models.ForeignKey(Event, related_name='ref', on_delete=models.CASCADE)
    event_score = models.ForeignKey(Event, related_name='score', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.event, self.event_score)

    def __repr__(self):
        return self.__str__()


class EventOfTheWeek(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    release_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, default='')
    comment = models.CharField(max_length=2000, blank=True, null=True)

    def save(self, *args, **kwargs):
        if EventOfTheWeek.objects.exclude(pk=self.pk).filter(release_date=self.release_date).exists():
            raise ValidationError('An dem Montag existier bereits ein Heimabend der Woche.')
        if EventOfTheWeek.objects.exclude(pk=self.pk).filter(event_id=self.event_id).exists():
            raise ValidationError('Dieser Heimabend wurde bereits ausgewählt.')

        super(EventOfTheWeek, self).save(*args, **kwargs)

    def __str__(self):
        return '{} - {}'.format(self.event, self.release_date)

    def __repr__(self):
        return self.__str__()
