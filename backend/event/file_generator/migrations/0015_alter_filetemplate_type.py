# Generated by Django 4.1.2 on 2022-10-06 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_generator', '0014_alter_filetemplate_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetemplate',
            name='type',
            field=models.CharField(choices=[('KJPC', 'KJP Liste Komplex'), ('IF', 'Rechnungserstellung Felix'), ('PL', 'Teilnehmerliste'), ('AL', 'Attributliste'), ('TM', 'Anreise Matrix'), ('KJR', 'KJR Liste')], default='KJPC', max_length=5),
        ),
    ]