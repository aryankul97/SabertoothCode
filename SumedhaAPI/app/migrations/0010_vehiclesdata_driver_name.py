# Generated by Django 3.1.1 on 2020-12-29 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20201228_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclesdata',
            name='driver_name',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
