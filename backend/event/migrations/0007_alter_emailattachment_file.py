# Generated by Django 4.0.3 on 2022-03-25 08:58

import backend.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0006_alter_email_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailattachment',
            name='file',
            field=models.FileField(storage=backend.storage_backends.EmailAttachmentMediaStorage(), upload_to=''),
        ),
    ]
