# Generated by Django 4.0.4 on 2022-05-20 22:07

import backend.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_generator', '0005_alter_generatedfiles_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetemplate',
            name='file',
            field=models.FileField(storage=backend.storage_backends.FileTemplateMediaStorage, upload_to=''),
        ),
        migrations.AlterField(
            model_name='generatedfiles',
            name='file',
            field=models.FileField(blank=True, null=True, storage=backend.storage_backends.GeneratedFilesStorage, upload_to=''),
        ),
    ]
