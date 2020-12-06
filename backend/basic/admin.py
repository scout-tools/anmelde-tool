from django.contrib import admin
from .models import Event, AgeGroup, EventLocation, Person, ScoutHerarchy, Registration


admin.site.register(Event)
admin.site.register(AgeGroup)
admin.site.register(EventLocation)
admin.site.register(Person)
admin.site.register(ScoutHerarchy)
admin.site.register(Registration)
