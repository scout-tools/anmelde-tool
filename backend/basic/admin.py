from django.contrib import admin
from django.db.models import F, Value, CharField
from django.db.models.functions import Concat
from polymorphic.admin import PolymorphicChildModelAdmin, PolymorphicParentModelAdmin, PolymorphicChildModelFilter

from .models import ScoutHierarchy, ZipCode, ScoutOrgaLevel, TagType, AbstractAttribute, Tag, \
    BooleanAttribute, TimeAttribute, IntegerAttribute, FloatAttribute, TravelAttribute, StringAttribute, Description, \
    EatHabit, FrontendTheme, Message, MessageType
admin.site.register(ScoutOrgaLevel)
admin.site.register(Description)
admin.site.register(FrontendTheme)
admin.site.register(Message)
admin.site.register(MessageType)


@admin.register(EatHabit)
class EatHabitAdmin(admin.ModelAdmin):
    def get_participants(self, obj: EatHabit):
        participants = obj.registrationparticipant_set.all()[:5].values(
            full_name=Concat(F('first_name'), Value(' '), F('last_name'), Value(' ('), F('registration__event__name'),
                             Value(')'), output_field=CharField()))
        list_names = [participant['full_name'] for participant in participants]
        return ', '.join(list_names)

    list_display = ('name', 'get_participants')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    search_fields = ('name',)
    autocomplete_fields = ('type',)


@admin.register(ScoutHierarchy)
class ScoutHierarchyAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'zip_code', 'parent')
    list_filter = ('level',)
    search_fields = ('name',)


@admin.register(ZipCode)
class ZipCodeAdmin(admin.ModelAdmin):
    list_display = ('zip_code', 'city')
    search_fields = ('zip_code', 'city')


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


class AbstractAttributeChildAdmin(PolymorphicChildModelAdmin):
    """ Base admin class for all child models """
    base_model = AbstractAttribute  # Optional, explicitly set here.
    list_display = ('name', 'type', 'template')
    search_fields = ('name', 'type')
    autocomplete_fields = ('type',)
    show_in_index = True


@admin.register(BooleanAttribute)
class BooleanAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = BooleanAttribute


@admin.register(TimeAttribute)
class TimeAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = TimeAttribute


@admin.register(IntegerAttribute)
class IntegerAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = IntegerAttribute


@admin.register(FloatAttribute)
class FloatAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = FloatAttribute


@admin.register(TravelAttribute)
class TravelAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = TravelAttribute


@admin.register(StringAttribute)
class StringAttributeAdmin(AbstractAttributeChildAdmin):
    base_model = StringAttribute


@admin.register(AbstractAttribute)
class AbstractAttributeParentAdmin(PolymorphicParentModelAdmin):
    """ The parent model admin """
    base_model = AbstractAttribute  # Optional, explicitly set here.
    child_models = (BooleanAttribute, TimeAttribute, IntegerAttribute, FloatAttribute, TravelAttribute, StringAttribute)
    list_filter = (PolymorphicChildModelFilter,)  # This is optional.
    list_display = ('name', 'type', 'template')
