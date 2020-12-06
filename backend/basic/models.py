from django.db import models


class EventLocation(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=20, blank=True)
    zipCode = models.CharField(max_length=5, blank=True)
    address = models.CharField(max_length=30, blank=True)


class AgeGroup(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)


class ScoutOrgaLevel(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)


class ScoutHerarchy(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    level = models.ForeignKey(
        ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=20, blank=True)
    zipCode = models.CharField(max_length=5, blank=True)
    parent = models.ForeignKey(
        'self', null=True,
        on_delete=models.PROTECT,
        related_name='scoutherarchy',
        blank=True
    )

    def __str__(self):
        return "{} - {}".format(self.level, self.name)

    def __repr__(self):
        return self.__str__()


class Person(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=30)
    scoutOrganisation = models.ForeignKey(
        ScoutHerarchy, on_delete=models.PROTECT, null=True, blank=True)
    emailAddress = models.EmailField()
    mobileNumber = models.CharField(max_length=20, blank=True)


class Event(models.Model):
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
    contacts = models.ManyToManyField(Person, blank=True)
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


class Registration(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    scoutOrganisation = models.ForeignKey(
        ScoutHerarchy, on_delete=models.PROTECT, null=True, blank=True)
    numberOfParticipants = models.IntegerField(blank=False, unique=False)
    responsiblePerson = models.ForeignKey(
        Person, on_delete=models.PROTECT, null=True, blank=True)
