from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from UniQInvoice.models import Company_Master, Dealer_Master, Login_Master
from ItemMaster.models import Item_Master
from django.contrib.auth import authenticate, login, logout
import datetime  
from django.contrib import messages
from django.conf import settings
from Uniq_Invoice.settings import EMAIL_HOST_USER
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mass_mail   
import re 
import random
import string

import io 
from io import BytesIO
from reportlab.pdfgen import canvas

from datetime import date
from datetime import timedelta
import sweetify
import json



# Create your views here.

def AdminCanWatch(request):
    
    allcompany = Company_Master.objects.all()
    
    print(type(allcompany[0].IsActive))
    
    return render(request,'admin.html',{'allcompany':allcompany})

def companyaccept(request, id):
    
    company = Company_Master.objects.get(id=id)
    
    loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))
    
    text = f'your registration is accepted...\nthis is your credential\n\nUsername : {company.Email_Address}\nPassword : {loginPassword}'
    message1 = ('Uniq Invoice - Credential', text, EMAIL_HOST_USER, [company.Email_Address])
    
    
    
    
    message2 = ('UniqInvoice - Company Acceptance', f'you accepted registration of {company.Company_Name}', EMAIL_HOST_USER, ['hulkmarvadi@gmail.com'])

    send_mass_mail((message1, message2), fail_silently=False)
  
    loginmaster = Login_Master(Company_id_id=company.id,User_Name = company.Email_Address, Password=loginPassword)
    loginmaster.save()
    
    company.IsActive = '1'
    company.save()
    
    
    
    
    
    allcompany = Company_Master.objects.all()
    return render(request,'admin.html',{'allcompany':allcompany})
    
def companyreject(request,id): 
    
    deletecompany = Company_Master.objects.get(id=id)
    deletecompany.delete()
    
    allcompany = Company_Master.objects.all()
    return render(request,'admin.html',{'allcompany':allcompany})

def Company_register(request):
    if request.method == "POST":
        Company_Name=request.POST.get('Company_Name')
        Owner_Name=request.POST.get('Owner_Name')
        GST_Number=request.POST.get('GST_Number')
        Address=request.POST.get('Address')
        Email_Address=request.POST.get('Email_Address')
        Phone_Number = request.POST.get('Phone_Number')
        Office_Number=request.POST.get('Office_Number')
        Company_website=request.POST.get('Company_website')
        CreatedDate=datetime.date.today()
        ModifiedDate=datetime.date.today()
        
        if len(Company_website) == 0:
            Company_website = None
        
        
        if len(GST_Number)== 15:
            print("valid")
            pass
        else:
            print("invalid gst number")
            g_msg = "YOU HAVE TO ENTER 15 DIGIT"
            return render(request,"Company-signup.html",{'g_msg':g_msg})
        
        regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
    
        if(re.fullmatch(regex, Email_Address)):
            pass   
        else:
            print("invalid email")
            e_msg = "PLEASE ENTER VALID EMAIL"
            return render(request,"Company-signup.html",{'e_msg':e_msg})
    
    
       
    
        
        
        if Phone_Number.isdigit():
            if len(Phone_Number) == 10:
                print("valid")
                pass
        else:
            print("invalid")
            m_msg = "YOU SHOULD ENTER 10 DIGIT"
            return render(request,"Company-signup.html",{'m_msg':m_msg})
        CompanyMaster = Company_Master(Company_website=Company_website, Company_Name = Company_Name, Owner_name = Owner_Name,GST_Number = GST_Number,Address = Address,Email_Address=Email_Address,Phone_Number=Phone_Number,Office_Number =Office_Number,IsDeleted= '0',IsActive='0',CreatedBy='raj',CreatedDate=ModifiedDate,ModifiedBy='raj',ModifiedDate=ModifiedDate)
        CompanyMaster.save()

        
        message1 = ('Uniq Invoice', 'Thank you for registration,We will provide you your credential in your registered mail, once admin approve your registration', EMAIL_HOST_USER, [Email_Address])
        message2 = ('Uniq Invoice', 'one more company avilable please accept or reject', EMAIL_HOST_USER, ['dharmesh@uniqdatasolution.com'])

        send_mass_mail((message1, message2), fail_silently=False)
        

        print("email sent")
        # def test_view(request):
        # sweetify.success(request, 'You did it', text='Good job! You successfully showed a SweetAlert message', persistent='Hell yeah')
        # return redirect('/companylogin/')   
        msg = "successfully registered"
        return render(request,'success_reg.html',{'msg':msg})
        
    else: 
        return render(request,'Company-signup.html')
      
