# Generated by Django 3.1.1 on 2021-01-12 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_dieselbilldata_patrolbilldata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dieselbilldata',
            old_name='created_date',
            new_name='bill_date',
        ),
        migrations.RenameField(
            model_name='patrolbilldata',
            old_name='created_date',
            new_name='bill_date',
        ),
    ]
