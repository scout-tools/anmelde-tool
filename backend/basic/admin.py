from django.contrib import admin

from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, \
    Registration, ZipCode, ParticipantGroup, \
    Role, MethodOfTravel, Tent, ScoutOrgaLevel, ParticipantPersonal, \
    EatHabitType, EatHabit, TravelType, \
    TentType, EventTag, EventRoleMapping, EventRole, PostalAddress, RegistrationMatching, \
    Workshop, Contact

admin.site.register(AgeGroup)
admin.site.register(Role)
admin.site.register(MethodOfTravel)
admin.site.register(ScoutOrgaLevel)
admin.site.register(ParticipantPersonal)
admin.site.register(EatHabitType)
admin.site.register(EatHabit)
admin.site.register(TravelType)
admin.site.register(TentType)
admin.site.register(Tent)
admin.site.register(EventTag)
admin.site.register(EventRoleMapping)
admin.site.register(EventRole)
admin.site.register(PostalAddress)
admin.site.register(Workshop)
admin.site.register(Contact)


@admin.register(ScoutHierarchy)
class ScoutHierarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'zip_code', 'parent', 'level')
    list_filter = ('parent', 'level')
    search_fields = ('name',)


@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'city')
    search_fields = ('zip_code', 'city')


@admin.register(ParticipantGroup)
class ParticipantGroupAdmin(admin.ModelAdmin):
    list_display = ('registration', 'number_of_persons', 'participant_role')
    search_fields = ('registration__scout_organisation__name', 'registration__event__name')
    autocomplete_fields = ('registration',)


@admin.register(EventLocation)
class EventLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_type', 'registration', 'zip_code')
    search_fields = ('name',)
    autocomplete_fields = ('registration', 'zip_code')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)


@admin.register(RegistrationMatching)
class RegistrationMatchingAdmin(admin.ModelAdmin):
    search_fields = ('registrations__scout_organisation__name', 'event_location__city', 'sleeping_location')
    list_display = ('event', 'Matched_Scout_Hierachies', 'event_location', 'sleeping_location')
    autocomplete_fields = ('registrations', 'event', 'event_location', 'sleeping_location')

    def Matched_Scout_Hierachies(self, obj):
        return ", ".join([repr(r) for r in obj.registrations.all()])


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('scout_organisation', 'event', 'Responsible_Persons',)
    search_fields = ('scout_organisation__name', 'event__name')
    autocomplete_fields = ('scout_organisation', 'event', 'responsible_persons')

    def Responsible_Persons(self, obj):
        return ", ".join([str(r) for r in obj.responsible_persons.all()])
