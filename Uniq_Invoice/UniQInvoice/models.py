from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Company_Master(models.Model):
    Company_Name = models.CharField(max_length=250, null = False)
    GST_Number = models.CharField(max_length=250, null = False)
    Address = models.CharField(max_length=250, null = False)
    Email_Address = models.EmailField(max_length=250, null = False, unique = True)
    Phone_Number= models.IntegerField(null = False)
    Office_Number = models.IntegerField(null = False)
    Owner_name = models.CharField(max_length=100,null = False)
    Company_website = models.CharField(max_length=200)
    IsDeleted = models.IntegerField(null = False)
    IsActive = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    
    
    def __str__(self):
        return self.Company_Name
    
class Dealer_Master(models.Model):
    Company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE)
    dealer_company_name = models.CharField(max_length=250, null = False)
    dealre_name = models.CharField(max_length=250, null = False)
    dealer_address = models.CharField(max_length=250, null = False)
    gst_number = models.CharField(max_length=250, null =True)
    dealer_email_address = models.CharField(max_length=250, null = False)
    dealer_phone_number = models.CharField(max_length=250, null = False)
    dealer_office_number = models.CharField(max_length=250, null = False)
    IsActive = models.IntegerField(null = False)
    IsDeleted = models.IntegerField(null = False)
    CreatedBy = models.CharField(max_length=250,null = False)
    CreatedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    ModifiedBy = models.CharField(max_length=250,null = False)
    ModifiedDate = models.DateField(auto_now=False, auto_now_add=False,null = False)
    IsDealer = models.BooleanField(null=True)
    
    
    def __str__(self):
        return self.dealer_company_name
    
    
class Login_Master(models.Model):
    Company_id = models.ForeignKey(Company_Master,on_delete=models.CASCADE)
    User_Name = models.EmailField(max_length=250, null = False)
    Password= models.CharField(max_length=250,null = False)
 
    

    def __str__(self):
        return self.User_Name
    

    
    