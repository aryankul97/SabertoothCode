# Generated by Django 3.1.1 on 2021-01-16 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0028_auto_20210115_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='cylinderassigndata2',
            name='cost_price',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cylinderassigndata2',
            name='filled_cylinder_deducted',
            field=models.CharField(default='100', max_length=50),
        ),
    ]
