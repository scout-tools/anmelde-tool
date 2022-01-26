from django.contrib import admin

from event.models import EventLocation, Event, SleepingLocation


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
    list_display = ('name', 'price', 'event')
    search_fields = ('name',)
    autocomplete_fields = ('event',)
