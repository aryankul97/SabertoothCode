# Generated by Django 3.1.5 on 2021-02-20 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210220_1730'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillData',
            fields=[
                ('bill_date', models.DateField(auto_now=True)),
                ('bill_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('customer_id', models.CharField(blank=True, max_length=50, null=True)),
                ('store_id', models.CharField(max_length=50)),
                ('total_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('total_tax_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('total_discount_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('total_amount_to_pay', models.CharField(blank=True, max_length=50, null=True)),
                ('pay_mode', models.CharField(blank=True, max_length=50, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('bill_pdf_url', models.CharField(blank=True, max_length=100, null=True)),
                ('delete', models.CharField(default='0', max_length=50)),
            ],
            options={
                'db_table': 'BillData',
            },
        ),
        migrations.CreateModel(
            name='BillItemData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_id', models.CharField(max_length=50)),
                ('medicine_id', models.CharField(max_length=50)),
                ('store_id', models.CharField(max_length=50)),
                ('quantity', models.CharField(blank=True, max_length=50, null=True)),
                ('amount', models.CharField(blank=True, max_length=50, null=True)),
                ('tax_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('discount_amount', models.CharField(blank=True, max_length=50, null=True)),
                ('amount_to_pay', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'BillItemData',
            },
        ),
    ]
