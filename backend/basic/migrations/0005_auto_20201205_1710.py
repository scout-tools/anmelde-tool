# Generated by Django 3.1.4 on 2020-12-05 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_remove_event_caro'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('emailAddress', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100)),
                ('city', models.CharField(blank=True, max_length=20)),
                ('zipCode', models.CharField(blank=True, max_length=5)),
                ('address', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='ageGroups',
            field=models.ManyToManyField(blank=True, to='basic.AgeGroup'),
        ),
        migrations.AddField(
            model_name='event',
            name='endTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='registrationDeadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='startTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.eventcontact'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.eventlocation'),
        ),
    ]