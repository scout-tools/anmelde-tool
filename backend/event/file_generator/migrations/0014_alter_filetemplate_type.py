# Generated by Django 4.1 on 2022-09-13 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_generator', '0013_alter_generatedfiles_error_msg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetemplate',
            name='type',
            field=models.CharField(choices=[('K', 'KJP Liste'), ('I', 'Rechnungserstellung Felix'), ('P', 'Teilnehmerliste'), ('A', 'Attributliste'), ('T', 'Anreise Matrix'), ('j', 'KJR Liste')], default='K', max_length=1),
        ),
    ]
