# Generated by Django 4.0.3 on 2022-03-19 12:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userextended',
            name='id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]