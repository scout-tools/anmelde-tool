# Generated by Django 4.0.2 on 2022-02-26 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0039_alter_standardeventinstance_other_modules'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardeventinstance',
            name='letter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='letter', to='event.eventmodulemapper'),
        ),
    ]
