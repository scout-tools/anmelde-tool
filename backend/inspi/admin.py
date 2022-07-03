from django.contrib import admin
from .models import Tag, Event, TagCategory, Event, Image, \
    MaterialItem, ExperimentItem, Experiment, Faq, \
    Message, MaterialName, MaterialUnit, MessageType

from import_export import resources
from import_export.admin import ImportExportModelAdmin

class EventResource(resources.ModelResource):
    class Meta:
         model = Event
class EventAdmin(ImportExportModelAdmin):
   resource_class = EventResource

class TagResource(resources.ModelResource):
    class Meta:
         model = Tag
class TagAdmin(ImportExportModelAdmin):
   resource_class = TagResource

class TagCategoryResource(resources.ModelResource):
    class Meta:
         model = TagCategory
class TagCategoryAdmin(ImportExportModelAdmin):
   resource_class = TagCategoryResource

class ImageResource(resources.ModelResource):
    class Meta:
         model = Image
class ImageAdmin(ImportExportModelAdmin):
   resource_class = ImageResource

class FaqResource(resources.ModelResource):
    class Meta:
         model = Faq
class FaqAdmin(ImportExportModelAdmin):
   resource_class = FaqResource

class MaterialItemResource(resources.ModelResource):
    class Meta:
         model = MaterialItem
class MaterialItemAdmin(ImportExportModelAdmin):
   resource_class = MaterialItemResource

class MaterialUnitResource(resources.ModelResource):
    class Meta:
         model = MaterialUnit
class MaterialUnitAdmin(ImportExportModelAdmin):
   resource_class = MaterialUnitResource

class MaterialNameResource(resources.ModelResource):
    class Meta:
         model = MaterialName
class MaterialNameAdmin(ImportExportModelAdmin):
   resource_class = MaterialNameResource

class MessageResource(resources.ModelResource):
    class Meta:
         model = Message
class MessageAdmin(ImportExportModelAdmin):
   resource_class = MessageResource

class MessageTypeResource(resources.ModelResource):
    class Meta:
         model = MessageType
class MessageTypeAdmin(ImportExportModelAdmin):
   resource_class = MessageTypeResource

admin.site.register(Event, EventAdmin)
admin.site.register(TagCategory, TagCategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Faq, FaqAdmin)
admin.site.register(MaterialItem, MaterialItemAdmin)
admin.site.register(MaterialUnit, MaterialUnitAdmin)
admin.site.register(MaterialName, MaterialNameAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MessageType, MessageTypeAdmin)
