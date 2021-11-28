from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from .models import EventLocation, ScoutHierarchy, ZipCode, ScoutOrgaLevel, TagType, Event, AbstractAttribute, Tag, \
    BooleanAttribute, TimeAttribute

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


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'zip_code')
    search_fields = ('name',)
    autocomplete_fields = ('zip_code',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_public')
    search_fields = ('name',)


@admin.register(TagType)
class EventTagTypeAdmin(admin.ModelAdmin):
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


@admin.register(AbstractAttribute)
class AbstractAttributeParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = AbstractAttribute  # Optional, explicitly set here.
    child_models = (Tag, BooleanAttribute, TimeAttribute)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
