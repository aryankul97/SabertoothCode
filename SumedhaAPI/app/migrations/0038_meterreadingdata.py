# Generated by Django 3.1.1 on 2021-03-12 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20210310_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeterReadingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('business_id', models.CharField(max_length=50)),
                ('photo', models.FileField(default='NA', upload_to='meterreadings/')),
                ('fuel_type', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'MeterReadingData',
            },
        ),
    ]