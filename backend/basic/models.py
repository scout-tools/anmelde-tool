from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True


class ZipCode(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    zip_code = models.CharField(max_length=5, blank=True)
    city = models.CharField(max_length=60, blank=True)
    lat = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)
    lon = models.DecimalField(max_digits=20, decimal_places=15, default=0.000)

    def __str__(self):
        return f"{self.zip_code} {self.city}"


class TagType(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class AttributeDescription(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    header = models.CharField(max_length=1000, blank=True)
    name = models.CharField(max_length=1000, blank=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.name


class AbstractAttribute(PolymorphicModel):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    type = models.ForeignKey(TagType, null=True, blank=False, on_delete=models.PROTECT)
    is_custom = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=True)
    description = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.type}: {self.name}'


class DescriptionEventAttributeRelation(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    description = models.ForeignKey(AttributeDescription, null=True, on_delete=models.PROTECT)
    event = models.ForeignKey("Event", null=True, on_delete=models.PROTECT)
    attribute = models.ForeignKey(AbstractAttribute, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.event}: {self.attribute}'


class DescriptionRegistrationAttributeRelation(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    description = models.ForeignKey(AttributeDescription, null=True, on_delete=models.PROTECT)
    registration = models.ForeignKey("Registration", null=True, on_delete=models.PROTECT)
    attribute = models.ForeignKey(AbstractAttribute, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.event}: {self.registration}'


class Tag(AbstractAttribute):
    pass


class BooleanAttribute(AbstractAttribute):
    boolean_field = models.BooleanField(default=False)


class TimeAttribute(AbstractAttribute):
    date_field = models.DateTimeField()


class EventLocation(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=60, blank=True)
    contact_name = models.CharField(max_length=30, blank=True)
    contact_email = models.CharField(max_length=30, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    capacity = models.IntegerField(blank=True, null=True)
    per_person_fee = models.FloatField(blank=True, null=True)
    fix_fee = models.FloatField(blank=True, null=True)
    tags = models.ManyToManyField(Tag)


def __str__(self):
    return self.name


class ScoutOrgaLevel(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class ScoutHierarchy(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    level = models.ForeignKey(ScoutOrgaLevel, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=60, blank=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, on_delete=models.PROTECT, related_name='scouthierarchy', blank=True)
    abbreviation = models.CharField(max_length=5, blank=True, null=True)

    def __str__(self):
        return f"{self.level} - {self.name}"


class RegistrationType(models.TextChoices):
    SingleOnly = 'SO', _('Single Only')
    GroupOnly = 'GO', _('Groups Only')
    GroupsOptionalSingleOptional = 'GOSO', _('Groups Optional, Single Optional')
    GroupsRequiredSingleOptional = 'GRSO', _('Groups Required Single Optional')


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
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    responsible_persons = models.ManyToManyField(User)
    keycloak_path = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField(Tag)
    registration_model = models.CharField(max_length=4, choices=RegistrationType.choices,
                                          default=RegistrationType.GroupOnly)

    def __str__(self):
        return f"{self.name}: {self.start_time} - {self.end_time}, {self.location}"


class SleepingLocations(TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    additional_price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tags = models.ManyToManyField(Tag)

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
