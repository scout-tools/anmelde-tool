# Generated by Django 4.0.1 on 2022-01-30 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0014_alter_abstracteventmodule_polymorphic_ctype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstracteventmodule',
            name='description',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='abstracteventmodule',
            name='name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.DeleteModel(
            name='EventModuleSleeping',
        ),
    ]
