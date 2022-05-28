# Generated by Django 4.0.4 on 2022-05-28 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_generator', '0010_alter_filetemplate_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetemplate',
            name='type',
            field=models.CharField(choices=[('K', 'KJP Liste'), ('I', 'Rechnungserstellung Felix'), ('P', 'Teilnehmerliste')], default='K', max_length=1),
        ),
    ]