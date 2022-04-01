import uuid
from django.contrib.auth.models import User, Group
from django.db import models
from basic import models as basic_models
from event import choices as event_choices
from email_services import models as email_services_model


class EventLocation(basic_models.TimeStampMixin):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200, blank=True)
    zip_code = models.ForeignKey(basic_models.ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    address = models.CharField(max_length=60, blank=True)
    contact_name = models.CharField(max_length=30, blank=True)
    contact_email = models.CharField(max_length=30, blank=True)
    contact_phone = models.CharField(max_length=30, blank=True)
    per_person_fee = models.FloatField(blank=True, null=True)
    fix_fee = models.FloatField(blank=True, null=True)
    tags = models.ManyToManyField(basic_models.Tag, blank=True)

    def __str__(self):
        return f'{self.name}: ({self.address}, {self.zip_code})'


class EventPlanerModule(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    type = models.ForeignKey(basic_models.TagType, null=True, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.type}: {self.name}'


class EventModule(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, default='', blank=True)
    type = models.ForeignKey(basic_models.TagType, on_delete=models.PROTECT)
    header = models.CharField(max_length=100, default='Default Header')
    internal = models.BooleanField(default=False)
    custom = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.type}: {self.name}'


class AttributeEventModuleMapper(models.Model):
    """
    if the is_required is set to True the user has explicity do a choice or has to confirm smth.
    min_length, max_length are only relevant for attributes with texts
    tooltip = extra description which appears when hovering above the element
    """
    id = models.AutoField(primary_key=True)
    attribute = models.ForeignKey(basic_models.AbstractAttribute, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=1000, null=True)
    text = models.CharField(max_length=10000, null=True)
    is_required = models.BooleanField(default=False)
    min_length = models.IntegerField(default=0)
    max_length = models.IntegerField(default=0)
    tooltip = models.CharField(max_length=1000, null=True, blank=True)
    default_value = models.CharField(max_length=1000, null=True, blank=True)
    field_type = models.CharField(max_length=25, null=True, blank=True)
    icon = models.CharField(max_length=25, null=True, blank=True)
    max_entries = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.title}'


