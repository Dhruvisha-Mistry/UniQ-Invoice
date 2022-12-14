# Generated by Django 4.0.6 on 2022-07-16 06:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UniQInvoice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warehouse_name', models.CharField(max_length=250)),
                ('warehouse_address', models.CharField(max_length=250)),
                ('IsDeleted', models.IntegerField()),
                ('IsActive', models.IntegerField()),
                ('CreatedBy', models.CharField(max_length=250)),
                ('CreatedDate', models.DateField()),
                ('ModifiedBy', models.CharField(max_length=250)),
                ('ModifiedDate', models.DateField()),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniQInvoice.company_master')),
            ],
        ),
        migrations.CreateModel(
            name='Item_Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=250)),
                ('item_description', models.CharField(max_length=250)),
                ('model_name', models.CharField(max_length=250)),
                ('manufecture_date', models.DateField()),
                ('receiving_data', models.DateField()),
                ('DP_price', models.IntegerField()),
                ('MRP', models.IntegerField()),
                ('Battery_type', models.CharField(max_length=250)),
                ('Ampear', models.CharField(max_length=250)),
                ('Quantity', models.IntegerField()),
                ('IsDeleted', models.IntegerField()),
                ('IsActive', models.IntegerField()),
                ('CreatedBy', models.CharField(max_length=250)),
                ('CreatedDate', models.DateField()),
                ('ModifiedBy', models.CharField(max_length=250)),
                ('ModifiedDate', models.DateField()),
                ('warehouse_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ItemMaster.warehouse_master')),
            ],
        ),
    ]
