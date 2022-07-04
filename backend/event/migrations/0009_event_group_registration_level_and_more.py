# Generated by Django 4.0.4 on 2022-06-27 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_travelattributev2'),
        ('event', '0008_registrationparticipant_scout_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='group_registration_level',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='group_registration_level', to='basic.scoutorgalevel'),
        ),
        migrations.AddField(
            model_name='event',
            name='single_registration_level',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='single_registration_level', to='basic.scoutorgalevel'),
        ),
        migrations.AlterField(
            model_name='eventmodulemapper',
            name='overwrite_description',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]