def Dashboard(request):
    try:
        user = request.session['email']
        uid = Login_Master.objects.get(User_Name=user)
        if uid is not None:
            lid = Login_Master.objects.get(id = request.session['id'])
            companyname = Company_Master.objects.get(id = lid.Company_id_id)
            return render(request, 'index.html',{'companyname':companyname})
        else:
            return redirect('/companylogin/')
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def companylogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        passw = request.POST.get('password')
        try:
            uid = Login_Master.objects.get(User_Name=email)
            if email == uid.User_Name:
                if passw == uid.Password:
                    request.session['id'] = uid.id
                    request.session['email'] = uid.User_Name
                    return redirect('/dashboard/')
                else:
                    messages.error(request,'Invalid Password', extra_tags='loginpass')
                    return render(request,'Login.html')
            else:
                messages.error(request,'Invalid Email', extra_tags='logemail')
                return render(request, 'Login.html')
        except:
            messages.error(request,'invalid cradencial', extra_tags = 'log')
    else:
        messages.error(request, 'hiiiiiiiiiiiii')
    return render(request,"Login.html")

def view_profile(request):
    try:
        user = request.session['email']
        lid = Login_Master.objects.get(id = request.session['id'])
        # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',lid)
        c_id = Company_Master.objects.get(id = lid.Company_id_id)
        # print("************************************************************************",c_id)
        
        return render (request,"company_profile.html",{"c_id":c_id})   
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def select_profile(request):    
    try:
        user = request.session['email']
        if request.user.is_authenticated:
            if request.method=="GET":
                lid = Login_Master.objects.get(id = request.session['id'])
                # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&',lid)
                c_id = Company_Master.objects.get(id = lid.Company_id_id)
                print("************************************************************************",c_id)
                
                return render (request,"select_profile.html",{"c_id":c_id})
            elif request.method=="POST":
                Company_Name=request.POST['Company_Name']
                GST_Number=request.POST['GST_Number']
                Address=request.POST['Address']
                Email_Address=request.POST['Email_Address']
                Phone_Number=request.POST['Phone_Number']
                Office_Number=request.POST['Office_Number']
                Owner_name=request.POST['Owner_name']
                Company_website=request.POST['Company_website']
                
                if len(Company_website) == 0:
                    Company_website = None
                
                
                if len(GST_Number)== 15:
                    print("valid gst")
                    pass
                else:
                    print("invalid gst number")
                    messages.error(request,'You Have to Enter 15 Digit', extra_tags='gst')
                    
                    return redirect('/select_profile/')
                
                regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
            
                if(re.fullmatch(regex, Email_Address)):
                    pass   
                else:
                    print("invalid email")

                    messages.error(request, 'Please Enter Valid Email', extra_tags='email')
                    return redirect('/select_profile/')

                
                
                if len(Phone_Number ) == 10:
                    print("valid phone number")
                    pass
                else:
                    messages.error(request, 'You Have to Enter 10 Digit', extra_tags='mobile_no')
            
                    return redirect('/select_profile/')
                
                
                lid = Login_Master.objects.get(id = request.session['id'])
                c_id = Company_Master.objects.get(id = lid.Company_id_id)
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!",c_id)
                c_id.Company_Name = Company_Name
                c_id.GST_Number = GST_Number
                c_id.Address=Address
                c_id.Email_Address=Email_Address
                c_id.Phone_Number=Phone_Number
                c_id.Office_Number=Office_Number
                c_id.Owner_name=Owner_name
                c_id.Company_website=Company_website
                

                c_id.save()
                
                return redirect('/view_profile/')
        else:
            return redirect('/companylogin/')
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def company_logout(request):
    logout(request)
    return render(request, 'Login.html')
       
