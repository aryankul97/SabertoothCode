# Generated by Django 3.1.1 on 2020-12-28 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20201228_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffdata',
            name='driving_license',
            field=models.FileField(default='NA', upload_to='drivinglicense/'),
        ),
        migrations.AlterField(
            model_name='staffdata',
            name='profile_picture',
            field=models.FileField(default='NA', upload_to='staffprofilepicture/'),
        ),
    ]
