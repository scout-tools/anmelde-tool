from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from event.models import EventLocation, Event, SleepingLocation, EventModule, EventModuleMapper, \
    AttributeEventModuleMapper


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'zip_code')
    search_fields = ('name',)
    autocomplete_fields = ('zip_code',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_public')
    search_fields = ('name',)
    autocomplete_fields = ('responsible_persons',)


@admin.register(SleepingLocation)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event')
    search_fields = ('name',)
    autocomplete_fields = ('event',)


@admin.register(EventModule)
class EventModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    autocomplete_fields = ('type',)
    search_fields = ('name',)


@admin.register(EventModuleMapper)
class EventModuleMapperAdmin(admin.ModelAdmin):
    list_display = ('module', 'position')


@admin.register(AttributeEventModuleMapper)
class AttributeEventModuleMapperAdmin(admin.ModelAdmin):
    list_display = ('attribute',)
