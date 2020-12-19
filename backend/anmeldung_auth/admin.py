from django.contrib import admin
from .models import UserExtended


@admin.register(UserExtended)
class UserExtendedAdmin(admin.ModelAdmin):
    list_display = ('user', 'password_date', 'scoutOrganisation')
