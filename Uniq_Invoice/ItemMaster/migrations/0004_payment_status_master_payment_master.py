# Generated by Django 4.0.6 on 2022-08-15 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UniQInvoice', '0002_remove_company_master_password_and_more'),
        ('ItemMaster', '0003_invoice_master_invoice_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='PAYMENT_STATUS_MASTER',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(default='PENDING', max_length=200)),
                ('Total_Amount', models.IntegerField()),
                ('Received_Amount', models.IntegerField()),
                ('Full_Payment_Received_Date', models.DateField()),
                ('Invoice_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ItemMaster.invoice_master')),
            ],
        ),
        migrations.CreateModel(
            name='PAYMENT_MASTER',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Payment_Id', models.CharField(max_length=50)),
                ('Amount', models.IntegerField()),
                ('Payment_Date', models.DateField()),
                ('Dealer_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UniQInvoice.dealer_master')),
                ('Invoice_Id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ItemMaster.invoice_master')),
            ],
        ),
    ]