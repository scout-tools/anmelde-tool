# Generated by Django 3.2.9 on 2022-01-30 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0008_auto_20211231_1346'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagtype',
            name='max',
            field=models.IntegerField(default=9999),
        ),
        migrations.AddField(
            model_name='tagtype',
            name='min',
            field=models.IntegerField(default=0),
        ),
    ]