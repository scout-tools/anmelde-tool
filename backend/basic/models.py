from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils.translation import gettext_lazy as _


class TravelType(models.TextChoices):
    Train = 'T', _('Bahn')
    Bus = 'B', _('Reisebus')
    Car = 'C', _('PKW')
    Other = 'O', _('Sonstiges')


class TravelSlots(models.TextChoices):
    Early = 'E', _('16:00-18:00')
    Normal = 'N', _('18:00-20:00')
    Late = 'L', _('20:00-22:00')
    SuperLate = 'SL', _('22:00-24:00')
    Other = 'O', _('Noch Später')


class DescriptionType(models.TextChoices):
    FAQ = 'FAQ', _('FAQ')
    Privacy = 'P', _('Datenschutz')
    LegalNotice = 'LN', _('Impressum')


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class ZipCode(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=60, blank=True)
    lat = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)
    lon = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)

    def __str__(self):
        return f"{self.zip_code} {self.city}"


class TagType(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    color = ColorField(default='#FF0000')
    min = models.IntegerField(default=0)
    max = models.IntegerField(default=9999)

    def __str__(self):
        return self.name


class AttributeDescription(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    header = models.CharField(max_length=1000, blank=True)
    name = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    type = models.ForeignKey(TagType, null=True, blank=False, on_delete=models.PROTECT)
    is_custom = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.type}: {self.name}'


class AbstractAttribute(PolymorphicModel):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    type = models.ForeignKey(TagType, null=True, blank=False, on_delete=models.PROTECT)
    template = models.BooleanField(default=False)
    template_id = models.IntegerField(default=-1)

    def __str__(self):
        return f'{self.type}: {self.name}'


class BooleanAttribute(AbstractAttribute):
    boolean_field = models.BooleanField(default=False)


class TimeAttribute(AbstractAttribute):
    date_field = models.DateTimeField()


class IntegerAttribute(AbstractAttribute):
    integer_field = models.IntegerField(default=0)


class FloatAttribute(AbstractAttribute):
    float_field = models.FloatField()


class StringAttribute(AbstractAttribute):
    string_field = models.CharField(max_length=10000, blank=True, null=True)


class TravelAttribute(AbstractAttribute):
    type_field = models.CharField(max_length=1, choices=TravelType.choices, null=True, blank=True)
    time_field = models.CharField(max_length=2, choices=TravelSlots.choices, null=True, blank=True)


class ScoutOrgaLevel(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class ScoutHierarchy(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    level = models.ForeignKey(ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=60, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.PROTECT, related_name='scouthierarchy', blank=True)
    abbreviation = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.level} - {self.name}"


class Description(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    public = models.BooleanField(default=False)
    question = models.CharField(max_length=250, null=True, blank=True)
    answer = models.CharField(max_length=10000, null=True, blank=True)
    type = models.CharField(max_length=3, choices=DescriptionType.choices, default=DescriptionType.FAQ)

    def __str__(self):
        return f'{self.get_type_display()}: {self.question}'
