# Generated by Django 4.0.2 on 2022-02-27 13:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0042_rename_group_registraion_event_group_registration_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StandardEventInstance',
            new_name='StandardEventTemplate',
        ),
    ]
