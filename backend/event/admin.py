from django.contrib import admin
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from event.models import EventLocation, Event, SleepingLocation, AbstractEventModule, EventModuleStandard


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'zip_code')
    search_fields = ('name',)
    autocomplete_fields = ('zip_code',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_public')
    search_fields = ('name',)
    autocomplete_fields = ('responsible_person',)


@admin.register(SleepingLocation)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event')
    search_fields = ('name',)
    autocomplete_fields = ('event',)


class AbstractAbstractEventModule(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = AbstractEventModule  # Optional, explicitly set here.
    list_display = ('name', 'type', 'position')
    search_fields = ('name', 'type')
    # autocomplete_fields = ('type',)
    show_in_index = True


@admin.register(EventModuleStandard)
class EventModuleStandardAdmin(AbstractAbstractEventModule):
    base_model = EventModuleStandard


@admin.register(AbstractEventModule)
class AbstractAttributeParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = AbstractEventModule  # Optional, explicitly set here.
    child_models = (EventModuleStandard,)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
    list_display = ('name', 'type', 'position')
