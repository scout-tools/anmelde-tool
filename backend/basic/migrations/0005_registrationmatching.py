# Generated by Django 3.2.3 on 2021-06-19 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_auto_20210306_1847'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationMatching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registrations', models.ManyToManyField(to='basic.Registration')),
            ],
        ),
    ]