from django.contrib import admin
from django.urls import path
from ItemMaster import views

app_name = "ItemMaster"

urlpatterns = [
    path('add_item/', views.add_item, name='add_item'),
    path('display/', views.display, name='display'), 
    path('itemedit/<int:pk>/', views.itemedit, name='itemedit'),
    path('itemdelete/<int:pk>/', views.delete_data, name='itemdelete'),
    # path('', views.warehouse, name='warehouse'), 
    path('warehouseshow/', views.warehouseshow, name='warehouseshow'),
    path('addwarehouse/', views.warehouse, name='addwarehouse') ,
    path('warehouse_edit/<int:pk>/', views.warehouse_edit, name='warehouse_edit') ,
    path('delete_warehouse/<int:pk>/', views.delete_warehouse, name='delete_warehouse'),
    path('user/', views.user, name='user'),
    path('user_data/', views.user_data, name='user_data'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit') ,
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('invoice_file/',views.invoice_file, name= "invoice_file"),
    path('Invoice_View/',views.Invoice_View, name= "Invoice_View"),
    
    
] 

