from django.contrib import admin
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy,\
    Registration, ZipCode, Participant, ParticipantRole,\
    Role, MethodOfTravel, Tent, ScoutOrgaLevel, ParticipantExtended,\
    EatHabitType, EatHabit, TravelType, TentType


admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(EventLocation)
admin.site.register(Registration)
admin.site.register(ZipCode)
admin.site.register(Participant)
admin.site.register(ParticipantRole)
admin.site.register(Role)
admin.site.register(MethodOfTravel)
admin.site.register(ScoutOrgaLevel)
admin.site.register(ParticipantExtended)
admin.site.register(EatHabitType)
admin.site.register(EatHabit)
admin.site.register(TravelType)
admin.site.register(TentType)
admin.site.register(Tent)


@admin.register(ScoutHierarchy)
class ScoutHierarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'zip_code', 'parent', 'level')
    list_filter = ('parent', 'level')
