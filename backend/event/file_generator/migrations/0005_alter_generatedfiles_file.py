# Generated by Django 4.0.4 on 2022-05-20 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_generator', '0004_rename_filegenereted_generatedfiles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generatedfiles',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
