from django.contrib import admin

from .models import Tag, TagCategory, Event, Image, \
    MaterialItem, ExperimentItem, Experiment, Faq, FaqRating, \
    Message, MaterialName, MaterialUnit

admin.site.register(Event)
admin.site.register(TagCategory)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(MaterialItem)
admin.site.register(Experiment)
admin.site.register(ExperimentItem)
admin.site.register(Faq)
admin.site.register(FaqRating)
admin.site.register(MaterialUnit)
admin.site.register(MaterialName)
admin.site.register(Message)
