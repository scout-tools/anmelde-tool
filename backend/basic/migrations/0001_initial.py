# Generated by Django 3.1.4 on 2020-12-19 20:58

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
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MeetHabit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberVegan', models.IntegerField(blank=True, null=True)),
                ('numberVegetarian', models.IntegerField(blank=True, null=True)),
            ],
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
            name='ZipCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('zipCode', models.CharField(blank=True, max_length=5)),
                ('city', models.CharField(blank=True, max_length=30)),
                ('lat', models.DecimalField(decimal_places=15, default=0.0, max_digits=20)),
                ('lon', models.DecimalField(decimal_places=15, default=0.0, max_digits=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SpecialHabit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numberLactose', models.IntegerField(blank=True, null=True)),
                ('numberGluten', models.IntegerField(blank=True, null=True)),
                ('numberEier', models.IntegerField(blank=True, null=True)),
                ('numberNuesse', models.IntegerField(blank=True, null=True)),
                ('numberHuelsenfruechte', models.IntegerField(blank=True, null=True)),
                ('meetHabit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.meethabit')),
            ],
        ),
        migrations.CreateModel(
            name='ScoutHerarchy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, max_length=30)),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scoutorgalevel')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='scoutherarchy', to='basic.scoutherarchy')),
                ('zipCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
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
                ('isUserConfirmed', models.BooleanField(default=0)),
                ('isAccepted', models.BooleanField(default=0)),
                ('responsiblePersons', models.ManyToManyField(default='', to=settings.AUTH_USER_MODEL)),
                ('scoutOrganisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scoutherarchy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Participants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('numberOfPersons', models.IntegerField(blank=True, null=True)),
                ('ageGroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.agegroup')),
                ('registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.registration')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='meethabit',
            name='participants',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.participants'),
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('address', models.CharField(blank=True, max_length=30)),
                ('contactEmail', models.CharField(blank=True, max_length=30)),
                ('contactPhone', models.CharField(blank=True, max_length=30)),
                ('zipCode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.zipcode')),
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
                ('startTime', models.DateTimeField(blank=True, null=True)),
                ('endTime', models.DateTimeField(blank=True, null=True)),
                ('registrationDeadline', models.DateTimeField(blank=True, null=True)),
                ('registrationStart', models.DateTimeField(blank=True, null=True)),
                ('participationFee', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('minHelper', models.IntegerField(blank=True, null=True)),
                ('minParticipation', models.IntegerField(blank=True, null=True)),
                ('maxParticipation', models.IntegerField(blank=True, null=True)),
                ('isPublic', models.BooleanField(default=0)),
                ('isActive', models.BooleanField(default=0)),
                ('ageGroups', models.ManyToManyField(blank=True, to='basic.AgeGroup')),
                ('contacts', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.eventlocation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
