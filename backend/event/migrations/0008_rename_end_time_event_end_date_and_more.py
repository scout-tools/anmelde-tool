# Generated by Django 4.0.3 on 2022-03-12 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_alter_registrationparticipant_needs_confirmation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='end_time',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='start_time',
            new_name='start_date',
        ),
    ]