# Generated by Django 3.2.9 on 2021-12-28 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_event_registration_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='basic.Tag'),
        ),
    ]