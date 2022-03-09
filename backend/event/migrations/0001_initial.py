# Generated by Django 4.0.2 on 2022-03-09 17:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basic', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeEventModuleMapper',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('is_required', models.BooleanField(default=False)),
                ('attribute', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.abstractattribute')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=50)),
                ('short_description', models.CharField(blank=True, max_length=100)),
                ('long_description', models.CharField(blank=True, max_length=10000)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('registration_deadline', models.DateTimeField(blank=True, null=True)),
                ('registration_start', models.DateTimeField(blank=True, null=True)),
                ('last_possible_update', models.DateTimeField(blank=True, null=True)),
                ('invitation_code', models.CharField(blank=True, max_length=20)),
                ('is_public', models.BooleanField(default=False)),
                ('single_registration', models.CharField(choices=[('N', 'No'), ('A', 'Attached'), ('M', 'Mixed'), ('E', 'External')], default='N', max_length=1)),
                ('group_registration', models.CharField(choices=[('N', 'No'), ('O', 'Optional'), ('R', 'Required')], default='N', max_length=1)),
                ('personal_data_required', models.BooleanField(default=False)),
                ('keycloak_admin_path', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keycloak_admin_group', to='auth.group')),
                ('keycloak_path', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='keycloak_group', to='auth.group')),
                ('limited_registration_hierarchy', models.ForeignKey(default=493, on_delete=django.db.models.deletion.SET_DEFAULT, to='basic.scouthierarchy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventModule',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('header', models.CharField(default='Default Header', max_length=100)),
                ('internal', models.BooleanField(default=False)),
                ('custom', models.BooleanField(default=False)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='basic.tagtype')),
            ],
        ),
        migrations.CreateModel(
            name='EventModuleMapper',
            fields=[
                ('ordering', models.IntegerField(auto_created=True, default=999)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('required', models.BooleanField(default=False)),
                ('overwrite_description', models.CharField(blank=True, max_length=1000, null=True)),
                ('standard', models.BooleanField(default=False)),
                ('attributes', models.ManyToManyField(blank=True, to='event.AttributeEventModuleMapper')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='event.eventmodule')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_accepted', models.BooleanField(default=False)),
                ('single', models.BooleanField(default=False)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('responsible_persons', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('scout_hierachy', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scouthierarchy')),
                ('tags', models.ManyToManyField(blank=True, to='basic.AbstractAttribute')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RegistrationParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('scout_name', models.CharField(blank=True, max_length=100, null=True)),
                ('first_name', models.CharField(default='Generated', max_length=100)),
                ('last_name', models.CharField(default='Generated', max_length=100)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('birthday', models.DateField(null=True)),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.registration')),
                ('scout_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scouthierarchy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100)),
                ('free_text', models.CharField(blank=True, max_length=1000)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('min_person', models.IntegerField(blank=True, null=True)),
                ('max_person', models.IntegerField(blank=True, null=True)),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='event.registration')),
                ('supervisor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='basic.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WorkshopParticipant',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('participant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.registrationparticipant')),
                ('workshop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.workshop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardEventTemplate',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event', to='event.event')),
                ('introduction', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='introduction', to='event.eventmodulemapper')),
                ('letter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='letter', to='event.eventmodulemapper')),
                ('other_optional_modules', models.ManyToManyField(blank=True, related_name='other_optional_modules', to='event.EventModuleMapper')),
                ('other_required_modules', models.ManyToManyField(blank=True, related_name='other_required_modules', to='event.EventModuleMapper')),
                ('personal_registration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='personal_registration', to='event.eventmodulemapper')),
                ('registration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group_registration', to='event.eventmodulemapper')),
                ('summary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='confirmation', to='event.eventmodulemapper')),
            ],
        ),
        migrations.CreateModel(
            name='SleepingLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('bookable_from', models.DateTimeField(blank=True, null=True)),
                ('bookable_till', models.DateTimeField(blank=True, null=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='event.event')),
                ('tags', models.ManyToManyField(blank=True, to='basic.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='registrationparticipant',
            name='sleeping_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='event.sleepinglocation'),
        ),
        migrations.AddField(
            model_name='registrationparticipant',
            name='tags',
            field=models.ManyToManyField(to='basic.AbstractAttribute'),
        ),
        migrations.AddField(
            model_name='registrationparticipant',
            name='zip_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode'),
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(blank=True, max_length=60)),
                ('contact_name', models.CharField(blank=True, max_length=30)),
                ('contact_email', models.CharField(blank=True, max_length=30)),
                ('contact_phone', models.CharField(blank=True, max_length=30)),
                ('per_person_fee', models.FloatField(blank=True, null=True)),
                ('fix_fee', models.FloatField(blank=True, null=True)),
                ('tags', models.ManyToManyField(blank=True, to='basic.Tag')),
                ('zip_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='event.eventlocation'),
        ),
        migrations.AddField(
            model_name='event',
            name='responsible_persons',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, to='basic.Tag'),
        ),
    ]
