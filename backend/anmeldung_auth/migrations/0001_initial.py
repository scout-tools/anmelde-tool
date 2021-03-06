# Generated by Django 3.1.5 on 2021-02-25 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtended',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_date', models.DateTimeField(auto_now=True)),
                ('mobile_number', models.CharField(blank=True, max_length=20)),
                ('scout_name', models.CharField(blank=True, max_length=20)),
                ('scout_organisation', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='basic.scouthierarchy')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
