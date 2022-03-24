from django.contrib import admin

from .models import UserExtended


# Register your models here.
@admin.register(UserExtended)
class UserExtendedAdmin(admin.ModelAdmin):
    list_display = ('user', 'scout_organisation')
    autocomplete_fields = ('scout_organisation',)