def create_invoice(request):
    
    response = HttpResponse(content_type='application/pdf')
    pdf_file = "test_report_lab.pdf"                                               
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer,pdf_file)
    
    lid = Login_Master.objects.get(id = request.session['id'])
    print("``````````````````````````````````````",lid)
    c_id = Company_Master.objects.get(id = lid.Company_id_id)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~",c_id)
    d_id = Dealer_Master.objects.get(id = lid.Company_id_id)
    print("|||||||||||||||||||||||||||||||||||||||",d_id)


    c.drawString(100, 740, 'Company')
    c.drawString(30, 700, 'Company Name :')
    c.drawString(130, 700, c_id.Company_Name)
    c.drawString(30, 680, 'Owner name :')
    c.drawString(130, 680, c_id.Owner_name)
    c.drawString(30, 660, 'Email :')
    c.drawString(130, 660, c_id.Email_Address)
    c.drawString(30, 640, 'GST Number :')
    c.drawString(130, 640, c_id.GST_Number)
    c.drawString(30, 620, 'Address :')
    c.drawString(130, 620, c_id.Address)
    c.drawString(30, 600, 'Phone Number :')
    n = str(c_id.Phone_Number)
    c.drawString(130, 600, n)
    c.drawString(30, 580, 'Office Number :')
    officeno = str(c_id.Office_Number)
    c.drawString(130, 580, officeno)

 
  
    
    c.drawString(450, 740, 'Dealer')
    c.drawString(300, 700, 'dealer company name :')
    c.drawString(450, 700, d_id.dealer_company_name)
    c.drawString(300, 680, 'dealre name :')
    c.drawString(450, 680, d_id.dealre_name)
    c.drawString(300, 660, 'dealer_email_address :')
    c.drawString(450, 660, d_id.dealer_email_address)
    c.drawString(300, 640, 'gst number :')
    c.drawString(450, 640, d_id.gst_number)
    c.drawString(300, 620, 'dealer_address :')
    c.drawString(450, 620, d_id.dealer_address)
    c.drawString(300, 600, 'Phone Number :')
    n = str(d_id.dealer_phone_number)
    c.drawString(450, 600, n)
    c.drawString(300, 580, 'Office Number :')
    officeno = str(d_id.dealer_office_number)
    c.drawString(450, 580, officeno) 
    
    
    
    c.showPage()
    c.save()
    # print(type(my_canvas))
    pdf =buffer.getvalue()
    buffer.close()
    response.write(pdf)

    # b = table_content(request)
    
    return response
    # return render(request,'dealer_view.html',{'dealer_in':dealer_in,'company_in':company_in})

def dealercanwatch(request):
    try:
        user = request.session['email']
        alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
        lid = Login_Master.objects.get(id = request.session['id'])
        companyname = Company_Master.objects.get(id = lid.Company_id_id)
        # print(type(allcompany[0].IsActive))

        return render(request,'dealer_View.html',{'alldealer':alldealer,'companyname':companyname})
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def add_Dealer_Master(request):
    try:
        user = request.session['email']
        if request.method == "POST":
            dealer_company_name=request.POST.get('dealer_company_name')
            dealre_name=request.POST.get('dealre_name')
            dealer_address=request.POST.get('dealer_address')
            gst_number=request.POST.get('gst_number')
            dealer_email_address=request.POST.get('dealer_email_address')
            dealer_phone_number=request.POST.get('dealer_phone_number')
            dealer_office_number=request.POST.get('dealer_office_number')
            CreatedDate=datetime.date.today()
            ModifiedDate=datetime.date.today()

            print(request.session['id'])
            L_id = Login_Master.objects.get(id=request.session['id'])
            
            cid = Company_Master.objects.get(id=L_id.Company_id_id)
            print("###########################################################################################################",cid)
            
            regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
        
            if(re.fullmatch(regex, dealer_email_address)):
                pass   
            else:
                sel_dealer= Dealer_Master.objects.get(id = id)
                print("invalid email")
                e_msg = "PLEASE ENTER VALID EMAIL"

                return render(request,"Dealermaster.html",{'e_msg':e_msg})
        
            
            if dealer_phone_number.isdigit():
                if len(dealer_phone_number)== 10:
                    print("valid")
                    pass
            else:
                sel_dealer= Dealer_Master.objects.get(id = id)
                print("invalid")
                m_msg = "YOU SHOULD ENTER 10 DIGIT"
                # return redirect('/select_Dealer_Master/{{sel_dealer}}', {'m_msg':m_msg})
                return render(request,"Dealermaster.html",{'m_msg':m_msg})


            DealerMaster = Dealer_Master.objects.create(Company_id_id = cid.id, dealer_company_name = dealer_company_name,dealre_name = dealre_name,dealer_address = dealer_address,gst_number=gst_number,dealer_email_address=dealer_email_address,dealer_phone_number =dealer_phone_number,dealer_office_number=dealer_office_number,IsActive='1',IsDeleted='0',CreatedBy='raj',CreatedDate=ModifiedDate,ModifiedBy='raj',ModifiedDate=ModifiedDate ,IsDealer='True')
            alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
            return render(request,"dealer_view.html",{'alldealer':alldealer})
        else:
            return render(request,"Dealermaster.html")
            # pass
            
        return render(request,'company_dash.html')   
    
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def delete_Dealer_Master(request,id):
    del_dealer = Dealer_Master.objects.get(id=id)
    del_dealer.IsDeleted=1
    del_dealer.save()
    alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
    return  redirect("/dealercanwatch/",{'alldealer':alldealer})

