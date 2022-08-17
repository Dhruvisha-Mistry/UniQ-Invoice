from tkinter import Y
from django.shortcuts import render,redirect
from ItemMaster.models import*
import datetime
from datetime import datetime
# from .models import Login_Master
from UniQInvoice.models import Company_Master
from UniQInvoice.models import Login_Master
# Create your views here.
import random
from datetime import date
from datetime import timedelta

import json
from django.http import HttpResponse
from django.http import JsonResponse

def add_item(request):
    if 'id'  in request.session:
    
    
        if request.method== "POST":
            
            warehousename=request.POST.get('warehousename')
            itemname=request.POST.get('itemname')
            itemdescription=request.POST.get('itemdescription')
            modelname=request.POST.get('modelname')
            manufecturedate=request.POST.get('manufectuerdate')
            # print(" manufecturedate : ", manufecturedate) 
            receivingdata=request.POST.get('receivingdate')
            DPprice=request.POST.get('dpprice')
            mrp=request.POST.get('mrp')
            Batterytype=request.POST.get('battery')
            Ampear=request.POST.get('ampear')
            Quantity=request.POST.get('quantity')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()
            # print("warehousenam = ", warehousename)

            print("Dates = ", manufecturedate, receivingdata)
            wid= Warehouse_Master.objects.get(id = warehousename)
            cid = Company_Master.objects.get(id=request.session['id'])
            Item_Master.objects.create(company_id=cid,         
                                       warehouse_id = wid,
                                        item_name = itemname,
                                        item_description = itemdescription,
                                        model_name = modelname,
                                        manufecture_date = manufecturedate,
                                        receiving_data = receivingdata,
                                        DP_price = DPprice,
                                        MRP = mrp,
                                        Battery_type = Batterytype,
                                        Ampear = Ampear,
                                        Quantity = Quantity,
                                        IsDeleted = '0',
                                        IsActive ='1',
                                        CreatedBy ='uniq',
                                        CreatedDate = CreatedDate,
                                        ModifiedBy = 'warehose owner',
                                        ModifiedDate = ModifiedDate
                                        )
            print("sucessfully registerd ") 
            tid= Item_Master.objects.all()
            return render(request,"Item-Master_data.html",{'wid':wid,'tid':tid})
        else:
            wid= Warehouse_Master.objects.all()
            tid= Item_Master.objects.all()

            # for i in wid:
            #     print("i = ",i.id)
            return render(request,"Item-Master.html",{'wid':wid,'tid':tid})
    else:
       return redirect('/companylogin/')
        
def display(request):
     if 'id'  in request.session:
    
        tid= Item_Master.objects.all()
        return render(request,"Item-Master_data.html",{'tid':tid})
     else:
       return redirect('/companylogin/')

def itemedit(request,pk):
    
        if request.method=="GET":
            
            L_id = Login_Master.objects.get(id=request.session['id'])
        
            cid = Company_Master.objects.get(id=L_id.Company_id_id)
            warehousedata = Warehouse_Master.objects.filter(company_id_id = cid.id)
            
            imt= Item_Master.objects.get(id = pk)
            itm_mdate= imt.manufecture_date
            itm_rdate=imt.receiving_data
            m_date = itm_mdate.strftime("%Y-%m-%d") # "%m/%d/%Y"
            r_date =itm_rdate.strftime("%Y-%m-%d")
            print("itm_mdate",itm_mdate)
            print("date and time:",m_date)	
            print("date and time:",r_date)	
            return render (request,"Item-master_edit.html",{"warehousedata":warehousedata,"imt":imt,'itm_mdate':itm_mdate,'r_date':r_date,'m_date':m_date,'itm_rdate':itm_rdate,'itm_date': itm_mdate})
        elif request.method=="POST":
            
            itemname=request.POST['itemname']
            itemdescription=request.POST['itemdescription']
            modelname=request.POST['modelname']
            manufecturedate=request.POST['manufectuerdate']
            print(" manufecturedate : ", manufecturedate)
            receivingdata=request.POST['receivingdate']
            DPprice=request.POST['dpprice']
            mrp=request.POST['mrp']
            Batterytype=request.POST['battery']
            Ampear=request.POST['ampear']
            Quantity=request.POST['quantity']
 

            imt= Item_Master.objects.get(id = pk)
            imt.item_name=itemname
            imt.item_description=itemdescription
            imt.model_name=modelname
            imt.manufecture_date=manufecturedate
            print(" imt.manufecture_date : ", imt.manufecture_date)
            imt.receiving_data=receivingdata
            imt.DP_price=DPprice
            imt.MRP=mrp
            imt.Battery_type=Batterytype
            imt.Ampear=Ampear
            imt.Quantity=Quantity

            imt.save()
            
            tid= Item_Master.objects.all()
            return render(request,"Item-Master_data.html",{'tid':tid})

