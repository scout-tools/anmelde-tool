from django.contrib import admin
from django.contrib.admin import display

from basic.models import AbstractAttribute
from event.models import EventLocation, Event, BookingOption, EventModule, EventModuleMapper, \
    AttributeEventModuleMapper, StandardEventTemplate, Registration, RegistrationParticipant, EventPlanerModule, \
    Workshop, WorkshopParticipant

admin.site.register(Workshop)
admin.site.register(WorkshopParticipant)


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'zip_code')
    search_fields = ('name',)
    autocomplete_fields = ('zip_code',)


@admin.register(EventPlanerModule)
class EventPlanerModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name',)
    autocomplete_fields = ('type',)
    list_filter = ('type',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_public')
    search_fields = ('name',)
    autocomplete_fields = ('responsible_persons', 'tags', 'event_planer_modules')


@admin.register(BookingOption)
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
    list_display = ('id', 'standard', 'module', 'get_event_name', 'ordering')
    search_fields = ('module',)

    @display(ordering='event__name', description='Event name')
    def get_event_name(self, obj):
        return obj.event.name


@admin.register(AttributeEventModuleMapper)
class AttributeEventModuleMapperAdmin(admin.ModelAdmin):
    list_display = ('attribute',)


@admin.register(StandardEventTemplate)
class StandardEventTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('event', 'name')

    def get_form(self, request, obj=None, **kwargs):
        form = super(StandardEventTemplateAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['introduction'].queryset = EventModuleMapper.objects.exclude(standard=False)
        form.base_fields['summary'].queryset = EventModuleMapper.objects.exclude(standard=False)
        form.base_fields['registration'].queryset = EventModuleMapper.objects.exclude(standard=False)
        form.base_fields['personal_registration'].queryset = EventModuleMapper.objects.exclude(standard=False)
        form.base_fields['letter'].queryset = EventModuleMapper.objects.exclude(standard=False)
        form.base_fields['other_required_modules'].queryset = EventModuleMapper.objects.exclude(standard=False)
        form.base_fields['other_optional_modules'].queryset = EventModuleMapper.objects.exclude(standard=False)
        return form


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('scout_organisation', 'get_event_name', 'single')
    search_fields = ('scout_organisation', 'event')
    autocomplete_fields = ('event', 'scout_organisation')
    list_filter = ('event__name',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(RegistrationAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['tags'].queryset = AbstractAttribute.objects.exclude(template=True)
        return form

    @display(ordering='event__name', description='Event name')
    def get_event_name(self, obj):
        return obj.event.name


@admin.register(RegistrationParticipant)
class RegistrationParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'registration',
        'first_name',
        'last_name',
        'scout_name',
        'generated',
        'deactivated',
        'needs_confirmation'
    )
    list_filter = ('registration__event__name','registration__scout_organisation__name')
    search_fields = ('scout_name', 'first_name', 'first_name')
    autocomplete_fields = ('zip_code',)
