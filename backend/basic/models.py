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


class EventContact(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=30)
    emailAddress = models.EmailField()


class Event(models.Model):
    id = models.AutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name='ID')
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)
    location = models.ForeignKey(EventLocation, on_delete=models.PROTECT, null=True, blank=True)
    ageGroups = models.ManyToManyField(AgeGroup, blank=True)
    contact = models.ForeignKey(EventContact, on_delete=models.PROTECT, null=True, blank=True)
    startTime = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    endTime = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registrationDeadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registrationStart = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    participationFee = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
