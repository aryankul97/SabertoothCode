# Generated by Django 2.1.1 on 2021-01-08 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_medicinedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicineData',
            fields=[
                ('created_date', models.DateTimeField(auto_now=True)),
                ('medicine_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('store_id', models.CharField(max_length=50)),
                ('dist_id', models.CharField(default='Not Availiable', max_length=50)),
                ('medicine_name', models.CharField(max_length=100)),
                ('medicine_description', models.CharField(max_length=150)),
                ('medicine_contents', models.CharField(max_length=100)),
                ('medicine_benifits', models.CharField(default='Not Availiable', max_length=100)),
                ('medicine_alternatives', models.CharField(default='Not Availiable', max_length=200)),
                ('medicine_quantity', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_measuringunit', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_1stripequals', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_costprice', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_sellprice', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_mrp', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_fixedrate', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_discount', models.CharField(default='Not Availiable', max_length=10)),
                ('medicine_gst', models.CharField(default='Not Availiable', max_length=10)),
                ('status', models.CharField(default='0', max_length=50)),
                ('prescription_required', models.CharField(default='0', max_length=50)),
                ('low_stock', models.CharField(default='0', max_length=50)),
                ('contains_expired_stock', models.CharField(default='0', max_length=50)),
            ],
            options={
                'db_table': 'MedicineData',
            },
        ),
    ]
