from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from .models import ScoutHierarchy, ZipCode, ScoutOrgaLevel, TagType, AbstractAttribute, Tag, \
    BooleanAttribute, TimeAttribute, IntegerAttribute, FloatAttribute, TravelAttribute

admin.site.register(ScoutOrgaLevel)


@admin.register(ScoutHierarchy)
class ScoutHierarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'zip_code', 'parent')
    list_filter = ('level',)
    search_fields = ('name',)


@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'city')
    search_fields = ('zip_code', 'city')


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


class AbstractAttributeChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = AbstractAttribute  # Optional, explicitly set here.
    list_display = ('name', 'type',)
    search_fields = ('name', 'type')
    autocomplete_fields = ('type',)
    show_in_index = True


@admin.register(BooleanAttribute)
class BooleanAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = BooleanAttribute


@admin.register(TimeAttribute)
class TimeAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = TimeAttribute


@admin.register(Tag)
class EventTagAdmin(AbstractAttributeChildAdmin):
    base_model = Tag


@admin.register(IntegerAttribute)
class IntegerAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = IntegerAttribute


@admin.register(FloatAttribute)
class FloatAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = FloatAttribute


@admin.register(TravelAttribute)
class TravelAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = TravelAttribute


@admin.register(AbstractAttribute)
class AbstractAttributeParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = AbstractAttribute  # Optional, explicitly set here.
    child_models = (Tag, BooleanAttribute, TimeAttribute, IntegerAttribute, FloatAttribute, TravelAttribute)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