def select_Dealer_Master(request,id):
    try:
        user = request.session['email']
        if request.method=="GET":
            sel_dealer= Dealer_Master.objects.get(id = id)

            
            return render (request,"select_dealer.html",{"sel_dealer":sel_dealer})
        elif request.method=="POST":
            
            dealer_company_name=request.POST['dealer_company_name']
            dealre_name=request.POST['dealre_name']
            dealer_address=request.POST['dealer_address']
            gst_number=request.POST['gst_number']
            dealer_email_address=request.POST['dealer_email_address']
            dealer_phone_number=request.POST['dealer_phone_number']
            dealer_office_number=request.POST['dealer_office_number']
            sel_dealer= Dealer_Master.objects.get(id = id)

            regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
        
            if(re.fullmatch(regex, dealer_email_address)):
                pass   
            else:
                sel_dealer= Dealer_Master.objects.get(id = id)
                print("invalid email")
                e_msg = "PLEASE ENTER VALID EMAIL"

                return render(request,"select_dealer.html",{'sel_dealer':sel_dealer,'e_msg':e_msg})
            
            if dealer_phone_number.isdigit():
                if len(dealer_phone_number)== 10:
                    print("valid")
                    pass
            else:
                sel_dealer= Dealer_Master.objects.get(id = id)
                print("invalid")
                m_msg = "YOU SHOULD ENTER 10 DIGIT"
                # return redirect('/select_Dealer_Master/{{sel_dealer}}', {'m_msg':m_msg})
                return render(request,"select_dealer.html",{'sel_dealer':sel_dealer,'m_msg':m_msg})

            sel_dealer.dealer_company_name = dealer_company_name
            sel_dealer.dealre_name = dealre_name
            sel_dealer.dealer_address=dealer_address
            sel_dealer.gst_number=gst_number
            sel_dealer.dealer_email_address=dealer_email_address
            sel_dealer.dealer_phone_number=dealer_phone_number
            sel_dealer.dealer_office_number=dealer_office_number

            sel_dealer.save()
            return redirect('/dealercanwatch/')    
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def customer_all(request):
    try:
        user = request.session['email']
        customer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
        return render(request,'customer_view.html',{'customer':customer})
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def Customer_Master(request):
    try:
        user = request.session['email']
        if request.method == "POST":
            customer_company_name=request.POST.get('company_name')
            customer_name=request.POST.get('dealre_name')
            customer_address=request.POST.get('address')
            customer_gst_number=request.POST.get('gst_number')
            customer_email_address=request.POST.get('email_address')
            customer_phone_number=request.POST.get('phone_number')
            customer_office_number=request.POST.get('office_number')
            CreatedDate=datetime.date.today()
            ModifiedDate=datetime.date.today()
            # print("customer_company_name",customer_company_name)
            print(request.session['id'])
            L_id = Login_Master.objects.get(id=request.session['id'])
            
            cid = Company_Master.objects.get(id=L_id.Company_id_id)
            

            regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
        
            if(re.fullmatch(regex, customer_email_address)):
                pass   
            else:
                sel_dealer= Dealer_Master.objects.get(id = id)
                print("invalid email")
                e_msg = "PLEASE ENTER VALID EMAIL"

                return render(request,"customer.html",{'e_msg':e_msg})
        

            if customer_phone_number.isdigit():
                if len(customer_phone_number)== 10:
                    print("valid")
                    pass
            else:
                sel_dealer= Dealer_Master.objects.get(id = id)
                print("invalid")
                m_msg = "YOU SHOULD ENTER 10 DIGIT"
                # return redirect('/select_Dealer_Master/{{sel_dealer}}', {'m_msg':m_msg})
                return render(request,"customer.html",{'m_msg':m_msg})

            DealerMaster = Dealer_Master.objects.create(Company_id_id = cid.id, dealer_company_name = customer_company_name,dealre_name = customer_name,dealer_address = customer_address,gst_number=customer_gst_number,dealer_email_address=customer_email_address,dealer_phone_number =customer_phone_number,dealer_office_number=customer_office_number,IsActive='1',IsDeleted='0',CreatedBy='raj',CreatedDate=ModifiedDate,ModifiedBy='raj',ModifiedDate=ModifiedDate ,IsDealer='False' )
            customer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
        
            return render(request,"customer_view.html",{'customer':customer})
        else:
            return render(request,"customer.html")
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def select_Customer_Master(request,id):
    try:
        user = request.session['email']
        if request.method=="GET":
            sel_customer= Dealer_Master.objects.get(id = id)

            
            return render (request,"customer_edit.html",{"sel_customer":sel_customer})
        elif request.method=="POST":
            
            customer_company_name=request.POST['company_name']
            customer_name=request.POST['customer_name']
            customer_address=request.POST['address']
            gst_number=request.POST['gst_number']
            customer_email_address=request.POST['email_address']
            customer_phone_number=request.POST['phone_number']
            customer_office_number=request.POST['office_number']
            sel_customer= Dealer_Master.objects.get(id = id)
            
            regex = r'\b[A-Za-z0-9._%+-]+@gmail.com\b'
        
            if(re.fullmatch(regex, customer_email_address)):
                pass   
            else:
                sel_customer= Dealer_Master.objects.get(id = id)
                print("invalid email")
                e_msg = "PLEASE ENTER VALID EMAIL"

                return render(request,"customer_edit.html",{'sel_customer':sel_customer,'e_msg':e_msg})
            
            if customer_phone_number.isdigit():
                if len(customer_phone_number)== 10:
                    print("valid")
                    pass
            else:
                sel_customer= Dealer_Master.objects.get(id = id)
                print("invalid")
                m_msg = "YOU SHOULD ENTER 10 DIGIT"
                return render(request,"customer_edit.html",{'sel_customer':sel_customer,'m_msg':m_msg})

            sel_customer.dealer_company_name = customer_company_name
            sel_customer.dealre_name = customer_name
            sel_customer.dealer_address=customer_address
            sel_customer.gst_number=gst_number
            sel_customer.dealer_email_address=customer_email_address
            sel_customer.dealer_phone_number=customer_phone_number
            sel_customer.dealer_office_number=customer_office_number

            sel_customer.save()
            return redirect('/customer_all/')
        
    except:
        messages.error(request,'you have to login first')
        return redirect('/companylogin/')

