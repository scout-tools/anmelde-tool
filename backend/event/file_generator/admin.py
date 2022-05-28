from django.contrib import admin

from event.file_generator.models import GeneratedFiles, FileTemplate


@admin.register(GeneratedFiles)
class GeneratedFilesAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'updated_at', 'status', 'extension')
    autocomplete_fields = ('user',)
    ordering = ('created_at', 'updated_at')


@admin.register(FileTemplate)
class GeneratedFilesAdmin(admin.ModelAdmin):
    list_display = ('type', 'version', 'extension')
    ordering = ('type', 'version')
