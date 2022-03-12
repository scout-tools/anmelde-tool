from django.contrib import admin
from event.models import EventLocation, Event, BookingOption, EventModule, EventModuleMapper, \
    AttributeEventModuleMapper, StandardEventTemplate, Registration, RegistrationParticipant


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'zip_code')
    search_fields = ('name',)
    autocomplete_fields = ('zip_code',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_public')
    search_fields = ('name',)
    autocomplete_fields = ('responsible_persons', 'tags')


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
    list_display = ('id', 'standard', 'module', 'ordering')
    search_fields = ('module',)


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
    list_display = ('scout_organisation', 'event', 'single')
    search_fields = ('scout_organisation', 'event')
    autocomplete_fields = ('event',)
    list_filter = ('event__name',)


@admin.register(RegistrationParticipant)
class RegistrationParticipantAdmin(admin.ModelAdmin):
    list_display = ('registration', 'first_name', 'last_name', 'scout_name')
    list_filter = ('registration__event__name',)
