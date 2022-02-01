from django.contrib.auth.models import User, Group
from django.db import models
from polymorphic.models import PolymorphicModel
from django.utils.translation import gettext_lazy as _

from basic.models import ZipCode, Tag, AbstractAttribute, AttributeDescription, TimeStampMixin, ScoutHierarchy, TagType


class RegistrationType(models.TextChoices):
    SingleOnly = 'SO', _('Single Only')
    GroupOnly = 'GO', _('Groups Only')
    GroupsOptionalSingleOptional = 'GOSO', _('Groups Optional, Single Optional')
    GroupsRequiredSingleOptional = 'GRSO', _('Groups Required Single Optional')


class EventLocation(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=60, blank=True)
    contact_name = models.CharField(max_length=30, blank=True)
    contact_email = models.CharField(max_length=30, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    per_person_fee = models.FloatField(blank=True, null=True)
    fix_fee = models.FloatField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return f'{self.name}: ({self.address}, {self.zip_code})'


class EventModule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', blank=True)
    description = models.CharField(max_length=1000, default='', blank=True)
    type = models.ForeignKey(TagType, on_delete=models.PROTECT)
    header = models.CharField(max_length=100, default='Default Header')
    internal = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type}: {self.name}'


class AttributeEventModuleMapper(models.Model):
    id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(AbstractAttribute, on_delete=models.PROTECT, null=True)
    description = models.CharField(max_length=1000, null=True)


class Event(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    location = models.ForeignKey(EventLocation, on_delete=models.PROTECT, null=True, blank=True)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_deadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_start = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_possible_update = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    invitation_code = models.CharField(max_length=20, blank=True)
    is_public = models.BooleanField(default=False)
    responsible_persons = models.ManyToManyField(User)
    keycloak_path = models.ForeignKey(Group, blank=True, on_delete=models.SET_NULL, null=True,
                                      related_name='keycloak_group')
    keycloak_admin_path = models.ForeignKey(Group, blank=True, on_delete=models.SET_NULL, null=True,
                                            related_name='keycloak_admin_group')
    tags = models.ManyToManyField(Tag, blank=True)
    registration_model = models.CharField(max_length=4, choices=RegistrationType.choices,
                                          default=RegistrationType.GroupOnly)


    def __str__(self):
        return f"{self.name}: {self.start_time} - {self.end_time}, {self.location}"


class EventModuleMapper(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.IntegerField(default=999, auto_created=True)
    module = models.ForeignKey(EventModule, on_delete=models.PROTECT, null=True, blank=True)
    attributes = models.ManyToManyField(AttributeEventModuleMapper, blank=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.position}: {self.module.name}'


class SleepingLocation(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tags = models.ManyToManyField(Tag, blank=True)
    bookable_from = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    bookable_till = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Registration(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    scout_hierachy = models.ForeignKey(ScoutHierarchy, null=True, on_delete=models.PROTECT)
    responsible_persons = models.ManyToManyField(User)
    is_confirmed = models.BooleanField(default=0)
    is_accepted = models.BooleanField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)


class RegistrationParticipant(TimeStampMixin):
    scout_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, default="Generated")
    last_name = models.CharField(max_length=100, default="Generated")
    street = models.CharField(max_length=100, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    scout_group = models.ForeignKey(ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(null=True)
    birthday = models.DateField(null=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    sleeping_location = models.ForeignKey(SleepingLocation, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.registration}: {self.last_name}, {self.first_name}"


class Workshop(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True)
    free_text = models.CharField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    min_person = models.IntegerField(blank=True, null=True)
    max_person = models.IntegerField(blank=True, null=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class WorkshopParticipant(TimeStampMixin):
    id = models.AutoField(primary_key=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True)
    participant = models.ForeignKey(RegistrationParticipant, on_delete=models.CASCADE, null=True)