def delete_data(request,pk):
    
    print(pk)
    itm= Item_Master.objects.get(id = pk)
    itm.delete()
    tid= Item_Master.objects.all()
    return render(request,"Item-Master_data.html",{'tid':tid})
    return redirect(display)

def warehouse(request):
    if 'id'  in request.session:
        if request.method== "POST":
            warehousename=request.POST.get('warehousename')
            warehouseadd=request.POST.get('Warehouse_Add')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()

            # C_id = Company_Master.objects.get(id=request.session['id'])
            
            L_id = Login_Master.objects.get(id=request.session['id'])
        
            cid = Company_Master.objects.get(id=L_id.Company_id_id)


            Warehouse_Master.objects.create(    
                                        company_id_id =cid.id,
                                        warehouse_name= warehousename,
                                        warehouse_address=warehouseadd,
                                        IsDeleted = '0',
                                        IsActive ='1',
                                        CreatedBy ='uniq',
                                        CreatedDate = CreatedDate,
                                        ModifiedBy = 'warehose owner',
                                        ModifiedDate = ModifiedDate
            )
            print("sucessfully registerd ") 
            wid= Warehouse_Master.objects.all()
            return render(request,"Warehouse-Master.html",{'wid':wid})

        else:
            print("get method")
            return render(request,"Warehouse-Master.html")
    else:
        return redirect('companylogin')

def warehouseshow(request):
    
    wid= Warehouse_Master.objects.all()

    for i in wid:
        print("i = ", i)
    return render(request,"Warehouse-Master.html",{'wid':wid})

def warehouse_edit(request,pk):

        if request.method=="GET":
            ware_edit= Warehouse_Master.objects.get(id = pk)
            
            return render (request,"Warehouse-Master_edit.html",{"ware_edit":ware_edit})
        elif request.method=="POST":
            
            warehousename=request.POST['warehousename']
            warehouseaddress=request.POST['Warehouse_Add']

            ware_edit= Warehouse_Master.objects.get(id = pk)
            ware_edit.warehouse_name=warehousename
            ware_edit.warehouse_address=warehouseaddress
          
            ware_edit.save()
            wid= Warehouse_Master.objects.all()
            
            return render(request,"Warehouse-Master.html",{'wid':wid})

def delete_warehouse(request,pk):
    
    print(pk)
    
    ware_delete= Warehouse_Master.objects.get(id = pk)
    ware_delete.delete()
    
    wid= Warehouse_Master.objects.all()
    return render(request,"Warehouse-Master.html",{'wid':wid})

def user (request ) :
    if 'id'  in request.session:
        if request.POST:
  
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            phoneno=request.POST.get('Mob_num')
           
            email=request.POST.get('email')
            password=request.POST.get('Password')
            cpassword=request.POST.get('Cpassword')
            CreatedDate=datetime.now()
            ModifiedDate=datetime.now()
            # print("warehousenam = ", warehousename)

            if password == cpassword :
            
                L_id = Login_Master.objects.get(id=request.session['id'])
        
                cid = Company_Master.objects.get(id=L_id.Company_id_id)

                User_Master.objects.create(     company_id_id= cid.id,
                                                    First_name = firstname,
                                                    Last_name = lastname,
                                                    phone_number = phoneno,
                                                    email_address = email,
                                                    password = password,
                                                    IsDeleted = '0',
                                                    IsActive ='1',
                                                    CreatedBy ='user',
                                                    CreatedDate = CreatedDate,
                                                    ModifiedBy = 'Customer',
                                                    ModifiedDate = ModifiedDate
                                                )
                print("sucessfully registerd ") 
                
                uid= User_Master.objects.all()
                return render(request,"User-Master-data.html",{ 'uid':uid })
            
            else:
                return render(request,"user-master.html",{ 'error':'password does not match' })
        else:
            return render (request ,"user-master.html")
    else:
        return redirect('/companylogin/')

