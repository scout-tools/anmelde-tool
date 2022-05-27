# Generated by Django 4.0.4 on 2022-05-19 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingoption',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookingoption',
            name='max_participants',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bookingoption',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
