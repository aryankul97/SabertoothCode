# Generated by Django 3.1.5 on 2021-02-20 12:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210220_1436'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BillData',
        ),
        migrations.DeleteModel(
            name='BillItemData',
        ),
    ]
