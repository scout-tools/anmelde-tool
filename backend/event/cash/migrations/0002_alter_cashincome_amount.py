# Generated by Django 4.0.4 on 2022-09-21 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashincome',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
