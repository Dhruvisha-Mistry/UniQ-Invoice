from django.db import models
from UniQInvoice.models import Company_Master, Dealer_Master


# Create your models here.



class Warehouse_Master(models.Model):
    company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE,null=False)
    warehouse_name=models.CharField(max_length=250,null=False)
    warehouse_address=models.CharField(max_length=250,null=False)
    IsDeleted = models.IntegerField(null = False)
    IsActive = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)

    def _str_ (self):
        return self.warehouse_name


class Item_Master(models.Model):
    company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE,null=False)
    warehouse_id = models.ForeignKey(Warehouse_Master,on_delete=models.CASCADE,null=False)
    item_name=models.CharField(max_length=250,null=False)
    item_description=models.CharField(max_length=250,null=False)
    model_name=models.CharField(max_length=250,null=False)
    manufecture_date=models.DateField(auto_now=False, auto_now_add=False, null=False)
    receiving_data=models.DateField(auto_now=False, auto_now_add=False, null=False)
    DP_price=models.IntegerField(null=False)
    MRP=models.IntegerField(null=False)
    Battery_type=models.CharField(max_length=250)
    Ampear=models.CharField(max_length=250)
    Quantity=models.IntegerField(default=0)
    IsDeleted = models.IntegerField(null = False)
    IsActive = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)


    def _str_ (self):
        return self.item_name



class User_Master(models.Model):
    company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE,null=False) 
    First_name =models.CharField(max_length=250,null=False)
    Last_name =models.CharField(max_length=250,null=False)
    phone_number = models.CharField(max_length=250,null=False)
    email_address = models.CharField(unique=True,max_length=250,null=False)
    password = models.CharField(max_length=20,null=False)
    IsDeleted = models.IntegerField(null = False)
    IsActive = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)

    def str (self):
        return self.First_name


class Stock(models.Model):
    Warehouse_id = models.ForeignKey(Warehouse_Master,on_delete=models.CASCADE,null=False)
    Item_id = models.ForeignKey(Item_Master,on_delete=models.CASCADE,null=False)
    Quantity=models.IntegerField(default=0)
    Arrving_Date=models.DateField(auto_now=False, auto_now_add=False, null=False)

    def str (self):
        return self.Item_id.item_name

class INVOICE_MASTER(models.Model):
    InvoiceNo =models.CharField(max_length=250, null = False)
    InvoiceDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    InvoiceDueDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    DealerId = models.ForeignKey(Dealer_Master, on_delete=models.CASCADE, null = False)
    TotalAmount = models.IntegerField(null = False)
    TotalTax = models.CharField(max_length=50, null = False)
    CreatedBy = models.CharField(max_length=50, null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    ModifiedBy = models.CharField(max_length=50, null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False, null = False)
    
    def __str__(self):
        return self.InvoiceNo
    
class INVOICE_DETAILS(models.Model):
    Invoiceid = models.ForeignKey(INVOICE_MASTER, on_delete=models.CASCADE, null = False)
    ItemId = models.ForeignKey(Item_Master, on_delete=models.CASCADE, null = False)
    Quantity = models.IntegerField(null = True)
    Rate = models.IntegerField(null=True)
    ItemServiceNo = models.IntegerField(null = True)