# Generated by Django 4.1.2 on 2022-10-06 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_person_userextended_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('M', 'Männlich'), ('W', 'Weiblich'), ('D', 'Divers'), ('N', 'Keine Angabe')], default='N', max_length=1),
        ),
    ]
