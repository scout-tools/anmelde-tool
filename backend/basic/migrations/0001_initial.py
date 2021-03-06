# Generated by Django 3.1.5 on 2021-02-25 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('min_age', models.IntegerField(blank=True, null=True)),
                ('max_age', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EatHabitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('is_custom', models.BooleanField(default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('start_time', models.DateTimeField(blank=True, null=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('registration_deadline', models.DateTimeField(blank=True, null=True)),
                ('registration_start', models.DateTimeField(blank=True, null=True)),
                ('participation_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('min_helper', models.IntegerField(blank=True, null=True)),
                ('min_participation', models.IntegerField(blank=True, null=True)),
                ('max_participation', models.IntegerField(blank=True, null=True)),
                ('invitation_code', models.CharField(blank=True, max_length=6)),
                ('is_public', models.BooleanField(default=0)),
                ('age_groups', models.ManyToManyField(blank=True, to='basic.AgeGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventLocationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('free_text', models.CharField(blank=True, max_length=1000)),
                ('custom_choice', models.IntegerField(default=0)),
                ('is_confirmed', models.BooleanField(default=0)),
                ('is_accepted', models.BooleanField(default=0)),
                ('event', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.event')),
                ('responsible_persons', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=40)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('force_email', models.BooleanField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScoutHierarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=60)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ScoutOrgaLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TravelTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TravelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ZipCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('zip_code', models.CharField(blank=True, max_length=5)),
                ('city', models.CharField(blank=True, max_length=60)),
                ('lat', models.DecimalField(decimal_places=15, default=0.0, max_digits=20)),
                ('lon', models.DecimalField(decimal_places=15, default=0.0, max_digits=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Tent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.registration')),
                ('tent_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.tenttype')),
                ('used_by_scout_groups', models.ManyToManyField(blank=True, to='basic.ScoutHierarchy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='scouthierarchy',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scoutorgalevel'),
        ),
        migrations.AddField(
            model_name='scouthierarchy',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='scouthierarchy', to='basic.scouthierarchy'),
        ),
        migrations.AddField(
            model_name='scouthierarchy',
            name='zip_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode'),
        ),
        migrations.AddField(
            model_name='registration',
            name='scout_organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scouthierarchy'),
        ),
        migrations.CreateModel(
            name='PostalAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('address_addition', models.CharField(blank=True, max_length=100)),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.registration')),
                ('zip_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantPersonal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('scout_name', models.CharField(blank=True, max_length=100)),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('street', models.CharField(blank=True, max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('is_group_leader', models.BooleanField(default=0)),
                ('age_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.agegroup')),
                ('eat_habit_type', models.ManyToManyField(blank=True, to='basic.EatHabitType')),
                ('participant_role', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='basic.role')),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.registration')),
                ('scout_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scouthierarchy')),
                ('zip_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParticipantGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('number_of_persons', models.IntegerField(blank=True, null=True)),
                ('age_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.agegroup')),
                ('participant_role', models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='basic.role')),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.registration')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MethodOfTravel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('number_of_persons', models.IntegerField(blank=True, null=True)),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.registration')),
                ('travel_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.traveltag')),
                ('travel_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.traveltype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventRoleMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='basic.event')),
                ('event_role', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='basic.eventrole')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('address', models.CharField(blank=True, max_length=60)),
                ('contact_name', models.CharField(blank=True, max_length=30)),
                ('contact_email', models.CharField(blank=True, max_length=30)),
                ('contact_phone', models.CharField(blank=True, max_length=30)),
                ('is_public', models.BooleanField(default=0)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('per_person_fee', models.FloatField(blank=True, null=True)),
                ('fix_fee', models.FloatField(blank=True, null=True)),
                ('capacity_corona', models.IntegerField(blank=True, null=True)),
                ('location_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.eventlocationtype')),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.registration')),
                ('zip_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='event',
            name='event_tags',
            field=models.ManyToManyField(blank=True, to='basic.EventTag'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.eventlocation'),
        ),
        migrations.AddField(
            model_name='event',
            name='max_scout_orga_level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scoutorgalevel'),
        ),
        migrations.CreateModel(
            name='EatHabit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_persons', models.IntegerField(blank=True, null=True)),
                ('eat_habit_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.eathabittype')),
                ('participant_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.participantgroup')),
            ],
        ),
    ]
