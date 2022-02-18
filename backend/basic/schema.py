import graphene
from graphene_django import DjangoObjectType

from basic.models import *


class EventTagType(DjangoObjectType):
    class Meta:
        model = EventTag
        fields = "__all__"


class EventType(DjangoObjectType):
    class Meta:
        model = Event
        fields = "__all__"


class AgeGroupType(DjangoObjectType):
    class Meta:
        model = AgeGroup
        fields = "__all__"


class WorkshopType(DjangoObjectType):
    class Meta:
        model = Workshop
        fields = "__all__"


class RegistrationType(DjangoObjectType):
    class Meta:
        model = Registration
        fields = "__all__"


class ParticipantPersonalType(DjangoObjectType):
    class Meta:
        model = ParticipantPersonal
        fields = "__all__"


class ScoutHierarchyType(DjangoObjectType):
    class Meta:
        model = ScoutHierarchy
        fields = "__all__"


class ZipCodeType(DjangoObjectType):
    class Meta:
        model = ZipCode
        fields = "__all__"


class ParticipantPersonalType(DjangoObjectType):
    class Meta:
        model = ParticipantPersonal
        fields = "__all__"


class EatHabitTypeType(DjangoObjectType):
    class Meta:
        model = EatHabitType
        fields = "__all__"


class Query(graphene.ObjectType):
    event_tag = graphene.Field(EventTagType, id=graphene.Int())
    all_event_tags = graphene.List(EventTagType)

    event = graphene.Field(EventType, id=graphene.Int())
    all_events = graphene.List(EventType)

    age_group = graphene.Field(AgeGroupType, id=graphene.Int())
    all_age_groups = graphene.List(AgeGroupType)

    workshop = graphene.Field(WorkshopType, id=graphene.Int())
    all_workshops = graphene.List(WorkshopType)

    scout_hierarchy = graphene.Field(ScoutHierarchyType, id=graphene.Int())
    all_scout_hierarchies = graphene.List(ScoutHierarchyType)

    registration = graphene.Field(RegistrationType, id=graphene.Int())
    all_registrations = graphene.List(RegistrationType)

    zip_code = graphene.Field(ZipCodeType, id=graphene.Int())
    all_zip_codes = graphene.List(ZipCodeType)

    participant_personal = graphene.Field(ParticipantPersonalType, id=graphene.Int())
    all_participant_personals = graphene.List(ParticipantPersonalType)

    eat_habit_type = graphene.Field(EatHabitTypeType, id=graphene.Int())
    all_eat_habit_types = graphene.List(EatHabitTypeType)

    def resolve_event(self, context, id=None):
        if id is not None:
            return Event.objects.get(pk=id)

        return None

    def resolve_registration(self, context, id=None):
        if id is not None:
            return Registration.objects.get(pk=id)

        return None

    def resolve_all_event_tags(root, info):
        return EventTag.objects.all()

    def resolve_all_events(self, context):
        return Event.objects.all()

    def resolve_all_workshops(self, context):
        return Workshop.objects.all()

    def resolve_all_scout_hierarchies(self, context):
        return ScoutHierarchy.objects.all()

    def resolve_all_zip_codes(self, context):
        return ZipCode.objects.all()

    def resolve_all_registrations(self, context):
        return Registration.objects.all()

    def resolve_all_participant_personals(self, context):
        return Registration.objects.all()

    def resolve_all_eat_habit_types(self, context):
        return Registration.objects.all()


schema = graphene.Schema(query=Query)
