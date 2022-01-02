from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from polymorphic.models import PolymorphicModel


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

    def __str__(self):
        return self.name


class AttributeDescription(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    header = models.CharField(max_length=1000, blank=True)
    name = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class AbstractAttribute(PolymorphicModel):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    type = models.ForeignKey(TagType, null=True, blank=False, on_delete=models.PROTECT)
    is_custom = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.type}: {self.name}'


class Tag(AbstractAttribute):
    pass


class BooleanAttribute(AbstractAttribute):
    boolean_field = models.BooleanField(default=False)


class TimeAttribute(AbstractAttribute):
    date_field = models.DateTimeField()


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
