from django.contrib import admin
from .models import Event, AgeGroup, EventLocation, ScoutHierarchy, Registration, ZipCode, Participants, EventTag


admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(EventLocation)
admin.site.register(Registration)
admin.site.register(ZipCode)
admin.site.register(Participants)
admin.site.register(EventTag)


@admin.register(ScoutHierarchy)
class ScoutHierarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'zip_code', 'parent', 'level')
    list_filter = ('parent', 'level')
