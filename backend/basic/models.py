from django.db import models
from django.contrib.auth.models import User


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
    zipCode = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=30, blank=True)
    lat = models.DecimalField(
        max_digits=20, decimal_places=15, default=0.000)
    lon = models.DecimalField(
        max_digits=20, decimal_places=15, default=0.000)


class EventLocation(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    zipCode = models.ForeignKey(
        ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=30, blank=True)
    contactEmail = models.CharField(max_length=30, blank=True)
    contactPhone = models.CharField(max_length=30, blank=True)

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
    level = models.ForeignKey(
        ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=30, blank=True)
    zipCode = models.ForeignKey(
        ZipCode, on_delete=models.PROTECT, null=True, blank=True)
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
    ageGroups = models.ManyToManyField(AgeGroup, blank=True)
    contacts = models.ManyToManyField(User, blank=True)
    startTime = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    endTime = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    registrationDeadline = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    registrationStart = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    participationFee = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.00)
    minHelper = models.IntegerField(blank=True, null=True)
    minParticipation = models.IntegerField(blank=True, null=True)
    maxParticipation = models.IntegerField(blank=True, null=True)
    isPublic = models.BooleanField(default=0)
    isActive = models.BooleanField(default=0)

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
    scoutOrganisation = models.ForeignKey(
        ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    responsiblePersons = models.ManyToManyField(User, default='')
    isUserConfirmed = models.BooleanField(default=0)
    isAccepted = models.BooleanField(default=0)


class Participants(TimeStampMixin):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    numberOfPersons = models.IntegerField(blank=True, null=True)
    ageGroup = models.ForeignKey(
        AgeGroup, on_delete=models.PROTECT, null=True, blank=True)
    registration = models.ForeignKey(
        Registration, on_delete=models.PROTECT, null=True, blank=True)


class MeatHabit(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    numberVegan = models.IntegerField(blank=True, null=True)
    numberVegetarian = models.IntegerField(blank=True, null=True)
    participants = models.ForeignKey(
        Participants, on_delete=models.PROTECT, null=True, blank=True)


class SpecialHabit(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    meatHabit = models.ForeignKey(
        MeatHabit, on_delete=models.PROTECT, null=True, blank=True)
    numberLactose = models.IntegerField(blank=True, null=True)
    numberGluten = models.IntegerField(blank=True, null=True)
    numberEier = models.IntegerField(blank=True, null=True)
    numberNuesse = models.IntegerField(blank=True, null=True)
    numberHuelsenfruechte = models.IntegerField(blank=True, null=True)
