# Generated by Django 4.0.4 on 2022-05-26 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_generator', '0009_rename_file_template_generatedfiles_template'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetemplate',
            name='type',
            field=models.CharField(choices=[('K', 'KJP Liste'), ('I', 'Rechnungserstellungsvorlage'), ('P', 'Teilnehmerliste')], default='K', max_length=1),
        ),
    ]