def user_data(request):
    if 'id'  in request.session:
        
        uid= User_Master.objects.all()
        return render(request,"User-Master-data.html",{'uid':uid})
    else:
       return redirect('/companylogin/') 

def user_edit (request,pk ) :
    if request.method=="GET":
            u_edit= User_Master.objects.get(id = pk)
          
            return render (request,"User-Master-edit.html",{"u_edit":u_edit})
    elif request.method=="POST":
            fname=request.POST['firstname']
            lname=request.POST['lastname']
            phone=request.POST['Mob_num']
            email=request.POST['email']
            psw=request.POST['Password']
            # print("warehousenam = ", warehousename)
            u_edit= User_Master.objects.get(id = pk)
           
            u_edit.First_name=fname
            u_edit.Last_name=lname
            u_edit.phone_number=phone
            u_edit.email_address=email
            u_edit.password=psw
            u_edit.save()
            
            uid=User_Master.objects.all()
            return render(request,"User-Master-data.html",{'uid':uid })

def delete_user(request,pk):
    
   
    u_delete= User_Master.objects.get(id = pk)
    u_delete.delete()
    uid= User_Master.objects.all()
    return render(request,"User-Master-Data.html",{'uid':uid})

def Invoice_View(request):
    allinvoice = INVOICE_MASTER.objects.all()
    return render(request,"Invoice_View.html",{'allinvoice':allinvoice})

def create_invoice(request):
        invoice_a = "INV"
        invoice_b = "2122"
        invoice_c = ' '.join([str(random.randint(0, 999)).zfill(6) for _ in range(1)])
        Invoice_no = invoice_a + invoice_b + invoice_c
        
        lid = Login_Master.objects.get(id = request.session['id'])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",lid)
        c_id = Company_Master.objects.filter(id = lid.Company_id_id)
        
        print("@@@@@@@@@@@",c_id)
        d_id = Dealer_Master.objects.filter(Company_id_id = lid.Company_id_id)
        print("```````````````````````````````````````````````",d_id)

        alldealer = Dealer_Master.objects.filter(IsDeleted='0')
        # allcustomer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
        # print("allcustomer :-  ",allcustomer)
        allitem= Item_Master.objects.filter(IsDeleted = '0')
        print("tid  :-   ",allitem)
        
        for i in allitem:
            print(i)
        
        today = date.today()
        d1 = today.strftime("%b. %d, %Y")
        due_date = today + timedelta(days=15)
        Due_Date =due_date.strftime("%Y-%m-%d")
        return render(request,'invoicetest.html',{'allitem':allitem,'c_id':c_id,'lid':lid,'d_id':d_id,'d1':d1,'Due_Date':Due_Date,'alldealer':alldealer,'Invoice_no':Invoice_no}) 

def invoice_file(request):
    if request.method == "POST":
       in_no = request.POST['Invoice_Number']
    #    print("in_no :------------------------------------------------------------------------------",in_no)
       in_date = request.POST['invoice_date']
       in_duedate = request.POST['Invoice_Due_Date']
       dealer = request.POST['dealer']
       print("dealer")
       in_total = request.POST['total']
       in_sgst = request.POST['sgst']
       item_quntity = request.POST['item_quntity']
    #    price = request.POST['DP_price']
       
       print("quantity ==================================================",item_quntity)     
    #    print("price ==================================================",price)       
       
    #    sum = int(item_quntity) * int(price)
    #    print("sum :===============================================",sum)
       INVOICE_MASTER.objects.create(InvoiceNo=in_no,InvoiceDate=in_date,InvoiceDueDate=in_duedate,TotalAmount=in_total,TotalTax=in_sgst,CreatedBy = "dhruvisha",CreatedDate = "2022-1-1",ModifiedBy = "dhruvisha",ModifiedDate = "2022-1-1",DealerId_id = dealer)
    #    IN = INVOICE_DETAILS.objects.create(Quantity=item_quntity)
    #    print("invoice_details :!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",IN)
       
       
       return redirect("/invoice_file/")
       
