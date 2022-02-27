# Generated by Django 4.0.2 on 2022-02-27 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0046_remove_standardeventtemplate_other_modules_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='single_registration',
            field=models.CharField(choices=[('N', 'No'), ('A', 'Attached'), ('M', 'Mixed'), ('E', 'External')], default='N', max_length=1),
        ),
    ]
