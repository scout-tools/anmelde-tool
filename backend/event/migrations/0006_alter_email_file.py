# Generated by Django 4.0.3 on 2022-03-25 08:57

import backend.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_alter_emailattachment_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='file',
            field=models.FileField(storage=backend.storage_backends.EmailMediaStorage(), upload_to=''),
        ),
    ]