def get_sum(request,pk):
    if request.method == "POST":
        dataID = request.POST['dataID']
        itm= Item_Master.objects.get(id=pk)
        print("itm----------------------------",itm)
        # price = request.POST['DP_price']
        
        print("itemid :-------------------",dataID)
        # print("price :--------------",price)
        try:
            subject = Item_Master.objects.filter(id = dataID)
            print("subject:-------------",subject)
            for i in subject:
                print("i :----------",i)
                price = i.DP_price
                print("price :------------",price)
                qty = i.user_qty
                print("qty :-----------",qty)
                totamount = price * qty   
        except Exception:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(subject.values()), safe = False) 
    
       
       
def get_items_ajax(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        print("itemid :------------------",item_id)
        try:
            subject = Item_Master.objects.filter(id = item_id)
            for i in subject:
                name=i.item_name

                print("name",name)

        except Exception:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(subject.values('item_name','item_description','model_name','DP_price','Ampear','Quantity')), safe = False) 
    
def dealerinformation(request):
    if request.method == "POST":
        dealerinfo_id = request.POST['dealinfo']
        try:
            info = Dealer_Master.objects.filter(id = dealerinfo_id)
            
            print("!!!!!!!!!!!!!!!!!!!!!!!",info)
        except Exception:
            print("###")
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(info.values('id','dealer_company_name','dealre_name','dealer_address','gst_number','dealer_email_address','dealer_phone_number','dealer_office_number')), safe = False)
        
def customerinformation(request):
    if request.method == "POST":
        custinfo_id = request.POST['custinfo']
        try:
            info = Dealer_Master.objects.filter(id = custinfo_id)
            
            print("!!!!!!!!!!!!!!!!!!!!!!!",info)
        except Exception:
            print("###")
            data['error_message'] = 'error'
            return JsonResponse(data)
        return JsonResponse(list(info.values('id','dealer_company_name','dealre_name','dealer_address','gst_number','dealer_email_address','dealer_phone_number','dealer_office_number')), safe = False)

# def save_invoice(request):
#     if request.method== "POST":
#         =request.POST.get('')


def xyz(request):
        invoice_a = "INV"
        invoice_b = "2122"
        invoice_c = ' '.join([str(random.randint(0, 999)).zfill(6) for _ in range(1)])
        Invoice_no = invoice_a + invoice_b + invoice_c
        
        lid = Login_Master.objects.get(id = request.session['id'])
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",lid)
        c_id = Company_Master.objects.filter(id = lid.Company_id_id)
        
        print("@@@@@@@@@@@",c_id)
        d_id = Dealer_Master.objects.filter(Company_id_id = lid.Company_id_id)
        print("```````````````````````````````````````````````",d_id)

        alldealer = Dealer_Master.objects.filter(IsDeleted='0')
        # allcustomer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
        # print("allcustomer :-  ",allcustomer)
        allitem= Item_Master.objects.filter(IsDeleted = '0')
        print("tid  :-   ",allitem)
        
        for i in allitem:
            print(i)
        
        today = date.today()
        d1 = today.strftime("%b. %d, %Y")
        due_date = today + timedelta(days=15)
        Due_Date =due_date.strftime("%Y-%m-%d")
        
        return render(request,'test.html',{'allitem':allitem,'c_id':c_id,'lid':lid,'d_id':d_id,'d1':d1,'Due_Date':Due_Date,'alldealer':alldealer,'Invoice_no':Invoice_no}) 
    # return render(request,"test.html")