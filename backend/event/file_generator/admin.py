from django.contrib import admin

from event.file_generator.models import GeneratedFiles, FileTemplate

admin.site.register(FileTemplate)


@admin.register(GeneratedFiles)
class GeneratedFilesAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'status', 'type', 'extension')
    autocomplete_fields = ('user',)
    ordering = ('created_at', 'updated_at')
