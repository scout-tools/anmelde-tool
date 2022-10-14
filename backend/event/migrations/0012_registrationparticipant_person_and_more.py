# Generated by Django 4.0.4 on 2022-10-13 21:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_person_owned_by_remove_person_created_by_and_more'),
        ('event', '0011_alter_registrationparticipant_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationparticipant',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authentication.person'),
        ),
        migrations.AlterField(
            model_name='registrationparticipant',
            name='gender',
            field=models.CharField(choices=[('M', 'Männlich'), ('F', 'Weiblich'), ('D', 'Divers'), ('N', 'Keine Angabe')], default='N', max_length=1),
        ),
        migrations.AlterField(
            model_name='registrationparticipant',
            name='leader',
            field=models.CharField(choices=[('N', 'Kein Amt'), ('BuFue', 'Bundesführung'), ('RinFue', 'Ringführung'), ('StaFue', 'Stammesführung'), ('SiFue', 'Sippenführung'), ('RoFue', 'Roverrundenführung'), ('MeuFue', 'Meutenführung')], default='N', max_length=6),
        ),
    ]