class Event(basic_models.TimeStampMixin):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    technical_name = models.CharField(max_length=15, null=True, blank=True)
    short_description = models.CharField(max_length=100, blank=True)
    long_description = models.CharField(max_length=10000, blank=True)
    cloud_link = models.CharField(max_length=200, blank=True, null=True)
    event_url = models.CharField(max_length=200, blank=True, null=True)
    location = models.ForeignKey(EventLocation, on_delete=models.PROTECT, null=True, blank=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_deadline = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    registration_start = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_possible_update = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    invitation_code = models.CharField(max_length=20, blank=True)
    invitation_code_single = models.CharField(max_length=20, blank=True)
    invitation_code_group = models.CharField(max_length=20, blank=True)
    is_public = models.BooleanField(default=False)
    responsible_persons = models.ManyToManyField(User)
    keycloak_path = models.ForeignKey(Group, blank=True, on_delete=models.SET_NULL, null=True,
                                      related_name='keycloak_group')
    keycloak_admin_path = models.ForeignKey(Group, blank=True, on_delete=models.SET_NULL, null=True,
                                            related_name='keycloak_admin_group')
    tags = models.ManyToManyField(basic_models.Tag, blank=True)
    event_planer_modules = models.ManyToManyField(EventPlanerModule, blank=True)
    limited_registration_hierarchy = models.ForeignKey(basic_models.ScoutHierarchy, default=493,
                                                       on_delete=models.SET_DEFAULT)
    single_registration = models.CharField(max_length=1, choices=event_choices.RegistrationTypeSingle.choices,
                                           default=event_choices.RegistrationTypeSingle.No)
    group_registration = models.CharField(max_length=1, choices=event_choices.RegistrationTypeGroup.choices,
                                          default=event_choices.RegistrationTypeGroup.No)
    personal_data_required = models.BooleanField(default=False)
    theme = models.ForeignKey(basic_models.FrontendTheme, on_delete=models.SET_NULL, default=1, null=True, blank=True)
    email_set = models.ForeignKey(email_services_model.StandardEmailRegistrationSet, on_delete=models.PROTECT,
                                  null=True, blank=True)

    def __str__(self):
        return f"{self.name}: {self.start_date} - {self.end_date}, {self.location}"


class EventModuleMapper(models.Model):
    """
    - a standard module is a prefinded module which will be used
     for creating new events containing a predefined set of modules
    - when the required flag is set, this module cannot be deleted/changed by user by hand i.e. in the modules overview
    """
    id = models.AutoField(primary_key=True)
    ordering = models.IntegerField(default=999, auto_created=True)
    module = models.ForeignKey(EventModule, on_delete=models.PROTECT)
    attributes = models.ManyToManyField(AttributeEventModuleMapper, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    overwrite_description = models.CharField(max_length=1000, null=True, blank=True)
    standard = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.ordering}: {self.module.name}, {self.standard=}'


class BookingOption(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    tags = models.ManyToManyField(basic_models.Tag, blank=True)
    bookable_from = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    bookable_till = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    event = models.ForeignKey(Event, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Registration(basic_models.TimeStampMixin):
    """
    is_confirmed = the registrator confirms that the current state of the registration is complete in the last step of
        the registration
    is_accepted = the registration is accepted automatically as long as changes are made before the
        registration deadline after that the registration has to be accepted manually
    """
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    scout_organisation = models.ForeignKey(basic_models.ScoutHierarchy, null=True, on_delete=models.PROTECT)
    responsible_persons = models.ManyToManyField(User)
    is_confirmed = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(basic_models.AbstractAttribute, blank=True)
    single = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.created_at:
            # If self.pk is not None then it's an update.
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            # This will get the current model state since super().save() isn't called yet.
            new = self  # This gets the newly instantiated Mode object with the new values.
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
                except:  # Catch field does not exist exception
                    pass
            kwargs['update_fields'] = changed_fields
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.event.name}: {self.scout_organisation.name}"


class RegistrationParticipant(basic_models.TimeStampMixin):
    scout_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100, default="Generated")
    last_name = models.CharField(max_length=100, default="Generated")
    street = models.CharField(max_length=100, blank=True)
    zip_code = models.ForeignKey(basic_models.ZipCode, on_delete=models.PROTECT, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    scout_group = models.ForeignKey(basic_models.ScoutHierarchy, on_delete=models.PROTECT, null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(null=True, blank=True)
    birthday = models.DateTimeField(null=True, blank=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(basic_models.AbstractAttribute, blank=True)
    booking_option = models.ForeignKey(BookingOption, on_delete=models.SET_NULL, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=event_choices.Gender.choices, default=event_choices.Gender.Nothing)
    deactivated = models.BooleanField(default=False)
    generated = models.BooleanField(default=False)
    needs_confirmation = models.CharField(max_length=2, choices=event_choices.ParticipantActionConfirmation.choices,
                                          default=event_choices.ParticipantActionConfirmation.Nothing)
    eat_habit = models.ManyToManyField(basic_models.EatHabit, blank=True)
    leader = models.CharField(max_length=6, choices=event_choices.LeaderTypes.choices,
                              default=event_choices.LeaderTypes.KeineFuehrung)

    def __str__(self):
        return f"{self.registration}: {self.last_name}, {self.first_name}"


class Workshop(basic_models.TimeStampMixin):
    id = models.UUIDField(auto_created=True, primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    free_text = models.CharField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    min_person = models.IntegerField(blank=True, null=True)
    max_person = models.IntegerField(blank=True, null=True)
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    registration = models.ForeignKey(Registration, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class WorkshopParticipant(basic_models.TimeStampMixin):
    id = models.AutoField(primary_key=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True)
    participant = models.ForeignKey(RegistrationParticipant, on_delete=models.CASCADE, null=True)


class StandardEventTemplate(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    event = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL, related_name='event')
    introduction = models.ForeignKey(EventModuleMapper, null=True, on_delete=models.SET_NULL,
                                     related_name='introduction')
    summary = models.ForeignKey(EventModuleMapper, null=True, on_delete=models.SET_NULL,
                                related_name='confirmation')
    registration = models.ForeignKey(EventModuleMapper, null=True, on_delete=models.SET_NULL,
                                     related_name='group_registration')
    personal_registration = models.ForeignKey(EventModuleMapper, null=True, on_delete=models.SET_NULL,
                                              related_name='personal_registration')
    letter = models.ForeignKey(EventModuleMapper, null=True, on_delete=models.SET_NULL,
                               related_name='letter')
    planer_modules = models.ManyToManyField(EventPlanerModule, blank=True)

    other_required_modules = models.ManyToManyField(EventModuleMapper, blank=True,
                                                    related_name='other_required_modules')

    other_optional_modules = models.ManyToManyField(EventModuleMapper, blank=True,
                                                    related_name='other_optional_modules')
