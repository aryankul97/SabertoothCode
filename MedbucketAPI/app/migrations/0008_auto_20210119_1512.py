# Generated by Django 3.1.5 on 2021-01-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_medicinebatchdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storedata',
            name='status',
            field=models.CharField(default='0', max_length=100),
        ),
    ]
