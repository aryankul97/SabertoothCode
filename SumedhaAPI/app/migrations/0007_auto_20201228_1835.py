# Generated by Django 3.1.1 on 2020-12-28 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20201228_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehiclesdata',
            old_name='user_id',
            new_name='business_id',
        ),
        migrations.RenameField(
            model_name='vehiclesdata',
            old_name='vehicle_insurance',
            new_name='hazardous_license_expiry_date',
        ),
        migrations.RemoveField(
            model_name='vehiclesdata',
            name='driver_id',
        ),
        migrations.RemoveField(
            model_name='vehiclesdata',
            name='manufacture_date',
        ),
        migrations.AddField(
            model_name='vehiclesdata',
            name='driver_assigned',
            field=models.CharField(default='0', max_length=5),
        ),
        migrations.AddField(
            model_name='vehiclesdata',
            name='insurence_expiry_date',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclesdata',
            name='insurence_number',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclesdata',
            name='manufacturer',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiclesdata',
            name='staff_id',
            field=models.CharField(default='N/A', max_length=50),
        ),
        migrations.AddField(
            model_name='vehiclesdata',
            name='vehicle_photo',
            field=models.FileField(default=1, upload_to='vehicles/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehiclesdata',
            name='puc',
            field=models.CharField(max_length=50),
        ),
    ]
