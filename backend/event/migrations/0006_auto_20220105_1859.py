# Generated by Django 3.2.9 on 2022-01-05 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_auto_20211231_1346'),
        ('event', '0005_alter_event_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventlocation',
            name='capacity',
        ),
        migrations.AlterField(
            model_name='eventlocation',
            name='tags',
            field=models.ManyToManyField(blank=True, to='basic.Tag'),
        ),
    ]
