# Generated by Django 3.1.1 on 2021-03-10 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0036_auto_20210218_1111'),
    ]

    operations = [
        migrations.AddField(
            model_name='dieselpurchasedata',
            name='bill',
            field=models.FileField(default='NA', upload_to='dieselbills/'),
        ),
        migrations.AddField(
            model_name='petrolpurchasedata',
            name='bill',
            field=models.FileField(default='NA', upload_to='petrolbills/'),
        ),
    ]