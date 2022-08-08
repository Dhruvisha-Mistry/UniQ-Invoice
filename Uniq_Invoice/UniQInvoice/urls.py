from django.urls import path
from UniQInvoice import views

app_name = "UniQInvoice"


urlpatterns = [
    path('',views.Company_register, name= "Company_register"),
    path('dashboard/',views.Dashboard, name= "dashboard"),
    path('uniq/invoice/admin/UniQ-Invoice/can/Watch',views.AdminCanWatch, name= "Admincanwatch"),
    # path('company_dashboard/',views.company_dashboard, name= "company_dashboard"),
    path('add_Dealer_Master/',views.add_Dealer_Master, name= "add_Dealer_Master"),
    path('companylogin/',views.companylogin, name= "companylogin"),
    path('companyaccept/<int:id>',views.companyaccept, name= "companyaccept"),
    path('companyreject/<int:id>',views.companyreject, name= "companyreject"),
    path('company_logout/',views.company_logout, name= "company_logout"),
    
    
    path('select_profile/',views.select_profile, name= "select_profile"),
    path('view_profile/',views.view_profile, name= "view_profile"),
    path('create_invoice/',views.create_invoice, name= "create_invoice"),
    # path('invoice_file/',views.invoice_file, name= "invoice_file"),
    
    
    path('delete_Dealer_Master/<int:id>',views.delete_Dealer_Master, name= "delete_Dealer_Master"),
    path('select_Dealer_Master/<int:id>',views.select_Dealer_Master, name= "select_Dealer_Master"),
    path('dealercanwatch/',views.dealercanwatch, name= "dealercanwatch"),
    path('Customer_Master/',views.Customer_Master, name= "Customer_Master"),
    path('customer_all/',views.customer_all, name= "customer_all"),
    path('select_Customer_Master/<int:id>',views.select_Customer_Master, name= "select_Customer_Master"),
    path('delete_Customer_Master/<int:id>',views.delete_Customer_Master, name= "delete_Customer_Master"),
    path('test/',views.test, name= "test"),

]