def delete_Customer_Master(request,id):
    del_dealer = Dealer_Master.objects.get(id=id)
    del_dealer.IsDeleted=1
    del_dealer.save()
    customer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
   
    return  redirect("/customer_all/",{'customer':customer})


# def invoice_file(request):
#     invoice_a = "INV"
#     invoice_b = "2122"
#     invoice_c = ' '.join([str(random.randint(0, 999)).zfill(6) for _ in range(1)])
#     Invoice_no = invoice_a + invoice_b + invoice_c

#     lid = Login_Master.objects.get(id = request.session['id'])
#     d_id = Dealer_Master.objects.filter(Company_id_id = lid.Company_id_id)

#     alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
#     allcustomer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
    
#     today = date.today()
#     d1 = today.strftime("%b. %d, %Y")
#     due_date = today + timedelta(days=15)

#     return render(request,'invoicetest.html',{'lid':lid,'d_id':d_id,'d1':d1,'due_date':due_date,'alldealer':alldealer,'allcustomer':allcustomer,'Invoice_no':Invoice_no})   
    # except:
    #     messages.error(request,'you have to login first')
    #     return redirect('/companylogin/')



def test(request):
    alldealer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='1')
    allcustomer = Dealer_Master.objects.filter(IsDeleted='0',IsDealer='0')
    allitem= Item_Master.objects.filter(IsDeleted = '0')
    items=[]
    for i in allitem:
        if len(i.item_name) == 0:
            break
        items.append(i)
        
    print("items:",items)
    return render(request,'test.html',{'items':items,'alldealer':alldealer,'allcustomer':allcustomer,'allitem':allitem})
    
    
    
        
        
        
        
        
# def itemforinvoice(request):
#     print("allitem  ----- ",allitem)
#     for val in allitem:
#         a = val.id 
#         print("a------- ",a)
#         # p = []
#         # p.append(val)   
#         # print(p, type(p)) 
        

#         mydata = {'a':a}
#         return render(request, 'test.html', context={"mydata_json": json.dumps(mydata)})