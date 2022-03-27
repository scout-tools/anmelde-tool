from django.contrib import admin

from email_services.models import Email, EmailAttachment, EmailPicture, StandardEmailSet, StandardEmailRegistrationSet

admin.site.register(Email)
admin.site.register(EmailAttachment)
admin.site.register(EmailPicture)
admin.site.register(StandardEmailSet)
admin.site.register(StandardEmailRegistrationSet)
