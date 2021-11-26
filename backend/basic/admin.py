from django.contrib import admin

from .models import AgeGroup, EventLocation, ScoutHierarchy, ZipCode, ScoutOrgaLevel, Tag, TagType, Event

admin.site.register(AgeGroup)
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
class EventTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


@admin.register(Tag)
class EventTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'type',)
    search_fields = ('name', 'type')
    autocomplete_fields = ('type',)
