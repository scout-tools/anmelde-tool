from django.contrib import admin
from .models import Event, AgeGroup, EventLocation, ScoutHerarchy, Registration, ZipCode


admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(EventLocation)
admin.site.register(Registration)
admin.site.register(ZipCode)


@admin.register(ScoutHerarchy)
class ScoutHerarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'zipCode', 'parent', 'level')
    list_filter = ('parent', 'level')
