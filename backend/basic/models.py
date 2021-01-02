from django.db import models
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True


class ZipCode(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=60, blank=True)
    lat = models.DecimalField(
        max_digits=20, decimal_places=15, default=0.000)
    lon = models.DecimalField(
        max_digits=20, decimal_places=15, default=0.000)

    def __str__(self):
        return self.zip_code + ' - ' + self.city

    def __repr__(self):
        return self.__str__()


class EventLocation(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=60, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=60, blank=True)
    contact_email = models.CharField(max_length=30, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class AgeGroup(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Role(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    force_email = models.BooleanField(default=0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ScoutOrgaLevel(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ScoutHierarchy(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    level = models.ForeignKey(ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=60, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True,
        on_delete=models.PROTECT,
        related_name='scouthierarchy',
        blank=True
    )

    def __str__(self):
        return "{} - {}".format(self.level, self.name)

    def __repr__(self):
        return self.__str__()


class Event(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    location = models.ForeignKey(
        EventLocation, on_delete=models.PROTECT, null=True, blank=True)
    age_groups = models.ManyToManyField(AgeGroup, blank=True)
    contacts = models.ManyToManyField(User, blank=True)
    start_time = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_deadline = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_start = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    participation_fee = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    min_helper = models.IntegerField(blank=True, null=True)
    min_participation = models.IntegerField(blank=True, null=True)
    max_participation = models.IntegerField(blank=True, null=True)
    invitation_code = models.CharField(max_length=6, blank=True)
    max_scout_orga_level = models.IntegerField(blank=True, null=True)
    min_scout_orga_level = models.IntegerField(blank=True, null=True)
    is_public = models.BooleanField(default=0)
    is_personal = models.BooleanField(default=0)
    is_bundesfahrt = models.BooleanField(default=0)
    # ToDo: add pdf attatchment
    # ToDo: add html description

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Registration(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    scout_organisation = models.ForeignKey(
        ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    responsible_persons = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, null=True, blank=True)
    is_confirmed = models.BooleanField(default=0)
    is_accepted = models.BooleanField(default=0)


class Participant(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    number_of_persons = models.IntegerField(blank=True, null=True)
    age_group = models.ForeignKey(
        AgeGroup, on_delete=models.PROTECT, null=True, blank=True)
    registration = models.ForeignKey(
        Registration, on_delete=models.PROTECT, null=True, blank=True)
    scout_group = models.ForeignKey(
        ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)


class ParticipantExtended(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    participant = models.ForeignKey(
        Participant, on_delete=models.PROTECT, null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    zip_code = models.ForeignKey(
        ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    date_birth = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    is_group_leader = models.BooleanField(default=0)


class ParticipantRole(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    participant = models.ForeignKey(
        Participant, on_delete=models.PROTECT, null=True, blank=True)
    event = models.ForeignKey(
        Event, on_delete=models.PROTECT, null=True, blank=True)
    role = models.ForeignKey(
        Role, on_delete=models.PROTECT, null=True, blank=True)


class EatHabitType(models.Model):
<<<<<<< Updated upstream
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class EatHabit(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    eat_habit_type = models.ForeignKey(
        EatHabitType, on_delete=models.PROTECT, null=True, blank=True)
    participant = models.ForeignKey(
        Participant, on_delete=models.PROTECT, null=True, blank=True)


class TravelType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class MethodOfTravel(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(
        Registration, on_delete=models.PROTECT, null=True, blank=True)
    travel_type = models.ForeignKey(
        TravelType, on_delete=models.PROTECT, null=True, blank=True)
    number_of_persons = models.IntegerField(blank=True, null=True)


class TentType(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class Tent(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    registration = models.ForeignKey(
        Registration, on_delete=models.PROTECT, null=True, blank=True)
    tent_type = models.ForeignKey(
        TentType, on_delete=models.PROTECT, null=True, blank=True)
    used_by_scout_groups = models.ManyToManyField(ScoutHierarchy, blank=True)
